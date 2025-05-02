import time
import numpy as np
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

# Make sure your models.py is accessible
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import Article

sys.stdout.reconfigure(encoding='utf-8')

# Set the DATABASE_URL to point to your SQLite DB in the Backend folder
DATABASE_URL = "sqlite:///./Backend/database.db"

# Connect to SQLite
def connect_to_sqlite():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()

# Base path to the embedded folder
EMBEDDED_FOLDER = r"C:\My Web Sites\backup\debug1 – Kopi\embedded"

def update_article_embedding_by_filename(base_name, session):
    """Updates the embedding for an existing article matched by filename in the PDF URL."""
    npy_file_path = os.path.join(EMBEDDED_FOLDER, f"{base_name}.npy")

    if not os.path.exists(npy_file_path):
        print(f"Embedding file not found: {npy_file_path}")
        return

    try:
        embedding = np.load(npy_file_path).tobytes()
    except Exception as e:
        print(f"Error loading embedding for {base_name}: {e}")
        return

    try:
        # Find the article by matching the filename in the pdf_url
        article = (
            session.query(Article)
            .filter(Article.pdf_url.ilike(f"%{base_name}%"))
            .first()
        )

        if article:
            article.embeddings = embedding
            session.commit()
            print(f"Updated embedding for: {article.title} (matched by filename: {base_name})")
        else:
            print(f"Article not found in DB for filename: {base_name}")
    except Exception as e:
        print(f"Error updating article for filename '{base_name}': {e}")
        session.rollback()

def process_embeddings_folder(embedded_folder, session):
    """Processes all .npy files in the embedded folder to update embeddings."""
    print(f"Scanning embedded folder: {embedded_folder}")

    # Collect all .npy files
    npy_files = [
        f for f in os.listdir(embedded_folder)
        if f.endswith(".npy")
    ]

    if not npy_files:
        print("No .npy embedding files found.")
        return

    # Process with progress bar
    for npy_file in tqdm(npy_files, desc="Updating Embeddings", unit="file"):
        base_name = npy_file.replace(".npy", "")
        update_article_embedding_by_filename(base_name, session)

def main():
    start_time = time.time()
    session = connect_to_sqlite()

    try:
        process_embeddings_folder(EMBEDDED_FOLDER, session)
        print("Embedding updates completed successfully!")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        session.close()

    print(f"Time taken: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
