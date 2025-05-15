## Denne file håndterer parsin og tolkning av brukerens spørring. 
## Den prøver å lage en strukturert filter liste som author, topic og year fra spørringen.

import re
import string
import ast
from database import SessionLocal
from models import Article

def normalize(text):
    if not text:
        return ""
    if isinstance(text, list):
        text = " ".join(text)
    translator = str.maketrans("", "", string.punctuation)
    return text.lower().translate(translator).strip()

def author_matches(stored_author, filter_author):
    if not stored_author or stored_author == "None":
        return False
    try:
        authors_list = ast.literal_eval(stored_author)
        if authors_list is None:
            authors_list = []
    except Exception:
        authors_list = [stored_author]

    if not isinstance(authors_list, list):
        authors_list = [authors_list]
    if not authors_list:
        return False

    filter_words = normalize(filter_author).split()
    for author in authors_list:
        if not author:
            continue
        author_clean = normalize(author)
        if ',' in author_clean:
            parts = [p.strip() for p in author_clean.split(',')]
            reversed_author = " ".join(parts[::-1])
        else:
            reversed_author = author_clean

        if (all(word in author_clean for word in filter_words) or
                all(word in reversed_author for word in filter_words)):
            return True
    return False

def clean_author_field(stored_author):
    if not stored_author or stored_author == "None":
        return ""
    try:
        authors_list = ast.literal_eval(stored_author)
        if isinstance(authors_list, list):
            cleaned_authors = []
            for author in authors_list:
                if ',' in author:
                    parts = [p.strip() for p in author.split(',', 1)]
                    cleaned_authors.append(f"{parts[1]} {parts[0]}")
                else:
                    cleaned_authors.append(author.strip())
            return ", ".join(cleaned_authors)
    except Exception:
        pass
    return stored_author

def looks_like_person_name(text):
    disallowed_words = {"data", "things", "internet", "science", "model", "learning", "of", "the"}
    words = text.strip().split()
    if not (1 < len(words) <= 3):
        return False
    return all(w.lower() not in disallowed_words for w in words)

def extract_filters_from_query(raw_query):
    filter_author = ""
    filter_topic = ""
    filter_year = ""
    filter_location = ""

    original_query = raw_query.strip()
    raw_query_lower = raw_query.lower()

    m_author = re.search(
        r'\b(by|av)\s+([A-ZÆØÅ][a-zæøå]+(?:\s+[A-ZÆØÅ][a-zæøå]+){0,3})\b',
        raw_query,
        re.IGNORECASE
    )
    if m_author:
        filter_author = m_author.group(2).strip()
        original_query = original_query.replace(m_author.group(0), '').strip()

    m_location = re.search(
        r'\b(from|fra)\s+([a-zA-ZæøåÆØÅ\s,]+?)(?=\s+(19|20)\d{2}|$)',
        raw_query,
        re.IGNORECASE
    )
    if m_location:
        filter_location = m_location.group(2).strip()
        original_query = original_query.replace(m_location.group(0), '').strip()

    m_year = re.search(r'\b(19|20)\d{2}\b', raw_query_lower)
    if m_year:
        filter_year = m_year.group(0)
        original_query = original_query.replace(filter_year, '').strip()

    candidate_text = original_query.strip()
    filler_patterns = [
        r'\bgive me\b', r'\bshow me\b', r'\bfind\b', r'\bsearch\b', r'\bfetch\b',
        r'\barticles?\b', r'\bpapers?\b', r'\bstudies?\b', r'\babout\b',
        r'\bon\b', r'\bthe\b', r'\bpaper\b', r'\bwritten\b', r'\bby\b', r'\bfrom\b',
        r'\bartikler?\b', r'\bskrevet\b', r'\bom\b', r'\bav\b', r'\bfra\b'
    ]
    candidate_text = re.sub("|".join(filler_patterns), "", candidate_text, flags=re.IGNORECASE)
    candidate_text = re.sub(r'\s+', ' ', candidate_text).strip()

    words = candidate_text.split()
    common_topic_words = {
        "data", "science", "learning", "analyse", "modell", "forskning", "helse", "teknologi"
    }

    if not filter_author and filter_year:
        if 1 < len(words) <= 3 and all(w.lower() not in common_topic_words for w in words):
            filter_author = candidate_text.title()
            candidate_text = ""

    if not filter_author and not filter_topic:
        if len(words) == 1 and words[0].isalpha():
            norm_word = words[0].lower()
            with SessionLocal() as session:
                match = session.query(Article).filter(Article.author.ilike(f"%{norm_word}%")).first()
            if match:
                filter_author = words[0].title()
                print(f"FINAL FALLBACK: Found author match in DB → '{filter_author}'")
            else:
                filter_topic = words[0]
                print(f"FINAL FALLBACK: No author match, treating as topic → '{filter_topic}'")
        elif 1 < len(words) <= 3 and looks_like_person_name(candidate_text):
            filter_author = candidate_text.title()
            print(f"FINAL FALLBACK: Name-like phrase treated as author → '{filter_author}'")
        else:
            filter_topic = candidate_text
            print(f"FINAL FALLBACK: Treated as topic → '{filter_topic}'")
    elif not filter_topic and candidate_text:
        filter_topic = candidate_text.strip()

    print(f"[Parsed Query] Raw: '{raw_query}' → Author: '{filter_author}', Location: '{filter_location}', Topic: '{filter_topic}', Year: '{filter_year}'")
    return filter_author, filter_topic, filter_year, filter_location
