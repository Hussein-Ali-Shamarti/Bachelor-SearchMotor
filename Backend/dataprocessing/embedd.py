import os
import sys
import numpy as np
import logging
from sentence_transformers import SentenceTransformer

# Define paths
SOURCE_FOLDER = r"C:\My Web Sites\backup\debug1 – Kopi"
DEST_FOLDER = os.path.join(SOURCE_FOLDER, "embedded")
LOG_FILE = os.path.join(SOURCE_FOLDER, "embedding_errors.log")

# Create the destination folder if it doesn't exist
os.makedirs(DEST_FOLDER, exist_ok=True)

# Set up logging
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(message)s")

# Load Sentence-Transformers model
model = SentenceTransformer("all-MiniLM-L6-v2")

# List to store failed files
failed_files = []

# Process each .txt file in the source folder
for filename in os.listdir(SOURCE_FOLDER):
    if filename.endswith(".txt"):  # Process only text files
        file_path = os.path.join(SOURCE_FOLDER, filename)
        npy_filename = filename.replace(".txt", ".npy")
        npy_path = os.path.join(DEST_FOLDER, npy_filename)

        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Generate embedding
            embedding = model.encode(text)

            # Save embedding as a NumPy file in the "embedded" folder
            np.save(npy_path, embedding)

            print(f" Processed: {filename} -> {npy_filename}")

        except Exception as e:
            # Log the error and store the failed filename
            logging.error(f"Failed to process {filename}: {e}")
            failed_files.append(filename)
            print(f"Error processing {filename}: {e}")

# Ensure UTF-8 encoding for Windows console
os.system("chcp 65001")  # Changes code page to UTF-8
sys.stdout.reconfigure(encoding="utf-8")

# Print the summary of failed files
if failed_files:
    print("\nThe following files failed to process:")
    for failed_file in failed_files:
        print(f"  - {failed_file}")
    print(f"\nCheck the log file for details: {LOG_FILE}")
else:
    print("\nAll files processed successfully!")

print("Embedding process completed!")
