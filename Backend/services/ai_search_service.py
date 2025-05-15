from flask import jsonify, current_app
import numpy as np
from database import SessionLocal
from models import Article
from utils.query_utils import extract_filters_from_query, author_matches, clean_author_field, normalize
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
    filter_topic = ""
    filter_year = ""
    filter_location = ""

    if raw_query:
        ex_author, ex_topic, ex_year, ex_location = extract_filters_from_query(raw_query)
        filter_author = ex_author or filter_author_input
        filter_topic = ex_topic or filter_topic_input
        filter_year = filter_year_input or ex_year
        filter_location = ex_location or filter_location_input
    else:
        filter_author = filter_author_input
        filter_topic = filter_topic_input
        filter_year = filter_year_input
        filter_location = filter_location_input

    is_author_topic_same = (
        filter_author and filter_topic and 
        normalize(filter_author) == normalize(filter_topic)
    )


    is_db_only_query = (
        (filter_author or filter_year or filter_location)
        and (not filter_topic or is_author_topic_same)
    )

    if is_db_only_query:
        return handle_db_query(filter_author, filter_year, filter_location, raw_query)

    return get_faiss_results(query_embedding, filter_author, filter_topic, filter_year, filter_location,)

def handle_db_query(filter_author, filter_year, filter_location, raw_query):
    results = []
    with SessionLocal() as session:
        query = session.query(Article)
        
        if filter_year:
            query = query.filter(Article.publication_date.like(f"{filter_year}%"))

        if filter_author:
            norm_author = normalize(filter_author)
            parts = norm_author.split(",") if "," in norm_author else norm_author.split()
            last_name = parts[0] if "," in norm_author else parts[-1]
            query = query.filter(Article.author.ilike(f"%{last_name}%"))

        if filter_location:
            query = query.filter(Article.location.ilike(f"%{filter_location}%"))

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
        error_msg = f"No articles found for search: {raw_query}"
    
    return jsonify({"error": error_msg}), 404

