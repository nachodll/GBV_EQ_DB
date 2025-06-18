"""Reset the PostgreSQL database using the reset template."""

import logging
import os
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    logger.info("Resetting the database...")

    with open(TEMPLATE_PATH) as f:
        sql_script = os.path.expandvars(f.read())

    subprocess.run(
        ["psql", "-U", "postgres"],
        input=sql_script.encode(),
        check=True,
    )
    logger.info("Database reset completed")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
