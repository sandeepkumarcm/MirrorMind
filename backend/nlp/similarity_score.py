import re
import numpy as np
from numpy.linalg import norm
from backend.nlp.embeddings import get_embedding

SIMILARITY_WEIGHT = 0.6
KEYWORD_WEIGHT = 0.4


def _cosine_similarity(vec_a, vec_b):
    if vec_a is None or vec_b is None:
        return 0.0
    dot_product = np.dot(vec_a, vec_b)
    magnitude = norm(vec_a) * norm(vec_b)
    if magnitude == 0:
        return 0.0
    return float(dot_product / magnitude)


def _check_keyword_coverage(transcript, keywords):
    """
    Checks how many keywords appear in the transcript using
    word-boundary matching (case-insensitive).
    """
    text = transcript.lower()
    matched = []
    missing = []

    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        if re.search(pattern, text):
            matched.append(keyword)
        else:
            missing.append(keyword)

    coverage_pct = (len(matched) / len(keywords) * 100) if keywords else 0.0

    return {
        "matched": matched,
        "missing": missing,
        "coverage_pct": round(coverage_pct, 2)
    }


def evaluate_technical_answer(transcript, ideal_answer, keywords):
    """
    Full Phase 5 pipeline:
    transcript -> embed -> cosine similarity vs ideal_answer
                -> keyword coverage
                -> technical_score = 0.6*similarity + 0.4*coverage

    Returns dict:
    {
      "similarity_pct": float,
      "matched_keywords": [...],
      "missing_keywords": [...],
      "keyword_coverage_pct": float,
      "technical_score": float
    }
    """
    if not transcript or not transcript.strip():
        return {
            "similarity_pct": 0.0,
            "matched_keywords": [],
            "missing_keywords": keywords,
            "keyword_coverage_pct": 0.0,
            "technical_score": 0.0
        }

    transcript_vec = get_embedding(transcript)
    ideal_vec = get_embedding(ideal_answer)

    similarity = _cosine_similarity(transcript_vec, ideal_vec)
    similarity_pct = round(max(similarity, 0.0) * 100, 2)  # clamp negative to 0

    keyword_result = _check_keyword_coverage(transcript, keywords)

    technical_score = round(
        (SIMILARITY_WEIGHT * similarity_pct) + (KEYWORD_WEIGHT * keyword_result["coverage_pct"]),
        2
    )

    return {
        "similarity_pct": similarity_pct,
        "matched_keywords": keyword_result["matched"],
        "missing_keywords": keyword_result["missing"],
        "keyword_coverage_pct": keyword_result["coverage_pct"],
        "technical_score": technical_score
    }