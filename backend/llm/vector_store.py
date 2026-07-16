import faiss
import numpy as np
import json
import os
from backend.nlp.embeddings import get_embedding

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "questions.json")

_index = None
_documents = []  # parallel list: each entry = {"question": ..., "ideal_answer": ..., "category": ..., "keywords": [...]}


def _build_index():
    """
    Builds a FAISS index (once, at import time) from every ideal_answer
    in the question bank. This is the RAG "knowledge base."
    """
    global _index, _documents

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    embeddings = []
    for q in questions:
        vec = get_embedding(q["ideal_answer"])
        if vec is not None:
            embeddings.append(vec)
            _documents.append({
                "question": q["question"],
                "ideal_answer": q["ideal_answer"],
                "category": q["category"],
                "keywords": q["keywords"]
            })

    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]  # 384 for all-MiniLM-L6-v2
    _index = faiss.IndexFlatL2(dimension)
    _index.add(embeddings)


def retrieve_similar_concepts(transcript, k=3, exclude_question=None):
    """
    Given a candidate's transcript, retrieves the top-k most semantically
    similar concept documents (question + ideal_answer + keywords) from
    across the ENTIRE question bank — not just the current question.

    exclude_question: optionally exclude the exact question being answered,
    so retrieval surfaces genuinely NEW related concepts, not the same one.

    Returns list of dicts: [{"question": ..., "ideal_answer": ..., "category": ...}, ...]
    """
    if _index is None:
        _build_index()

    if not transcript or not transcript.strip():
        return []

    query_vec = get_embedding(transcript)
    if query_vec is None:
        return []

    query_vec = np.array([query_vec]).astype("float32")

    search_k = k + 1 if exclude_question else k
    distances, indices = _index.search(query_vec, search_k)

    results = []
    for idx in indices[0]:
        if idx == -1 or idx >= len(_documents):
            continue
        doc = _documents[idx]
        if exclude_question and doc["question"] == exclude_question:
            continue
        results.append(doc)
        if len(results) >= k:
            break

    return results


# Build the index once when this module is first imported
_build_index()