from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal
from models import Article
import requests

# Initialize Flask app
print("Flask app is starting...")
app = Flask(__name__)
CORS(app)  # ✅ Allow all origins to access the API

print("Flask module imported successfully!")
print("App initialized!")

@app.route("/ai-search", methods=["GET"])
def ai_search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "Please provide a search query"}), 400

    session = SessionLocal()
    try:
        # Fetch articles matching the query
        results = session.query(Article).filter(Article.title.ilike(f"%{query}%")).all()
        if not results:
            return jsonify({"error": "No articles found"}), 404

        # Select the first article
        selected_article = results[0]
        article_text = selected_article.abstract
        print(f"✅ Selected article text: {article_text}")  # Debugging

        # Send the article text to Ollama for AI generation
        ollama_response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "mistral", "prompt": f"Summarize this article: {article_text}"},
        )

        # ✅ NEW: Print Raw Ollama Response for Debugging
        print(f"✅ Ollama Raw Response: {ollama_response.text}")

        # ✅ Handle Ollama's Response Format
        try:
            ollama_result = ollama_response.json()  # Try to parse JSON
            ai_summary = ollama_result.get("response", "No summary generated.")
        except ValueError as e:
            print(f"⚠️ Error parsing Ollama response: {e}")
            print(f"⚠️ Raw Response: {ollama_response.text}")  # Debugging
            ai_summary = "⚠️ Failed to generate AI summary due to unexpected response format."

        # ✅ Return the final response
        return jsonify({
            "article": {
                "title": selected_article.title,
                "abstract": selected_article.abstract,
                "author": selected_article.author,
                "publication_date": selected_article.publication_date
            },
            "ai_summary": ai_summary
        })
    except Exception as e:
        print(f"❌ Error: {e}")  # Debugging
        return jsonify({"error": "❌ Failed to generate AI summary"}), 500
    finally:
        session.close()

# ✅ Run Flask on port 5001
if __name__ == "__main__":
    print("🚀 Running Flask server on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)
