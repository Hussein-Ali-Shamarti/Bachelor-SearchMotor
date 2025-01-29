import os
import re
import glob
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Ensure required NLTK resources are downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define directory
directory = r'C:\My Web Sites\data\pdftexts'  # Use raw string for Windows paths
txt_files = glob.glob(os.path.join(directory, '*.txt'))

if not txt_files:
    print(f"No text files found in {directory}.")
    exit()

for txt_file in txt_files:
    try:
        # Read file with UTF-8 and error handling
        with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Debug: Check if content is read properly
        if not content.strip():
            print(f"Skipping empty file: {txt_file}")
            continue  # Skip empty files

        print(f"Processing file: {txt_file} (Original length: {len(content)} chars)")

        # Text cleaning steps
        content = content.lower()  # Convert to lowercase
        content = re.sub(r'\s+', ' ', content)  # Remove extra whitespaces
        content = re.sub(r'[^\w\s]', '', content)  # Remove punctuation
        tokens = word_tokenize(content)  # Tokenize words
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]  # Lemmatize & remove stopwords
        cleaned_content = ' '.join(tokens)  # Convert back to string

        # Debug: Check if cleaning removed all text
        if not cleaned_content.strip():
            print(f"Warning: Cleaning removed all text from {txt_file}. Skipping write to avoid data loss.")
            continue  # Don't overwrite file with empty content

        # Write cleaned content back to the file
        with open(txt_file, 'w', encoding='utf-8', errors='replace') as f:
            f.write(cleaned_content)

        print(f"Successfully cleaned: {txt_file} (New length: {len(cleaned_content)} chars)")

    except Exception as e:
        print(f"Error processing file {txt_file}: {e}")

print("Data cleaning completed!")
