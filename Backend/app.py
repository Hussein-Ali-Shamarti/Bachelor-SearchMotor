from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Import blueprints from routes
from routes.generate_embedding import generate_embedding_bp
from routes.ai_search import ai_search_bp
from routes.get_article import article_bp
from routes.chatbot import chat_bp

# Import services to initialize the model and FAISS index
from services.model_service import init_model
from services.faiss_service import init_faiss_index

# Load environment variables
load_dotenv()

# Create Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}})

# Initialize the Sentence Transformer model and FAISS index
MODEL = init_model()
INDEX, IDS = init_faiss_index()
if INDEX is None:
    print("FAISS index is empty! No embeddings found in the database.")

# Save global objects in app config for use in blueprints
app.config['MODEL'] = MODEL
app.config['INDEX'] = INDEX
app.config['IDS'] = IDS

# Register blueprints for each route
app.register_blueprint(generate_embedding_bp)
app.register_blueprint(ai_search_bp)
app.register_blueprint(article_bp)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    print("Running Flask server on port 5001...")
    app.run(debug=True, host="0.0.0.0", port=5001)
