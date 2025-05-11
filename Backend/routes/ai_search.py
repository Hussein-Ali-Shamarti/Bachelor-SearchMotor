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

def extract_filters_from_query(raw_query):
    filter_author = ""
    filter_topic = ""
    filter_year = ""
    filter_location = ""

    m_year = re.search(r'\b(19|20)\d{2}\b', raw_query)
    if m_year:
        filter_year = m_year.group(0)
        raw_query = raw_query.replace(m_year.group(0), '').strip()

    m_author = re.search(r'\b(by|av)\s+([a-z\u00e6\u00f8\u00e5\u00c6\u00d8\u00c5\s,]+?)(\s+(from|fra)|(19|20)\d{2}|$)', raw_query)
    if m_author:
        filter_author = m_author.group(2).strip()
        raw_query = raw_query.replace(m_author.group(0), '').strip()

    m_location = re.search(r'\b(from|fra)\s+([a-z\u00e6\u00f8\u00e5\u00c6\u00d8\u00c5\s,]+?)(\s+(19|20)\d{2}|$)', raw_query)
    if m_location:
        filter_location = m_location.group(2).strip()
        raw_query = raw_query.replace(m_location.group(0), '').strip()

    filter_topic = raw_query.strip()

    filler_patterns = [
        r'\barticles?\b', r'\bpapers?\b', r'\bstudies?\b', r'\babout\b',
        r'\bon\b', r'\bthe\b', r'\bpaper\b', r'\bwritten\b',
        r'\bav\b', r'\bfra\b', r'\bom\b', r'\bartikler?\b', r'\bskrevet\b'
    ]
    filter_topic = re.sub("|".join(filler_patterns), "", filter_topic)
    filter_topic = re.sub(r'\s+', ' ', filter_topic).strip()

    if not filter_author:
        name_match = re.match(r'^([a-zæøåæøå]+(?:\s+[a-zæøåæøå]+){1,3})$', raw_query.strip(), re.UNICODE | re.IGNORECASE)
        if name_match:
            filter_author = name_match.group(1)
            filter_topic = ""

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

        filter_author = data.get("author", "").lower().strip()
        filter_topic = data.get("topic", "").lower().strip()
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
            if filter_year and filter_topic and not filter_author:
                if len(filter_topic.split()) >= 2:
                    filter_author = filter_topic
                    filter_topic = ""

        is_db_only_query = bool(filter_author) and not filter_topic

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
                        norm_title = normalize(article.title)
                        norm_keywords = normalize(article.keywords)
                        norm_abstract = normalize(article.abstract)
                        topic_words = filter_topic.split()
                        match_count = sum(1 for word in topic_words if word in norm_title or word in norm_keywords)
                        if match_count >= 1:
                            topic_match = True
                            boost *= 1 + (0.5 * match_count)
                        if any(word in norm_abstract for word in topic_words):
                            topic_match = True
                            boost *= 1.1

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
