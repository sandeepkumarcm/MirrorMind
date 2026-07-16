import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
import base64
import time

from backend.data.question_selector import get_random_question
from backend.nlp.similarity_score import evaluate_technical_answer
from backend.llm.feedback_generator import generate_feedback
from frontend.components.dashboard import render_dashboard
from frontend.components.styles import (
    inject_custom_css, render_hero, render_stat_strip,
    glass_card_open, glass_card_close,
    render_section_header, render_live_badge,
    render_tech_stack_expander
)

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="MirrorMind", layout="wide", page_icon="🪞")
inject_custom_css()
render_hero()
render_tech_stack_expander()

# ---------------- Session State Init ----------------
defaults = {
    "video_started": False,
    "current_question": None,
    "emotion_history": [],
    "session_start_time": None,
    "last_evaluated_transcript": None,
    "technical_result": None,
    "ai_feedback": None,
    "completed_scores": [],
    "completed_categories": set(),
    "snapshot_video_state": {},
    "snapshot_audio_state": {},
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------- Stat Strip ----------------
avg_score = round(sum(st.session_state.completed_scores) / len(st.session_state.completed_scores), 1) if st.session_state.completed_scores else 0
session_time_str = "—"
if st.session_state.session_start_time:
    elapsed_min = int((time.time() - st.session_state.session_start_time) // 60)
    elapsed_sec = int((time.time() - st.session_state.session_start_time) % 60)
    session_time_str = f"{elapsed_min}m {elapsed_sec}s"

render_stat_strip(
    questions_answered=len(st.session_state.completed_scores),
    categories_covered=len(st.session_state.completed_categories),
    avg_score=avg_score,
    session_time_str=session_time_str
)

# ---------------- Pill Tabs ----------------
tab_setup, tab_live, tab_results = st.tabs(["🎯 Setup", "🎥 Live Session", "📊 Results"])

with tab_setup:
    with st.container(border=True):
        render_section_header(
            "Interview Question",
            subtitle="Pick a category and pull a question to begin your session.",
            icon="🎯"
        )

        col_q1, col_q2 = st.columns([3, 1])
        with col_q2:
            category = st.selectbox("Category", ["Any", "Python", "SQL", "Machine Learning", "Deep Learning", "AI/NLP/Computer Vision"])
            if st.button("Get New Question"):
                selected_category = None if category == "Any" else category
                st.session_state.current_question = get_random_question(category=selected_category)
                st.session_state.last_evaluated_transcript = None
                st.session_state.technical_result = None
                st.session_state.ai_feedback = None
        with col_q1:
            if st.session_state.current_question:
                q = st.session_state.current_question
                st.info(f"**{q['category']} | {q['difficulty']}**\n\n{q['question']}")
            else:
                st.info("Click 'Get New Question' to begin.")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("▶ Start Interview"):
                requests.post(f"{API_BASE}/video/start")
                st.session_state.video_started = True
                st.session_state.session_start_time = time.time()
                st.session_state.emotion_history = []
        with col_b:
            if st.button("⏹ Stop Interview"):
                requests.post(f"{API_BASE}/video/stop")
                st.session_state.video_started = False
        with col_c:
            # 👇 THIS IS WHERE THE 60-SECOND ANSWER DURATION IS SET.
            # Change duration_sec=60 below (and the button label) to whatever you want.
            if st.button("🎙 Start Answer (60 sec)"):
                if st.session_state.current_question is None:
                    st.warning("Pick a question first.")
                else:
                    requests.post(f"{API_BASE}/audio/start", params={"duration_sec": 60})
                    st.session_state.last_evaluated_transcript = None
                    st.session_state.technical_result = None
                    st.session_state.ai_feedback = None

live_placeholder = tab_live.empty()
results_placeholder = tab_results.empty()

if not st.session_state.video_started:
    with live_placeholder.container():
        st.info("Start the interview from the Setup tab to see your live camera feed and transcript here.")

if not (st.session_state.technical_result and st.session_state.ai_feedback):
    with results_placeholder.container():
        st.info("Complete an answer to see your evaluation dashboard here.")

# ---------------- Live Loop ----------------
while st.session_state.video_started:
    try:
        video_state = requests.get(f"{API_BASE}/video/state", timeout=2).json()
        audio_state = requests.get(f"{API_BASE}/audio/state", timeout=2).json()
    except requests.exceptions.RequestException:
        with live_placeholder.container():
            st.warning("Backend not reachable. Is uvicorn running?")
        break

    if video_state.get("emotion") and video_state.get("emotion_confidence") is not None:
        elapsed = round(time.time() - st.session_state.session_start_time, 1)
        st.session_state.emotion_history.append({
            "timestamp": elapsed,
            "emotion": video_state["emotion"],
            "confidence": video_state["emotion_confidence"]
        })

    transcript = audio_state.get("transcript") or ""
    is_new_transcript = (
        transcript
        and not audio_state.get("recording", False)
        and transcript != st.session_state.last_evaluated_transcript
        and st.session_state.current_question is not None
    )

    if is_new_transcript:
        q = st.session_state.current_question

        # SNAPSHOT: freeze video/audio state at the moment of evaluation,
        # so the Results tab doesn't keep drifting as the live camera
        # continues running after the answer is done.
        st.session_state.snapshot_video_state = dict(video_state)
        st.session_state.snapshot_audio_state = dict(audio_state)

        st.session_state.technical_result = evaluate_technical_answer(
            transcript=transcript, ideal_answer=q["ideal_answer"], keywords=q["keywords"]
        )
        emotion_labels = [e["emotion"] for e in st.session_state.emotion_history]
        emotion_summary = ", ".join(sorted(set(emotion_labels))) if emotion_labels else "No data"
        st.session_state.ai_feedback = generate_feedback(
            transcript=transcript,
            technical_score=st.session_state.technical_result["technical_score"],
            missing_keywords=st.session_state.technical_result["missing_keywords"],
            emotion_summary=emotion_summary,
            eye_contact_pct=video_state.get("eye_contact_pct", 0),
            wpm=audio_state.get("wpm", 0),
            pause_count=audio_state.get("pause_count", 0),
            answer_duration_label=audio_state.get("answer_classification", ""),
            current_question=q["question"]
        )
        st.session_state.last_evaluated_transcript = transcript
        st.session_state.completed_categories.add(q["category"])

    with live_placeholder.container():
        glass_card_open()
        if audio_state.get("recording", False):
            render_live_badge("RECORDING ANSWER")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Live Camera**")
            if video_state.get("frame_b64"):
                frame_bytes = base64.b64decode(video_state["frame_b64"])
                st.image(frame_bytes, use_column_width=True)
            else:
                st.warning("Waiting for camera frame...")
            st.metric("Emotion", video_state.get("emotion") or "—")
            st.metric("Emotion Confidence", f"{video_state.get('emotion_confidence') or 0}%")
            st.metric("Eye Contact %", f"{video_state.get('eye_contact_pct', 0)}%")
            st.metric("Head Pose", video_state.get("head_pose", "Unknown"))
        with c2:
            st.markdown("**Transcript**")
            st.write(audio_state.get("transcript") or "—")
            st.metric("WPM", f"{audio_state.get('wpm', 0)} ({audio_state.get('wpm_classification', '')})")
            st.metric("Filler Words", f"{audio_state.get('filler_count', 0)} ({audio_state.get('filler_classification', '')})")
            st.metric("Pauses", f"{audio_state.get('pause_count', 0)} (Longest: {audio_state.get('longest_pause', 0)}s)")
            st.metric("Answer Timer", f"{audio_state.get('answer_duration', 0)}s ({audio_state.get('answer_classification', '')})")
        glass_card_close()

    with results_placeholder.container():
        if st.session_state.technical_result and st.session_state.ai_feedback:
            overall_score = render_dashboard(
                video_state=st.session_state.get("snapshot_video_state", video_state),
                audio_state=st.session_state.get("snapshot_audio_state", audio_state),
                technical_result=st.session_state.technical_result,
                ai_feedback=st.session_state.ai_feedback,
                emotion_history=st.session_state.emotion_history
            )
            if overall_score is not None and (not st.session_state.completed_scores or st.session_state.completed_scores[-1] != overall_score):
                st.session_state.completed_scores.append(overall_score)
        else:
            st.info("Complete an answer to see your evaluation dashboard here.")

    time.sleep(0.1)