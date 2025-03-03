from flask import Blueprint, request, jsonify, current_app
import numpy as np
from database import SessionLocal
from models import Article, Conference  # Ensure Conference model is imported
import gzip
import re
import string

ai_search_bp = Blueprint('ai_search', __name__)

def normalize(text):
    """Lowercase text, remove punctuation and extra whitespace."""
    if not text:
        return ""
    translator = str.maketrans("", "", string.punctuation)
    return text.lower().translate(translator).strip()

@ai_search_bp.route("/ai-search", methods=["POST"])
def ai_search():
    """
    Perform semantic search using FAISS and then apply detailed filters:
      - Author (article.author)
      - Location (only the dedicated location field, normalized)
      - University (searches the first part of the PDF text)
      - Conference name (from the Conference table)
    
    Additionally, for conference versions, return only the version(s) matching the article’s publication year.
    
    If a location filter is provided (or extracted from the query) but no matching candidates are found via the FAISS search,
    a fallback query is executed.
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
        filter_author = data.get("author", "").lower()
        filter_location = data.get("location", "").lower()  # e.g. "luxembourg"
        if not filter_location:
            raw_query = data.get("query", "").lower()
            m = re.search(r'from\s+([a-z\s,]+)', raw_query)
            if m:
                filter_location = m.group(1).strip()
        filter_university = data.get("university", "").lower()
        filter_conf_name = data.get("conference_name", "").lower()

        filtered_results = []
        seen_ids = set()

        while k <= max_k and not filtered_results:
            distances, indices = index.search(query_embedding, k)
            with SessionLocal() as session:
                for i, idx in enumerate(indices[0]):
                    if idx in seen_ids or idx >= len(ids):
                        continue
                    seen_ids.add(idx)
                    article = session.query(Article).filter_by(id=ids[idx]).first()
                    if not article:
                        continue

                    # Retrieve conference details if available.
                    conference = None
                    if article.conference_id:
                        conference = session.query(Conference).filter_by(id=article.conference_id).first()

                    match = True

                    # Filter by author.
                    if filter_author:
                        if not article.author or filter_author not in article.author.lower():
                            match = False

                    # Filter by location: use only the dedicated location field.
                    if filter_location:
                        normalized_filter = normalize(filter_location)
                        normalized_article_location = normalize(article.location)
                        if not normalized_article_location or normalized_filter not in normalized_article_location:
                            match = False

                    # Filter by university: check only the beginning of the article's PDF text.
                    if filter_university:
                        normalized_university_filter = normalize(filter_university)
                        raw_text = ""
                        if article.pdf_texts:
                            try:
                                raw_text = gzip.decompress(article.pdf_texts).decode("utf-8")
                            except Exception:
                                raw_text = ""
                        initial_text = normalize(raw_text[:1000])  # first 1000 characters
                        if normalized_university_filter not in initial_text:
                            match = False

                    # Filter by conference name.
                    if filter_conf_name:
                        if not conference or not conference.name or filter_conf_name not in conference.name.lower():
                            match = False

                    if not match:
                        continue

                    # Determine conference versions matching publication year.
                    conference_versions = None
                    if conference and conference.articles:
                        pub_year = None
                        if article.publication_date:
                            pub_year = article.publication_date[:4]
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
            if not filtered_results:
                k += 50

        # Fallback query if still no results and a location filter was provided.
        if not filtered_results and filter_location:
            with SessionLocal() as session:
                fallback_articles = session.query(Article).filter(
                    Article.location.ilike(f"%{filter_location}%")
                ).all()
                for article in fallback_articles:
                    if article.id in seen_ids:
                        continue
                    seen_ids.add(article.id)
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
            return jsonify({"error": "No articles found for search results"}), 404

        return jsonify(filtered_results)

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
