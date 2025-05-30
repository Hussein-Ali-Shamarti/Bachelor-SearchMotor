# Denne filen håndterer parsing og tolkning av brukerens spørring.
# Den prøver å lage en strukturert filterliste bestående av forfatter, emne, sted og år
# ved å analysere både eksplisitte og implisitte signaler i spørringsteksten – inkludert norsk og engelsk språkbruk.


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

def is_weak_topic(phrase):
    phrase = normalize(phrase)
    weak_patterns = [
        r'^(find|see|get|show|list|view)\b',
        r'\bstudies\b',
        r'\barticles?\b',
        r'\bpapers?\b',
        r'^find (studies|articles|papers)\b'
    ]
    return any(re.search(pat, phrase) for pat in weak_patterns)


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
    pattern = r'\b(written\s+by|about|by|from|in|on|is|om|av|fra)\b'
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
    filter_topics = []
    filter_year = ""
    filter_location = ""

    raw_query = translate_norwegian(raw_query.strip())
    raw_query_lower = raw_query.lower()
    original_query_clean = re.sub(r"[^\w\s,']", '', raw_query).strip()

    m_year = re.search(r'\b(19|20)\d{2}\b', raw_query_lower)
    if m_year:
        filter_year = m_year.group(0)
        raw_query = raw_query.replace(filter_year, '').strip()

    phrases = split_query_phrases(raw_query)

    for prep, phrase in phrases:
        norm = normalize(phrase)
        if prep in {"about", "om", "on"}:
            filter_topics.extend([
                topic.strip() for topic in re.split(r",| og | and ", phrase, flags=re.IGNORECASE)
                if topic.strip()
            ])
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
                pattern = re.compile(re.escape(author_re.group(0)), re.IGNORECASE)
                raw_query = pattern.sub('', raw_query).strip()

    # Remove filler and search-related tokens *after* primary filter parsing
    raw_query = re.sub(
        r'\b(find|search|fetch|articles?|papers?|studies?|written|by|in|from|about|om|av|fra|all|some|any)\b',
        '',
        raw_query,
        flags=re.IGNORECASE
    )
    raw_query = re.sub(r"\bn\b", "in", raw_query)
    raw_query = re.sub(r'\s+', ' ', raw_query).strip()

    # Clean and split query into fragments
    candidate_text = original_query_clean
    candidate_text = re.sub(r"[^\w\s,']", '', candidate_text)
    candidate_text = re.sub(r'\s+', ' ', candidate_text).strip()
    fragments = re.split(r",|\s+og\s+|\s+and\s+", candidate_text, flags=re.IGNORECASE)
    fragments = [frag.strip() for frag in fragments if frag.strip()]
    stopwords = {"all", "some", "any"}

    with SessionLocal() as session:
        authors = session.query(Article.author).distinct().all()

        if not filter_author:
            full_query = re.sub(r"[^\w\s]", "", raw_query).strip()
            if full_query.lower() not in {"me", "i", "we", "you", "they", "he", "she", "him", "her", "us"}:
                for stored_author in authors:
                    if stored_author and author_matches(stored_author[0], full_query):
                        filter_author = full_query.title()
                        print(f"[Safe full-query fallback] Matched author '{filter_author}'")
                        break

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

            if (
                normalize(frag) != normalize(filter_location)
                and normalize(frag) != normalize(filter_author)
                and not re.fullmatch(r'\d{4}', frag.strip())
                and not (filter_author and normalize(filter_author) in normalize(frag))
                and not (filter_year and filter_year in frag)
            ):
                filter_topics.append(frag)
                print(f"[Multi-part fallback] Adding topic: {frag}")

    # Loose fallback: add leftover cleaned raw_query if nothing was added to topics
    if not filter_topics and raw_query.strip():
        leftover = raw_query
        leftover = re.sub(r"[^\w\s]", "", leftover)
        leftover = re.sub(r'\s+', ' ', leftover).strip()

        if filter_author:
            author_words = normalize(filter_author).split()
            for word in author_words:
                leftover = re.sub(rf'\b{re.escape(word)}\b', '', leftover, flags=re.IGNORECASE)
        if filter_location:
            leftover = re.sub(re.escape(filter_location), '', leftover, flags=re.IGNORECASE)

        leftover = re.sub(r'\s+', ' ', leftover).strip()

        banned_topics = {"me", "i", "we", "you", "they", "he", "she", "him", "her", "us"}
        if leftover.lower() in banned_topics:
            print(f"[Loose fallback] Skipped weak leftover topic: {leftover}")
        elif leftover:
            print(f"[Loose fallback] Adding topic from leftover text: {leftover}")
            filter_topics.append(leftover)


    # Final topic cleanup
    filter_topics = [
        topic for topic in list(dict.fromkeys(filter_topics))
        if not is_weak_topic(topic)
    ]
    print(f"[Parsed Query] Raw: '{raw_query}' Author: '{filter_author}', Location: '{filter_location}', Topics: '{filter_topics}', Year: '{filter_year}'")
    return filter_author, filter_topics, filter_year, filter_location
