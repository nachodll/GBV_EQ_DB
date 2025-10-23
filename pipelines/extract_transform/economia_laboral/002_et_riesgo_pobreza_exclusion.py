"""Extract and transform data
Sources:
    INE022
Target tables:
    riesgo_pobreza_exclusion
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

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE022-RiesgoPobrezaExclusiónSocial.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "economia_laboral" / "riesgo_pobreza_exclusion.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Rename columns
        df = df.rename(
            columns={
                "Periodo": "anio",
                "Tasa de riesgo de pobreza o exclusión social (estrategia Europa 2020) (y sus componentes)": "indicador",  # noqa: E501
                "Total": "porcentaje",
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
            }
        )

        # Normalize and validate columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["porcentaje"] = apply_and_check(df["porcentaje"], normalize_positive_float)
        df["indicador"] = apply_and_check_dict(
            df["indicador"],
            {
                "Tasa de riesgo de pobreza o exclusión social (indicador AROPE)": "Tasa de riesgo de pobreza o exclusión social (indicador AROPE)",  # noqa: E501
                "En riesgo de pobreza (renta año anterior a la entrevista)": "En riesgo de pobreza (renta año anterior a la entrevista)",  # noqa: E501
                "Con carencia material severa": "Con carencia material severa",
                "Viviendo en hogares con baja intensidad en el trabajo (de 0 a 59 años)": "Viviendo en hogares con baja intensidad en el trabajo (de 0 a 59 años)",  # noqa: E501
            },
        )

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
