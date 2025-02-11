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
        article_text = selected_article.pdf_texts # Full text of the article
        article_abstract = selected_article.abstract  # Context of the article
        pdf_url = selected_article.pdf_url  # Correct field name

        print(f"✅ Selected article text: {article_abstract}")  # Debugging
        print(f"✅ PDF URL: {pdf_url}")  # Debugging PDF URL

        # Send the article text to Ollama for AI generation (streaming response)
        ollama_response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "mistral", "prompt": (
                    f"Summarize the following article in a strict and clear, structured format with the following sections: \n"
                    f"1. Objective: What is the main purpose or goal of the article? \n"
                    f"2. Key Findings: What are the important findings, contributions, or insights? \n"
                    f"3. Conclusion: What conclusions are drawn, and what are the implications of the findings? \n"
                    f"Article Text: {article_text}"
                    ),
            },
            stream=True  # Enable streaming
        )

        ai_summary = ""
        if ollama_response.status_code == 200:
            # Iterate over each chunk of the response
            for line in ollama_response.iter_lines():
                if line:
                    try:
                        chunk_data = line.decode('utf-8')
                        response_data = json.loads(chunk_data)
                        ai_summary += response_data.get("response", "").replace("\n", "<br>")
                        if response_data.get("done", False):
                            break
                    except Exception as e:
                        ai_summary = "⚠️ Failed to parse Ollama response."
                        break

        else:
            ai_summary = "⚠️ Failed to generate AI summary due to an error with Ollama."

        # ✅ Return the final response with the article's context (abstract)
        return jsonify({
            "article": {
                "title": selected_article.title,
                "abstract": selected_article.abstract,
                "author": selected_article.author,
                "publication_date": selected_article.publication_date,
                "pdf_url": pdf_url  # Add the pdf_url field to the response
            },
            "ai_summary": ai_summary,
            "context": article_text
        })
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")  # Log the error
        return jsonify({"error": "❌ Failed to generate AI summary"}), 500
    finally:
        session.close()

@app.route("/chat", methods=["POST"])
def chat():
    # Extract user message, conversation history, and context
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])
    context = data.get("context", "")  # Context should be passed here from the frontend

    # Validate user message
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Build the prompt, including the context if provided
    prompt = ""
    if context:  # Prepend context to the conversation
        prompt += f"Context: {context}\n\n"

    # Append the previous conversation history to the prompt
    for entry in conversation_history:
        prompt += f"{entry['role']}: {entry['content']}\n"

    prompt += f"user: {user_message}\nassistant:"

    # Add a restriction to the assistant's responses to ensure it's focused on the article context only
    prompt += "\nImportant: Please only refer to the provided article text in your response. Do not discuss anything unrelated to the article."

    try:
        # Send the prompt to Ollama for a conversational response
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "mistral", "prompt": prompt},
            stream=True  # Enable streaming for real-time responses
        )

        ai_response = ""
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    chunk_data = line.decode('utf-8')
                    response_data = json.loads(chunk_data)
                    ai_response += response_data.get("response", "")
                    if response_data.get("done", False):
                        break

        else:
            ai_response = "⚠️ Failed to generate response from Ollama."

        # Append the AI's response to the conversation history
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Return the AI's response and updated conversation history
        return jsonify({
            "response": ai_response,
            "history": conversation_history
        })

    except Exception as e:
        app.logger.error(f"Unexpected error during chat: {str(e)}")
        return jsonify({"error": "❌ Failed to process chat request"}), 500
    
# ✅ Run Flask on port 5001
if __name__ == "__main__":
    print("🚀 Running Flask server on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)
