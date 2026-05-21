from typing import Any


import csv
import sqlite3
import time
import sys
import os
import json
from datetime import datetime

# Import models.py from parent folder 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models import get_connection

CSV_PATH = os.path.join(os.path.dirname(__file__), "../../data/clients_sample.csv")
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


# -------------------------------------------------------
# FILE I/O — reading a CSV
# -------------------------------------------------------

def read_csv(path: str) -> list[dict]:
    """
        Reads a CSV file and returns a list of dicts.
        Each dict is one row: { "company_name": ..., "contact_email": ..., ... }
    """
    rows = []

    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)  # uses first row as keys automatically
            for row in reader:
                rows.append(row)
        print(f"Read {len(rows)} rows from CSV.")
    except FileNotFoundError:
        print(f"ERROR: CSV not found at {path}")
        raise  # re-raise so the caller knows something went wrong
    except PermissionError:
        print(f"ERROR: No permission to read {path}")
        raise
    return rows


# -------------------------------------------------------
# COLLECTIONS — dict vs list, and when to use which
# -------------------------------------------------------
# rows        → list of dicts   (ordered collection, iterate in sequence)
# row         → dict            (key-value pairs, access by name not index)
# seen_emails → set             (unordered, unique values only — fast membership check)

def validate_rows(rows: list[dict]) -> list[dict]:
    """
    Filters out rows with missing required fields.
    Demonstrates: list, dict access, set for deduplication.
    """
    valid = []
    seen_emails = set[Any]()  # catch duplicates within the CSV itself

    for row in rows:
        email = row.get("contact_email", "").strip()
        name  = row.get("company_name", "").strip()

        if not name or not email:
            print(f"  SKIP: missing name or email → {row}")
            continue

        if email in seen_emails:
            print(f"  SKIP: duplicate email in CSV → {email}")
            continue

        seen_emails.add(email)
        valid.append({
            "company_name":  name,
            "contact_email": email,
            "service_type":  row.get("service_type", "").strip() or None,
        })

    return valid


# -------------------------------------------------------
# RETRY LOGIC — two common patterns
# -------------------------------------------------------

# Pattern 1: simple loop with counter
def upsert_with_retry(rows: list[dict]) -> dict:
    """
    Tries to upsert all rows into the DB.
    Retries up to MAX_RETRIES times on OperationalError (e.g. DB locked).
    Returns a summary dict: { "synced": int, "failed": int, "errors": list }
    """
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            result = upsert_clients(rows)
            return result  # success — exit immediately
        except sqlite3.OperationalError as e:
            attempt += 1
            print(f"  DB error (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                print(f"  Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                print("  Max retries reached. Giving up.")
                raise  # let it bubble up after all retries exhausted


# Pattern 2: exponential backoff (stretch — comment shows the idea)
# delay = RETRY_DELAY
# for attempt in range(MAX_RETRIES):
#     try:
#         return upsert_clients(rows)
#     except sqlite3.OperationalError:
#         time.sleep(delay)
#         delay *= 2      # 2s → 4s → 8s
# raise


# -------------------------------------------------------
# DB WRITE — upsert (insert or update)
# -------------------------------------------------------
def upsert_clients(rows: list[dict]) -> dict:
    """
    Upsert just means update or insert lol.
    INSERT OR REPLACE upserts each row.
    If contact_email already exists → row is replaced (updated).
    If it's new → row is inserted.
    Logs the result to the jobs table as a transaction.
    """
    synced = 0
    failed = 0
    errors = []

    conn = get_connection()
    try:
        for row in rows:
            try:
                conn.execute("""
                    INSERT INTO clients (company_name, contact_email, service_type)
                    VALUES (:company_name, :contact_email, :service_type)
                    ON CONFLICT(contact_email)
                    DO UPDATE SET
                        company_name  = excluded.company_name,
                        service_type  = excluded.service_type
                """, row)
                synced += 1
            except sqlite3.IntegrityError as e:
                # Shouldn't happen with ON CONFLICT, but handle defensively
                failed += 1
                errors.append(str(e))
                print(f"  INTEGRITY ERROR on {row['contact_email']}: {e}")

        # ---- transaction: commit synced rows + write job log atomically ----
        status  = "success" if failed == 0 else "failed"
        message = f"Synced {synced}, failed {failed}"
        if errors:
            message += f" | Errors: {'; '.join(errors)}"

        conn.execute("""
            INSERT INTO jobs (client_id, script_name, status, message)
            VALUES (NULL, 'sync_clients.py', ?, ?)
        """, (status, message))
        # client_id is NULL here — this job log isn't tied to one client,
        # it's a system-level log. We'll adjust the schema slightly below.

        conn.commit()
        print(f"Committed: {synced} upserted, {failed} failed.")

    except Exception as e:
        conn.rollback()
        print(f"Unexpected error, rolled back: {e}")
        raise

    finally:
        conn.close()

    return {"synced": synced, "failed": failed, "errors": errors}

# -------------------------------------------------------
# WRITING TO A FILE — saving the result as JSON
# -------------------------------------------------------

def write_report(result: dict, path: str = None):
    """Writes the sync summary to a JSON file."""
    if path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(os.path.dirname(__file__), f"../../data/logs/syncReports/sync_report_{timestamp}.json")

    report = {
        "ran_at":  datetime.now().isoformat(),
        "script":  "sync_clients.py",
        "result":  result,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {path}")


# -------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------
if __name__ == "__main__":
    print("=== sync_clients.py starting ===")
    try:
        rows   = read_csv(CSV_PATH)  # Put data from CSV into list of rows(Dictionary)
        valid  = validate_rows(rows)  # Rows are put into a filtering process
        result = upsert_with_retry(valid)  # With validated dictionaries, the prcoess of inserting or updating the data into DB
        write_report(result) # Finally create the results from the entire process.
        print("=== Done ===")
    except Exception as e:
        print(f"FATAL: script failed — {e}")
        sys.exit(1)  # exit code 1 signals failure to the OS (cron will see this)