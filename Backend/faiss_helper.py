import faiss as faiss_cpu
import numpy as np
import os
from database import SessionLocal
from models import Article

FAISS_INDEX_PATH = "faiss.index"
D = 384 # Number of dimensions in the embeddings

def rebuild_faiss_index():
    print("🔄 Rebuilding FAISS index...")

    with SessionLocal() as session:
        articles = session.query(Article.id, Article.embeddings).all()
        if not articles:
            print("⚠️ No articles found in the database!")
            return None, None

        ids = []
        embeddings = []

        for article_id, embedding_blob in articles:
            if embedding_blob is None:
                print(f"⚠️ Skipping ID {article_id} due to missing embedding (NoneType)")
                continue  # Skip if embedding is missing

            embedding = np.frombuffer(embedding_blob, dtype='float32')
            if embedding.shape[0] == 384:  # ✅ Ensure correct dimension
                ids.append(article_id)
                embeddings.append(embedding)
            else:
                print(f"⚠️ Skipping ID {article_id} due to incorrect embedding size: {embedding.shape[0]}")

        if not embeddings:
            print("⚠️ No valid embeddings found after filtering.")
            return None, None

        embeddings = np.array(embeddings, dtype='float32')
        index = faiss_cpu.IndexFlatL2(384)  # Ensure dimensions match
        index.add(embeddings)

        print(f"✅ FAISS index rebuilt with {len(embeddings)} articles.")

        return index, ids