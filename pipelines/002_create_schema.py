"""Create the database schema."""

import logging
import os
import subprocess
from pathlib import Path

SCHEMA_PATH = Path("sql") / "schema.sql"

# Logger setup
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Creating the database schema...")

    subprocess.run(
        ["psql", "-U", os.getenv("DB_USER"), "-d", os.getenv("DB_NAME"), "-f", str(SCHEMA_PATH)],
        check=True,
    )

    logger.info("Database schema created")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
