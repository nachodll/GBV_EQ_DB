"""Extract and transform data
Sources:
    INE012
Target tables:
    tasa_actividad_paro_empleo
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_positive_float,
    normalize_provincia,
    normalize_quarter,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE012-TasaActividadParoEmpleo.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "economia_laboral" / "tasa_actividad_paro_empleo.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Split periodo into year and quarter
        df[["anio", "trimestre"]] = df["Periodo"].str.split("T", expand=True)
        df = df.drop(columns=["Periodo"])

        # Rename columns
        df = df.rename(
            columns={
                "Sexo": "sexo",
                "Provincias": "provincia_id",
                "Tasas": "tasa",
                "Total": "total",
            }
        )

        # Drop rows with ".." in total column and cast to float
        df = df[df["total"] != ".."]
        df["total"] = df["total"].astype(str).str.replace(",", ".", regex=False).astype(float)

        # Normalize and validate columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["trimestre"] = apply_and_check(df["trimestre"], normalize_quarter)
        df["total"] = apply_and_check(df["total"], normalize_positive_float)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer", "Ambos sexos": "Total"})
        df["tasa"] = apply_and_check_dict(
            df["tasa"],
            {
                "Tasa de actividad": "Tasa de actividad",
                "Tasa de paro de la población": "Tasa de paro",
                "Tasa de empleo de la población": "Tasa de empleo",
            },
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
