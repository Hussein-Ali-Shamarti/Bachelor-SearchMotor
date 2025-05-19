# Dette skriptet leser HTML-filer for konferanser, henter ut konferansenavn og tilhørende artikler, 
# og lagrer denne informasjonen som .txt-filer. Det bruker BeautifulSoup for parsing og tqdm for fremdriftsvisning.


import os
from bs4 import BeautifulSoup
from tqdm import tqdm  # Progress bar library

def conference_info(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extracting the main content of the conference.
    main_content = soup.find("td", class_="text")
    
    # Extracting the conference name from the span class "a2none"
    conference_name = None
    conference_name_element = main_content.find("span", class_="a2none") if main_content else None
    if conference_name_element:
        conference_name = conference_name_element.text.strip()

    # Extracting the articles (conference details) from the unordered list
    articles = []
    ul_tag = main_content.find("ul") if main_content else None
    if ul_tag:
        article_links = ul_tag.find_all("a", class_="a3")
        articles = [article.text.strip() for article in article_links]

    # Add extracted information to the dictionary
    extracted_info = {
        "Conference Name": conference_name,
        "Articles": articles
    }

    # Debugging: Print the extracted data for inspection
    print(f"Extracted from {html_file}:")
    print(f"Conference Name: {conference_name}")
    print(f"Articles: {articles}")
    print(f"Extracted Info: {extracted_info}\n")

    return extracted_info

# Define source and destination folders.
source_folder = r"C:\My Web Sites\dataset\www.thinkmind.org\library"
destination_folder = r"C:\My Web Sites\data\conference"
os.makedirs(destination_folder, exist_ok=True)  # Ensure the destination folder exists.

# Get list of HTML files in the source folder.
html_files = [f for f in os.listdir(source_folder) if f.endswith('.html')]

# Process each HTML file and extract conference information.
with tqdm(total=len(html_files), desc="Processing HTML files") as pbar:
    for html_file in html_files:
        source_file = os.path.join(source_folder, html_file)
        destination_file_txt = os.path.join(destination_folder, os.path.splitext(html_file)[0] + '.txt')

        # Skip already processed files.
        if os.path.exists(destination_file_txt):
            pbar.update(1)
            continue

        # Extract conference information.
        conference_data = conference_info(source_file)

        if conference_data:
            # Save extracted information to the destination file.
            with open(destination_file_txt, 'w', encoding='utf-8') as f:
                for key, value in conference_data.items():
                    f.write(f'{key}: {value}\n')

        pbar.update(1)

print("Conference information extraction complete!")
