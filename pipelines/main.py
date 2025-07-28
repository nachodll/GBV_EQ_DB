#!/usr/bin/env python3
"""Orchestrate database pipeline steps.

Usage:
    python pipeline.py [step] [--only] [--schema SCHEMA]

Steps:
    drop   - Drop all schemas
    create - Create all database schemas
    et     - Run extract and transform pipelines
    load   - Load data into the database

Options:
    --only      Run only the specified step, skipping previous steps.
    --schema    If provided, only ET and load for this schema will be run
                (geo and metadata are always loaded).

If ``step`` is omitted, the script executes the full pipeline. When a ``step``
is provided, all previous steps are also run unless ``--only`` is supplied.
If ``--schema`` is provided, only extract-transform and load steps for that
schema will be executed (geo and metadata always included).
"""

import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from utils.logging import setup_logging
from utils.run_script import run_python_script

load_dotenv()

PIPELINES_DIR = Path("pipelines")
ACTIONS: dict[str, list[Path]] = {
    "drop": [PIPELINES_DIR / "drop_schemas.py"],
    "create": [PIPELINES_DIR / "create_schemas.py"],
    "et": [PIPELINES_DIR / "extract_transform_data.py"],
    "load": [PIPELINES_DIR / "load_data.py"],
}


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
    parser.add_argument(
        "--schema",
        type=str,
        help="If provided, only ET and load for this schema will be run",
    )
    args = parser.parse_args()

    scripts_to_run: list[tuple[Path, list[str]]] = []
    step_order = list(ACTIONS.keys())

    # Build the list of scripts and their arguments
    if args.step is None:
        for step in step_order:
            for script in ACTIONS[step]:
                scripts_to_run.append((script, []))
    elif args.only:
        for script in ACTIONS[args.step]:
            scripts_to_run.append((script, []))
    else:
        end_index = step_order.index(args.step) + 1
        for step in step_order[:end_index]:
            for script in ACTIONS[step]:
                scripts_to_run.append((script, []))

    # If --schema is provided, pass it to extract_transform_data.py and load_data.py
    if args.schema:
        scripts_to_run = (
            [
                (PIPELINES_DIR / "drop_schemas.py", []),
                (PIPELINES_DIR / "create_schemas.py", []),
                (PIPELINES_DIR / "extract_transform_data.py", [args.schema]),
                (PIPELINES_DIR / "load_data.py", [args.schema]),
            ]
            if args.step is None
            else [
                (script, [args.schema] if script.name in {"extract_transform_data.py", "load_data.py"} else [])
                for script, _ in scripts_to_run
            ]
        )

    for script, script_args in scripts_to_run:
        logging.info("----------------------------------------")
        logging.info(f"Running {script.name} {' '.join(script_args)}")
        logging.info("----------------------------------------")
        run_python_script(script, *script_args)


if __name__ == "__main__":
    setup_logging()
    main()
