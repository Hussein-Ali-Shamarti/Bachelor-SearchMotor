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
    disallowed_words = {
    "data", "things", "internet", "science", "model", "learning",
    "of", "the", "articles", "papers", "studies", "find", "finn", "gi", "hent", "søk"
}

    words = text.strip().split()
    if not (1 < len(words) <= 3):
        return False
    return all(w.lower() not in disallowed_words for w in words)

def translate_norwegian(text):
    replacements = {
        r"\bfinn artikler\b": "find articles",
        r"\bfinn\b": "find",
        r"\bskrevet av\b": "written by",
        r"\bav\b": "by",
        r"\bom\b": "about",
        r"\bfra\b": "from",
        r"\bartikler\b": "articles"
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text.strip()



def extract_filters_from_query(raw_query):
    filter_author = ""
    filter_topic = ""
    filter_year = ""
    filter_location = ""

    raw_query = translate_norwegian(raw_query.strip())
    original_query = raw_query
    raw_query_lower = raw_query.lower()

    # -- 1. Eksplicit author: "by Ola Nordmann"
    m_author = re.search(
        r'\b(by|av)\s+([A-ZÆØÅ][a-zæøå]+(?:\s+[A-ZÆØÅ][a-zæøå]+){0,3})\b',
        raw_query,
        re.IGNORECASE
    )
    if m_author:
        filter_author = m_author.group(2).strip()
        original_query = original_query.replace(m_author.group(0), '').strip()

    # -- 2. Eksplicit location: "from Paris"
    m_location = re.search(
        r'\b(from|fra)\s+([a-zA-ZæøåÆØÅ\s,]+?)(?=\s+(19|20)\d{2}|$)',
        raw_query,
        re.IGNORECASE
    )
    if m_location:
        filter_location = m_location.group(2).strip()
        original_query = original_query.replace(m_location.group(0), '').strip()

    # -- 3. Eksplicit år
    m_year = re.search(r'\b(19|20)\d{2}\b', raw_query_lower)
    if m_year:
        filter_year = m_year.group(0)
        original_query = original_query.replace(filter_year, '').strip()

    # -- 4. Rens tekst
    candidate_text = original_query.strip()
    filler_patterns = [
        r'\bgive me\b', r'\bshow me\b', r'\bfind\b', r'\bsearch\b', r'\bfetch\b',
        r'\barticles?\b', r'\bpapers?\b', r'\bstudies?\b', r'\babout\b',
        r'\bon\b', r'\bthe\b', r'\bpaper\b', r'\bwritten\b', r'\bby\b', r'\bfrom\b',
        r'\bartikler?\b', r'\bskrevet\b', r'\bom\b', r'\bav\b', r'\bfra\b'
    ]
    candidate_text = re.sub("|".join(filler_patterns), "", candidate_text, flags=re.IGNORECASE)
    candidate_text = re.sub(r'\s+', ' ', candidate_text).strip()

    # -- 5. Analyser kommadelt input (f.eks. "barcelona, machine learning")
    fragments = [frag.strip() for frag in candidate_text.split(",") if frag.strip()]

    with SessionLocal() as session:
        authors = session.query(Article.author).distinct().all()

        for frag in fragments:
            norm_frag = normalize(frag)

            # Prøv som author via author_matches
            if not filter_author:
                for stored_author in authors:
                    if stored_author and author_matches(stored_author[0], frag):
                        filter_author = frag.title()
                        print(f"[Multi-part fallback] Matched author → '{filter_author}'")
                        break
                if filter_author:
                    continue

            # Prøv som location
            if not filter_location:
                location_match = session.query(Article).filter(Article.location.ilike(f"%{norm_frag}%")).first()
                if location_match:
                    filter_location = frag.title()
                    print(f"[Multi-part fallback] Found location → '{filter_location}'")
                    continue

            # Hvis ingen match, behandle som topic
            if not filter_topic:
                filter_topic = frag
                print(f"[Multi-part fallback] Treating as topic → '{filter_topic}'")

    # -- 6. Ekstra fallback hvis det fortsatt er ingenting
    words = candidate_text.split()
    if not (filter_author or filter_topic or filter_location):
        if len(words) == 1 and words[0].isalpha():
            norm_word = words[0].lower()
            with SessionLocal() as session:
                authors = session.query(Article.author).distinct().all()
                for stored_author in authors:
                    if stored_author and author_matches(stored_author[0], norm_word):
                        filter_author = words[0].title()
                        print(f"FINAL FALLBACK: Matched author by initials → '{filter_author}'")
                        break
                else:
                    location_match = session.query(Article).filter(Article.location.ilike(f"%{norm_word}%")).first()
                    if location_match:
                        filter_location = words[0].title()
                        print(f"FINAL FALLBACK: Found location match in DB → '{filter_location}'")
                    else:
                        filter_topic = words[0]
                        print(f"FINAL FALLBACK: No author or location match, treating as topic → '{filter_topic}'")
        elif 1 < len(words) <= 3 and looks_like_person_name(candidate_text):
            filter_author = candidate_text.title()
            print(f"FINAL FALLBACK: Name-like phrase treated as author → '{filter_author}'")
        else:
            filter_topic = candidate_text
            print(f"FINAL FALLBACK: Treated as topic → '{filter_topic}'")

    print(f"[Parsed Query] Raw: '{raw_query}' → Author: '{filter_author}', Location: '{filter_location}', Topic: '{filter_topic}', Year: '{filter_year}'")
    return filter_author, filter_topic, filter_year, filter_location
