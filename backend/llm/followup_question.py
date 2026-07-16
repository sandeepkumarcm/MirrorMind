from groq import Groq
from backend.core.config import settings

_client = Groq(api_key=settings.GROQ_API_KEY)

FALLBACK_QUESTION = "Can you elaborate further on the approach you just described?"


def generate_followup(previous_question, candidate_answer):
    """
    Generates exactly one relevant follow-up interview question
    based on the candidate's previous answer. Returns plain text.
    """
    prompt = f"""You are an AI interview coach conducting a technical interview.

Original question: {previous_question}
Candidate's answer: {candidate_answer}

Based on the candidate's answer, ask exactly ONE relevant follow-up question
that probes deeper into their understanding or asks them to clarify or expand
on something specific they said. Return ONLY the follow-up question text,
with no preamble, no numbering, no quotation marks."""

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100,
        )
        followup = response.choices[0].message.content.strip()
        followup = followup.strip('"').strip("'")

        if not followup:
            return FALLBACK_QUESTION

        return followup

    except Exception as e:
        print(f"Groq Error: {e}")

        return FALLBACK_QUESTION