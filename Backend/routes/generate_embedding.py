from flask import Blueprint, request, jsonify, current_app

generate_embedding_bp = Blueprint('generate_embedding', __name__)

@generate_embedding_bp.route("/generate-embedding", methods=["POST"])
def generate_embedding():
    """
    Generate a text embedding using the SentenceTransformer model.
    """
    data = request.get_json()
    text = data.get("text", "").strip()
    author = data.get("author", "").strip()
    year = data.get("year", "").strip()
    location = data.get("location", "").strip()
    conference_name = data.get("conference_name", "").strip()

    # Build full enriched text
    enriched_parts = []
    if text:
        enriched_parts.append(f"Articles about {text}")
    if author:
        enriched_parts.append(f"written by {author}")
    if year:
        enriched_parts.append(f"published in {year}")
    if location:
        enriched_parts.append(f"presented in {location}")
    if conference_name:
        enriched_parts.append(f"at {conference_name}")

    full_text = " ".join(enriched_parts).strip()

    if not full_text:
        return jsonify({"error": "Text cannot be empty"}), 400

    try:
        model = current_app.config['MODEL']
        embedding = model.encode(full_text).tolist()
        return jsonify({"embedding": embedding})
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return jsonify({"error": "Failed to generate embedding", "details": str(e)}), 500

