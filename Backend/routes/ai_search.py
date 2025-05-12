from flask import Blueprint, request, jsonify, current_app
import numpy as np
from database import SessionLocal
from models import Article
import re
import string
import ast

ai_search_bp = Blueprint('ai_search', __name__)

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
    """
    Returns True if the string looks like a real person name.
    Accepts lowercase and titlecase input.
    """
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

    # Extract year
    m_year = re.search(r'\b(19|20)\d{2}\b', original_query)
    if m_year:
        filter_year = m_year.group(0)
        original_query = original_query.replace(filter_year, '').strip()

    # Extract author (English and Norwegian: by / av)
    m_author = re.search(
        r'\b(by|av)\s+([A-ZÆØÅ][a-zæøå]+(?:\s+[A-ZÆØÅ][a-zæøå]+){0,3})\b',
        original_query,
        re.IGNORECASE
    )
    if m_author:
        filter_author = m_author.group(2).strip()
        original_query = original_query.replace(m_author.group(0), '').strip()

    # Extract location (from / fra)
    m_location = re.search(
        r'\b(from|fra)\s+([a-zA-ZæøåÆØÅ\s,]+?)($|\s+(19|20)\d{2})',
        original_query,
        re.IGNORECASE
    )
    if m_location:
        filter_location = m_location.group(2).strip()
        original_query = original_query.replace(m_location.group(0), '').strip()

    # Clean up potential topic text
    candidate_text = original_query.strip()
    filler_patterns = [
        # English
        r'\barticles?\b', r'\bpapers?\b', r'\bstudies?\b', r'\babout\b',
        r'\bon\b', r'\bthe\b', r'\bpaper\b', r'\bwritten\b', r'\bby\b', r'\bfrom\b',
        # Norwegian
        r'\bartikler?\b', r'\bskrevet\b', r'\bom\b', r'\bav\b', r'\bfra\b'
    ]
    candidate_text = re.sub("|".join(filler_patterns), "", candidate_text, flags=re.IGNORECASE)
    candidate_text = re.sub(r'\s+', ' ', candidate_text).strip()

    # Determine if candidate is name-like (2–3 words, not common topic terms)
    words = candidate_text.split()
    common_topic_words = {"data", "science", "learning", "analyse", "analyse", "modell", "forskning", "helse", "teknologi"}

    if not filter_author and filter_year:
        if 1 < len(words) <= 3:
            non_topic_words = sum(1 for w in words if w.lower() not in common_topic_words)
            if non_topic_words == len(words):
                filter_author = candidate_text.title()
                candidate_text = ""

        # Fallback: treat as author only if it's a likely personal name (no 'of', etc.)
    if not filter_author and not filter_topic:
        if looks_like_person_name(candidate_text):
            filter_author = candidate_text.title()
            candidate_text = ""


    if not filter_topic and candidate_text:
        filter_topic = candidate_text.strip()

    # Final fallback: treat full query as topic if nothing else worked
    if not filter_author and not filter_topic:
        filter_topic = candidate_text if candidate_text else original_query

    print(f"[Parsed Query] Author: '{filter_author}', Topic: '{filter_topic}', Year: '{filter_year}'")
    return filter_author, filter_topic, filter_year, filter_location

@ai_search_bp.route("/ai-search", methods=["POST"])
def ai_search():
    try:
        print("Flask: entered /ai-search route")
        data = request.get_json()
        if "embedding" not in data:
            return jsonify({"error": "Missing 'embedding' key"}), 400

        query_embedding = np.array(data["embedding"], dtype='float32').reshape(1, -1)
        if query_embedding.shape[1] != 384:
            return jsonify({"error": f"Invalid embedding dimension: {query_embedding.shape[1]}"}), 400

        filter_author = data.get("author", None)
        if filter_author:
            filter_author = filter_author.lower().strip()
        else:
            filter_author = ""

        filter_topic = data.get("topic", None)
        if filter_topic:
            filter_topic = filter_topic.lower().strip()
        else:
            filter_topic = ""

        filter_year = data.get("year", "").strip()


        raw_query = data.get("query", "").lower().strip()
        if raw_query:
            ex_author, ex_topic, ex_year, _ = extract_filters_from_query(raw_query)
            if not filter_author:
                filter_author = ex_author
            if not filter_topic:
                filter_topic = ex_topic
            if not filter_year:
                filter_year = ex_year
        print(f"[AI Search Debug] Final Filters -> Author: '{filter_author}', Topic: '{filter_topic}', Year: '{filter_year}'")

        is_db_only_query = (filter_author != "") and (filter_topic == "")

        if is_db_only_query:
            results = []
            with SessionLocal() as session:
                query = session.query(Article)

                if filter_year:
                    query = query.filter(Article.publication_date.like(f"{filter_year}%"))

                if filter_author:
                    parts = filter_author.strip().split()
                    last_name = parts[-1] if len(parts) > 1 else parts[0]
                    query = query.filter(Article.author.ilike(f"%{last_name}%"))

                matching_articles = query.all()

                for article in matching_articles:
                    results.append({
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": clean_author_field(article.author),
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": None,
                        "conference_location": article.location,
                    })
                    

            if not results:
                return jsonify({"error": "No articles found for search results"}), 404

            print(f"DB-only query returned {len(results)} result(s).")
            for res in results:
                print(f"  → ID: {res['id']}, Title: {res['title']}, Author: {res['author']}")

            return jsonify(results)


        index = current_app.config['INDEX']
        ids = current_app.config['IDS']
        if index is None:
            return jsonify({"error": "No articles found in FAISS index"}), 404

        enriched_results = []
        seen_ids = set()
        pure_semantic_query = not (filter_author or filter_topic or filter_year)

        initial_k, max_k, k = 50, 200, 50
        while k <= max_k:
            distances, indices = index.search(query_embedding, k)
            with SessionLocal() as session:
                for i, idx in enumerate(indices[0]):
                    if idx in seen_ids or idx >= len(ids):
                        continue
                    seen_ids.add(idx)
                    article = session.query(Article).filter_by(id=ids[idx]).first()
                    if not article:
                        continue
                    
                    boost = 1.0
                    author_match = False
                    topic_match = False

                    if filter_author and author_matches(article.author, filter_author):
                        author_match = True

                    if filter_topic:
                        topic_phrase = normalize(filter_topic)
                        norm_title = normalize(article.title)
                        # Handle keywords as list or string
                        if isinstance(article.keywords, list):
                            norm_keywords = normalize(" ".join(article.keywords))
                        else:
                            norm_keywords = normalize(article.keywords)
                        norm_abstract = normalize(article.abstract)

                        print(f"Checking article {article.id}:")
                        print(f"  Title: {article.title}")
                        print(f"  Normalized Keywords: {norm_keywords}")
                        print(f"  Topic Phrase: '{topic_phrase}'")

                        if topic_phrase in norm_title or topic_phrase in norm_keywords or topic_phrase in norm_abstract:
                            topic_match = True
                            boost *= 2.0
                            print(f"  ➤ Full phrase match found. Boost now {boost}")
                        else:
                            topic_words = topic_phrase.split()
                            match_count = sum(1 for word in topic_words if word in norm_title or word in norm_keywords)
                            if match_count >= 1:
                                topic_match = True
                                boost *= 1 + (0.3 * match_count)
                                print(f"  ➤ {match_count} topic word(s) in title/keywords. Boost now {boost}")
                            if any(word in norm_abstract for word in topic_words):
                                topic_match = True
                                boost *= 1.1
                                print(f"  ➤ Topic words found in abstract. Boost now {boost}")

                        print(f"  Final topic_match: {topic_match}")

                    # Optional: filter out irrelevant articles
                    if not pure_semantic_query and not topic_match and not author_match:
                        print(f"  Skipped: no topic or author match.")
                        continue
                    
                    if pure_semantic_query:
                        adjusted_distance = float(distances[0][i])
                    else:
                        if filter_author and filter_topic:
                            if author_match and topic_match:
                                boost *= 3.0
                        elif author_match:
                            boost *= 2.0
                        elif topic_match:
                            boost *= 1.5
                        adjusted_distance = float(distances[0][i]) / boost

                    print(f"  Distance: {distances[0][i]:.4f}, Boost: {boost:.2f}, Adjusted: {adjusted_distance:.4f}\n")

                    enriched_results.append({
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": clean_author_field(article.author),
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": adjusted_distance,
                        "conference_location": article.location,
                    })
            k += 50

            

        # Fallback to top unfiltered semantic results if no matches with filters
        if not enriched_results and not is_db_only_query:
            fallback_results = []
            distances, indices = index.search(query_embedding, 10)
            with SessionLocal() as session:
                for i, idx in enumerate(indices[0]):
                    article = session.query(Article).filter_by(id=ids[idx]).first()
                    if not article:
                        continue
                    fallback_results.append({
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": clean_author_field(article.author),
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": float(distances[0][i]),
                        "conference_location": article.location,
                    })
            return jsonify(fallback_results)


        enriched_results.sort(key=lambda x: x["distance"])
        return jsonify(enriched_results)

    except Exception as e:
        current_app.logger.exception("Search error:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
