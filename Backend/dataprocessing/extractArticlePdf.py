"""
  This code extracts the text contents from the pdf files
  in the source folder and writes the extracted information to a text file in the destination folder.
"""

import os
from pdfminer.high_level import extract_text
import pdfplumber
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # For progress bar

# Define directories for files.
input_dir = r"C:\My Web Sites\dataset\www.thinkmind.org\articles"
output_dir = r"C:\My Web Sites\data\pdftexts"

# Create the output directory if it doesn't exist already.
os.makedirs(output_dir, exist_ok=True)

def process_pdf(pdf_path, txt_path):
    """Extract text from PDF and save to a text file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""  # Ensure we don't get None
        with open(txt_path, "w", encoding='utf-8') as text_file:
            text_file.write(text)
    except Exception as e:
        logging.error(f"Error processing PDF {os.path.basename(pdf_path)}: {e}")

def process_html(html_path, txt_path):
    """Extract text from HTML and save to a text file."""
    try:
        with open(html_path, "r", encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
            text = soup.get_text()
        with open(txt_path, "w", encoding='utf-8') as text_file:
            text_file.write(text)
    except Exception as e:
        print(f"Error processing HTML {os.path.basename(html_path)}: {e}")

# Gather files to process
files = [f for f in os.listdir(input_dir) if f.lower().endswith((".pdf", ".html"))]

# Use ThreadPoolExecutor for parallel processing
with tqdm(total=len(files), desc="Processing files") as pbar:
    with ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(process_pdf if filename.lower().endswith(".pdf") else process_html, 
                            os.path.join(input_dir, filename), 
                            os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")): filename
            for filename in files
            if not os.path.exists(os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")) or os.path.getsize(os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")) == 0
        }

        for future in tqdm(future_to_file, desc="Processing files", total=len(future_to_file)):
            future.result()  # Wait for task completion

print("Text extraction complete!")