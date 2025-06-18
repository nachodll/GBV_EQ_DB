#!/usr/bin/env python3
"""Orchestrate database pipeline steps.

Usage::

    python pipeline.py [step] [--only]

Steps:
    reset  - Drop and recreate the database and user
    schema - Create database schema
    load   - Run extract/transform and load pipelines

If ``step`` is omitted, the script executes the full pipeline. When a ``step``
is provided, all previous steps are also run unless ``--only`` is supplied.
"""

import argparse
import logging
import subprocess
from datetime import datetime
from pathlib import Path

PIPELINES_DIR = Path("pipelines")
ACTIONS: dict[str, list[Path]] = {
    "reset": [PIPELINES_DIR / "001_reset_db.py"],
    "schema": [PIPELINES_DIR / "002_create_schema.py"],
    "load": [PIPELINES_DIR / "003_et_data.py", PIPELINES_DIR / "004_load_data.py"],
}
STEP_ORDER = ["reset", "schema", "load"]

LOG_DIR = Path("logs") / "orchestrator"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"


def setup_logging() -> None:
    """Configure root logger to log to stdout and file."""
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_PATH),
        ],
    )


def run(script: Path) -> None:
    """Run a standalone script."""
    logging.info("Running %s", script.name)
    subprocess.run(["python", str(script)], check=True)


def main() -> None:
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
