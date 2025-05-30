# Denne filen håndterer semantisk søk i FAISS-indeksen.
# Den bruker embedding og eventuelle metadatafiltre (som forfatter, emne, år og sted) 
# til å hente og booste relevante artikler basert på semantisk likhet og filtreringskriterier.


from flask import jsonify, current_app
from database import SessionLocal
from models import Article, Conference
from utils.query_utils import normalize, author_matches, clean_author_field, normalize_keywords

def get_faiss_results(query_embedding, filter_author, filter_topics, filter_year, filter_location):
    index = current_app.config['INDEX']
    ids = current_app.config['IDS']
    if index is None:
        return jsonify({"error": "No articles found in FAISS index"}), 404

    enriched_results = []
    seen_ids = set()
    pure_semantic_query = not (filter_author or filter_topics or filter_year)

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

                author_match = author_matches(article.author, filter_author) if filter_author else False
                topic_match = False
                boost = 1.0

                if filter_topics:
                    for topic in filter_topics:
                        topic_phrase = normalize(topic)
                        norm_title = normalize(article.title)
                        norm_keywords = normalize(" ".join(article.keywords) if isinstance(article.keywords, list) else article.keywords)
                        norm_abstract = normalize(article.abstract)

                        if topic_phrase in norm_title or topic_phrase in norm_keywords or topic_phrase in norm_abstract:
                            topic_match = True
                            boost = max(boost, 2.0)
                        else:
                            topic_words = topic_phrase.split()
                            match_count = sum(1 for word in topic_words if word in norm_title or word in norm_keywords)
                            if match_count >= 1:
                                topic_match = True
                                boost = max(boost, 1 + 0.3 * match_count)
                            if any(word in norm_abstract for word in topic_words):
                                topic_match = True
                                boost *= 1.1
                if filter_author and not author_match:
                    continue
                if filter_topics and not topic_match:
                    continue
                if filter_location:
                    norm_article_loc = normalize(article.location or "")
                    norm_filter_loc = normalize(filter_location)
                    if norm_filter_loc not in norm_article_loc:
                        continue
                if filter_year:
                    if not article.publication_date or not article.publication_date.startswith(str(filter_year)):
                        continue


                if author_match and topic_match:
                    boost *= 5.0
                elif author_match:
                    boost *= 3.0
                elif topic_match:
                    boost *= 2.0

                adjusted_distance = float(distances[0][i]) if pure_semantic_query else float(distances[0][i]) / boost
                conference = session.query(Conference).filter_by(id=article.conference_id).first()
                conference_name = conference.name if conference else None
                enriched_results.append({
                    "id": article.id,
                    "title": article.title,
                    "abstract": article.abstract,
                    "author": clean_author_field(article.author),
                    "publication_date": article.publication_date,
                    "pdf_url": article.pdf_url,
                    "keywords": normalize_keywords(article.keywords),
                    "isbn": article.isbn,
                    "distance": adjusted_distance,
                    "conference_location": article.location,
                    "conference_name": conference_name
                })
        k += 50

    if not enriched_results:
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
                    "keywords": normalize_keywords(article.keywords),
                    "isbn": article.isbn,
                    "distance": float(distances[0][i]),
                    "conference_location": article.location,
                })
        if fallback_results:
            return jsonify(fallback_results)
        else:
            error_msg = "No articles found matching your query"
            if filter_location:
                error_msg += f" (location: '{filter_location}')"
            if filter_year:
                error_msg += f" (year: {filter_year})"
            if filter_author:
                error_msg += f" (author: '{filter_author}')"
            if filter_topics:
                error_msg += f" (topic: '{filter_topics}')"

            return jsonify({"error": error_msg}), 404

    enriched_results.sort(key=lambda x: x["distance"])
    return jsonify(enriched_results)