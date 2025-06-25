"""Create the database schema."""

import logging
from pathlib import Path

from utils.run import run_sql_script

SCHEMA_PATH = Path("sql") / "schema.sql"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    logger.info("Creating the database schema...")

    run_sql_script(SCHEMA_PATH.read_text())

    logger.info("Database schema created")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
