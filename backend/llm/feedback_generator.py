from groq import Groq
import json
import re
from backend.core.config import settings
from backend.nlp.vector_store import retrieve_similar_concepts

_client = Groq(api_key=settings.GROQ_API_KEY)

FALLBACK_FEEDBACK = {
    "strengths": ["Candidate provided a response to the question."],
    "weaknesses": ["Unable to generate detailed feedback at this time."],
    "suggestions": ["Please review the transcript manually."],
    "final_summary": "AI feedback generation failed. Manual review recommended."
}


def _extract_json(text):
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def _call_llama(prompt):
    response = _client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def _format_retrieved_context(retrieved_docs):
    """
    Formats retrieved concept documents into a readable context block
    for the prompt. This is the "Augmentation" step of RAG.
    """
    if not retrieved_docs:
        return "No additional reference concepts retrieved."

    lines = []
    for i, doc in enumerate(retrieved_docs, 1):
        lines.append(
            f"{i}. [{doc['category']}] {doc['question']}\n"
            f"   Reference explanation: {doc['ideal_answer']}"
        )
    return "\n".join(lines)


def generate_feedback(
    transcript,
    technical_score,
    missing_keywords,
    emotion_summary,
    eye_contact_pct,
    wpm,
    pause_count,
    answer_duration_label,
    current_question=None,
):
    """
    RAG-enhanced feedback generation:
    1. RETRIEVE: find the top-3 most semantically related concepts from the
       full question bank based on the candidate's transcript (via FAISS).
    2. AUGMENT: inject those retrieved reference explanations into the prompt.
    3. GENERATE: Llama 3 writes feedback grounded in that retrieved context,
       instead of relying purely on its own parametric knowledge.
    """
    retrieved_docs = retrieve_similar_concepts(
        transcript=transcript,
        k=3,
        exclude_question=current_question
    )
    retrieved_context = _format_retrieved_context(retrieved_docs)

    base_prompt = f"""You are an AI interview coach evaluating a candidate's answer.

Transcript: {transcript}
Technical Score: {technical_score}%
Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}
Emotion Summary: {emotion_summary}
Eye Contact: {eye_contact_pct}%
Words Per Minute: {wpm}
Pause Count: {pause_count}
Answer Length: {answer_duration_label}

Relevant reference concepts retrieved from the knowledge base (use these to
ground your feedback in specific, accurate technical explanations where relevant):
{retrieved_context}

Respond with a JSON object in this EXACT format:

{{
  "strengths": ["point 1", "point 2"],
  "weaknesses": ["point 1", "point 2"],
  "suggestions": ["point 1", "point 2"],
  "final_summary": "a 2-3 sentence overall summary"
}}"""

    strict_prompt = base_prompt + "\n\nIMPORTANT: Respond ONLY with the JSON object, nothing else."

    for attempt_prompt in [base_prompt, strict_prompt]:
        try:
            raw_output = _call_llama(attempt_prompt)
            json_str = _extract_json(raw_output)
            parsed = json.loads(json_str)

            required_keys = {"strengths", "weaknesses", "suggestions", "final_summary"}
            if required_keys.issubset(parsed.keys()):
                parsed["retrieved_concepts"] = [d["question"] for d in retrieved_docs]
                return parsed

        except Exception:
            continue

    return FALLBACK_FEEDBACK