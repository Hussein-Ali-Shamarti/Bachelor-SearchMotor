from flask import Blueprint, request, jsonify, current_app

generate_embedding_bp = Blueprint('generate_embedding', __name__)

@generate_embedding_bp.route("/generate-embedding", methods=["POST"])
def generate_embedding():
    """
    Generate a text embedding using the SentenceTransformer model.
    """
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
    try:
        model = current_app.config['MODEL']
        embedding = model.encode(text).tolist()
        return jsonify({"embedding": embedding})
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return jsonify({"error": "Failed to generate embedding", "details": str(e)}), 500
