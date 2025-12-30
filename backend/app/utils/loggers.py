import logging
from datetime import datetime

# Utility logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# Utility function to log events
def log_event(event_type: str, message: str):
    logging.info(f"{event_type} | {message}")

# Utility function to log errors
def log_error(message: str):
    logging.error(message)
