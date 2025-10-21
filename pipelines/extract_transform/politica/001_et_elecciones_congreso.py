"""Extract and transform data
Sources:
    MININTERIOR001
Target tables:
    elecciones_congreso
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_month,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSVS_DIR = Path("data") / "raw" / "MININTERIOR" / "MININTERIOR001-CongresoDiputados"
CLEAN_CSV_PATH = Path("data") / "clean" / "politica" / "elecciones_congreso.csv"


def main():
    try:
        # Read all CSV files and concatenate them into a single dataframe
        all_files = list(RAW_CSVS_DIR.glob("*.csv"))
        if not all_files:
            raise FileNotFoundError(f"No CSV files found in directory: {RAW_CSVS_DIR}")
        df = pd.concat((pd.read_csv(f, sep=";", decimal=",", thousands=".") for f in all_files), ignore_index=True)

        # Drop unnused columns
        df["anio"] = df["Id convocatoria"].astype(str).str.slice(0, 4).astype(int)
        df["mes"] = df["Id convocatoria"].astype(str).str.slice(4, 6).astype(int)
        df = df.drop(
            columns=[
                "Id convocatoria",
                "Tipo convocatoria",
                "ccaa",
                "prv",
                "circunscripcion",
                "municipio",
                "distrito",
                "votos validos",
                "votos censo",
                "votos candidaturas",
                "tipo de representante",
            ]
        )

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
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
