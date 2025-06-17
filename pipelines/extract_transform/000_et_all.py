import os
import subprocess

# Define extract transform scripts to run
et_scripts_dir = os.path.join("pipelines", "extract_transform")
SCRIPTS = [
    "001_et_feminicidios_pareja.py",
    "002_et_feminicidios_no_pareja.py",
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
    script_path = os.path.join(et_scripts_dir, script)
    run_script(script_path)
