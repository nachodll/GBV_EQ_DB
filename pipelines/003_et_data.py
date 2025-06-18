import subprocess
from pathlib import Path

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("scripts") / "extract_transform"
SCRIPTS = [
    ET_SCRIPTS_DIR / "001_et_feminicidios_pareja.py",
    ET_SCRIPTS_DIR / "002_et_feminicidios_no_pareja.py",
]


def run_script(script_path):
    print(f"🔄 Running: {script_path}")
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_path}")
        print(e.stderr)


for script in SCRIPTS:
    run_script(script)
