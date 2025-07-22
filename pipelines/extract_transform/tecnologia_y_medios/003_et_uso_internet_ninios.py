"""Extract and transform data
Sources:
    INE017
Target tables
    uso_internet_ninios
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE017-UsoInternetNiños.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "tecnologia_y_medios" / "uso_internet_ninios.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep="\t", decimal=",")  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Periodo": "anio",
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
                "Tipo de uso de TIC": "tipo_uso",
                "Total": "porcentaje",
            },
            inplace=True,
        )

        # Normalize and validate columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["tipo_uso"] = apply_and_check(df["tipo_uso"], normalize_plain_text)
        df["porcentaje"] = apply_and_check(df["porcentaje"], normalize_positive_float)

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
