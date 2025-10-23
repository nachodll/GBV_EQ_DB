"""Extract and transform data
Sources:
    INE021
Target tables
    tasas_homicidios_criminalidad
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE021-TasaHomicidiosCriminalidad.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "seguridad_criminalidad" / "tasas_homicidios_criminalidad.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Rename columns
        df = df.rename(
            columns={
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
                "Periodo": "anio",
                "Tipo de tasa": "tipo_tasa",
                "Total": "total",
            }
        )
        df = df.drop(columns=["Total Nacional"], errors="ignore")

        # Entries with missing values for comunidad_autonoma are "Total Nacional"
        df = df.fillna({"comunidad_autonoma_id": "Total Nacional"})

        # Normalize and validate columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["tipo_tasa"] = apply_and_check_dict(
            df["tipo_tasa"],
            {"Tasa de homicidios": "Tasa de homicidios", "Tasa de criminalidad": "Tasa de criminalidad"},
        )
        df["total"] = apply_and_check(df["total"], normalize_positive_float)

        # Save the cleaned DataFrame to a CSV file
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
