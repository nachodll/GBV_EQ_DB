"""Extract and transform data
Sources:
    INE027
Target tables:
    tasa_paro_comunidades
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
    normalize_quarter,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE027-TasaParoComunidades.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "economia_laboral" / "tasa_paro_comunidades.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Split periodo into year and quarter
        df[["anio", "trimestre"]] = df["Periodo"].str.split("T", expand=True)
        df = df.drop(columns=["Periodo"])

        # Leave only rows with "Total" in Edad column and drop such column
        df = df[df["Edad"] == "Total"].drop(columns=["Edad"])

        # Drop rows with ".." in tasa_paro column and cast to float
        df = df[df["Total"] != ".."]
        df["Total"] = df["Total"].astype(str).str.replace(",", ".", regex=False).astype(float)

        # Rename columns
        df = df.rename(
            columns={
                "Sexo": "sexo",
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
                "Total": "tasa_paro",
            }
        )

        # Normalize and validate columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["trimestre"] = apply_and_check(df["trimestre"], normalize_quarter)
        df["tasa_paro"] = apply_and_check(df["tasa_paro"], normalize_positive_float)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer", "Ambos sexos": "Total"})

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
