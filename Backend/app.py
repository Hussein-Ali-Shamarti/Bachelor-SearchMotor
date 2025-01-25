from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
from models import Base, Item
from database import engine, SessionLocal

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enable CORS for communication with React frontend

# Create tables in the database (if not already created)
Base.metadata.create_all(bind=engine)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()
    if not query:
    return jsonify({"error": "Please provide a search query"}), 400

# Open a database session
session = SessionLocal()
try:
# Search for items in the database
results = session.query(Item).filter(
(Item.name.ilike(f"%{query}%")) | (Item.description.ilike(f"%{query}%"))
).all()

# Return results as JSON
return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in results])
finally:
session.close()

if __name__ == "__main__":
app.run(debug=True)