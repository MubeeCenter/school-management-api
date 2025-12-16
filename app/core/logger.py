import logging
import sys
from pythonjsonlogger import jsonlogger
import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"

def setup_logging(log_level=logging.INFO):
    """
    Configure root logger for structured JSON output.
    Call once in main.py.
    """
    root_logger = logging.getLogger()

    # Prevent duplicate handlers on reload
    if root_logger.handlers:
        return root_logger

    root_logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Reduce noise from uvicorn internals
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

    # Silence asyncio CancelledError spam
    logging.getLogger("asyncio").setLevel(logging.ERROR)

    root_logger.info("logging_initialized")

    return root_logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("school-api")
