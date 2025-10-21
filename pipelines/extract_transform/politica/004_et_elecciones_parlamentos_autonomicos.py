"""Extract and transform data
Sources:
    JEC001
Target tables:
    elecciones_parlamentos_autonomicos
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
    normalize_positive_integer,
)

RAW_CSV_PATH = Path("data") / "raw" / "JEC" / "JEC001-ParlamentosAutonomicos.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "politica" / "elecciones_parlamentos_autonomicos.csv"


def main():
    try:
        # Read csv file
        df = pd.read_csv(RAW_CSV_PATH, sep=";", keep_default_na=False, na_values=[])

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["fecha"] = apply_and_check(df["fecha"], normalize_date)
        df["candidatura"] = apply_and_check(df["candidatura"], normalize_plain_text)
        df["votos"] = apply_and_check(df["votos"], normalize_positive_integer)
        df["representantes"] = apply_and_check(df["representantes"], normalize_positive_integer)

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
