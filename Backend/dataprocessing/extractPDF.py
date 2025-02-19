import os
import re
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from pdf2image import convert_from_path
import pytesseract
from tqdm import tqdm

# ---------------- Configuration ---------------- #

INPUT_DIR = r"C:\My Web Sites\dataset\www.thinkmind.org\articles"
OUTPUT_DIR = r"C:\My Web Sites\data\refpdftexts"
DEBUG_DIR = os.path.join(OUTPUT_DIR, "debug")
LOG_DIR = os.path.join(OUTPUT_DIR, "logs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Set up logging to both console and a log file for failed scans.
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler (logs to LOG_DIR/failed_scans.log)
log_file_path = os.path.join(LOG_DIR, "failed_scans.log")
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ---------------- OCR Extraction ---------------- #

def ocr_extract_text(pdf_path):
    """
    Force OCR extraction on all pages of the PDF.
    """
    try:
        poppler_path = r"C:\Users\henri\OneDrive\Skrivebord\poppler-24.08.0\Library\bin"  # Update this path if necessary!
        pages = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n"
        return text
    except Exception as e:
        logger.error(f"OCR extraction failed for {pdf_path}: {e}")
        return ""  # Return an empty string on failure

# ---------------- PDF Processing ---------------- #

def process_pdf(pdf_path):
    """
    Process a PDF by:
      1. Extracting text via OCR on all pages.
      2. Saving the full OCR text to a debug file.
    """
    try:
        ocr_text = ocr_extract_text(pdf_path)
        
        # Save the raw OCR text for debugging.
        debug_file = os.path.join(DEBUG_DIR, os.path.splitext(os.path.basename(pdf_path))[0] + "_debug.txt")
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(ocr_text)
    except Exception as e:
        logger.error(f"Error processing {pdf_path}: {e}")

# ---------------- Main ---------------- #

def main():
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    tasks = []
    with ThreadPoolExecutor() as executor:
        with tqdm(total=len(pdf_files), desc="Processing PDFs") as pbar:
            for filename in pdf_files:
                pdf_path = os.path.join(INPUT_DIR, filename)
                tasks.append(executor.submit(process_pdf, pdf_path))
            for task in as_completed(tasks):
                try:
                    task.result()
                except Exception as e:
                    logger.error(f"Task error: {e}")
                pbar.update(1)

if __name__ == "__main__":
    main()
