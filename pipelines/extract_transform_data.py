"""Run extract-transform steps for the raw datasets."""

import logging
import sys
from pathlib import Path
from typing import List, Optional

from utils.logging import setup_logging
from utils.run_script import run_python_script

# Define extract transform scripts to run
ET_SCRIPTS_DIR = Path("pipelines") / "extract_transform"
SCRIPTS: List[Path] = [
    ET_SCRIPTS_DIR / "violencia_genero" / "001_et_feminicidios_pareja_expareja.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "002_et_feminicidios_fuera_pareja_expareja.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "003_et_menores_victimas_mortales.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "004_et_servicio_016.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "005_et_usuarias_atenpro.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "006_et_dispositivos_electronicos_seguimiento.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "007_et_ayudas_articulo_27.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "008_et_viogen.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "009_et_autorizaciones_residencia_trabajo_vvg.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "010_et_denuncias_vg_pareja.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "011_et_ordenes_proteccion.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "012_et_renta_activa_insercion.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "013_et_contratos_bonificados_sustitucion.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "014_et_ayudas_cambio_residencia.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "015_et_denuncias_vg_presentadas.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "016_et_infracciones_penales_inputadas_vg.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "017_et_encuesta_europea_2022.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "018_et_macroencuesta_2019.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "019_et_macroencuesta_2015.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "020_et_macroencuesta_2011.py",
    ET_SCRIPTS_DIR / "violencia_genero" / "021_et_fusion_encuestas.py",
    ET_SCRIPTS_DIR / "demografia" / "001_et_poblacion_municipios.py",
    ET_SCRIPTS_DIR / "demografia" / "002_et_poblacion_grupo_edad.py",
    ET_SCRIPTS_DIR / "demografia" / "003_et_matrimonios_heterosexuales.py",
    ET_SCRIPTS_DIR / "demografia" / "004_et_matrimonios_homosexuales.py",
    ET_SCRIPTS_DIR / "demografia" / "005_et_tasa_divorcialidad.py",
    ET_SCRIPTS_DIR / "demografia" / "006_et_divorcios_segun_duracion_matrimonio.py",
    ET_SCRIPTS_DIR / "demografia" / "007_et_nulidades_separaciones_divorcios.py",
    ET_SCRIPTS_DIR / "demografia" / "008_et_hogares_monoparentales.py",
    ET_SCRIPTS_DIR / "demografia" / "009_et_tasa_bruta_natalidad.py",
    ET_SCRIPTS_DIR / "demografia" / "010_et_uso_tiempo.py",
    ET_SCRIPTS_DIR / "migracion" / "001_et_residentes_extranjeros.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "001_et_eige_dominios.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "002_et_eige_indicadores.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "003_et_eige_interseccionalidades.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "004_et_eige_violencia.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "005_et_ganancia_por_hora_trabajo.py",
    ET_SCRIPTS_DIR / "igualdad_formal" / "006_et_mujeres_cargos_autonomicos.py",
    ET_SCRIPTS_DIR / "educacion_juventud" / "001_et_matriculados_educacion_no_universitaria.py",
    ET_SCRIPTS_DIR / "educacion_juventud" / "002_et_matriculados_universidad.py",
    ET_SCRIPTS_DIR / "educacion_juventud" / "003_et_egresados_universidad.py",
    ET_SCRIPTS_DIR / "tecnologia_y_medios" / "001_et_acceso_internet_viviendas.py",
    ET_SCRIPTS_DIR / "tecnologia_y_medios" / "002_et_uso_internet_personas.py",
    ET_SCRIPTS_DIR / "tecnologia_y_medios" / "003_et_uso_internet_ninios.py",
    ET_SCRIPTS_DIR / "tecnologia_y_medios" / "004_et_usuarios_redes_sociales.py",
    ET_SCRIPTS_DIR / "salud" / "001_et_ive_total.py",
    ET_SCRIPTS_DIR / "salud" / "002_et_ive_grupo_edad.py",
    ET_SCRIPTS_DIR / "salud" / "003_et_ive_ccaa.py",
    ET_SCRIPTS_DIR / "politica" / "001_et_elecciones_congreso.py",
    ET_SCRIPTS_DIR / "politica" / "002_et_presidentes_espania.py",
    ET_SCRIPTS_DIR / "politica" / "003_et_presidentes_autonomicos.py",
    ET_SCRIPTS_DIR / "politica" / "004_et_elecciones_parlamentos_autonomicos.py",
    ET_SCRIPTS_DIR / "politicas_publicas_igualdad_violencia" / "001_et_legislacion.py",
    ET_SCRIPTS_DIR / "politicas_publicas_igualdad_violencia" / "002_et_institutos_mujer.py",
]


def main(schema_to_et: Optional[str] = None):
    """Main function to run extract-transform scripts. If schema_to_et is provided,
    only scripts for that schema will be run. If no schema is provided, all scripts will
    be run."""

    logging.info("Starting extract-transform scripts...")

    if schema_to_et:
        schema_to_et = schema_to_et.lower()
        filtered_scripts = [script for script in SCRIPTS if script.parent.name.lower() == schema_to_et]
    else:
        filtered_scripts = SCRIPTS

    for script in filtered_scripts:
        logging.info(f"Running script: {script.name}")
        run_python_script(script)

    logging.info("All extract-transform scripts completed")


if __name__ == "__main__":
    setup_logging()
    schema_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(schema_arg)
