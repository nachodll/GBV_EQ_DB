#!/usr/bin/env python3
"""Reset the PostgreSQL database using the reset template."""

import os
import subprocess
from pathlib import Path


def main() -> None:
    template_path = Path("sql/reset_db_template.sql")
    with open(template_path) as f:
        sql_script = os.path.expandvars(f.read())

    subprocess.run(
        ["psql", "-U", "postgres"],
        input=sql_script.encode(),
        check=True,
    )


if __name__ == "__main__":
    main()
