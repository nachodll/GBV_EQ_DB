"""Run extract-transform steps for the raw datasets."""

import logging
from pathlib import Path

from utils.logging import setup_logging
from utils.run import run_python_script

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("pipelines") / "extract_transform"
SCRIPTS = [
    ET_SCRIPTS_DIR / "001_et_feminicidios_pareja_expareja.py",
    ET_SCRIPTS_DIR / "002_et_feminicidios_fuera_pareja_expareja.py",
    ET_SCRIPTS_DIR / "003_et_menores_victimas_mortales.py",
    ET_SCRIPTS_DIR / "004_et_servicio_016.py",
    ET_SCRIPTS_DIR / "005_et_usuarias_atenpro.py",
    ET_SCRIPTS_DIR / "006_et_dispositivos_electronicos_seguimiento.py",
    ET_SCRIPTS_DIR / "007_et_ayudas_articulo_27.py",
    ET_SCRIPTS_DIR / "008_et_viogen.py",
    ET_SCRIPTS_DIR / "009_et_autorizaciones_residencia_trabajo_vvg.py",
    ET_SCRIPTS_DIR / "010_et_denuncias_vg_pareja.py",
    ET_SCRIPTS_DIR / "011_et_ordenes_proteccion.py",
    ET_SCRIPTS_DIR / "012_et_renta_activa_insercion.py",
    ET_SCRIPTS_DIR / "013_et_contratos_bonificados_sustitucion.py",
    ET_SCRIPTS_DIR / "014_et_ayudas_cambio_residencia.py",
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
