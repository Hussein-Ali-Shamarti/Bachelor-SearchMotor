import time
import numpy as np
import os
import ast
import re
import sys
from sqlalchemy import cast, create_engine, String, or_, func
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import Article, Conference
from tqdm import tqdm

sys.stdout.reconfigure(encoding='utf-8')

# Set the DATABASE_URL to point to your SQLite DB in the Backend folder
DATABASE_URL = "sqlite:///./Backend/HybridSearch.db"

# Connect to SQLite
def connect_to_sqlite():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()

# Base path to the embedded folder
EMBEDDED_FOLDER = r"C:/My Web Sites/data/embedded"
PDFTEXTS_FOLDER = r"C:/My Web Sites/data/pdftexts"

def extract_dates(dates_text):
    # Use regex to extract two dates from the format: "from June 19, 2011 to June 24, 2011"
    date_pattern = re.findall(r"([A-Za-z]+ \d{1,2}, \d{4})", dates_text)
    if len(date_pattern) == 2:
        return date_pattern[0], date_pattern[1]  # (start_date, end_date)
    else:
        print(f"Warning: Could not parse dates from '{dates_text}'")
        return "Unknown", "Unknown"

def get_article_data_from_txt(file_path):
    """Extracts article metadata from a .txt file"""
    article_data = {
        "title": "",
        "author": [],
        "publication_date": "",
        "pdf_url": "",
        "pdf_texts": "",
        "embeddings": None,
        "start_date": "Unknown",
        "end_date": "Unknown",
        "conference_title": "Unknown Conference",
        "Keywords": [],
        "Abstract": "",
        "Location": "",
        "isbn": "None",
    }

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.readlines()

    for line in content:
        if line.startswith("title:"):
            article_data["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("isbn:"):
            article_data["isbn"] = line.split(":", 1)[1].strip()
        elif line.startswith("author:"):
            article_data["author"] = [author.strip() for author in line.split(":", 1)[1].split(",")]
        elif line.startswith("publication_date:"):
            article_data["publication_date"] = line.split(":", 1)[1].strip()
        elif line.startswith("conference_title:"):
            article_data["conference_title"] = line.split(":", 1)[1].strip()
        elif line.startswith("pdf_url:"):
            # Extract the pdf_url from the file
            pdf_url = line.split(":", 1)[1].strip()
            # If the url starts with the duplicated prefix, remove it.
            # For example, this converts:
            # "http://www.thinkmind.orghttps://www.thinkmind.org/articles/access_2011_1_10_40018.pdf"
            # into:
            # "https://www.thinkmind.org/articles/access_2011_1_10_40018.pdf"
            if pdf_url.startswith("http://www.thinkmind.org"):
                pdf_url = pdf_url.replace("http://www.thinkmind.org", "", 1)
            article_data["pdf_url"] = pdf_url
        elif line.startswith("Keywords:"):
            article_data["Keywords"] = [kw.strip() for kw in line.split(":", 1)[1].split(";")]
        elif line.startswith("Abstract:"):
            article_data["Abstract"] = line.split(":", 1)[1].strip()
        elif line.startswith("Location:"):
            article_data["Location"] = line.split(":", 1)[1].strip()
        elif line.startswith("Dates:"):
            dates_text = line.split(":", 1)[1].strip()
            article_data["start_date"], article_data["end_date"] = extract_dates(dates_text)

    # Extract base filename
    article_base_name = os.path.splitext(os.path.basename(file_path))[0]

    # Load full text
    pdf_text_path = os.path.join(PDFTEXTS_FOLDER, f"{article_base_name}.txt")
    if os.path.exists(pdf_text_path):
        try:
            with open(pdf_text_path, 'r', encoding='utf-8', errors='replace') as pdf_file:
                article_data["pdf_texts"] = pdf_file.read()
        except Exception as e:
            print(f"Error reading full text for {article_data['title']}: {e}")
            article_data["pdf_texts"] = ""
    else:
        print(f"No full text found for {article_data['title']}")

    # Load embedding
    npy_file_path = os.path.join(EMBEDDED_FOLDER, f"{article_base_name}.npy")
    if os.path.exists(npy_file_path):
        try:
            embedding = np.load(npy_file_path)
            article_data["embeddings"] = embedding.tobytes()  # Store as list for pgvector
        except Exception as e:
            print(f"Error loading embedding for {article_data['title']}: {e}")
            article_data["embeddings"] = None
    else:
        print(f"No embedding found for {article_data['title']}")
    return article_data

def insert_article_info(article_data, session):
    try:
        conference = None
        full_conference_title = article_data.get("conference_title", "").strip()

        # **Extract acronym before the comma and remove the year**
        first_part = full_conference_title.split(",", 1)[0].strip()
        conference_acronym = re.sub(r'\b\d{4}\b', '', first_part).strip()

        # **Query the database for a match using name and stored list**
        conference = (
            session.query(Conference)
            .filter(
                or_(
                    Conference.name.ilike(f"{conference_acronym},%"),
                    cast(Conference.articles, String).ilike(f"%{full_conference_title}%"),
                    cast(Conference.articles, String).ilike(f"%{conference_acronym}%")
                )
            )
            .first()
        )

        conference_id = conference.id if conference else None

        if not conference:
            print(f"Warning: No matching conference found for '{full_conference_title}'. Inserting article without conference link.")

        # **Create and insert the article**
        new_article = Article(
            title=article_data.get("title", "Unknown Title"),
            isbn=article_data.get("isbn", ""),
            author=", ".join(article_data.get("author", [])),
            publication_date=article_data.get("publication_date", ""),
            pdf_url=article_data.get("pdf_url", ""),
            pdf_texts=article_data.get("pdf_texts", ""),
            keywords=article_data.get("Keywords", []),
            abstract=article_data.get("Abstract", ""),
            location=article_data.get("Location", ""),
            start_date=article_data.get("start_date", "Unknown"),
            end_date=article_data.get("end_date", "Unknown"),
            embeddings=article_data.get("embeddings", None),
            conference_id=conference_id
        )

        session.add(new_article)
        session.commit()

    except Exception as e:
        print(f"Error inserting article '{article_data['title']}': {e}")
        session.rollback()

def get_conference_data_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    conference_data = {"Conference Name": "", "Articles": []}

    for line in content:
        if line.startswith("Conference Name:"):
            conference_data["Conference Name"] = line.split(":", 1)[1].strip()
            print(f"Found Conference: {conference_data['Conference Name']}")
        if line.startswith("Articles:"):
            articles_str = line.split(":", 1)[1].strip()
            try:
                # Convert the text list to an actual list
                conference_data["Articles"] = ast.literal_eval(articles_str)
            except Exception as e:
                print(f"Error parsing articles list for {conference_data['Conference Name']}: {e}")
                conference_data["Articles"] = []  # Default to empty list if parsing fails
    return conference_data

def insert_conference_info(conference_data, session):
    try:
        new_conference = Conference(
            name=conference_data["Conference Name"],
            articles=conference_data["Articles"]  # Store as ARRAY(String)
        )
        session.add(new_conference)
        session.commit()
        print(f"Inserted Conference: {new_conference.name} (ID: {new_conference.id})")
        return new_conference
    except Exception as e:
        print(f"[ERROR] Failed to insert conference '{conference_data['Conference Name']}': {e}")
        session.rollback()
        return None

def process_article_files(articles_folder, session):
    """Processes all article .txt files with a progress bar."""
    print(f"Scanning articles directory: {articles_folder}")

    # Collect all article files
    article_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(articles_folder)
        for file in files if file.endswith(".txt")
    ]

    if not article_files:
        print("No article files found.")
        return

    # Process articles with progress bar
    for file_path in tqdm(article_files, desc="Processing Articles", unit="file"):
        try:
            article_data = get_article_data_from_txt(file_path)
            insert_article_info(article_data, session)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def process_conference_files(conferences_folder, session):
    """Processes all conference .txt files only if they don’t exist in the database."""
    # Check if conferences already exist in the database
    existing_conferences = session.query(Conference).count()
    if existing_conferences > 0:
        print("Conferences already exist in the database. Skipping processing.")
        return

    print(f"Scanning conference directory: {conferences_folder}")

    # Collect all conference files
    conference_files = [
        os.path.join(root, file)
        for root, _, files in os.walk(conferences_folder)
        for file in files if file.endswith(".txt")
    ]

    if not conference_files:
        print("No conference files found.")
        return

    # Process conferences with progress bar
    for file_path in tqdm(conference_files, desc="Processing Conferences", unit="file"):
        try:
            conference_data = get_conference_data_from_txt(file_path)
            insert_conference_info(conference_data, session)
        except Exception as e:
            print(f"Error processing conference file {file_path}: {e}")

def main():
    start_time = time.time()
    session = connect_to_sqlite()

    try:
        conferences_folder = "C:/My Web Sites/data/conferences"
        process_conference_files(conferences_folder, session)

        articles_folder = "C:/My Web Sites/data/articles"
        process_article_files(articles_folder, session)

        print("Process completed successfully!")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        session.close()

    print(f"Time taken: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()