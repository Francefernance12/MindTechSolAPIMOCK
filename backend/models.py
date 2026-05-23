import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Important to connect DB across Flask
def get_connection() -> sqlite3.Connection:
    """Returns a connection with foreign key enforcement enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # lets you access columns by name: row["company_name"]
    conn.execute("PRAGMA foreign_keys = ON") # enables foreign key constraints
    return conn

# Database Schema
def create_tables() -> None:
    conn: sqlite3.Connection = get_connection()
    cursor: sqlite3.Cursor = conn.cursor() # allows you to execute SQL commands

    # --- clients table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            client_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT    NOT NULL,
            contact_email TEXT   UNIQUE,
            service_type TEXT,
            created_at   TEXT    DEFAULT (datetime('now'))
        )
    """)

    # --- jobs table ---
    # client_id here is a FOREIGN KEY — it must match a real client_id in clients.
    # ON DELETE CASCADE means: if a client is deleted, their job logs go with them.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id   INTEGER,
            script_name TEXT    NOT NULL,
            status      TEXT    NOT NULL CHECK(status IN ('success', 'failed')),
            ran_at      TEXT    DEFAULT (datetime('now')),
            message     TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created.")

if __name__ == "__main__":
    create_tables()