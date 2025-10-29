"""Create the database schema."""

import logging
from pathlib import Path

from utils.logging import setup_logging
from utils.run_script import run_sql_script

SCHEMA_PATH = Path("sql") / "schema.sql"
VIEWS_PATH = Path("sql") / "views.sql"
PERMISSIONS_PATH = Path("sql") / "permissions.sql"


def main():
    logging.info("Creating the database schema...")
    run_sql_script(SCHEMA_PATH.read_text())

    logging.info("Creating views...")
    run_sql_script(VIEWS_PATH.read_text())

    logging.info("Granting permissions...")
    run_sql_script(PERMISSIONS_PATH.read_text())

    logging.info("Database schema with views and permissions created")


if __name__ == "__main__":
    setup_logging()
    main()
