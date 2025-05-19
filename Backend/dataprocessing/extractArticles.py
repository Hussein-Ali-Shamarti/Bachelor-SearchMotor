# Dette skriptet går gjennom HTML-filer i en katalogstruktur, henter ut artikkelinformasjon fra meta-tags 
# og hovedinnhold, og lagrer metadataen som .txt-filer i en speilstruktur. HTML-filer uten nødvendig info hoppes over.


import os
from bs4 import BeautifulSoup
from tqdm import tqdm

def article_info(html_file):
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Check if required meta tags exist
        title = soup.find("meta", attrs={"name": "citation_title"})
        if not title:  # Skip if no citation_title meta tag is found
            print(f"Skipping {html_file}: No citation_title meta tag found.")
            return None

        # Extract meta tags
        title = title.get("content")

        author_elements = soup.find_all("meta", attrs={"name": "citation_author"})
        authors = [author_element.get("content") for author_element in author_elements] if author_elements else None

        isbn_element = soup.find("meta", attrs={"name": "citation_isbn"})
        isbn = isbn_element.get("content") if isbn_element else None

        publication_date_element = soup.find("meta", attrs={"name": "citation_publication_date"})
        publication_date = publication_date_element.get("content") if publication_date_element else None

        conference_title_element = soup.find("meta", attrs={"name": "citation_conference_title"})
        conference_title = conference_title_element.get("content") if conference_title_element else None

        pdf_url_element = soup.find("meta", attrs={"name": "citation_pdf_url"})
        pdf_url = pdf_url_element.get("content") if pdf_url_element else None

        # Extract main content
        main_content = soup.find("td", class_="text")
        all_p_tags = main_content.find_all("p", class_="a3") if main_content else None

        wanted_content = ["Authors:", "Keywords:", "Abstract:", "Location:", "Dates:"]
        extracted_info = {}

        if all_p_tags:
            for p_tag in all_p_tags:
                for content in wanted_content:
                    if content in p_tag.text:
                        info = p_tag.text.split(content)[1].strip()
                        extracted_info[content[:-1]] = info
        else:
            print(f"Warning: No main content found in {html_file}")

        return {
            "title": title,
            "isbn": isbn,
            "author": authors,
            "publication_date": publication_date,
            "conference_title": conference_title,
            "pdf_url": pdf_url,
            **extracted_info
        }
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return None

source_folder = r"C:\My Web Sites\dataset\www.thinkmind.org\library"
destination_folder = r"C:\My Web Sites\data\articles"

html_files = []
for root, _, files in os.walk(source_folder):
    for file in files:
        if file.endswith('.html'):
            html_files.append((root, file))

with tqdm(total=len(html_files), desc="Processing HTML files") as pbar:
    for root, file in html_files:
        source_file = os.path.join(root, file)
        relative_path = os.path.relpath(root, source_folder)
        destination_dir = os.path.join(destination_folder, relative_path)
        os.makedirs(destination_dir, exist_ok=True)

        destination_file_txt = os.path.join(destination_dir, os.path.splitext(file)[0] + '.txt')

        if os.path.exists(destination_file_txt):
            pbar.update(1)
            continue

        article_data = article_info(source_file)
        if article_data is None:
            pbar.update(1)
            continue

        with open(destination_file_txt, 'w', encoding='utf-8') as f:
            for key, value in article_data.items():
                f.write(f'{key}: {value}\n')

        pbar.update(1)

print("Article information extraction completed!")
