from flask import Blueprint, jsonify
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models import get_connection

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM jobs ORDER BY ran_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200