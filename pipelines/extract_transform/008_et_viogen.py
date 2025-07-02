"""Extract and transform data
Sources:
    DGVG008
Target tables:
    viogen
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG008-090VioGenSistemaSeguimientoIntegral.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "viogen.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Mes": "mes",
                "Provincia": "provincia_id",
                "Nivel de riesgo": "nivel_riesgo",
                "Número de casos": "num_casos",
                "Número de casos con protección policial": "num_casos_proteccion_policial",
            }
        )
        df = df.drop(columns=["Comunidad autónoma"])

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["nivel_riesgo"] = apply_and_check_dict(
            df["nivel_riesgo"],
            {
                "No apreciado": "No apreciado",
                "Bajo": "Bajo",
                "Medio": "Medio",
                "Alto": "Alto",
                "Extremo": "Extremo",
            },
        )
        df["num_casos"] = apply_and_check(df["num_casos"], normalize_positive_integer)
        df["num_casos_proteccion_policial"] = apply_and_check(
            df["num_casos_proteccion_policial"], normalize_positive_integer
        )

        # Save clean CSV
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
