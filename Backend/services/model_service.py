from sentence_transformers import SentenceTransformer

def init_model():
    """Initializes and returns the SentenceTransformer model."""
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
