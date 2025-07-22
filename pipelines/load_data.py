"""Load all specified data files into
the database tables with matching names.
"""

import logging
import os
import sys
from pathlib import Path

# Path to clean CSV data (CSV filenames should match SQL table names and columns)
from typing import Callable, Dict, List, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection

from pipelines.load.load_eige_dominios import load_eige_dominios
from pipelines.load.load_eige_indicadores import load_eige_indicadores
from pipelines.load.load_eige_interseccionalidades import load_eige_interseccionalidades
from pipelines.load.load_eige_violencia import load_eige_violencia
from pipelines.load.load_fuentes import load_fuentes
from pipelines.load.load_poblacion_grupo_edad import load_poblacion_grupo_edad
from pipelines.load.load_residentes_extranjeros import load_residentes_extranjeros
from utils.logging import setup_logging

CLEAN_DATA_DIR = Path("data") / "clean"

# Every table name should match the CSV filename (without extension)
# and the columns should match the SQL table schema.
# In any other case, a custom loader function should be provided.
# Parent folder should match the schema name.
TABLES_TO_LOAD: Dict[Path, Optional[Callable[[Connection, pd.DataFrame], None]]] = {
    CLEAN_DATA_DIR / "geo" / "comunidades_autonomas.csv": None,
    CLEAN_DATA_DIR / "geo" / "provincias.csv": None,
    CLEAN_DATA_DIR / "geo" / "municipios.csv": None,
    CLEAN_DATA_DIR / "geo" / "paises.csv": None,
    CLEAN_DATA_DIR / "metadata" / "fuentes.csv": load_fuentes,
    CLEAN_DATA_DIR / "violencia_genero" / "feminicidios_pareja_expareja.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "feminicidios_fuera_pareja_expareja.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "menores_victimas_mortales.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "servicio_016.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "usuarias_atenpro.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "dispositivos_electronicos_seguimiento.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "ayudas_articulo_27.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "viogen.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "autorizaciones_residencia_trabajo_vvg.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "denuncias_vg_pareja.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "ordenes_proteccion.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "renta_activa_insercion.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "contratos_bonificados_sustitucion.csv": None,
    CLEAN_DATA_DIR / "violencia_genero" / "ayudas_cambio_residencia.csv": None,
    CLEAN_DATA_DIR / "demografia" / "poblacion_municipios.csv": None,
    CLEAN_DATA_DIR / "demografia" / "poblacion_grupo_edad.csv": load_poblacion_grupo_edad,
    CLEAN_DATA_DIR / "migracion" / "residentes_extranjeros.csv": load_residentes_extranjeros,
    CLEAN_DATA_DIR / "igualdad_formal" / "eige_dominios.csv": load_eige_dominios,
    CLEAN_DATA_DIR / "igualdad_formal" / "eige_indicadores.csv": load_eige_indicadores,
    CLEAN_DATA_DIR / "igualdad_formal" / "eige_interseccionalidades.csv": load_eige_interseccionalidades,
    CLEAN_DATA_DIR / "igualdad_formal" / "eige_violencia.csv": load_eige_violencia,
    CLEAN_DATA_DIR / "educacion_juventud" / "matriculados_educacion_no_universitaria.csv": None,
    CLEAN_DATA_DIR / "tecnologia_y_medios" / "acceso_internet_viviendas.csv": None,
}


def load_csv_files(paths: List[Path]) -> Dict[str, pd.DataFrame]:
    """Load CSV files as DataFrames"""
    dataframes: Dict[str, pd.DataFrame] = {}
    for path in paths:
        try:
            df = pd.read_csv(path, sep=";")  # type: ignore
            schema = path.parent.name.lower()
            table_name = path.stem.lower()
            full_table_name = f"{schema}.{table_name}"
            dataframes[full_table_name] = df
        except Exception as e:
            logging.error(f"Failed to read '{path}': {e}")
    return dataframes


def truncate_tables(conn: Connection, table_names: List[str]):
    """Truncate each table before insert"""
    for table in table_names:
        try:
            conn.execute(text(f"TRUNCATE {table} RESTART IDENTITY CASCADE"))
        except Exception as e:
            logging.error(f"Could not truncate table '{table}': {e}")
    logging.info("Truncated all target tables")


def main(schema_to_load: Optional[str] = None):
    """Main function to load data into the database. If schema_to_load is provided,
    only tables from that schema will be loaded (geo and metadata are always loaded)."""

    # Genereate the list of tables to load per schema
    always_schemas = {"geo", "metadata"}
    schemas_to_load = set(always_schemas)
    if schema_to_load:
        schemas_to_load.add(schema_to_load.lower())
    filtered_tables = {
        path: loader for path, loader in TABLES_TO_LOAD.items() if path.parent.name.lower() in schemas_to_load
    }

    # Read CSV files into DataFrames
    dataframes = load_csv_files(list(filtered_tables.keys()))

    # Create database engine
    engine = create_engine(
        (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST', 'localhost')}/"
            f"{os.getenv('DB_NAME')}"
        ),
    )

    # Insert with full transaction
    with engine.begin() as conn:
        truncate_tables(conn, list(dataframes.keys()))

        for path, loader in filtered_tables.items():
            schema = path.parent.name.lower()
            table_name = path.stem.lower()
            full_table_name = f"{schema}.{table_name}"
            df = dataframes.get(full_table_name)
            if df is not None:
                try:
                    if loader is not None:
                        loader(conn, df)
                        logging.info(f"Loaded table with custom loader: {table_name}")
                    else:
                        df.to_sql(table_name, schema=schema, con=conn, if_exists="append", index=False)
                        logging.info(f"Loaded table: {table_name}")
                except Exception as e:
                    logging.error(f"Failed to load '{table_name}': {e}")
                    logging.warning("Performing rollback for all tables")
                    raise RuntimeError(f"Failed to load table '{table_name}': {e}")
            else:
                logging.error(f"No data for table: {table_name}")
                raise RuntimeError(f"No data found for table '{table_name}'")


if __name__ == "__main__":
    setup_logging()
    schema_arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(schema_arg)
