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

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    # Password is set in the environment for psql command
    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password

    # Ensure required environment variables are set
    if not all([host, port, db_name, db_user]):
        logger.error("Environment variables DB_USER and DB_NAME must be set.")
        raise ValueError("Missing required environment variables: DB_USER or DB_NAME")

    subprocess.run(
        ["psql", "-h", str(host), "-p", str(port), "-U", str(db_user), "-d", str(db_name), "-f", str(SCHEMA_PATH)],
        env=env,
        check=True,
    )

    logger.info("Database schema created")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
