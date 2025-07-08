"""Load all specified data files into
the database tables with matching names.
"""

import logging
import os
from pathlib import Path

# Path to clean CSV data (CSV filenames should match SQL table names and columns)
from typing import Callable, Dict, List, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection

from pipelines.load.load_fuentes import load_fuentes
from pipelines.load.load_poblacion_grupo_edad import load_poblacion_grupo_edad
from utils.logging import setup_logging

# Every table name should match the CSV filename (without extension)
# and the columns should match the SQL table schema.
# In any other case, a custom loader function should be provided.
TABLES_TO_LOAD: Dict[Path, Optional[Callable[[Connection, pd.DataFrame], None]]] = {
    Path("data") / "static" / "comunidades_autonomas.csv": None,
    Path("data") / "static" / "provincias.csv": None,
    Path("data") / "static" / "municipios.csv": None,
    Path("data") / "static" / "nacionalidades.csv": None,
    Path("data") / "static" / "fuentes.csv": load_fuentes,
    Path("data") / "clean" / "feminicidios_pareja_expareja.csv": None,
    Path("data") / "clean" / "feminicidios_fuera_pareja_expareja.csv": None,
    Path("data") / "clean" / "menores_victimas_mortales.csv": None,
    Path("data") / "clean" / "servicio_016.csv": None,
    Path("data") / "clean" / "usuarias_atenpro.csv": None,
    Path("data") / "clean" / "dispositivos_electronicos_seguimiento.csv": None,
    Path("data") / "clean" / "ayudas_articulo_27.csv": None,
    Path("data") / "clean" / "viogen.csv": None,
    Path("data") / "clean" / "autorizaciones_residencia_trabajo_vvg.csv": None,
    Path("data") / "clean" / "denuncias_vg_pareja.csv": None,
    Path("data") / "clean" / "ordenes_proteccion.csv": None,
    Path("data") / "clean" / "renta_activa_insercion.csv": None,
    Path("data") / "clean" / "contratos_bonificados_sustitucion.csv": None,
    Path("data") / "clean" / "ayudas_cambio_residencia.csv": None,
    Path("data") / "clean" / "poblacion_municipios.csv": None,
    Path("data") / "clean" / "poblacion_grupo_edad.csv": load_poblacion_grupo_edad,
}


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
    dataframes = load_csv_files(list(TABLES_TO_LOAD.keys()))

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

        for path, loader in TABLES_TO_LOAD.items():
            table_name = path.stem.lower()
            df = dataframes.get(table_name)
            if df is not None:
                try:
                    if loader is not None:
                        loader(conn, df)
                        logging.info(f"Loaded table with custom loader: {table_name}")
                    else:
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
