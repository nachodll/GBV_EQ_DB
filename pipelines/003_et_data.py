"""Run extract-transform steps for the raw datasets."""

import logging
import subprocess
from pathlib import Path

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("scripts") / "extract_transform"
SCRIPTS = [
    ET_SCRIPTS_DIR / "001_et_feminicidios_pareja.py",
    ET_SCRIPTS_DIR / "002_et_feminicidios_no_pareja.py",
    ET_SCRIPTS_DIR / "003_et_menores_victimas_mortales.py",
]

# Logger setup
logger = logging.getLogger(__name__)


def run_script(script_path: Path):
    logger.info(f"Running script: {script_path}")
    try:
        subprocess.run(["python", script_path], text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Script {script_path} failed with return code {e.returncode}")
        print(e.stderr)


def main():
    logger.info("Starting extract-transform scripts...")

    for script in SCRIPTS:
        run_script(script)

    logger.info("All extract-transform scripts completed")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
