"""Extract and transform data
Sources:
    MINSANIDAD001
Target tables
    ive_total
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_positive_float,
    normalize_positive_integer,
    normalize_year,
)

RAW_XLSX_PATH = Path("data") / "raw" / "MINSANIDAD" / "MINSANIDAD001-InterrupcionesVoluntariasEmbarazo.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "salud" / "ive_total.csv"


def main():
    try:
        # Read xlsx file into a DataFrame
        df = pd.read_excel(RAW_XLSX_PATH, sheet_name="Tabla 1", header=1)

        # Rename columns
        df.rename(
            columns={
                "Año": "anio",
                "Centros notificadores de I.V.E.": "centros_notificadores",
                "Total I.V.E.": "ives",
                "Tasa por 1.000 mujeres": "tasa",
            },
            inplace=True,
        )

        # Normalize and validate columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["centros_notificadores"] = apply_and_check(df["centros_notificadores"], normalize_positive_integer)
        df["ives"] = apply_and_check(df["ives"], normalize_positive_integer)
        df["tasa"] = apply_and_check(df["tasa"], normalize_positive_float)

        # Save to csv
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data saved to {CLEAN_CSV_PATH}")

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
