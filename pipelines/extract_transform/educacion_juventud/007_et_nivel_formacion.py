"""Extract and transform data
Sources:
    INE023
Target tables:
    nivel_formacion
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_age_group,
    normalize_comunidad_autonoma,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE023-NivelFormación.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "nivel_formacion.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Rename columns
        df = df.rename(
            columns={
                "Grupo de edad": "grupo_edad",
                "Nivel de formación": "nivel_formacion",
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
                "Periodo": "anio",
                "Total": "porcentaje",
            }
        )
        df = df.drop(columns=["Total Nacional"], errors="ignore")

        # Rows with missing values in 'comunidad_autonoma_id' are "Total Nacional"
        df = df.fillna({"comunidad_autonoma_id": "Total Nacional"})

        # Validate and normalize columns
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["nivel_formacion"] = apply_and_check_dict(
            df["nivel_formacion"],
            {
                "Nivel 0-2": "Nivel 0-2",
                "Nivel 3-8": "Nivel 3-8",
                "Nivel 3-4": "Nivel 3-4",
                "Nivel 5-8": "Nivel 5-8",
            },
        )
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["porcentaje"] = apply_and_check(df["porcentaje"], normalize_positive_float)

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
