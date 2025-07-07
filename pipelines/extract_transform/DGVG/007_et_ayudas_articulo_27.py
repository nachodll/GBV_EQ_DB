"""Extract and transform data
Sources:
    DGVG007
Target tables:
    ayudas_articulo_27
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG007-070AyudasArtículo27.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "ayudas_articulo_27.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Comunidad autónoma": "comunidad_autonoma_id",
                "Número de ayudas concedidas Art 27": "num_ayudas_concedidas",
            }
        )

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["num_ayudas_concedidas"] = apply_and_check(df["num_ayudas_concedidas"], normalize_positive_integer)

        # Save clean data
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Clean data saved to {CLEAN_CSV_PATH}")

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
