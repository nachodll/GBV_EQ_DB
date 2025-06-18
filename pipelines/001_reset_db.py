"""Reset the PostgreSQL database using the reset template."""

import os
import subprocess
from pathlib import Path

TEMPLATE_PATH = Path("sql") / "reset_db_template.sql"


def main() -> None:
    with open(TEMPLATE_PATH) as f:
        sql_script = os.path.expandvars(f.read())

    subprocess.run(
        ["psql", "-U", "postgres"],
        input=sql_script.encode(),
        check=True,
    )


if __name__ == "__main__":
    main()
