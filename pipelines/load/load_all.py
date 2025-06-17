import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Define load scripts to run (ordered)
SCRIPTS = [
    "pipelines/load/load_static_geo.py",  # provincias, ccaa
    "pipelines/load/load_feminicidios.py",  # pareja, no pareja
    "pipelines/load/load_servicio_016.py",  # servicio 016
    # Añade más scripts aquí
]


def run_script(script_path: str):
    print(f"\n🔄 Running: {script_path}")
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        print(f"✅ Success: {script_path}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_path}")
        print(e.stderr)


def main():
    print(f"\n🚀 Starting data load orchestration at {datetime.now()}\n")
    for script in SCRIPTS:
        run_script(script)
    print(f"\n✅ All scripts completed at {datetime.now()}\n")


if __name__ == "__main__":
    main()
