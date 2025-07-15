"""Reset the PostgreSQL database using the reset template."""

import logging
from pathlib import Path

from utils.logging import setup_logging
from utils.run import run_sql_script

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"
DROP_TABLES_PATH = Path("pipelines") / "001b_drop_all_tables.py"


def main():
    logging.info("Resetting database schemas..")

    # SQL to drop and recreate the public schema
    sql_script = """
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (SELECT schema_name FROM information_schema.schemata
                    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'public')) LOOP
                EXECUTE 'DROP SCHEMA IF EXISTS ' || quote_ident(r.schema_name) || ' CASCADE;';
            END LOOP;
        END $$;
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        """

    run_sql_script(sql_script)

    logging.info("All schemas dropped")
    return


if __name__ == "__main__":
    setup_logging()
    main()
