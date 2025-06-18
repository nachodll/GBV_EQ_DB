#!/usr/bin/env python3
"""Create the database schema."""

import os
import subprocess
from pathlib import Path


def main() -> None:
    schema_path = Path("sql/schema.sql")

    subprocess.run(
        ["psql", "-U", os.getenv("DB_USER"), "-d", os.getenv("DB_NAME"), "-f", str(schema_path)],
        check=True,
    )


if __name__ == "__main__":
    main()
