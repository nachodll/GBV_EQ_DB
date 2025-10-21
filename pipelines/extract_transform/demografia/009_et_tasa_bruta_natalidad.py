"""Extract and transform data
Sources:
    INE011
Target tables:
    tasa_bruta_natalidad
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

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE011-TasaNatalidad.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "tasa_bruta_natalidad.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", thousands=".", decimal=",")

        # Rename columns
        df.rename(
            columns={
                "Periodo": "anio",
                "Provincias": "provincia_id",
                "Total": "tasa_bruta_natalidad",
            },
            inplace=True,
        )

        # Drop columns with aggregated data
        df = df[df["provincia_id"] != "Total Nacional"]

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["tasa_bruta_natalidad"] = apply_and_check(df["tasa_bruta_natalidad"], normalize_positive_float)

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
