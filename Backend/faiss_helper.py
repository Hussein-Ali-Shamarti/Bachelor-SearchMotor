# Dette skriptet bygger og laster en FAISS-indeks basert på artiklers embeddings lagret i databasen. 
# Det håndterer normalisering, validering av dimensjoner, og lagring/gjenbruk av indeksen og ID-mapping.
# Indeksen oppdateres automatisk dersom nye eller endrede artikler oppdages.

import faiss as faiss_cpu
import numpy as np
import os
from database import SessionLocal
from models import Article

FAISS_INDEX_PATH = "faiss.index"
FAISS_IDS_PATH = "faiss_ids.npy"
D = 384  # Number of dimensions in the embeddings

def normalize_embeddings(embeddings):
    """
    Normalize the embeddings to unit length for better indexing/search performance.
    """
    norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norm
    return embeddings

def rebuild_faiss_index():
    print("Rebuilding FAISS index from the database...")

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
        embeddings = normalize_embeddings(embeddings)

        # Create the FAISS index
        index = faiss_cpu.IndexFlatL2(D)
        index.add(embeddings)

        print(f"FAISS index rebuilt with {len(embeddings)} articles.")
        return index, ids

def load_or_rebuild_faiss_index():
    """
    Load the FAISS index and corresponding IDs from disk if they exist and are up-to-date.
    If new rows are found in the database, rebuild the index and update the saved files.
    """
    if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_IDS_PATH):
        try:
            index = faiss_cpu.read_index(FAISS_INDEX_PATH)
            ids = np.load(FAISS_IDS_PATH).tolist()
            print("Loaded FAISS index and IDs from disk.")

            # Check for any new rows in the database
            with SessionLocal() as session:
                articles = session.query(Article.id, Article.embeddings).all()
                db_ids = []
                for article_id, embedding_blob in articles:
                    if embedding_blob is None:
                        continue
                    embedding = np.frombuffer(embedding_blob, dtype='float32')
                    if embedding.shape[0] != D:
                        continue
                    db_ids.append(article_id)

            if set(db_ids) != set(ids):
                print("New or updated rows detected in the database. Rebuilding FAISS index...")
                raise ValueError("Index out-of-date")
            else:
                print("No new rows found. Using existing FAISS index.")
                return index, ids

        except Exception as e:
            print(f"Error loading FAISS index or detecting new rows: {e}")
            print("Falling back to rebuilding the index...")

    else:
        print("FAISS index or IDs file not found. Rebuilding index...")

    # Rebuild the index if loading failed or new rows were detected.
    index, ids = rebuild_faiss_index()
    if index is not None and ids is not None:
        try:
            faiss_cpu.write_index(index, FAISS_INDEX_PATH)
            np.save(FAISS_IDS_PATH, np.array(ids))
            print(f"FAISS index saved to {FAISS_INDEX_PATH} and IDs saved to {FAISS_IDS_PATH}")
        except Exception as e:
            print(f"Failed to save FAISS index or IDs: {e}")
    return index, ids
