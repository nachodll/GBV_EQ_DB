"""Extract and transform data
Sources:
    DGVG011
Target tables:
    ordenes_proteccion
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_positive_integer,
    normalize_provincia,
    normalize_quarter,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG011-120ÓrdenesProtección.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "ordenes_proteccion.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Trimestre": "trimestre",
                "Provincia": "provincia_id",
                "Incoadas-Resueltas": "estado_proceso",
                "Instancia": "instancia",
                "Número de órdenes de protección": "ordenes_proteccion",
            }
        )
        estado_orden_proteccion_mapping = {
            "Incoadas": "Incoadas",
            "Resueltas. Adoptadas": "Adoptadas",
            "Resueltas. Denegadas": "Denegadas",
            "Pendientes final trimestre": "Pendientes",
            "Resueltas. Inadmitidas": "Inadmitidas",
        }
        instancia_mapping = {
            "A instancia de la víctima": "A instancia de la víctima",
            "A instancia de otras personas": "A instancia de otras personas",
            "A instancia del Minist. Fiscal": "A instancia del Minist. Fiscal",
            "De oficio": "De oficio",
            "A instancia de la Administración": "A instancia de la Administración",
        }

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["trimestre"] = apply_and_check(df["trimestre"], normalize_quarter)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["ordenes_proteccion"] = apply_and_check(df["ordenes_proteccion"], normalize_positive_integer)
        df["estado_proceso"] = apply_and_check_dict(df["estado_proceso"], estado_orden_proteccion_mapping)
        df["instancia"] = apply_and_check_dict(df["instancia"], instancia_mapping)

        # Save to CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Cleaned data saved to {CLEAN_CSV_PATH}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Could not parse: {e}")
        raise
    except ValueError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(f"Unexpected error processing: {e}")
        raise


if __name__ == "__main__":
    setup_logging()
    main()
