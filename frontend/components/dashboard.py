import streamlit as st
from frontend.components.charts import (
    compute_communication_score,
    compute_overall_score,
    render_emotion_timeline,
    render_wpm_chart,
    render_filler_chart,
    render_pause_chart,
)
from frontend.components.styles import render_radial_gauge, glass_card_open, glass_card_close


def render_dashboard(video_state, audio_state, technical_result, ai_feedback, emotion_history):
    tab1, tab2, tab3 = st.tabs(["💬 Communication", "🧠 Technical", "🏁 Final"])

    with tab1:
        glass_card_open()
        st.subheader("Communication Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Emotion", video_state.get("emotion") or "—")
            st.metric("Eye Contact %", f"{video_state.get('eye_contact_pct', 0)}%")
        with col2:
            st.metric("WPM", f"{audio_state.get('wpm', 0)} ({audio_state.get('wpm_classification', '')})")
            st.metric("Filler Words", f"{audio_state.get('filler_count', 0)} ({audio_state.get('filler_classification', '')})")
        with col3:
            st.metric("Pause Count", audio_state.get("pause_count", 0))
            st.metric("Answer Duration", f"{audio_state.get('answer_duration', 0)}s ({audio_state.get('answer_classification', '')})")
        glass_card_close()

        st.plotly_chart(render_emotion_timeline(emotion_history), use_container_width=True)

        chart_col1, chart_col2, chart_col3 = st.columns(3)
        with chart_col1:
            st.plotly_chart(render_wpm_chart(audio_state.get("wpm", 0)), use_container_width=True)
        with chart_col2:
            st.plotly_chart(render_filler_chart(audio_state.get("filler_count", 0)), use_container_width=True)
        with chart_col3:
            st.plotly_chart(render_pause_chart(audio_state.get("pause_count", 0)), use_container_width=True)

    with tab2:
        glass_card_open()
        st.subheader("Technical Evaluation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Similarity %", f"{technical_result.get('similarity_pct', 0)}%")
        with col2:
            st.metric("Keyword Coverage %", f"{technical_result.get('keyword_coverage_pct', 0)}%")
        with col3:
            st.metric("Technical Score", f"{technical_result.get('technical_score', 0)}%")

        if technical_result.get("missing_keywords"):
            st.write("**Missing Keywords:**", ", ".join(technical_result["missing_keywords"]))
        if technical_result.get("matched_keywords"):
            st.write("**Matched Keywords:**", ", ".join(technical_result["matched_keywords"]))
        glass_card_close()

    with tab3:
        communication_score = compute_communication_score(
            eye_contact_pct=video_state.get("eye_contact_pct", 0),
            wpm=audio_state.get("wpm", 0),
            filler_count=audio_state.get("filler_count", 0),
            pause_count=audio_state.get("pause_count", 0),
        )
        overall_score = compute_overall_score(
            technical_score=technical_result.get("technical_score", 0),
            communication_score=communication_score,
        )

        glass_card_open()
        col1, col2 = st.columns([1, 1])
        with col1:
            render_radial_gauge(overall_score, label="Overall Score")
        with col2:
            st.metric("Communication Score", f"{communication_score}%")
            st.metric("Technical Score", f"{technical_result.get('technical_score', 0)}%")
        glass_card_close()

        glass_card_open()
        st.markdown("### AI Feedback")
        st.write("**Strengths**")
        for s in ai_feedback.get("strengths", []):
            st.write(f"- {s}")
        st.write("**Weaknesses**")
        for w in ai_feedback.get("weaknesses", []):
            st.write(f"- {w}")
        st.write("**Suggestions**")
        for sug in ai_feedback.get("suggestions", []):
            st.write(f"- {sug}")
        st.write("**Summary**")
        st.write(ai_feedback.get("final_summary", ""))
        glass_card_close()

        return overall_score