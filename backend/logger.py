import logging
import os

LOG_DIR  = os.path.join(os.path.dirname(__file__), "../logs")
LOG_FILE = os.path.join(LOG_DIR, "mindtech.log")

# Create logs/ directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger that writes to both the console and a log file.
    Call this at the top of any module: logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler 1: write to file
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler 2: write to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)   # less noise in the terminal
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger