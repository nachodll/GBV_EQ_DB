import logging
import re
import sys
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style


class ColorFormatter(logging.Formatter):
    """Formatter that adds colors based on the log level and applies it to the entire line."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.RED,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.LIGHTMAGENTA_EX,
        logging.CRITICAL: Fore.GREEN,
    }

    def format(self, record: logging.LogRecord):
        levelname = record.levelname
        color = self.LEVEL_COLORS.get(record.levelno, "")
        record.levelname = f"{color}{levelname}{Style.RESET_ALL}"
        try:
            formatted = super().format(record)
            return f"{color}{formatted}{Style.RESET_ALL}"
        finally:
            record.levelname = levelname


def strip_metadata(line: str) -> tuple[str, int]:
    """Strip repeated logging metadata and return indentation depth."""
    # Remove ANSI escape sequences for colors
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    clean_line = ansi_escape.sub("", line)
    pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (?:DEBUG|INFO|WARNING|ERROR|CRITICAL) \[[^\]]+\] "
    )
    depth = 0
    previous = None
    while previous != clean_line:
        previous = clean_line
        clean_line = pattern.sub("", clean_line)
        if previous != clean_line:
            depth += 1
    return clean_line, depth


def setup_logging() -> None:
    """Configure root logger with colored output and file logging."""
    LOG_DIR = Path("logs") / "main"

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColorFormatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))

    # Save to file only if the file name is main.py
    if Path(sys.argv[0]).name == "main.py":
        LOG_DIR.parent.mkdir(exist_ok=True)
        LOG_DIR.mkdir(exist_ok=True)
        log_path = LOG_DIR / f"{datetime.now().isoformat()}.log"
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
        logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

    return
