import csv
import sqlite3
import time
import sys
import os
import json
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from models import get_connection
from logger import get_logger

logger = get_logger(__name__)   # __name__ = "scripts.sync_clients" in the log

CSV_PATH    = os.path.join(os.path.dirname(__file__), "../../data/clients_sample.csv")
MAX_RETRIES = 3
RETRY_DELAY = 2


# -------------------------------------------------------
# NOTIFICATION — called on fatal failure
# -------------------------------------------------------
def notify_fatal(script_name: str, error: str):
    """
    In a real system this would send an email or Slack message.
    For now it logs a CRITICAL entry — easy to swap later.
    """
    logger.critical(f"FATAL ERROR in {script_name}: {error}")
    logger.critical("Action required: check logs and rerun manually.")
    # Stretch goal: swap the lines above for smtplib email or a Slack webhook


def read_csv(path: str) -> list[dict]:
    rows = []
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        logger.info(f"Read {len(rows)} rows from {path}")
    except FileNotFoundError:
        logger.error(f"CSV not found: {path}")
        raise
    except PermissionError:
        logger.error(f"Permission denied reading: {path}")
        raise
    return rows


def validate_rows(rows: list[dict]) -> list[dict]:
    valid = []
    seen_emails = set()
    for row in rows:
        email = row.get("contact_email", "").strip()
        name  = row.get("company_name",  "").strip()
        if not name or not email:
            logger.warning(f"Skipping row with missing fields: {row}")
            continue
        if email in seen_emails:
            logger.warning(f"Skipping duplicate email in CSV: {email}")
            continue
        seen_emails.add(email)
        valid.append({
            "company_name":  name,
            "contact_email": email,
            "service_type":  row.get("service_type", "").strip() or None,
        })
    logger.info(f"Validated {len(valid)}/{len(rows)} rows")
    return valid


def upsert_clients(rows: list[dict]) -> dict:
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
                        company_name = excluded.company_name,
                        service_type = excluded.service_type
                """, row)
                synced += 1
            except sqlite3.IntegrityError as e:
                failed += 1
                errors.append(str(e))
                logger.error(f"Integrity error on {row['contact_email']}: {e}")

        status  = "success" if failed == 0 else "failed"
        message = f"Synced {synced}, failed {failed}"
        if errors:
            message += f" | {'; '.join(errors)}"

        conn.execute("""
            INSERT INTO jobs (client_id, script_name, status, message)
            VALUES (NULL, 'sync_clients.py', ?, ?)
        """, (status, message))

        conn.commit()
        logger.info(f"DB commit complete: {message}")

    except Exception as e:
        conn.rollback()
        logger.error(f"Rolled back transaction: {e}")
        raise
    finally:
        conn.close()

    return {"synced": synced, "failed": failed, "errors": errors}


def upsert_with_retry(rows: list[dict]) -> dict:
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            return upsert_clients(rows)
        except sqlite3.OperationalError as e:
            attempt += 1
            logger.warning(f"DB error attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt < MAX_RETRIES:
                logger.info(f"Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached.")
                raise


def write_report(result: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(
        os.path.dirname(__file__),
        f"../../logs/syncReports/sync_report_{timestamp}.json"
    )
    report = {"ran_at": datetime.now().isoformat(), "script": "sync_clients.py", "result": result}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    logger.info(f"Report written: {path}")


def run():
    logger.info("=== sync_clients.py starting ===")
    try:
        rows   = read_csv(CSV_PATH)
        valid  = validate_rows(rows)
        result = upsert_with_retry(valid)
        write_report(result)
        logger.info("=== sync_clients.py complete ===")
    except Exception as e:
        notify_fatal("sync_clients.py", str(e))
        sys.exit(1)


if __name__ == "__main__":
    run()