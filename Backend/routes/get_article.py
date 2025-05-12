from flask import Blueprint, request, jsonify
from database import SessionLocal
from models import Article
import gzip
import asyncio
from utils.summarization import summarize_full_text

article_bp = Blueprint('article', __name__)

@article_bp.route("/article-text/<int:article_id>", methods=["GET"])
def get_article_text(article_id):
    """
    Retrieve the full text of an article by its ID.
    """
    try:
        with SessionLocal() as session:
            article = session.query(Article).filter_by(id=article_id).first()
            if article is None:
                return jsonify({"error": f"Article with ID {article_id} not found"}), 404
            if not article.pdf_texts:
                return jsonify({"error": f"No PDF text available for article {article_id}"}), 404

            decompressed_text = gzip.decompress(article.pdf_texts).decode("utf-8")
            return jsonify({"text": decompressed_text})
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@article_bp.route("/article-summary/<int:article_id>", methods=["GET"])
def get_article_summary(article_id):
    """
    Generate and return a summary of an article's text.
    """
    try:
        generate_summary = request.args.get("generate", "").lower() == "true"

        with SessionLocal() as session:
            article = session.query(Article).filter_by(id=article_id).first()
            if article is None:
                return jsonify({"error": "Article not found"}), 404
            if not article.pdf_texts:
                return jsonify({"error": "No PDF text available"}), 404

            abstract = article.abstract
            if not abstract:
                return jsonify({"error": "No abstract available"}), 404

            abstract_length = len(abstract.split())
            full_text = gzip.decompress(article.pdf_texts).decode("utf-8")
            if not full_text.strip():
                return jsonify({"error": "Article text is empty"}), 400

            summary = ""
            if generate_summary:
                summary = asyncio.run(summarize_full_text(full_text))
                if not summary or summary.strip() == "":
                    return jsonify({"error": "Failed to generate summary"}), 500

            return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
