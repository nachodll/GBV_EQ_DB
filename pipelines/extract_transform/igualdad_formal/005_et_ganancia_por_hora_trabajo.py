"""Extract and transform data
Sources:
    INE013, - 2008-2023
    INE014 - 2004-2007
Target tables:
    ganancia_por_hora_trabajo
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH_POST_2007 = Path("data") / "raw" / "INE" / "INE013-GananciaHoraTrabajo.csv"
RAW_CSV_PATH_PRE_2007 = Path("data") / "raw" / "INE" / "INE014-GananciaHoraTrabajoPre2007.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "igualdad_formal" / "ganancia_por_hora_trabajo.csv"


def load_pre_2007_data() -> pd.DataFrame:
    # Read dsv file
    df = pd.read_csv(RAW_CSV_PATH_PRE_2007, sep=";")

    # Rename columns
    df = df.rename(
        columns={
            "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
            "Sectores de actividad": "sector_actividad",
            "Sexo": "sexo",
            "periodo": "anio",
            "Total": "ganancia_por_hora_trabajo",
        }
    )
    df = df.drop(columns=["Total Nacional"], errors="ignore")

    # Null values in 'comunidad_autonoma_id' are 'Total nacional'
    df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].fillna("Total Nacional")

    # Adapt to expected values in 'sector_actividad' column
    df["sector_actividad"] = df["sector_actividad"].replace({"Todos los sectores de actividad": "Todos los sectores"})

    return df


def load_post_2007_data() -> pd.DataFrame:
    # Read csv file
    df = pd.read_csv(RAW_CSV_PATH_POST_2007, sep=";")

    # Rename columns
    df = df.rename(
        columns={
            "Comunidades autónomas": "comunidad_autonoma_id",
            "Sectores de actividad": "sector_actividad",
            "Sexo": "sexo",
            "Periodo": "anio",
            "Total": "ganancia_por_hora_trabajo",
        }
    )

    return df


def main():
    try:
        # Load both files into dataframes and merge them
        df_pre_2007 = load_pre_2007_data()
        df_post_2007 = load_post_2007_data()
        df = pd.concat([df_pre_2007, df_post_2007], ignore_index=True)

        # Drop rows with missing values (..) in 'ganancia_por_hora_trabajo' column
        df = df[df["ganancia_por_hora_trabajo"] != ".."]

        # Strip leading -  and change decimal separator from  'ganancia_por_hora_trabajo' column
        df["ganancia_por_hora_trabajo"] = df["ganancia_por_hora_trabajo"].str.lstrip("-")
        df["ganancia_por_hora_trabajo"] = df["ganancia_por_hora_trabajo"].str.replace(",", ".")

        # Normalize and validate all columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["sector_actividad"] = apply_and_check(df["sector_actividad"], normalize_plain_text)
        df["sexo"] = apply_and_check_dict(
            df["sexo"],
            {
                "Hombres": "Hombre",
                "Varones": "Hombre",
                "Mujeres": "Mujer",
                "Ambos sexos": "Total",
            },
        )
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["ganancia_por_hora_trabajo"] = apply_and_check(df["ganancia_por_hora_trabajo"], normalize_positive_float)

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
