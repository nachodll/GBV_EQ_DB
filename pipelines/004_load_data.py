import os
import subprocess

# Define load scripts to run
load_scripts_dir = os.path.join("scripts", "load")
SCRIPTS = [
    "001_load_geo.py",
    "002_load_feminicides.py",
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
    script_path = os.path.join(load_scripts_dir, script)
    run_script(script_path)
