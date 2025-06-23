"""Reset the PostgreSQL database using the reset template."""

import logging
import os
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    if os.getenv("SKIP_DB_RESET", "").lower() in {"1", "true", "yes"}:
        logger.info("Skipping database reset because SKIP_DB_RESET is set")
        return

    logger.info("Resetting the database...")

    # The template SQL script is loaded and variables are resolved to environment variables
    with open(TEMPLATE_PATH) as f:
        sql_script = os.path.expandvars(f.read())

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    admin_user = os.getenv("DB_ADMIN_USER")
    admin_password = os.getenv("DB_ADMIN_PASSWORD")

    # Pasword is set in the environment for psql command
    env = os.environ.copy()
    if admin_password:
        env["PGPASSWORD"] = admin_password

    # Ensure required environment variables are set
    if not all([host, port, admin_user]):
        logger.error("DB_HOST, DB_PORT, and DB_ADMIN_USER environment variables must be set.")
        raise ValueError("Missing required database connection environment variables.")

    subprocess.run(
        ["psql", "-h", str(host), "-p", str(port), "-U", str(admin_user)],
        input=sql_script.encode(),
        # env=env,
        check=True,
    )
    logger.info("Database reset completed")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
