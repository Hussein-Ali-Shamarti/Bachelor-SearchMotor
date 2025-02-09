import os
import sys
import io
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Conference, Article

# Set up logging configuration to log errors to a file
logging.basicConfig(
    filename='error_log.log',  # Log file where errors will be stored
    level=logging.ERROR,  # Log only errors and above
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to connect to the existing SQLite database (Items.db)
def connect_to_existing_database():
    DATABASE_URL = "sqlite:///Backend/Items.db"  # Ensure the path is correct
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


# Function to insert conference info into the Conferences table
def insert_conference_info(conference_data, session):
    new_conference = Conference(
        name=conference_data["Conference Name"],
        articles=",".join(conference_data["Articles"])  # Store articles as comma-separated string
    )
    session.add(new_conference)
    session.commit()  # Commit conference insertion to ensure conference is added to the database
    print(f"Inserted conference: {conference_data['Conference Name']} with ID: {new_conference.id}")  # Debugging
    return new_conference

# Function to insert article info into the Articles table
def insert_article_info(article_data, session):
    print(f"Inserting article: {article_data['title']}")  # Debugging

    try:
        # Extract the conference title from the article data
        full_conference_title = article_data.get("conference_title", "").strip()
        
        conference_search_term = full_conference_title.split(",")[0].strip()  # Extract only "ACHI 2012"
        print(f"Looking for conference with search term: '{conference_search_term}'")  # Debugging

        # Search for the corresponding conference by partial match in the name (without year)
        conference = session.query(Conference).filter(Conference.name.contains(conference_search_term.split(" ")[0])).first()
        
        print(f"Looking for conference with search term: '{conference_search_term}'")  # Debugging

        if not conference:
            # Search for the corresponding conference by partial match in the name
            conference = session.query(Conference).filter(Conference.name.contains(conference_search_term)).first()

            if not conference:
                print(f"[ERROR] Conference with search term '{conference_search_term}' not found. Article '{article_data['title']}' will be inserted without a conference.")
                # Insert the article without a conference_id
                conference_id = None
            else:
                conference_id = conference.id
        else:
            conference_id = conference.id

        print(f"[DEBUG] Found Conference: {conference.name if conference else 'No Conference'}")  # Debugging
        
        # Create the Article object
        new_article = Article(
            title=article_data.get("title", "Unknown Title"),
            isbn=article_data.get("isbn", ""),
            author=", ".join(article_data.get("author", [])),
            publication_date=article_data.get("publication_date", ""),
            pdf_url=article_data.get("pdf_url", ""),
            pdf_texts=article_data.get("pdf_texts", ""),
            authors=", ".join(article_data.get("Authors", [])),
            keywords=article_data.get("Keywords", ""),
            abstract=article_data.get("Abstract", ""),
            location=article_data.get("Location", ""),
            start_date=article_data.get("start_date", "Unknown"),
            end_date=article_data.get("end_date", "Unknown"),
            conference_id=conference_id  # Link to the conference, or None if no conference was found
        )

        # Debugging: Print article details before committing
        print(f"[DEBUG] Article ready to insert: {new_article}")

        session.add(new_article)
        session.commit()
        print(f"[SUCCESS] Article '{new_article.title}' inserted with Conference ID: {new_article.conference_id}")

    except Exception as e:
        print(f"[ERROR] Failed to insert article '{article_data['title']}': {e}")
        logging.error(f"Failed to insert article '{article_data['title']}': {e}", exc_info=True)  # Log the error
        session.rollback()

# Function to extract conference data from the .txt file
def get_conference_data_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    conference_data = {
        "Conference Name": "",
        "Articles": []
    }

    for line in content:
        if line.startswith("Conference Name:"):
            conference_data["Conference Name"] = line.split(":", 1)[1].strip()
            print(f"Found Conference Name: {conference_data['Conference Name']}")  # Debugging
        if line.startswith("Articles:"):
            conference_data["Articles"] = [article.strip() for article in line.split(":", 1)[1].split(",")]

    return conference_data

# Function to extract article data from the .txt file
def get_article_data_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()

    article_data = {
        "title": "",
        "author": [],
        "publication_date": "",
        "pdf_url": "",
        "pdf_texts": "",
        "start_date": "Unknown",
        "end_date": "Unknown",
        "conference_title": "Unknown Conference",  # Default value for missing conference title
        "Keywords": "",
        "Abstract": "",
        "Location": "",
        "isbn": "None",
        "Authors": []
    }
    dates = ""

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
            article_data["pdf_url"] = line.split(":", 1)[1].strip()
        # Remove the duplicate "http://www.thinkmind.org" if it occurs at the beginning of the URL
        if article_data["pdf_url"].startswith("http://www.thinkmind.org"):
            article_data["pdf_url"] = article_data["pdf_url"].replace("http://www.thinkmind.org", "", 1)  # Only replace the first occurrence
        elif line.startswith("Authors:"):
            article_data["Authors"] = [author.strip() for author in line.split(":", 1)[1].split(",")]
        elif line.startswith("Keywords:"):
            article_data["Keywords"] = line.split(":", 1)[1].strip()
        elif line.startswith("Abstract:"):
            article_data["Abstract"] = line.split(":", 1)[1].strip()
        elif line.startswith("Location:"):
            article_data["Location"] = line.split(":", 1)[1].strip()
        elif line.startswith("Dates:"):
            dates = line.split(":", 1)[1].strip() if ":" in line else ""
        if "to" in dates:
            try:
                start_date, end_date = dates.replace("from ", "").split(" to ")
                article_data["start_date"] = start_date.strip()
                article_data["end_date"] = end_date.strip()
            except ValueError:
                article_data["start_date"] = "Invalid format"
                article_data["end_date"] = "Invalid format"
                print(f"Failed to parse Dates for article: {file_path}")
        else:
            article_data["start_date"] = "Unknown"
            article_data["end_date"] = "Unknown"

    # Log if conference_title is missing
    if article_data["conference_title"] in ["", "None"]:
        print(f"Warning: Missing conference_title in file: {file_path}")
        article_data["conference_title"] = "Unknown Conference"
    
    # Get the base name of the article file (without the .txt extension)
    article_base_name = os.path.splitext(os.path.basename(file_path))[0]
    print(f"Generated article base name: '{article_base_name}'")  # Debugging output

    # Path to the PDF text file in pdftexts directory
    pdf_file_path = f"C:/My Web Sites/data/pdftexts/{article_base_name}.txt"
    print(f"Checking for PDF file at path: {pdf_file_path}")  # Debugging output

    # Check if the PDF text file exists
    if os.path.exists(pdf_file_path):
        try:
            with open(pdf_file_path, 'r', encoding='utf-8', errors='ignore') as pdf_file:
                article_data["pdf_texts"] = pdf_file.read()  # Load the content of the PDF text file
            print(f"Successfully found and added PDF text for article: {article_data['title']}")
        except Exception as e:
            print(f"Error reading PDF text file for article '{article_data['title']}': {e}")
            logging.error(f"Error reading PDF text file for article '{article_data['title']}': {e}", exc_info=True)
    else:
        article_data["pdf_texts"] = ""  # No PDF text found
        print(f"No PDF text found for article: {article_data['title']} at path: {pdf_file_path}")

    return article_data


# Function to process article files in the articles folder
def process_article_files(articles_folder, session):
    print(f"Scanning articles directory: {articles_folder}")  # Debugging
    for root_article, dirs_article, files_article in os.walk(articles_folder):
        for file_article in files_article:
            file_path = os.path.join(root_article, file_article)
            if file_path.endswith(".txt"):  # Only process .txt files
                try:
                    print(f"Processing article file: {file_path}")
                    article_data = get_article_data_from_txt(file_path)
                    insert_article_info(article_data, session)  # Insert each article into the database
                except Exception as e:
                    print(f"[ERROR] Failed to process article file {file_path}: {e}")
                    logging.error(f"Failed to process article file {file_path}: {e}", exc_info=True)

# Main function to handle the conference and article data
def main():
    start_time = time.time()
    session = connect_to_existing_database()

    try:
        conference_file_path = "path_to_conference_file.txt"  # Specify the actual conference data file
        conference_data = get_conference_data_from_txt(conference_file_path)
        conference = insert_conference_info(conference_data, session)

        articles_folder = "path_to_articles_folder"  # Specify the actual articles folder
        process_article_files(articles_folder, session)  # Process article files

        print("Process completed successfully!")

    except Exception as e:
        print(f"[ERROR] Unexpected error occurred: {e}")
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
    
    finally:
        session.close()

    print(f"Time taken: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()
