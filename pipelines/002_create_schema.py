"""Create the database schema."""

import logging
from pathlib import Path

from utils.logging import setup_logging
from utils.run import run_sql_script

SCHEMA_PATH = Path("sql") / "schema.sql"


def main():
    logging.info("Creating the database schema...")

    run_sql_script(SCHEMA_PATH.read_text())

    logging.info("Database schema created")


if __name__ == "__main__":
    setup_logging()
    main()
