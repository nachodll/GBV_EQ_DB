import logging
import os
import subprocess
from pathlib import Path

from utils.logging import strip_metadata


def run_python_script(script: Path):
    """Run a standalone python script and capture its output."""

    result = subprocess.run(
        ["python", script],
        text=True,
        capture_output=True,
    )

    if result.stderr:
        for line in result.stderr.splitlines():
            clean, level = strip_metadata(line)
            indent = "\t" * (level)
            if "DEBUG" in line:
                logging.debug(indent + clean)
            elif "WARNING" in line:
                logging.warning(indent + clean)
            elif "ERROR" in line:
                logging.error(indent + clean)
            elif "CRITICAL" in line:
                logging.critical(indent + clean)
            elif "INFO" in line:
                logging.info(indent + clean)
    result.check_returncode()


def run_sql_script(script: str):
    """Run a SQL script against the PostgreSQL database using psql command."""

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
        logging.error("DB_HOST, DB_PORT, and DB_USER environment variables must be set.")
        raise ValueError("Missing required database connection environment variables.")

    result = subprocess.run(
        ["psql", "-v", "ON_ERROR_STOP=1", "-h", str(host), "-p", str(port), "-U", str(user), "-d", str(db_name)],
        input=script.encode(),
        env=env,
        capture_output=True,
    )

    result.check_returncode()
