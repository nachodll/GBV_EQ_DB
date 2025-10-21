"""Extract and transform data
Sources:
    SMF001
Target tables
    usuarios_redes_sociales
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "SMF" / "SMF001-UsoRedesSociales" / "SMF001.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "tecnologia_y_medios" / "usuarios_redes_sociales.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", thousands=".")

        # Rename columns
        df.rename(
            columns={
                "ciudad": "ciudad",
                "usuarios": "usuarios",
                "anio": "anio",
                "red_social": "red_social",
            },
            inplace=True,
        )

        # Clean 'ciudad' column
        df["ciudad"] = df["ciudad"].str.replace("\xa0", " ", regex=False)
        df["ciudad"] = df["ciudad"].str.replace("º", "", regex=False).str.strip()
        df["ciudad"] = df["ciudad"].str.title()

        # Normalize and validate columns
        df["ciudad"] = apply_and_check(df["ciudad"], normalize_plain_text)
        df["usuarios"] = apply_and_check(df["usuarios"], normalize_positive_integer)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["red_social"] = apply_and_check(df["red_social"], normalize_plain_text)

        # Save to CSV
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
