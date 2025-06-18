import subprocess
from pathlib import Path

# Define load scripts to run
LOAD_SCRIPTS_DIR = Path("scripts") / "load"
SCRIPTS = [
    LOAD_SCRIPTS_DIR / "001_load_geo.py",
    LOAD_SCRIPTS_DIR / "002_load_feminicides.py",
]


def run_script(script_path):
    print(f"🔄 Running: {script_path}")
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_path}")
        print(e.stderr)


def main():
    for script in SCRIPTS:
        run_script(script)


if __name__ == "__main__":
    main()
