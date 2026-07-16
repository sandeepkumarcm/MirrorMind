from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Takes a plain text string, returns its embedding vector (numpy array).
    """
    if not text or not text.strip():
        return None
    return _model.encode(text, convert_to_numpy=True)