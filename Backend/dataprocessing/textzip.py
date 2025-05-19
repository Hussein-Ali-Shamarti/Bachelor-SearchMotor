
# Dette skriptet komprimerer alle .txt-filer i en angitt katalog til .gz-format ved hjelp av gzip, 
# og sletter de originale .txt-filene etter vellykket komprimering.


import os
import glob
import gzip
import shutil

# Define the directory where your processed text files are stored
directory = r'C:\My Web Sites\data\pdftexts'
txt_files = glob.glob(os.path.join(directory, '*.txt'))

if not txt_files:
    print(f"No text files found in {directory}.")
    exit()

for txt_file in txt_files:
    gz_file = txt_file + '.gz'
    try:
        with open(txt_file, 'rb') as f_in:
            with gzip.open(gz_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # After successful compression, remove the original .txt file.
        os.remove(txt_file)
        print(f"Compressed and removed {txt_file} -> {gz_file}")
    except Exception as e:
        print(f"Error processing {txt_file}: {e}")

print("Compression and replacement completed!")
