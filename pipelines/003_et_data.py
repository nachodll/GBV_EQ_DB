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
    ET_SCRIPTS_DIR / "004_et_servicio_016.py",
    ET_SCRIPTS_DIR / "005_et_usuarias_atenpro.py",
]

# Logger setup
logger = logging.getLogger(__name__)


def run_script(script_path: Path):
    logger.info(f"Running script: {script_path}")

    result = subprocess.run(
        ["python", script_path],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Script {script_path} failed with error: {result.stderr.strip()}")


def main():
    logger.info("Starting extract-transform scripts...")

    for script in SCRIPTS:
        run_script(script)

    logger.info("All extract-transform scripts completed")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
