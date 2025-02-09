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
logging.basicConfig(filename='error_log.log', level=logging.ERROR)

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
    query = re.sub(r'[^\w\s]', '', query)  # Remove non-alphanumeric characters

    session = SessionLocal()
    try:
        # Fetch articles matching the query
        results = session.query(Article).filter(Article.title.ilike(f"%{query}%")).all()
        if not results:
            return jsonify({"error": "No articles found"}), 404

        # Select the first article
        selected_article = results[0]
        article_text = selected_article.abstract
        pdf_url = selected_article.pdf_url  # Correct field name

        print(f"✅ Selected article text: {article_text}")  # Debugging

        # Send the article text to Ollama for AI generation (streaming response)
        ollama_response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "mistral", "prompt": f"Summarize this article: {article_text}"},
            stream=True  # Enable streaming
        )

        # Log the response status code, headers, and raw content for better insight
        print(f"✅ Ollama Response Status Code: {ollama_response.status_code}")
        print(f"✅ Ollama Response Headers: {ollama_response.headers}")
        
        ai_summary = ""
        if ollama_response.status_code == 200:
            # Iterate over each chunk of the response
            for line in ollama_response.iter_lines():
                if line:
                    # Decode the chunk and parse it using the json module
                    try:
                        chunk_data = line.decode('utf-8')
                        print(f"✅ Chunk Data: {chunk_data}")
                        
                        # Parse the chunk (it's a JSON object, so we need to load it)
                        response_data = json.loads(chunk_data)
                        
                        # Append the response part to the summary
                        ai_summary += response_data.get("response", "")
                        
                        # If the response is complete, break the loop
                        if response_data.get("done", False):
                            break

                    except Exception as e:
                        print(f"⚠️ Error processing chunk: {e}")
                        ai_summary = "⚠️ Failed to parse Ollama response."
                        break

        else:
            ai_summary = "⚠️ Failed to generate AI summary due to an error with Ollama."

        # ✅ Return the final response
        return jsonify({
            "article": {
                "title": selected_article.title,
                "abstract": selected_article.abstract,
                "author": selected_article.author,
                "publication_date": selected_article.publication_date,
                "pdf_url": pdf_url  # Add the pdf_url field to the response
            },
            "ai_summary": ai_summary
        })
    except Exception as e:
        # Log unexpected errors
        app.logger.error(f"Unexpected error: {str(e)}")  # Log the error
        print(f"❌ Error: {e}")  # Debugging
        return jsonify({"error": "❌ Failed to generate AI summary"}), 500
    finally:
        session.close()

# ✅ Run Flask on port 5001
if __name__ == "__main__":
    print("🚀 Running Flask server on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)
