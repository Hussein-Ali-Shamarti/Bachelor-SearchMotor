import os
import re
import glob
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import wordninja  # External library for word segmentation

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
        print(f"Processing file: {txt_file}")

        # Read file line by line to handle large files efficiently
        cleaned_tokens = []
        with open(txt_file, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                # Clean the line by removing unwanted punctuation but keeping spaces
                line = line.lower()  # Convert to lowercase
                line = re.sub(r'\s+', ' ', line)  # Normalize all whitespaces (single space)
                line = re.sub(r'[^\w\s]', '', line)  # Remove punctuation, keep words and spaces

                # If the line has concatenated words (CamelCase), break them
                line = wordninja.split(line)  # This will split CamelCase text
                line = ' '.join(line)  # Join back into a sentence

                tokens = word_tokenize(line)  # Tokenize words
                
                # Remove stopwords and lemmatize the words
                tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
                
                # Add cleaned tokens to list
                cleaned_tokens.extend(tokens)

        # Join the tokens back with a single space
        cleaned_content = ' '.join(cleaned_tokens)
        
        # Check if the content is empty after cleaning
        if not cleaned_content.strip():
            print(f"Warning: No meaningful content left in {txt_file} after cleaning. Skipping write operation.")
            continue  # Don't overwrite with empty content

        # Write cleaned content back to the file
        with open(txt_file, 'w', encoding='utf-8', errors='replace') as f:
            f.write(cleaned_content)

        print(f"Successfully cleaned: {txt_file} (New length: {len(cleaned_content)} chars)")

    except Exception as e:
        print(f"Error processing file {txt_file}: {e}")

print("Data cleaning completed!")
