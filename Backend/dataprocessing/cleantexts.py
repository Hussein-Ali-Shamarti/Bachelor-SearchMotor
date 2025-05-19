# Dette skriptet søker etter alle .txt-filer i en angitt katalog, 
# fjerner overflødig mellomrom, tomme linjer og ikke-ASCII-tegn, 
# og overskriver filene med den rensede teksten. Tomme eller ugyldige filer blir hoppet over.


import os
import re
import glob

# Define directory
directory = r'C:\My Web Sites\backup\textbackup\pdftexts'  # Use raw string for Windows paths
txt_files = glob.glob(os.path.join(directory, '*.txt'))

if not txt_files:
    print(f"No text files found in {directory}.")
    exit()

for txt_file in txt_files:
    try:
        with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        if not content.strip():
            print(f"Skipping empty file: {txt_file}")
            continue

        print(f"Processing file: {txt_file} (Original length: {len(content)} chars)")

        cleaned_content = re.sub(r'[ \t]+', ' ', content)

        cleaned_content = re.sub(r'\n+', '\n', cleaned_content)
        
        cleaned_content = re.sub(r'[^\x20-\x7E\n]', '', cleaned_content)

        if not cleaned_content.strip():
            print(f"Warning: Cleaning removed all text from {txt_file}. Skipping write to avoid data loss.")
            continue

        with open(txt_file, 'w', encoding='utf-8', errors='replace') as f:
            f.write(cleaned_content)

        print(f"Successfully cleaned: {txt_file} (New length: {len(cleaned_content)} chars)")

    except Exception as e:
        print(f"Error processing file {txt_file}: {e}")

print("Data cleaning completed!")
