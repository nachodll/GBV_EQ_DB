"""Run extract-transform steps for the raw datasets."""

import logging
from pathlib import Path
from typing import List

from utils.logging import setup_logging
from utils.run import run_python_script

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("pipelines") / "extract_transform"
SCRIPTS: List[Path] = [
    ET_SCRIPTS_DIR / "DGVG" / "001_et_feminicidios_pareja_expareja.py",
    ET_SCRIPTS_DIR / "DGVG" / "002_et_feminicidios_fuera_pareja_expareja.py",
    ET_SCRIPTS_DIR / "DGVG" / "003_et_menores_victimas_mortales.py",
    ET_SCRIPTS_DIR / "DGVG" / "004_et_servicio_016.py",
    ET_SCRIPTS_DIR / "DGVG" / "005_et_usuarias_atenpro.py",
    ET_SCRIPTS_DIR / "DGVG" / "006_et_dispositivos_electronicos_seguimiento.py",
    ET_SCRIPTS_DIR / "DGVG" / "007_et_ayudas_articulo_27.py",
    ET_SCRIPTS_DIR / "DGVG" / "008_et_viogen.py",
    ET_SCRIPTS_DIR / "DGVG" / "009_et_autorizaciones_residencia_trabajo_vvg.py",
    ET_SCRIPTS_DIR / "DGVG" / "010_et_denuncias_vg_pareja.py",
    ET_SCRIPTS_DIR / "DGVG" / "011_et_ordenes_proteccion.py",
    ET_SCRIPTS_DIR / "DGVG" / "012_et_renta_activa_insercion.py",
    ET_SCRIPTS_DIR / "DGVG" / "013_et_contratos_bonificados_sustitucion.py",
    ET_SCRIPTS_DIR / "DGVG" / "014_et_ayudas_cambio_residencia.py",
    ET_SCRIPTS_DIR / "INE" / "001_poblacion_municipios.py",
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
