"""Extract and transform data
Sources:
    INE005, - hombres
    INE006 - mujeres
Target tables:
    matrimonios_homosexuales
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_age_group,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH_HOMBRES = Path("data") / "raw" / "INE" / "INE005-MatrimoniosEntreHombres.csv"
RAW_CSV_PATH_MUJERES = Path("data") / "raw" / "INE" / "INE006-MatrimoniosEntreMujeres.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "matrimonios_homosexuales.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df_hombres = pd.read_csv(RAW_CSV_PATH_HOMBRES, sep="\t", thousands=".")
        df_mujeres = pd.read_csv(RAW_CSV_PATH_MUJERES, sep="\t", thousands=".")

        # Rename columns
        df_hombres.rename(
            columns={
                "Provincia": "provincia_id",
                "Grupos de edad del conyuge 1": "conyuge_1_grupo_edad",
                "Grupos de edad conyuge 2": "conyuge_2_grupo_edad",
                "Periodo": "anio",
                "Total": "matrimonios_hombres",
            },
            inplace=True,
        )
        df_mujeres.rename(
            columns={
                "Provincia": "provincia_id",
                "Grupos de edad del conyuge 1": "conyuge_1_grupo_edad",
                "Grupos de edad conyuge 2": "conyuge_2_grupo_edad",
                "Periodo": "anio",
                "Total": "matrimonios_mujeres",
            },
            inplace=True,
        )

        # Merge both DataFrames on common columns
        df = pd.merge(
            df_hombres,
            df_mujeres,
            on=["provincia_id", "conyuge_1_grupo_edad", "conyuge_2_grupo_edad", "anio"],
            how="outer",
        )

        # Map boolenan value `es_residente_espania` from provincia_id
        df["es_residente_espania"] = df["provincia_id"].apply(lambda x: False if x == "No residente" else True)
        df["provincia_id"] = df["provincia_id"].replace("No residente", None)

        # Replace matrimonios NaN with 0
        df["matrimonios_hombres"] = df["matrimonios_hombres"].fillna(0)
        df["matrimonios_mujeres"] = df["matrimonios_mujeres"].fillna(0)

        # Drop rows with aggregated data
        df = df[df["provincia_id"] != "Total"]
        df = df[df["conyuge_1_grupo_edad"] != "Todas las edades"]
        df = df[df["conyuge_2_grupo_edad"] != "Todas las edades"]

        # Adapt to expected format
        df["conyuge_1_grupo_edad"] = df["conyuge_1_grupo_edad"].replace("Menos de 15 años", "<15")
        df["conyuge_2_grupo_edad"] = df["conyuge_2_grupo_edad"].replace("Menos de 15 años", "<15")

        # Normalize and validate data
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["conyuge_1_grupo_edad"] = apply_and_check(df["conyuge_1_grupo_edad"], normalize_age_group)
        df["conyuge_2_grupo_edad"] = apply_and_check(df["conyuge_2_grupo_edad"], normalize_age_group)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["matrimonios_hombres"] = apply_and_check(df["matrimonios_hombres"], normalize_positive_integer)
        df["matrimonios_mujeres"] = apply_and_check(df["matrimonios_mujeres"], normalize_positive_integer)

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
