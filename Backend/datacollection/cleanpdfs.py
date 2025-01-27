"""
This script processes all .txt files in the specified 'pdftexts' directory that are larger than 75KB.
It decodes artifacts in the text files represented as (cid:xx) patterns, which often occur when extracting
text from PDFs. These patterns are replaced with their corresponding Unicode characters. The cleaned 
text files are saved in a separate 'cleanpdfs' directory, preserving the original files.

Key Features:
1. Processes only files larger than 75KB to save time and resources.
2. Decodes (cid:xx) patterns into readable characters using Unicode.
3. Saves the cleaned files in the 'cleanpdfs' directory with the same filenames.
4. Retains the original files in the 'pdftexts' directory.
"""

import os
import re

# Define the directories
pdftexts_dir = r"C:\My Web Sites\data\pdftexts"
cleanpdfs_dir = r"C:\My Web Sites\data\cleanpdfs"

# Create the cleanpdfs directory if it doesn't exist
os.makedirs(cleanpdfs_dir, exist_ok=True)

def decode_cid_artifacts(text):
    """
    Decode (cid:xx) patterns into their respective characters.
    """
    def cid_to_char(match):
        # Extract the number from the (cid:xx) pattern and convert to character
        cid_value = int(match.group(1))
        return chr(cid_value)
    
    # Replace all (cid:xx) patterns with their corresponding characters
    return re.sub(r"\(cid:(\d+)\)", cid_to_char, text)

def clean_and_decode_file(file_path, output_dir):
    """
    Decode (cid:xx) patterns in a text file and save the cleaned content.
    """
    try:
        # Read the original file content
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Decode the (cid:xx) patterns
        decoded_content = decode_cid_artifacts(content)
        
        # Save the cleaned content to the new file in the output directory
        filename = os.path.basename(file_path)
        cleaned_file_path = os.path.join(output_dir, filename)
        
        with open(cleaned_file_path, "w", encoding="utf-8") as file:
            file.write(decoded_content)
        
        print(f"Decoded and saved file: {cleaned_file_path}")
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

def clean_large_txt_files(input_dir, output_dir, size_limit_kb=100):
    """
    Process all .txt files in the input directory that are larger than the specified size.
    Decode (cid:xx) patterns and save to the output directory.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        return
    
    txt_files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    if not txt_files:
        print("No .txt files found in the input directory.")
        return
    
    print(f"Found {len(txt_files)} .txt files. Checking file sizes...")
    
    for txt_file in txt_files:
        file_path = os.path.join(input_dir, txt_file)
        file_size_kb = os.path.getsize(file_path) / 1024  # Convert bytes to KB
        
        # Process only files larger than the size limit
        if file_size_kb > size_limit_kb:
            print(f"Processing {txt_file} ({file_size_kb:.2f} KB)...")
            clean_and_decode_file(file_path, output_dir)
        else:
            print(f"Skipping {txt_file} ({file_size_kb:.2f} KB, below size limit).")
    
    print("Cleanup complete! All cleaned files saved to:", output_dir)

# Run the script
if __name__ == "__main__":
    clean_large_txt_files(pdftexts_dir, cleanpdfs_dir, size_limit_kb=75)
