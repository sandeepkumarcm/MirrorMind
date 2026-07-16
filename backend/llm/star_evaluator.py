from groq import Groq
import json
import re
from backend.core.config import settings

_client = Groq(api_key=settings.GROQ_API_KEY)

FALLBACK_STAR = {
    "situation": False,
    "task": False,
    "action": False,
    "result": False,
    "missing": ["situation", "task", "action", "result"],
    "suggestions": ["Unable to evaluate STAR structure. Please review manually."]
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
        temperature=0.3,
        max_tokens=400,
    )
    return response.choices[0].message.content


def evaluate_star(transcript):
    """
    Only call this for behavioral questions (pass is_behavioral flag
    from the calling route before invoking this function).
    Returns dict: {"situation": bool, "task": bool, "action": bool,
                    "result": bool, "missing": [...], "suggestions": [...]}
    """
    base_prompt = f"""You are evaluating a candidate's answer to a behavioral
interview question using the STAR framework (Situation, Task, Action, Result).

Transcript: {transcript}

Determine whether each STAR component is clearly present in the answer.
Respond in this EXACT JSON format, with no markdown, no code fences, no
preamble — respond with ONLY the JSON object:

{{
  "situation": true or false,
  "task": true or false,
  "action": true or false,
  "result": true or false,
  "missing": ["list of missing component names, lowercase"],
  "suggestions": ["1-3 specific suggestions to improve missing components"]
}}"""

    strict_prompt = base_prompt + "\n\nIMPORTANT: Respond ONLY in valid JSON. No markdown formatting, no ```json fences, no extra text before or after the JSON object."

    for attempt_prompt in [base_prompt, strict_prompt]:
        try:
            raw_output = _call_llama(attempt_prompt)
            json_str = _extract_json(raw_output)
            parsed = json.loads(json_str)

            required_keys = {"situation", "task", "action", "result", "missing", "suggestions"}
            if required_keys.issubset(parsed.keys()):
                return parsed

        except (json.JSONDecodeError, Exception):
            continue

    return FALLBACK_STAR