"""Load all specified data files into
the database tables with matching names.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection

from utils.logging import setup_logging

# Path to clean CSV data
# Name of the CSV files should match the table names
# Name of the CSV columns should match the table columns
# Ordered list of CSV files to load (without .csv extension)
TABLES_TO_LOAD: List[Dict[str, Any]] = [
    {"name": "comunidades_autonomas", "path": Path("data") / "static" / "comunidadesAutónomas.csv"},
    {"name": "provincias", "path": Path("data") / "static" / "provincias.csv"},
    {"name": "municipios", "path": Path("data") / "static" / "municipios.csv"},
    {"name": "feminicidios_pareja_expareja", "path": Path("data") / "clean" / "feminicidios_pareja_expareja.csv"},
    {
        "name": "feminicidios_fuera_pareja_expareja",
        "path": Path("data") / "clean" / "feminicidios_fuera_pareja_expareja.csv",
    },
    {"name": "menores_victimas_mortales", "path": Path("data") / "clean" / "menores_victimas_mortales.csv"},
    {"name": "servicio_016", "path": Path("data") / "clean" / "servicio_016.csv"},
    {"name": "usuarias_atenpro", "path": Path("data") / "clean" / "usuarias_atenpro.csv"},
    {
        "name": "dispositivos_electronicos_seguimiento",
        "path": Path("data") / "clean" / "dispositivos_electronicos_seguimiento.csv",
    },
    {"name": "ayudas_articulo_27", "path": Path("data") / "clean" / "ayudas_articulo_27.csv"},
    {"name": "viogen", "path": Path("data") / "clean" / "viogen.csv"},
    {
        "name": "autorizaciones_residencia_trabajo_vvg",
        "path": Path("data") / "clean" / "autorizaciones_residencia_trabajo_vvg.csv",
    },
    {"name": "denuncias_vg_pareja", "path": Path("data") / "clean" / "denuncias_vg_pareja.csv"},
    {"name": "ordenes_proteccion", "path": Path("data") / "clean" / "ordenes_proteccion.csv"},
    {"name": "renta_activa_insercion", "path": Path("data") / "clean" / "renta_activa_insercion.csv"},
    {
        "name": "contratos_bonificados_sustitucion",
        "path": Path("data") / "clean" / "contratos_bonificados_sustitucion.csv",
    },
    {"name": "ayudas_cambio_residencia", "path": Path("data") / "clean" / "ayudas_cambio_residencia.csv"},
    {"name": "poblacion_municipios", "path": Path("data") / "clean" / "poblacion_municipios.csv"},
]


def load_csv_files(tables: List[Dict[str, Any]]) -> Dict[str, pd.DataFrame]:
    """Load CSV files as DataFrames"""
    dataframes: Dict[str, pd.DataFrame] = {}
    for entry in tables:
        try:
            df = pd.read_csv(entry["path"], sep=";")  # type: ignore
            dataframes[entry["name"]] = df
        except Exception as e:
            logging.error(f"Failed to read '{entry['path']}': {e}")
    return dataframes


def truncate_tables(conn: Connection, table_names: List[str]):
    """Truncate each table before insert"""
    for table in table_names:
        try:
            conn.execute(text(f"TRUNCATE {table} RESTART IDENTITY CASCADE"))
            logging.info(f"Truncated table: {table}")
        except Exception as e:
            logging.error(f"Could not truncate table '{table}': {e}")


def main():
    dataframes = load_csv_files(TABLES_TO_LOAD)

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

        for table_entry in TABLES_TO_LOAD:
            table_name = table_entry["name"]
            df = dataframes.get(table_name)
            if df is not None:
                try:
                    df.to_sql(table_name, con=conn, if_exists="append", index=False)
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
    main()
