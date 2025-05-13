
## Hoveddelen som håndterer HTTP requesten og henter info fra de andre filene

from flask import Blueprint, request, jsonify, current_app
import numpy as np
from services.ai_search_service import handle_ai_search

ai_search_bp = Blueprint('ai_search', __name__)

@ai_search_bp.route("/ai-search", methods=["POST"])
def ai_search():
    try:
        return handle_ai_search(request)
    except Exception as e:
        current_app.logger.exception("Search error:")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
