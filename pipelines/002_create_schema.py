"""Create the database schema."""

import logging
import os
import subprocess
from pathlib import Path

SCHEMA_PATH = Path("sql") / "schema.sql"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    logger.info("Creating the database schema...")

    db_user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    if not db_user or not db_name:
        logger.error("Environment variables DB_USER and DB_NAME must be set.")
        raise ValueError("Missing required environment variables: DB_USER or DB_NAME")

    subprocess.run(
        ["psql", "-U", db_user, "-d", db_name, "-f", str(SCHEMA_PATH)],
        check=True,
    )

    logger.info("Database schema created")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
