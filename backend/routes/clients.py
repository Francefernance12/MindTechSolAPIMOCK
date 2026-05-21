from flask import Blueprint, jsonify, request
import sys, os
# Local Imports. Directory ../
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models import get_connection
from auth import require_api_key 

clients_bp = Blueprint("clients", __name__)


# --------------------------------------------------
# GET /clients — fetch all clients
# --------------------------------------------------
@clients_bp.route("/clients", methods=["GET"])
@require_api_key
def get_clients():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    clients = [dict(row) for row in rows]  # sqlite3.Row → plain dict → JSON-serializable
    return jsonify(clients), 200


# --------------------------------------------------
# GET /clients/<id> — fetch one client
# --------------------------------------------------
@clients_bp.route("/clients/<int:client_id>", methods=["GET"])
@require_api_key
def get_client(client_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM clients WHERE client_id = ?", (client_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Client not found"}), 404  # never return 200 with an error message

    return jsonify(dict(row)), 200


# --------------------------------------------------
# POST /clients — create a new client
# --------------------------------------------------
@clients_bp.route("/clients", methods=["POST"])
@require_api_key
def create_client():
    data = request.get_json()

    # Validate required fields — return 400 if missing
    if not data or not data.get("company_name") or not data.get("contact_email"):
        return jsonify({"error": "company_name and contact_email are required"}), 400

    conn = get_connection()
    try:
        cursor = conn.execute("""
            INSERT INTO clients (company_name, contact_email, service_type)
            VALUES (?, ?, ?)
        """, (
            data["company_name"],
            data["contact_email"],
            data.get("service_type")   # optional field
        ))
        conn.commit()
        new_id = cursor.lastrowid      # ID the DB assigned to the new row
        conn.close()
        return jsonify({"message": "Client created", "client_id": new_id}), 201  # 201 = Created

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# PUT /clients/<id> — update an existing client
# --------------------------------------------------
@clients_bp.route("/clients/<int:client_id>", methods=["PUT"])
@require_api_key
def update_client(client_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    conn = get_connection()

    # Check client exists first
    row = conn.execute(
        "SELECT * FROM clients WHERE client_id = ?", (client_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Client not found"}), 404

    # Merge: keep existing value if field not provided in request
    existing = dict(row)
    updated_name    = data.get("company_name",  existing["company_name"])
    updated_email   = data.get("contact_email", existing["contact_email"])
    updated_service = data.get("service_type",  existing["service_type"])

    try:
        conn.execute("""
            UPDATE clients
            SET company_name = ?, contact_email = ?, service_type = ?
            WHERE client_id = ?
        """, (updated_name, updated_email, updated_service, client_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Client updated"}), 200

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# DELETE /clients/<id> — delete a client
# --------------------------------------------------
@clients_bp.route("/clients/<int:client_id>", methods=["DELETE"])
@require_api_key
def delete_client(client_id):
    conn = get_connection()

    row = conn.execute(
        "SELECT * FROM clients WHERE client_id = ?", (client_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Client not found"}), 404

    conn.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Client deleted"}), 200