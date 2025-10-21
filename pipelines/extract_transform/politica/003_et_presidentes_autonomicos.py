"""Extract and transform data
Sources:
    SENADOA001
Target tables:
    presidentes_autonomicos
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_plain_text,
)

RAW_CSV_PATH = Path("data") / "raw" / "SENADO" / "SENADO001-PresidentesAutonómicos.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "politica" / "presidentes_autonomicos.csv"


def main():
    try:
        # Read csv file
        df = pd.read_csv(RAW_CSV_PATH, sep=";")

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["legislatura"] = apply_and_check(df["legislatura"], normalize_plain_text)
        df["presidente"] = apply_and_check(df["presidente"], normalize_plain_text)
        df["nombramiento"] = apply_and_check(df["nombramiento"], normalize_date)
        df["partido"] = apply_and_check(df["partido"], normalize_plain_text)

        # Save to clean CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data successfully transformed and saved to {CLEAN_CSV_PATH}")

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
