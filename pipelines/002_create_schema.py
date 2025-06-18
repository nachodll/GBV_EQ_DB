#!/usr/bin/env python3
"""Create the database schema."""

import os
import subprocess
from pathlib import Path

SCHEMA_PATH = Path("sql") / "schema.sql"


def main() -> None:
    subprocess.run(
        ["psql", "-U", os.getenv("DB_USER"), "-d", os.getenv("DB_NAME"), "-f", str(SCHEMA_PATH)],
        check=True,
    )


if __name__ == "__main__":
    main()
