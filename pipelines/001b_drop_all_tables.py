"""Drop all tables in the connected database."""

import logging
import os
import subprocess
from pathlib import Path

DROP_TABLES_PATH = Path("sql") / "drop_all_tables.sql"

logger = logging.getLogger(__name__)


def main():
    logger.info("Dropping all tables from database...")

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password

    if not all([host, port, db_name, db_user]):
        logger.error("DB_HOST, DB_PORT, DB_NAME and DB_USER environment variables must be set.")
        raise ValueError("Missing required environment variables for dropping tables.")

    subprocess.run(
        [
            "psql",
            "-h",
            str(host),
            "-p",
            str(port),
            "-U",
            str(db_user),
            "-d",
            str(db_name),
            "-f",
            str(DROP_TABLES_PATH),
        ],
        env=env,
        check=True,
    )

    logger.info("All tables dropped")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
    main()
