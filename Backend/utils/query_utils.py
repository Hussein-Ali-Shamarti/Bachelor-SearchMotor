## Denne file håndterer parsing og tolkning av brukerens spørring. 
## Den prøver å lage en strukturert filter liste som author, topic, location og year fra spørringen.

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

def normalize_keywords(raw_keywords):
    if not raw_keywords:
        return []

    try:
        keywords = ast.literal_eval(raw_keywords) if isinstance(raw_keywords, str) else raw_keywords
    except Exception:
        keywords = raw_keywords

    if not isinstance(keywords, list):
        keywords = [keywords]

    split_keywords = []
    for kw in keywords:
        if isinstance(kw, str):
            split_keywords.extend([k.strip() for k in kw.split(",") if k.strip()])
        elif isinstance(kw, list):
            split_keywords.extend([str(k).strip() for k in kw if str(k).strip()])

    return split_keywords


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

def split_query_phrases(query):
    pattern = r'\b(written\s+by|about|by|from|in|on|om|av|fra)\b'
    matches = list(re.finditer(pattern, query, flags=re.IGNORECASE))

    phrases = []
    for i, match in enumerate(matches):
        prep = match.group(1).lower()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(query)
        phrase = query[start:end].strip()
        if phrase:
            phrases.append((prep, phrase))
    return phrases

def extract_filters_from_query(raw_query):
    filter_author = ""
    filter_topic = ""
    filter_year = ""
    filter_location = ""

    raw_query = translate_norwegian(raw_query.strip())
    raw_query_lower = raw_query.lower()

    m_year = re.search(r'\b(19|20)\d{2}\b', raw_query_lower)
    if m_year:
        filter_year = m_year.group(0)
        raw_query = raw_query.replace(filter_year, '').strip()

    phrases = split_query_phrases(raw_query)

    for prep, phrase in phrases:
        norm = normalize(phrase)
        if prep in {"about", "om", "on"} and not filter_topic:
            filter_topic = phrase
        elif prep in {"by", "written by", "av"} and not filter_author:
            filter_author = phrase
        elif prep in {"from", "fra"} and not filter_location:
            filter_location = phrase
            if phrase:
                pattern = rf"\b{re.escape(prep)}\s+{re.escape(phrase)}\b"
                raw_query = re.sub(pattern, '', raw_query, flags=re.IGNORECASE).strip()

    if not filter_author:
        author_re = re.search(
            r'\b(written\s+by|by|av)\s+([A-ZÆØÅa-zæøå\.]+(?:\s+[A-ZÆØÅa-zæøå\.]+){0,3})\b',
            raw_query,
            re.IGNORECASE
        )
        if author_re:
            potential_author = author_re.group(2).strip()
            if not any(w in potential_author.lower() for w in ['about', 'om', 'on']):
                filter_author = potential_author
                raw_query = raw_query.replace(f"{author_re.group(1)} {author_re.group(2)}", '').strip()

    # Fallback: ekstra fragmentanalyse
    candidate_text = re.sub(r'\b(give me|show me|find|search|fetch|articles?|papers?|studies?|written|by|from|about|om|av|fra|og|all|some|any)\b', '', raw_query, flags=re.IGNORECASE)
    candidate_text = re.sub(r'\s+', ' ', candidate_text).strip()
    fragments = re.split(r",| og ", candidate_text, flags=re.IGNORECASE)
    fragments = [frag.strip() for frag in fragments if frag.strip()]

    stopwords = {"all", "some", "any"}


    with SessionLocal() as session:
        authors = session.query(Article.author).distinct().all()

        for frag in fragments:
            norm_frag = normalize(frag)
            if norm_frag in stopwords:
                continue

            if not filter_author:
                for stored_author in authors:
                    if stored_author and author_matches(stored_author[0], frag):
                        filter_author = frag.title()
                        print(f"[Multi-part fallback] Matched author '{filter_author}'")
                        break
                if filter_author:
                    continue

            if not filter_location:
                location_match = session.query(Article).filter(Article.location.ilike(f"%{norm_frag}%")).first()
                if location_match:
                    filter_location = frag.title()
                    print(f"[Multi-part fallback] Found location '{filter_location}'")
                    continue

            if not filter_topic and normalize(frag) != normalize(filter_location):
                filter_topic = frag
                print(f"[Multi-part fallback] Treating as topic '{filter_topic}'")


    print(f"[Parsed Query] Raw: '{raw_query}' Author: '{filter_author}', Location: '{filter_location}', Topic: '{filter_topic}', Year: '{filter_year}'")
    return filter_author, filter_topic, filter_year, filter_location
