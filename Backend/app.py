import json
import faiss as faiss_cpu
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal
from models import Article
from sentence_transformers import SentenceTransformer
from faiss_helper import rebuild_faiss_index
import requests
import os
import io
import sys
import traceback
import gzip

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Load embedding model once
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # ✅ Now generates 768D embeddings

# Load or rebuild FAISS index when the app starts
index, ids = rebuild_faiss_index()
if index is None:
    print("⚠️ FAISS index is empty! No embeddings found in the database.")

# Generate embedding
@app.route("/generate-embedding", methods=["POST"])
def generate_embedding():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400
    return jsonify({"embedding": model.encode(text).tolist()})


# AI search and article retrieval
@app.route("/ai-search", methods=["POST"])
def ai_search():
    try:
        data = request.get_json()
        print("🔍 Received JSON:", data)

        if "embedding" not in data:
            print("❌ Error: Missing 'embedding' key")
            return jsonify({"error": "Missing 'embedding' key"}), 400

        query_embedding = np.array(data["embedding"], dtype='float32').reshape(1, -1)
        print("✅ Embedding Shape:", query_embedding.shape)

        if query_embedding.shape[1] != 384:
            print(f"❌ Error: Invalid embedding dimension {query_embedding.shape[1]}")
            return jsonify({"error": f"Invalid embedding dimension: {query_embedding.shape[1]}"}), 400

        k = data.get("k", 5)
        if index is None:
            return jsonify({"error": "No articles found in FAISS index"}), 404

        distances, indices = index.search(query_embedding, k)
        print(f"📌 FAISS Search Indices: {indices}")
        print(f"🔢 Corresponding Article IDs: {[ids[idx] for idx in indices[0] if idx < len(ids)]}")

        with SessionLocal() as session:
            results = []
            for i, idx in enumerate(indices[0]):
                if idx < len(ids):
                    article = session.query(Article).filter_by(id=ids[idx]).first()
                    if article is None:
                        print(f"⚠️ No article found for FAISS ID: {ids[idx]}")
                        continue

                    results.append({
                        "id": article.id,
                        "title": article.title,
                        "abstract": article.abstract,
                        "author": article.author,
                        "publication_date": article.publication_date,
                        "pdf_url": article.pdf_url,
                        "keywords": article.keywords,
                        "isbn": article.isbn,
                        "distance": float(distances[0][i])  # ✅ Use `i` instead of `idx`
                    })

        if not results:
            print("⚠️ No valid articles found in database!")
            return jsonify({"error": "No articles found for search results"}), 404

        return jsonify(results)

    except Exception as e:
        print("❌ Exception in ai_search:", str(e))
        import traceback
        traceback.print_exc()  # Logs full error traceback
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route("/article-text/<int:article_id>", methods=["GET"])
def get_article_text(article_id):
    try:
        with SessionLocal() as session:
            article = session.query(Article).filter_by(id=article_id).first()
            if article is None:
                return jsonify({"error": "Article not found"}), 404
            if not article.pdf_texts:
                return jsonify({"error": "No PDF text available"}), 404

            # Decompress the stored gzip binary data
            import gzip
            decompressed_text = gzip.decompress(article.pdf_texts).decode("utf-8")
            return jsonify({"text": decompressed_text})
    except Exception as e:
        print("Error retrieving article text:", e)
        return jsonify({"error": "Internal server error"}), 500
    
@app.route("/article-summary/<int:article_id>", methods=["GET"])
def get_article_summary(article_id):
    try:
        with SessionLocal() as session:
            article = session.query(Article).filter_by(id=article_id).first()
            if article is None:
                return jsonify({"error": "Article not found"}), 404
            if not article.pdf_texts:
                return jsonify({"error": "No PDF text available"}), 404

            # Decompress the stored gzip binary data
            full_text = gzip.decompress(article.pdf_texts).decode("utf-8")

            # Create a prompt for summarization
            prompt = f"Summarize the following text:\n\n{full_text}"

            # Call Ollama's summarization API (adjust URL/model as needed)
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={"model": "mistral", "prompt": prompt},
                stream=True,
            )
            summary = ""
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        response_data = json.loads(line.decode("utf-8"))
                        summary += response_data.get("response", "")
                        if response_data.get("done", False):
                            break
            else:
                summary = "Failed to generate summary."

            return jsonify({"summary": summary})
    except Exception as e:
        print("Error generating article summary:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
    
# Chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])
    context = data.get("context", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    prompt = f"Context: {context}\n\n" if context else ""
    for entry in conversation_history:
        prompt += f"{entry['role']}: {entry['content']}\n"

    prompt += f"user: {user_message}\nassistant:"

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "mistral", "prompt": prompt},
            stream=True,
        )

        ai_response = ""
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    response_data = json.loads(line.decode("utf-8"))
                    ai_response += response_data.get("response", "")
                    if response_data.get("done", False):
                        break
        else:
            ai_response = "Failed to generate response."

        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response, "history": conversation_history})

    except Exception as e:
        print("❌ Error in /chat:", str(e))
        traceback.print_exc()  # Logs full error details
        return jsonify({"error": "Failed to process chat request"}), 500


# Run Flask
if __name__ == "__main__":
    print("🚀 Running Flask server on port 5001...")
    print(app.url_map)
    app.run(debug=True, host="0.0.0.0", port=5001)
