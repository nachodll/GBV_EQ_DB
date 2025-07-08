"""Load all specified data files into
the database tables with matching names.
"""

import logging
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection

from pipelines.load.load_fuentes import load_fuentes
from utils.logging import setup_logging

# Path to clean CSV data (CSV filenames should match SQL table names and columns)
TABLES_TO_LOAD: List[Path] = [
    Path("data") / "static" / "comunidades_autonomas.csv",
    Path("data") / "static" / "provincias.csv",
    Path("data") / "static" / "municipios.csv",
    Path("data") / "clean" / "feminicidios_pareja_expareja.csv",
    Path("data") / "clean" / "feminicidios_fuera_pareja_expareja.csv",
    Path("data") / "clean" / "menores_victimas_mortales.csv",
    Path("data") / "clean" / "servicio_016.csv",
    Path("data") / "clean" / "usuarias_atenpro.csv",
    Path("data") / "clean" / "dispositivos_electronicos_seguimiento.csv",
    Path("data") / "clean" / "ayudas_articulo_27.csv",
    Path("data") / "clean" / "viogen.csv",
    Path("data") / "clean" / "autorizaciones_residencia_trabajo_vvg.csv",
    Path("data") / "clean" / "denuncias_vg_pareja.csv",
    Path("data") / "clean" / "ordenes_proteccion.csv",
    Path("data") / "clean" / "renta_activa_insercion.csv",
    Path("data") / "clean" / "contratos_bonificados_sustitucion.csv",
    Path("data") / "clean" / "ayudas_cambio_residencia.csv",
    Path("data") / "clean" / "poblacion_municipios.csv",
    Path("data") / "clean" / "poblacion_grupo_edad.csv",
]


def load_csv_files(paths: List[Path]) -> Dict[str, pd.DataFrame]:
    """Load CSV files as DataFrames"""
    dataframes: Dict[str, pd.DataFrame] = {}
    for path in paths:
        try:
            df = pd.read_csv(path, sep=";")  # type: ignore
            table_name = path.stem.lower()
            dataframes[table_name] = df
        except Exception as e:
            logging.error(f"Failed to read '{path}': {e}")
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

        for table_name, df in dataframes.items():
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

        # Load fuentes
        # Special case to let PostgreSQL handle the foreign key constraints
        # It has to be done after all other tables are loaded, since it checks for their existence
        try:
            load_fuentes(conn)
        except Exception as e:
            logging.error(f"Failed to load fuentes: {e}")
            raise RuntimeError(f"Failed to load fuentes: {e}")
        logging.info("Loaded fuentes successfully")


if __name__ == "__main__":
    setup_logging()
    main()
