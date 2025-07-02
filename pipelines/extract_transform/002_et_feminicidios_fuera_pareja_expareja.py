"""Extract and transform data
Sources:
    DGVG002
Target tables:
    feminicios_no_pareja
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_positive_integer,
    normalize_year,
)

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG002-020FeminicidiosFueraParejaExpareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_fuera_pareja_expareja.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Comunidad autónoma (As)": "comunidad_autonoma_id",
                "Año": "anio",
                "Tipo de feminicidio": "tipo_feminicidio",
                "Feminicidos fuera pareja o expareja": "num_feminicidios",
            }
        )

        tipo_feminicidio_mapping = {
            "F. vicario -1-": "Vicario",
            "F. familiar": "Familiar",
            "F. sexual": "Sexual",
            "F. social": "Social",
        }

        # Normalize and validate all columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["num_feminicidios"] = apply_and_check(df["num_feminicidios"], normalize_positive_integer)
        df["tipo_feminicidio"] = apply_and_check_dict(df["tipo_feminicidio"], tipo_feminicidio_mapping)

        # Save cleaned CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")

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
