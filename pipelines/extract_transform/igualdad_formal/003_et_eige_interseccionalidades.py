"""Extract and transform data
Sources:
    EIGE003
Target tables:
    eige_interseccionalidades
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_nationality,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "EIGE" / "EIGE003-Intersectionalities.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "igualdad_formal" / "eige_interseccionalidades.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Time": "anio",
                "Geographic region": "pais_id",
                "Value": "valor",
                "Intersectionality": "interseccionalidad",
                "Indicator": "indicador",
                "Sex": "sexo",
            }
        )

        # Change nan for None in valor column
        df["valor"] = df["valor"].fillna(0).astype(int)  # type: ignore

        interseccionalidad_map = {
            v: v
            for v in [
                "Couple with children",
                "Couple without children",
                "With disability",
                "High educated",
                "Low educated",
                "Medium educated",
                "EU-born",
                "Foreign born",
                "Lone parent",
                "Native born",
                "Non-EU-born",
                "Without disability",
                "Single",
                "15/16/18-24",
                "25-34",
                "25-49",
                "35-44",
                "45-64",
                "50-64",
                "65-74",
                "65+",
                "75+",
            ]
        }

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["pais_id"] = apply_and_check(df["pais_id"], normalize_nationality)
        df["valor"] = apply_and_check(df["valor"], normalize_positive_integer)
        df["interseccionalidad"] = apply_and_check_dict(df["interseccionalidad"], interseccionalidad_map)
        df["indicador"] = apply_and_check(df["indicador"], normalize_plain_text)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Men": "Hombre", "Women": "Mujer"})

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
