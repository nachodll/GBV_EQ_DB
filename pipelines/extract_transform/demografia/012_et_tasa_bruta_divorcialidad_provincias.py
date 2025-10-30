"""Extract and transform data
Sources:
    INE026
Target tables:
    tasa_bruta_divorcialidad_provincias
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_positive_float,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE026-TasaBrutaDivorcialidadProvincias.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "tasa_bruta_divorcialidad_provincias.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Rename columns
        df.rename(
            columns={
                "Provincias": "provincia_id",
                "Periodo": "anio",
                "Total": "tasa_bruta_divorcialidad",
            },
            inplace=True,
        )

        # Drop rows with missing 'tasa_bruta_divorcialidad' and cast to float
        df = df[df["tasa_bruta_divorcialidad"] != ".."]
        df["tasa_bruta_divorcialidad"] = df["tasa_bruta_divorcialidad"].str.replace(",", ".").astype(float)

        # Validate and normalize columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["tasa_bruta_divorcialidad"] = apply_and_check(df["tasa_bruta_divorcialidad"], normalize_positive_float)

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
