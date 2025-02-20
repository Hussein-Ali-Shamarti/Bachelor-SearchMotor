import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import SessionLocal
from models import Article
import requests
import re
import logging

# Initialize Flask app
print("Flask app is starting...")
app = Flask(__name__)
CORS(app)  # ✅ Allow all origins to access the API

# Set up logging
logging.basicConfig(filename="error_log.log", level=logging.ERROR)

print("Flask module imported successfully!")
print("App initialized!")

@app.route("/ai-search", methods=["GET"])
def ai_search():
    query = request.args.get("query", "").strip()

    # Validate that query is not empty
    if not query:
        error_message = "Please provide a search query"
        app.logger.error(f"Validation error: {error_message}")  # Log the error
        return jsonify({"error": error_message}), 400

    # Sanitize the query by removing non-alphanumeric characters
    query = re.sub(r"[^\w\s]", "", query)

    try:
        # Use a context manager to handle the session properly
        with SessionLocal() as session:
            # Fetch articles matching the query
            results = session.query(
                Article.title,
                Article.abstract,
                Article.author,
                Article.publication_date,
                Article.pdf_url,
                Article.pdf_texts
            ).filter(Article.title.ilike(f"%{query}%")).all()

            if not results:
                return jsonify({"error": "No articles found"}), 404

            # Select the first article
            selected_article = results[0]
            title, abstract, author, publication_date, pdf_url, article_text = selected_article

            print(f"✅ Selected article: {title}")
            print(f"✅ PDF URL: {pdf_url}")

        # Send the article text to Ollama for AI processing
        ollama_response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": (
                    f"Summarize the following article in a structured format:\n"
                    f"1. Objective: What is the main goal?\n"
                    f"2. Key Findings: What are the main insights?\n"
                    f"3. Conclusion: What are the takeaways?\n\n"
                    f"Article Text: {article_text}"
                ),
            },
            stream=True,
        )

        ai_summary = ""
        if ollama_response.status_code == 200:
            for line in ollama_response.iter_lines():
                if line:
                    try:
                        chunk_data = line.decode("utf-8")
                        response_data = json.loads(chunk_data)
                        ai_summary += response_data.get("response", "").replace("\n", "<br>")
                        if response_data.get("done", False):
                            break
                    except Exception:
                        ai_summary = "⚠️ Failed to parse AI response."
                        break
        else:
            ai_summary = "⚠️ AI summary generation failed."

        return jsonify({
            "article": {
                "title": title,
                "abstract": abstract,
                "author": author,
                "publication_date": publication_date,
                "pdf_url": pdf_url,
            },
            "ai_summary": ai_summary,
            "context": article_text,
        })

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "❌ Failed to process request"}), 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])
    context = data.get("context", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Build the prompt
    prompt = f"Context: {context}\n\n" if context else ""
    for entry in conversation_history:
        prompt += f"{entry['role']}: {entry['content']}\n"

    prompt += f"user: {user_message}\nassistant:"
    prompt += "\nImportant: Please only refer to the provided article text."

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
                    chunk_data = line.decode("utf-8")
                    response_data = json.loads(chunk_data)
                    ai_response += response_data.get("response", "")
                    if response_data.get("done", False):
                        break
        else:
            ai_response = "⚠️ Failed to generate response from AI."

        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        return jsonify({"response": ai_response, "history": conversation_history})

    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({"error": "❌ Failed to process chat request"}), 500

# ✅ Run Flask on port 5001
if __name__ == "__main__":
    print("🚀 Running Flask server on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)
