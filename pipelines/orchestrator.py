#!/usr/bin/env python3
"""Orchestrate database pipeline steps.

Usage::

    python pipeline.py [step] [--only]

Steps:
    reset  - Drop and recreate the database and user
    schema - Create database schema
    load   - Run extract/transform and load pipelines

If ``step`` is omitted, the script executes the full pipeline. When a ``step``
is provided, all previous steps are also run unless ``--only`` is supplied."""

import argparse
import logging
import subprocess
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style

PIPELINES_DIR = Path("pipelines")
ACTIONS: dict[str, list[Path]] = {
    "reset": [PIPELINES_DIR / "001_reset_db.py"],
    "schema": [PIPELINES_DIR / "002_create_schema.py"],
    "load": [PIPELINES_DIR / "003_et_data.py", PIPELINES_DIR / "004_load_data.py"],
}
STEP_ORDER = ["reset", "schema", "load"]

LOG_DIR = Path("logs") / "orchestrator"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"


class ColorFormatter(logging.Formatter):
    """Formatter that adds colors based on the log level."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.RED,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.LIGHTMAGENTA_EX,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record: logging.LogRecord):
        levelname = record.levelname
        color = self.LEVEL_COLORS.get(record.levelno, "")
        record.levelname = f"{color}{levelname}{Style.RESET_ALL}"
        try:
            return super().format(record)
        finally:
            record.levelname = levelname


def setup_logging() -> Path:
    """Configure root logger with colored output and file logging."""

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"{datetime.now().isoformat()}.log"

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColorFormatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))

    logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])
    return log_path


def run(script: Path):
    """Run a standalone script and capture its output."""
    logging.info("Running %s", script.name)

    result = subprocess.run(["python", str(script)], text=True, capture_output=True)

    # Print all stdout
    if result.stdout:
        for line in result.stdout.splitlines():
            print("\t", line)

    if result.stderr:
        for line in result.stderr.splitlines():
            if " - INFO - " in line:
                logging.info(line)
            elif " - WARNING - " in line:
                logging.warning(line)
            elif " - ERROR - " in line:
                logging.error(line)

    result.check_returncode()


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Run pipeline steps")
    parser.add_argument(
        "step",
        choices=list(ACTIONS.keys()),
        nargs="?",
        help="Pipeline step to execute (default: run all steps)",
    )
    parser.add_argument(
        "--only",
        action="store_true",
        help="Run only the specified step without previous steps",
    )
    args = parser.parse_args()

    scripts_to_run: list[Path] = []

    if args.step is None:
        for step in STEP_ORDER:
            scripts_to_run.extend(ACTIONS[step])
    elif args.only:
        scripts_to_run.extend(ACTIONS[args.step])
    else:
        end_index = STEP_ORDER.index(args.step) + 1
        for step in STEP_ORDER[:end_index]:
            scripts_to_run.extend(ACTIONS[step])

    for script in scripts_to_run:
        run(script)


if __name__ == "__main__":
    main()
