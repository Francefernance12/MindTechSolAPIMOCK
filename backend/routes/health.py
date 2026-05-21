from flask import Blueprint, jsonify
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models import get_connection

health_bp = Blueprint("health", __name__)

# Liveness — "am I running?"
@health_bp.route("/health/live", methods=["GET"])
def liveness():
    return jsonify({"status": "alive"}), 200

# Readiness — "can I handle requests?" (checks DB connection)
@health_bp.route("/health/ready", methods=["GET"])
def readiness():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")   # cheapest possible DB query
        conn.close()
        return jsonify({"status": "ready", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "db": str(e)}), 500