"""
Simple, reusable logging utility for PySpark/Glue jobs.
Configures a logger with INFO level, stdout handler, and consistent formatting.
Prevents duplicate handlers in repeated calls.
"""

import logging
import sys
from typing import Optional


def get_logger(
    name: str,
    level: int = logging.INFO,
    fmt: str = "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S"
) -> logging.Logger:
    """
    Get or create a configured logger.

    Args:
        name: Logger name (usually __name__ or class name)
        level: Logging level (default: INFO)
        fmt: Log message format
        datefmt: Date/time format in messages

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers (common in Glue/PySpark restarts or repeated imports)
    if not logger.handlers:
        # Use stdout (Glue captures it in CloudWatch Logs)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(fmt, datefmt=datefmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Optional: Convenience function for root logger or quick setup
def setup_root_logger(level: int = logging.INFO) -> None:
    """
    Configure the root logger (useful for Glue jobs without many modules).
    """
    root = logging.getLogger()
    root.setLevel(level)
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)


# Example usage (can be called once at job start)
if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Logger initialized")
    logger.debug("This debug message won't show unless level is DEBUG")
    logger.warning("This is a warning")
    logger.error("This is an error example")
