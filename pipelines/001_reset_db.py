"""Reset the PostgreSQL database using the reset template."""

import logging
import os
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"
DROP_TABLES_PATH = Path("pipelines") / "001b_drop_all_tables.py"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    logger.info("Resetting the public schema...")

    # SQL to drop and recreate the public schema
    sql_script = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    db_name = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")

    # Password is set in the environment for psql command
    env = os.environ.copy()
    if password:
        env["PGPASSWORD"] = password

    # Ensure required environment variables are set
    if not all([host, port, user]):
        logger.error("DB_HOST, DB_PORT, and DB_USER environment variables must be set.")
        raise ValueError("Missing required database connection environment variables.")

    result = subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-h", str(host), "-p", str(port), "-U", str(user), "-d", str(db_name)],
        input=sql_script.encode(),
        env=env,
        capture_output=True,
    )

    if result.returncode != 0:
        logger.error(f"Failed to reset database: {result.stderr.decode()}")
        raise RuntimeError(f"Database reset failed with error: {result.stderr.decode()}")

    logger.info("Public schema reset completed")
    return


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
