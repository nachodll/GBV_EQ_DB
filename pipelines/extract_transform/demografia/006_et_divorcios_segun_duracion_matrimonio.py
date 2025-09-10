"""Extract and transform data
Sources:
    INE008
Target tables:
    divrorcios_segun_duracion_matrimonio
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_plain_text,
    normalize_positive_float,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH_PRE_2010 = Path("data") / "raw" / "INE" / "INE008-DivorciosSegunDuracionMatrimonio" / "2005-2010.csv"
RAW_CSV_PATH_POST_2010 = Path("data") / "raw" / "INE" / "INE008-DivorciosSegunDuracionMatrimonio" / "2010-2023.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "divorcios_segun_duracion_matrimonio.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df_pre_2010 = pd.read_csv(RAW_CSV_PATH_PRE_2010, sep="\t", decimal=",")  # type: ignore
        df_post_2010 = pd.read_csv(RAW_CSV_PATH_POST_2010, sep="\t", decimal=",")  # type: ignore

        # Merge both DataFrames
        df = pd.concat([df_pre_2010, df_post_2010], ignore_index=True)  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Provincias": "provincia_id",
                "Periodo": "anio",
                "Duración del matrimonio": "duracion_matrimonio",
                "Total": "porcentaje_divorcios",
            },
            inplace=True,
        )

        # Remove numbers from province names
        df["provincia_id"] = df["provincia_id"].str.replace(r"\b\d{2}\b", "", regex=True)

        # Drop rows with missing 'porcentaje_divorcios'
        df = df[df["porcentaje_divorcios"] != ".."]

        # Cast to 'porcentaje_divorcios' to float
        df["porcentaje_divorcios"] = (
            df["porcentaje_divorcios"].astype(str).str.replace(",", ".", regex=False).astype(float)
        )

        # Drop rows with aggregated data
        df = df[df["provincia_id"] != "Total Nacional"]

        # Normalize and validate data
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["duracion_matrimonio"] = apply_and_check(df["duracion_matrimonio"], normalize_plain_text)
        df["porcentaje_divorcios"] = apply_and_check(df["porcentaje_divorcios"], normalize_positive_float)

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
