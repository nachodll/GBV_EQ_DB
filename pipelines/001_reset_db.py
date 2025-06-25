"""Reset the PostgreSQL database using the reset template."""

import logging
from pathlib import Path

from utils.run import run_sql_script

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"
DROP_TABLES_PATH = Path("pipelines") / "001b_drop_all_tables.py"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    logger.info("Resetting the public schema...")

    # SQL to drop and recreate the public schema
    sql_script = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

    run_sql_script(sql_script)

    logger.info("Public schema reset completed")
    return


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
