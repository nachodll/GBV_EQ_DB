#!/usr/bin/env python3
"""Orchestrate database pipeline steps.

Usage::

    python pipeline.py [step] [--only]

Steps:
    reset  - Drop and recreate the database and user
    schema - Create database schema
    et     - Run extract and transform pipelines
    load   - Load data into the database

If ``step`` is omitted, the script executes the full pipeline. When a ``step``
is provided, all previous steps are also run unless ``--only`` is supplied."""

import argparse
import logging
from datetime import datetime
from pathlib import Path

from utils.logging import setup_logging
from utils.run import run_python_script

PIPELINES_DIR = Path("pipelines")
ACTIONS: dict[str, list[Path]] = {
    "reset": [PIPELINES_DIR / "reset_schema.py"],
    "schema": [PIPELINES_DIR / "create_schema.py"],
    "et": [PIPELINES_DIR / "extract_transform_data.py"],
    "load": [PIPELINES_DIR / "load_data.py"],
}

LOG_DIR = Path("logs") / "orchestrator"
LOG_PATH = LOG_DIR / f"{datetime.now().isoformat()}.log"


def main():
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
    step_order = list(ACTIONS.keys())

    if args.step is None:
        for step in step_order:
            scripts_to_run.extend(ACTIONS[step])
    elif args.only:
        scripts_to_run.extend(ACTIONS[args.step])
    else:
        end_index = step_order.index(args.step) + 1
        for step in step_order[:end_index]:
            scripts_to_run.extend(ACTIONS[step])

    for script in scripts_to_run:
        logging.info("----------------------------------------")
        logging.info(f"Running {script.name}")
        logging.info("----------------------------------------")
        run_python_script(script)


if __name__ == "__main__":
    setup_logging()
    main()
