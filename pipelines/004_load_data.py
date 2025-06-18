import logging
import subprocess
from pathlib import Path

# Define load scripts to run
LOAD_SCRIPTS_DIR = Path("scripts") / "load"
SCRIPTS = [
    LOAD_SCRIPTS_DIR / "001_load_geo.py",
    LOAD_SCRIPTS_DIR / "002_load_feminicides.py",
]


# Logger setup
logger = logging.getLogger(__name__)


def run_script(script_path):
    logger.info(f"Running script: {script_path}")
    try:
        subprocess.run(["python", script_path], text=True, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Script {script_path} failed with return code {e.returncode}")
        print(e.stderr)


def main():
    logger.info("Starting load scripts...")

    for script in SCRIPTS:
        run_script(script)

    logger.info("All load scripts completed")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
