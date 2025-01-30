import os
import pdfplumber
import pytesseract
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
import re

# Define directories
input_dir = r"C:\My Web Sites\dataset\www.thinkmind.org\articles"  # Folder containing PDFs
output_dir = r"C:\My Web Sites\data\pdftexts"  # Folder containing extracted .txt files

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define size limits
max_txt_size = 20 * 1024  # 20 KB (for processing PDFs)
large_txt_size = 140 * 1024  # 140 KB (for reprocessing if CID found)

# Error log file
error_log_path = os.path.join(output_dir, "error_log.txt")

# Function to log errors
def log_error(pdf_name, error_msg):
    with open(error_log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{pdf_name}: {error_msg}\n")

# Function to check if a text file exists and meets size conditions
def should_process_pdf(pdf_filename):
    """Returns True if the PDF should be processed (based on .txt size and CID content)."""
    txt_path = os.path.join(output_dir, os.path.splitext(pdf_filename)[0] + ".txt")

    if not os.path.exists(txt_path):
        return False  # No matching .txt file

    txt_size = os.path.getsize(txt_path)

    if txt_size < max_txt_size:
        return True  # Process if .txt file is small (<20KB)

    if txt_size > large_txt_size and contains_cid_values(txt_path):
        return True  # Reprocess large files (>140KB) with CID

    return False  # Otherwise, skip

# Function to check if a text file contains CID values
def contains_cid_values(txt_path):
    """Returns True if the text file contains CID values, indicating possible missing text."""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            text = f.read()
        return bool(re.search(r'\(CID:\s?\d+\)', text))  # Detect CID patterns
    except Exception as e:
        log_error(os.path.basename(txt_path), f"Failed to read TXT: {e}")
        return False

# Function to convert PDF to images (for OCR)
def convert_pdf_to_images(pdf_path):
    """Converts a PDF to images (one per page) for OCR."""
    return convert_from_path(pdf_path)

# Function to extract text using pdfplumber
def extract_text_from_pdf(pdf_path):
    """Extracts text using pdfplumber; returns None if extraction fails."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""  # Ensure no None values
        return text
    except Exception as e:
        log_error(os.path.basename(pdf_path), f"pdfplumber failed: {e}")
        return None

# Function to extract text using OCR
def ocr_pdf(pdf_path, txt_path):
    """Uses OCR to extract text from a PDF and saves it to a text file."""
    try:
        images = convert_pdf_to_images(pdf_path)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)

        with open(txt_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
    except Exception as e:
        log_error(os.path.basename(pdf_path), f"OCR failed: {e}")

def is_metadata_only(text):
    """Detects if text is mostly conference metadata instead of real content."""
    metadata_patterns = [
        r"Copyright \(c\) IARIA, \d{4}",
        r"Original source: ThinkMind Digital Library",
        r"ISBN: \d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}",
        r"International Conference on [\w\s,-]+"
    ]
    matches = sum(bool(re.search(pattern, text)) for pattern in metadata_patterns)
    return matches >= 2  # If at least two patterns are found, it's likely metadata

def needs_ocr(pdf_path):
    """Determines if a PDF requires OCR by checking extracted text."""
    text = extract_text_from_pdf(pdf_path)

    if text is None or len(text.strip()) == 0:
        return True  # No text at all, needs OCR

    if re.search(r'\(CID:\s?\d+\)', text):  # Detect CID issues
        return True  

    if len(text) < 500 or is_metadata_only(text):  # Too short or mostly metadata
        return True  

    return False

# Function to process PDFs
def process_pdf(pdf_path, txt_path):
    """Extracts text from a PDF normally; falls back to OCR if needed."""
    try:
        print(f"Processing: {os.path.basename(pdf_path)}")  # Log processing file
        text = extract_text_from_pdf(pdf_path)
        if text is None or len(text.strip()) == 0:
            print(f"Using OCR for: {os.path.basename(pdf_path)} (No text found)")
            ocr_pdf(pdf_path, txt_path)  # Fallback to OCR
        else:
            with open(txt_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
    except Exception as e:
        log_error(os.path.basename(pdf_path), f"PDF processing failed: {e}")

# Function to process PDFs with matching small text files
def process_selected_pdfs():
    """Processes only PDFs that have a matching .txt file < 20KB or >140KB with CID."""
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    # Filter PDFs based on matching .txt conditions
    files_to_process = [f for f in files if should_process_pdf(f)]

    with ThreadPoolExecutor() as executor:
        future_to_file = {
            executor.submit(
                ocr_pdf if needs_ocr(os.path.join(input_dir, filename)) else process_pdf,
                os.path.join(input_dir, filename),
                os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
            ): filename
            for filename in files_to_process
        }

        for future in future_to_file:
            future.result()  # Ensure each task completes

    print("Text extraction complete!")

# Run processing
process_selected_pdfs()
