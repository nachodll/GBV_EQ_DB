"""Extract and transform data
Sources:
    INE009
Target tables:
    nulidades_separaciones_divorcios
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE009-NulidadesSeparacionesDivorcios.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "nulidades_separaciones_divorcios.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep="\t", thousands=".")  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Tipo de disolución matrimonial": "tipo_disolucion",
                "Periodo": "anio",
                "Provincias": "provincia_id",
                "Total": "disoluciones_matrimoniales",
            },
            inplace=True,
        )

        # Drop rows with missing 'disoluciones_matrimoniales'
        df = df[df["disoluciones_matrimoniales"] != ".."]

        # Cast to 'disoluciones_matrimoniales' to integer
        df["disoluciones_matrimoniales"] = (
            df["disoluciones_matrimoniales"].astype(str).str.replace(".", "", regex=False).astype(int)
        )

        # Drop rows with aggregated data
        df = df[df["provincia_id"] != "Total Nacional"]
        df = df[df["tipo_disolucion"] != "Total"]

        # Normalize and validate data
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["tipo_disolucion"] = apply_and_check(df["tipo_disolucion"], normalize_plain_text)
        df["disoluciones_matrimoniales"] = apply_and_check(df["disoluciones_matrimoniales"], normalize_positive_integer)

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
