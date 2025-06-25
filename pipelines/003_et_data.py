"""Run extract-transform steps for the raw datasets."""

import logging
from pathlib import Path

from utils.logging import setup_logging
from utils.run import run_python_script

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("pipelines") / "extract_transform"
SCRIPTS = [
    ET_SCRIPTS_DIR / "001_et_feminicidios_pareja.py",
    ET_SCRIPTS_DIR / "002_et_feminicidios_no_pareja.py",
    ET_SCRIPTS_DIR / "003_et_menores_victimas_mortales.py",
    ET_SCRIPTS_DIR / "004_et_servicio_016.py",
    ET_SCRIPTS_DIR / "005_et_usuarias_atenpro.py",
]


def main():
    logging.info("Starting extract-transform scripts...")

    for script in SCRIPTS:
        logging.info(f"Running script: {script.name}")
        run_python_script(script)

    logging.info("All extract-transform scripts completed")


if __name__ == "__main__":
    setup_logging()
    main()
