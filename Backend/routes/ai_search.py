from flask import Blueprint, request, jsonify, current_app
import numpy as np
from database import SessionLocal
from models import Article, Conference  # Ensure Conference model is imported
import gzip
import re
import string
import ast  # For safely parsing the author string into a list

ai_search_bp = Blueprint('ai_search', __name__)

def normalize(text):
    """Lowercase text, remove punctuation and extra whitespace."""
    if not text:
        return ""
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

    filter_words = filter_author.split()
    for author in authors_list:
        if not author:
            continue
        author_clean = author.lower().strip()
        if ',' in author_clean:
            parts = [p.strip() for p in author_clean.split(',')]
            reversed_author = " ".join(parts[::-1])
        else:
            reversed_author = author_clean

        if (all(word in author_clean for word in filter_words) or 
            all(word in reversed_author for word in filter_words)):
            return True
    return False

@ai_search_bp.route("/ai-search", methods=["POST"])
def ai_search():
    """
    Perform semantic search using FAISS and then apply detailed filters:
      - Author (article.author)
      - Location (dedicated location field, normalized)
      - Conference name (from the Conference table)

    The FAISS search runs first. Then, if an author or location filter is provided,
    a fallback query is run to supplement the results (to catch articles that might not be in
    the FAISS candidate set).

    To filter by author, supply the "author" field in the payload or include the keyword "by" in your query
    (e.g., "Give me articles by Lasse Berntzen"). The keyword "from" is reserved for location filtering.
    """
    try:
        data = request.get_json()
        if "embedding" not in data:
            return jsonify({"error": "Missing 'embedding' key"}), 400

        query_embedding = np.array(data["embedding"], dtype='float32').reshape(1, -1)
        if query_embedding.shape[1] != 384:
            return jsonify({"error": f"Invalid embedding dimension: {query_embedding.shape[1]}"}), 400

        initial_k = 50
        max_k = 200
        k = initial_k

        index = current_app.config['INDEX']
        ids = current_app.config['IDS']
        if index is None:
            return jsonify({"error": "No articles found in FAISS index"}), 404

        # Extract filters from payload.
        filter_author = data.get("author", "").lower().strip()
        filter_location = data.get("location", "").lower().strip()
        filter_conf_name = data.get("conference_name", "").lower().strip()

        # Extract additional filters from the raw query string.
        raw_query = data.get("query", "").lower().strip()
        if not filter_author and raw_query:
            m_author = re.search(r'by\s+([a-z\s,]+)', raw_query)
            if m_author:
                filter_author = m_author.group(1).strip()
            elif len(raw_query.split()) == 2:
                filter_author = raw_query

        if not filter_location and raw_query:
            m_location = re.search(r'from\s+([a-z\s,]+)', raw_query)
            if m_location:
                candidate = m_location.group(1).strip()
                if len(candidate.split()) > 2 or candidate.split()[0] in {"new", "san", "los", "las"}:
                    filter_location = candidate

        current_app.logger.info("Filters extracted - author: '%s', location: '%s', conference: '%s'",
                                  filter_author, filter_location, filter_conf_name)

        filtered_results = []
        seen_ids = set()

        # --- Main FAISS-based search loop ---
        while k <= max_k:
            distances, indices = index.search(query_embedding, k)
            current_app.logger.info("FAISS search with k=%d returned %d candidate(s)", k, len(indices[0]))
            with SessionLocal() as session:
                for i, idx in enumerate(indices[0]):
                    if idx in seen_ids or idx >= len(ids):
                        continue
                    seen_ids.add(idx)
                    article = session.query(Article).filter_by(id=ids[idx]).first()
                    if not article:
                        continue

                    conference = None
                    if article.conference_id:
                        conference = session.query(Conference).filter_by(id=article.conference_id).first()

                    match = True

                    if filter_author:
                        if not author_matches(article.author, filter_author):
                            match = False

                    if filter_location:
                        normalized_filter = normalize(filter_location)
                        normalized_article_location = normalize(article.location)
                        if not normalized_article_location or normalized_filter not in normalized_article_location:
                            match = False

                    if filter_conf_name:
                        if not conference or not conference.name or filter_conf_name not in conference.name.lower():
                            match = False

                    if not match:
                        continue

                    conference_versions = None
                    if conference and conference.articles:
                        pub_year = article.publication_date[:4] if article.publication_date else None
                        if pub_year:
                            matching_versions = [v for v in conference.articles if pub_year in v]
                            conference_versions = matching_versions if matching_versions else conference.articles
                        else:
                            conference_versions = conference.articles

                    result_item = {
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": article.author,
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": float(distances[0][i]),
                        "conference_location": article.location
                    }
                    if conference:
                        result_item["conference_name"] = conference.name
                        result_item["conference_articles"] = conference_versions

                    filtered_results.append(result_item)
            k += 50

        # --- Supplement with fallback query results ---
        if filter_location or filter_author:
            current_app.logger.info("Running fallback query to supplement FAISS results.")
            with SessionLocal() as session:
                fallback_query = session.query(Article)
                if filter_location:
                    fallback_query = fallback_query.filter(Article.location.ilike(f"%{filter_location}%"))
                fallback_articles = fallback_query.all()
                current_app.logger.info("Fallback query returned %d article(s).", len(fallback_articles))
                for article in fallback_articles:
                    # Apply author filter if provided.
                    if filter_author and not author_matches(article.author, filter_author):
                        continue

                    # Check conference name filter.
                    match = True
                    if filter_conf_name:
                        conference = None
                        if article.conference_id:
                            conference = session.query(Conference).filter_by(id=article.conference_id).first()
                        if not conference or not conference.name or filter_conf_name not in conference.name.lower():
                            match = False
                    if not match:
                        continue

                    if article.id in seen_ids:
                        continue  # Skip articles already added.

                    conference = None
                    if article.conference_id:
                        conference = session.query(Conference).filter_by(id=article.conference_id).first()
                    conference_versions = None
                    if conference and conference.articles:
                        pub_year = article.publication_date[:4] if article.publication_date else None
                        if pub_year:
                            matching_versions = [v for v in conference.articles if pub_year in v]
                            conference_versions = matching_versions if matching_versions else conference.articles
                        else:
                            conference_versions = conference.articles

                    result_item = {
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": article.author,
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": None,
                        "conference_location": article.location
                    }
                    if conference:
                        result_item["conference_name"] = conference.name
                        result_item["conference_articles"] = conference_versions

                    filtered_results.append(result_item)

        if not filtered_results:
            current_app.logger.info("No articles found after fallback query.")
            return jsonify({"error": "No articles found for search results"}), 404

        return jsonify(filtered_results)

    except Exception as e:
        current_app.logger.exception("Search error:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
