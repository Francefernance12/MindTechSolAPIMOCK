from flask import request, jsonify
from functools import wraps
from config import API_KEY

# Decorator to wrap around request routes with needed authorization.
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")

        if not key:
            # Header missing entirely — client hasn't identified itself
            return jsonify({"error": "Missing API key"}), 401

        if key != API_KEY:
            # Header present but wrong value — client is known but not allowed
            return jsonify({"error": "Invalid API key"}), 403

        return f(*args, **kwargs)  # key is valid — proceed to the actual route
    return decorated