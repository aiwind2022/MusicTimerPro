import logging
from pathlib import Path


def setup_logger() -> logging.Logger:
    """Create and configure the application logger."""

    project_root = Path(__file__).resolve().parents[2]
    log_directory = project_root / "data" / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / "musictimer.log"

    logger = logging.getLogger("MusicTimerPro")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger