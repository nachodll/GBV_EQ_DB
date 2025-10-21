"""Extract and transform data
Sources:
    DGVG014
Target tables:
    ayudas_cambio_residencia
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG014-150AyudasCambioResidencia.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "ayudas_cambio_residencia.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Provincia": "provincia_id",
                "Número de ayudas para cambio de residencia": "ayudas_cambio_residencia",
            }
        )
        df = df.drop(columns=["Comunidad autónoma"])

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["ayudas_cambio_residencia"] = apply_and_check(df["ayudas_cambio_residencia"], normalize_positive_integer)

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
