import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_event(event_type: str, message: str):
    logging.info(f"{event_type} | {message}")

def log_error(message: str):
    logging.error(message)
