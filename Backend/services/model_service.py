# Dette skriptet initialiserer og returnerer en SentenceTransformer-modell 
# (all-MiniLM-L6-v2) for generering av tekstembeddings.


from sentence_transformers import SentenceTransformer

def init_model():
    """Initializes and returns the SentenceTransformer model."""
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
