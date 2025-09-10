"""Extract and transform data
Sources:
    INE007
Target tables:
    tasa_divorcialidad
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_positive_float,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH_PRE_2010 = Path("data") / "raw" / "INE" / "INE007-TasaDivorcialidad" / "2005-2010.csv"
RAWCSV_PATH_POST_2010 = Path("data") / "raw" / "INE" / "INE007-TasaDivorcialidad" / "2010-2023.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "tasa_divorcialidad.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df_pre_2010 = pd.read_csv(RAW_CSV_PATH_PRE_2010, sep="\t", decimal=",")  # type: ignore
        df_post_2010 = pd.read_csv(RAWCSV_PATH_POST_2010, sep="\t", decimal=",")  # type: ignore

        # Merge both DataFrames
        df = pd.concat([df_pre_2010, df_post_2010], ignore_index=True)  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Provincias": "provincia_id",
                "Grupo de edad": "grupo_edad",
                "Sexo": "sexo",
                "Periodo": "anio",
                "Total": "tasa_divorcialidad",
            },
            inplace=True,
        )

        # Remove numbers from province names
        df["provincia_id"] = df["provincia_id"].str.replace(r"\b\d{2}\b", "", regex=True)

        # Adapt to expected format
        df["grupo_edad"] = df["grupo_edad"].replace("19 y menos años", "<19")  # type: ignore
        df["grupo_edad"] = df["grupo_edad"].replace("18 y menos años", "<18")  # type: ignore

        # Drop rows with missing 'tasa_divorcialidad'
        df = df[df["tasa_divorcialidad"] != ".."]

        # Cast to 'tasa_divorcialidad' to float
        df["tasa_divorcialidad"] = df["tasa_divorcialidad"].astype(str).str.replace(",", ".", regex=False).astype(float)  # type: ignore

        # Drop rows with aggregated data
        df = df[df["sexo"] != "Ambos sexos"]
        df = df[df["provincia_id"] != "Total Nacional"]

        # Normalize and validate data
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["tasa_divorcialidad"] = apply_and_check(df["tasa_divorcialidad"], normalize_positive_float)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})

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
