import logging

from logging.handlers import RotatingFileHandler

from pathlib import Path

def setup_logger(
    name: str = "automation-tool-65",
    log_dir: str = "logs",
    log_file: str = "app.log",
    max_bytes: int = 1048576,  # 1 MB
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """Configure a logger with console and rotating file handlers."""
    # Ensure log directory exists
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    log_filepath = log_path / log_file
    # Get or create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Remove existing handlers to prevent duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # Console handler for info level output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    # Rotating file handler for debug and detailed logs
    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger

# Initialize default logger for the module
default_logger = setup_logger()