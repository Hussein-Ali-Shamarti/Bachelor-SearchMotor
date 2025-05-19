# Dette skriptet leser .txt-filer med artikkeltekst, beriker dem med tilhørende metadata (hvis tilgjengelig), 
# genererer tekst-embeddinger ved hjelp av Sentence-Transformers, og lagrer resultatet som .npy-filer. 
# Feil logges, og eventuelle manglende metadata håndteres automatisk.

import os
import sys
import numpy as np
import logging
from sentence_transformers import SentenceTransformer

# Define paths
SOURCE_FOLDER = r"C:\My Web Sites\data\pdftexts"
METADATA_ROOT = r"C:\My Web Sites\data\articles"         
DEST_FOLDER = os.path.join(SOURCE_FOLDER, "embedded")
LOG_FILE = os.path.join(SOURCE_FOLDER, "embedding_errors.log")

# Create the destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(message)s")

# Load Sentence-Transformers model
model = SentenceTransformer("all-MiniLM-L6-v2")

failed_files = []

def parse_metadata(metadata_text):
    """Parses the metadata file and returns a dict."""
    metadata = {}
    for line in metadata_text.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip().lower()] = value.strip()
    return metadata

def build_enriched_text(metadata, article_body):
    text_parts = []

    raw_author = metadata.get('author', metadata.get('authors', 'Unknown'))
    if raw_author.startswith("[") and raw_author.endswith("]"):
        try:
            import ast
            author_list = ast.literal_eval(raw_author)
            if isinstance(author_list, list):
                cleaned_author = "; ".join(author_list)
            else:
                cleaned_author = str(author_list)
        except:
            cleaned_author = raw_author
    else:
        cleaned_author = raw_author

    text_parts.append(f"Author(s): {cleaned_author}")
    text_parts.append(f"Title: {metadata.get('title', 'Unknown')}")
    text_parts.append(f"Publication Date: {metadata.get('publication_date', 'Unknown')}")
    text_parts.append(f"Conference: {metadata.get('conference_title', 'Unknown')}")
    text_parts.append(f"Location: {metadata.get('location', 'Unknown')}")
    text_parts.append(f"Keywords: {metadata.get('keywords', '')}")
    text_parts.append("")
    text_parts.append(article_body)
    return "\n".join(text_parts)

# Process each .txt file in the source folder
for filename in os.listdir(SOURCE_FOLDER):
    if filename.endswith(".txt"): 
        file_path = os.path.join(SOURCE_FOLDER, filename)
        npy_filename = filename.replace(".txt", ".npy")
        npy_path = os.path.join(DEST_FOLDER, npy_filename)

        base_name = filename.replace(".txt", "")

        try:
            parts = base_name.split("_")
            if len(parts) < 2:
                raise ValueError(f"Unexpected filename format: {filename}")

            conference = parts[0].upper()
            year = parts[1]
            conference_folder = f"{conference}_{year}"

            
            metadata_file_path = os.path.join(METADATA_ROOT, conference, conference_folder, f"{base_name}.txt")

           
            with open(file_path, "r", encoding="utf-8") as file:
                article_body = file.read()

            if os.path.exists(metadata_file_path):
                
                with open(metadata_file_path, "r", encoding="utf-8") as metafile:
                    metadata_text = metafile.read()
                    metadata = parse_metadata(metadata_text)

                    enriched_text = build_enriched_text(metadata, article_body)
                print(f"Processed with metadata: {filename}")
            else:
                
                enriched_text = article_body
                print(f"Metadata not found, embedding only full text: {filename}")

            
            embedding = model.encode(enriched_text)
            np.save(npy_path, embedding)

        except Exception as e:
            
            logging.error(f"Failed to process {filename}: {e}")
            failed_files.append(filename)
            print(f"Error processing {filename}: {e}")


os.system("chcp 65001")
sys.stdout.reconfigure(encoding="utf-8")


if failed_files:
    print("\nThe following files failed to process:")
    for failed_file in failed_files:
        print(f"  - {failed_file}")
    print(f"\nCheck the log file for details: {LOG_FILE}")
else:
    print("\n All files processed successfully!")

print("Embedding process completed!")
