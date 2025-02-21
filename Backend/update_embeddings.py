from database import SessionLocal
from models import Article
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm  # Progress bar

# Load the embedding model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Start database session
session = SessionLocal()
articles = session.query(Article).all()

total_articles = len(articles)
updated_count = 0
skipped_count = 0

print(f"Processing {total_articles} articles...")

# Initialize progress bar
with tqdm(total=total_articles, desc="Updating Embeddings", unit="article") as pbar:
    for article in articles:
        try:
            if article.pdf_texts:  # Ensure text exists
                old_embedding_size = len(article.embeddings) if article.embeddings else "None"
                
                # Generate new embedding
                new_embedding = model.encode(article.pdf_texts).astype(np.float32).tobytes()

                # Update only if embedding size is different
                if old_embedding_size != len(new_embedding):
                    article.embeddings = new_embedding
                    updated_count += 1
                    session.commit()

                    print(f"Article {article.id} updated: {old_embedding_size} -> {len(new_embedding)} bytes")

                else:
                    print(f"Skipping Article {article.id} (Already up-to-date)")
                    skipped_count += 1

            else:
                print(f"Skipping Article {article.id} (No text available)")
                skipped_count += 1

        except Exception as e:
            print(f"Error updating Article {article.id}: {str(e)}")
            skipped_count += 1

        # Update progress bar
        pbar.update(1)

session.close()

print(f"\nCompleted! Updated: {updated_count} | Skipped: {skipped_count} | Total: {total_articles}")
