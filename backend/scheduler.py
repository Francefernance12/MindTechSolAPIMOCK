import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import sys
import os

sys.path.append(os.path.dirname(__file__))
from logger import get_logger
from scripts.sync_clients import run as sync_run

logger = get_logger(__name__)


# -------------------------------------------------------
# CRON vs APScheduler
# -------------------------------------------------------
# Cron (Linux/Mac) — OS-level scheduler. Defined in a crontab file.
#   Format: minute hour day month weekday command
#   Example: */1 * * * * python /path/to/sync_clients.py
#   Runs the script as a separate process. Simple but hard to observe.
#
# APScheduler — Python library scheduler. Runs inside your process.
#   Easier to control, log, and debug from code.
#   Use APScheduler for dev and simple production.
#   Use cron or a task queue (Celery, etc.) for heavier production workloads.


def job_listener(event):
    """
    Fired after every scheduled job run.
    EVENT_JOB_EXECUTED = success, EVENT_JOB_ERROR = exception was raised.
    This is how you know a scheduled job ran — and whether it succeeded.
    """
    if event.exception:
        logger.error(f"Scheduled job FAILED: {event.job_id} | {event.exception}")
    else:
        logger.info(f"Scheduled job completed: {event.job_id}")


def start():
    scheduler = BackgroundScheduler()

    # Run sync_clients every 1 minute (change to 60 for hourly in production)
    scheduler.add_job(
        func=sync_run,
        trigger="interval",
        minutes=1,
        id="sync_clients",
        name="Sync clients from CSV",
        replace_existing=True,
    )

    # Attach the listener so every run is observed
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    scheduler.start()
    logger.info("Scheduler started. sync_clients running every 5 minute.")
    logger.info("Press Ctrl+C to stop.")

    try:
        # Keep the main thread alive — scheduler runs in the background
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    start()