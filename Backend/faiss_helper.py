import faiss as faiss_cpu
import numpy as np
import os
from database import SessionLocal
from models import Article

FAISS_INDEX_PATH = "faiss.index"
D = 384  # Number of dimensions in the embeddings

def normalize_embeddings(embeddings):
    """
    Normalize the embeddings to unit length for better indexing/search performance.
    """
    norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norm
    return embeddings

def rebuild_faiss_index():
    print("Rebuilding FAISS index...")

    with SessionLocal() as session:
        # Fetch all articles and their embeddings
        articles = session.query(Article.id, Article.embeddings).all()
        if not articles:
            print("No articles found in the database!")
            return None, None

        ids = []
        embeddings = []
        processed_count = 0

        for article_id, embedding_blob in articles:
            if embedding_blob is None:
                print(f"Skipping ID {article_id} due to missing embedding (NoneType)")
                continue  # Skip if embedding is missing

            embedding = np.frombuffer(embedding_blob, dtype='float32')

            if embedding.shape[0] != D:
                print(f"Skipping ID {article_id} due to incorrect embedding size: {embedding.shape[0]}")
                continue  # Skip embeddings with incorrect size

            ids.append(article_id)
            embeddings.append(embedding)
            processed_count += 1

        if processed_count == 0:
            print("No valid embeddings found after filtering.")
            return None, None

        embeddings = np.array(embeddings, dtype='float32')

        # Optional: Normalize embeddings (if necessary for better results)
        embeddings = normalize_embeddings(embeddings)

        # Create the FAISS index
        index = faiss_cpu.IndexFlatL2(D)
        index.add(embeddings)

        print(f"FAISS index rebuilt with {len(embeddings)} articles.")

        # Optionally, save the index if needed
        if os.path.exists(FAISS_INDEX_PATH):
            print(f"Index already exists at {FAISS_INDEX_PATH}. Overwriting...")
        faiss_cpu.write_index(index, FAISS_INDEX_PATH)
        print(f"FAISS index saved to {FAISS_INDEX_PATH}")

        return index, ids
