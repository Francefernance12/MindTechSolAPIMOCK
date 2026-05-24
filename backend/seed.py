# Local imports
from models import get_connection

def seed() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------
    # CREATE — INSERT rows
    # All four client rows inserted into the clients table.
    # -------------------------
    clients: list[tuple[str, str, str]] = [
        ("Acme Print Co.",    "info@acmeprint.com",   "print"),
        ("VoiceFirst Ltd.",   "ops@voicefirst.com",   "voip"),
        ("DocuFlow Inc.",     "admin@docuflow.com",   "docuware"),
        ("Maple IT Group",    "hello@mapleit.com",    "it"),
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO clients (company_name, contact_email, service_type)
        VALUES (?, ?, ?)
    """, clients)
    # INSERT OR IGNORE skips the row if contact_email already exists (it's UNIQUE).
    # This makes the seed script safe to run multiple times.

    conn.commit()
    print(f"Seeded clients.")

    # -------------------------
    # READ — SELECT rows
    # We analyzed the clients table and all four client rows are now in the clients table.
    # -------------------------
    print("\n--- All clients ---")
    cursor.execute("SELECT client_id, company_name, service_type FROM clients")
    rows = cursor.fetchall()  # returns a list of tuples from the SELECT query
    for row in rows:
        print(f"  [{row['client_id']}] {row['company_name']} ({row['service_type']})")  # row from SELECT query acts as a dictionary

    # -------------------------
    # UPDATE — change a value
    # We updated the service type for Acme Print Co. to 'print+it'.
    # -------------------------
    cursor.execute("""
        UPDATE clients
        SET service_type = 'print+it'
        WHERE company_name = 'Acme Print Co.'
    """)
    conn.commit()
    print("\nUpdated Acme Print Co. service type.")

    # -------------------------
    # DELETE — remove a row
    # We deleted the Maple IT Group row from the clients table.
    # -------------------------
    cursor.execute("DELETE FROM clients WHERE company_name = 'Maple IT Group'")
    conn.commit()
    print("Deleted Maple IT Group.")

    # -------------------------
    # READ again to confirm
    # We read the clients table again to confirm the update and delete.
    # -------------------------
    print("\n--- Clients after update + delete ---")
    cursor.execute("SELECT client_id, company_name, service_type FROM clients")
    for row in cursor.fetchall():
        print(f"  [{row['client_id']}] {row['company_name']} ({row['service_type']})")

    conn.close()


# -------------------------------------------------------
# TRANSACTIONS
# They maintain data integrity by ensuring that either all operations succeed or none do.
# -------------------------------------------------------
# A transaction bundles multiple writes into one atomic unit.
# Either ALL succeed, or NONE do. The DB never ends up half-written.

def log_job_for_client(client_id: int, script_name: str, status: str, message: str = None):
    """
    Atomically:
      1. Verify the client exists.
      2. Insert a job log row.
    If anything fails, the whole operation rolls back.
    """
    conn = get_connection()
    try:
        # Everything inside this block is one transaction.
        # conn.execute() without commit() keeps changes pending.

        # Step 1: verify client exists
        client = conn.execute(
            "SELECT client_id FROM clients WHERE client_id = ?", (client_id,)
        ).fetchone()

        if not client:
            raise ValueError(f"No client with id={client_id}")

        # Step 2: insert job log
        conn.execute("""
            INSERT INTO jobs (client_id, script_name, status, message)
            VALUES (?, ?, ?, ?)
        """, (client_id, script_name, status, message))

        conn.commit()   # <-- only NOW are the changes written to disk
        print(f"Job logged for client {client_id}: {status}")

    except Exception as e:
        conn.rollback() # <-- something went wrong — undo everything
        print(f"Transaction failed, rolled back: {e}")

    finally:
        conn.close()    # always close, whether success or failure


if __name__ == "__main__":
    seed()

    print("\n--- Logging jobs (transactions) ---")
    #  Hardcoded test data to test transaction rollback
    log_job_for_client(1, "sync_clients.py", "success", "TRANSACTION TEST: Synced 42 rows")
    log_job_for_client(2, "sync_clients.py", "failed",  "TRANSACTION TEST: Timeout after 30s")
    log_job_for_client(99, "sync_clients.py", "success", "TRANSACTION TEST: This should roll back")

    print("\n--- All job logs ---")
    conn = get_connection()
    for row in conn.execute("SELECT * FROM jobs").fetchall():
        print(f"  job {row['job_id']} | client {row['client_id']} | {row['status']} | {row['message']}")
    conn.close()