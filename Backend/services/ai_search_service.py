from flask import jsonify, current_app
import numpy as np
from database import SessionLocal
from models import Article, Conference
from utils.query_utils import extract_filters_from_query, author_matches, clean_author_field, normalize, normalize_keywords
from utils.semantic_utils import get_faiss_results


def handle_ai_search(request):
    data = request.get_json()

    if "embedding" not in data:
        return jsonify({"error": "Missing 'embedding' key"}), 400

    query_embedding = np.array(data["embedding"], dtype='float32').reshape(1, -1)
    if query_embedding.shape[1] != 384:
        return jsonify({"error": f"Invalid embedding dimension: {query_embedding.shape[1]}"}), 400

    raw_query = data.get("query", "").strip()
    filter_author_input = data.get("author", "").strip()
    filter_topic_input = data.get("topic", "").strip()
    filter_year_input = data.get("year", "").strip()
    filter_location_input = data.get("location", "").strip()

    filter_author = ""
    filter_topics = []
    filter_year = ""
    filter_location = ""

    if raw_query:
        ex_author, ex_topics, ex_year, ex_location = extract_filters_from_query(raw_query)
        filter_author = ex_author or filter_author_input
        filter_topics = ex_topics if ex_topics else normalize_keywords(filter_topic_input)
        filter_year = filter_year_input or ex_year
        filter_location = ex_location or filter_location_input
    else:
        filter_author = filter_author_input
        filter_topics = normalize_keywords(filter_topic_input)
        filter_year = filter_year_input
        filter_location = filter_location_input

    weak_topics = {"studies", "papers", "research"}
    filtered_topics = [t for t in filter_topics if normalize(t) not in weak_topics]
    
    is_author_topic_same = (
        filter_author and filtered_topics and
        normalize(filter_author) in [normalize(t) for t in filtered_topics]
    )
    
    is_db_only_query = (
        (filter_author or filter_year or filter_location)
        and (not filtered_topics or is_author_topic_same)
    )
    

    if is_db_only_query:
        return handle_db_query(filter_author, filter_year, filter_location, raw_query)

    return get_faiss_results(query_embedding, filter_author, filter_topics, filter_year, filter_location)

def handle_db_query(filter_author, filter_year, filter_location, raw_query):
    results = []
    with SessionLocal() as session:
        query = session.query(Article)

        if filter_year:
            query = query.filter(Article.publication_date.like(f"{filter_year}%"))

        if filter_location:
            query = query.filter(Article.location.ilike(f"%{filter_location}%"))

        # Load all relevant articles
        candidate_articles = query.all()

        for article in candidate_articles:
            if filter_author and not author_matches(article.author, filter_author):
                continue  # Skip non-matching authors
            conference = session.query(Conference).filter_by(id=article.conference_id).first()
            conference_name = conference.name if conference else None
       
            results.append({
                "id": article.id,
                "title": article.title,
                "abstract": article.abstract,
                "author": clean_author_field(article.author), 
                "publication_date": article.publication_date,
                "pdf_url": article.pdf_url,
                "keywords": normalize_keywords(article.keywords),
                "isbn": article.isbn,
                "distance": None,
                "conference_location": article.location,
                "conference_name": conference_name
            })

    if not results:
        error_msg = f"No articles found for search: '{raw_query}'"
        return jsonify({"error": error_msg}), 404

    return jsonify(results)



