"""Extract and transform data
Sources:
    INE020
Target tables:
    infracciones_penales_inputadas_vg
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE020-DenunciasIncoadasTipoInfracción.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "infracciones_penales_inputadas_vg.csv"


def main():
    try:
        # Read raw CSV
        df = pd.read_csv(RAW_CSV_PATH, sep=";", thousands=".")  # type: ignore

        # Rename columns
        df = df.rename(
            columns={
                "Periodo": "anio",
                "Comunidades y ciudades autónomas": "comunidad_autonoma_id",
                "Tipo de infracción": "tipo_infraccion",
                "Total": "infracciones_penales_inputadas",
            }
        )

        # Drop rows with missing values for 'infracciones_penales_inputadas'
        df = df[df["infracciones_penales_inputadas"].notnull()]

        # Drop rows with aggregate data
        df = df[df["comunidad_autonoma_id"] != "Total Nacional"]
        df = df[df["tipo_infraccion"] != "Total Infracciones"]

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["tipo_infraccion"] = apply_and_check(df["tipo_infraccion"], normalize_plain_text)
        df["infracciones_penales_inputadas"] = apply_and_check(
            df["infracciones_penales_inputadas"], normalize_positive_integer
        )

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
