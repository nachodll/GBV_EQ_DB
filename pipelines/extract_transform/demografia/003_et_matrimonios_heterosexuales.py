"""Extract and transform data
Sources:
    INE003,
    INE004 - estado civil anterior a partir de 2010
Target tables:
    matrimonios_heterosexuales
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE003-MatrimoniosDiferenteSexo.csv"
RAW_CSV_PATH_2 = Path("data") / "raw" / "INE" / "INE004-MatrimoniosDiferenteSexoEstadoCivilAnterior.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "matrimonios_heterosexuales.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep="\t", thousands=".")  # type: ignore
        df_2 = pd.read_csv(RAW_CSV_PATH_2, sep="\t", thousands=".")  # type: ignore

        # Adapt to expected format
        df_2["Total Nacional"] = df_2["Nacional y Provincias"].apply(  # type: ignore
            lambda x: "No residente" if x == "No residente" else "Total Nacional"  # type: ignore
        )
        df_2["Nacional y Provincias"] = df_2["Nacional y Provincias"].replace(["Total Nacional", "No residente"], None)  # type: ignore
        df_2 = df_2[df_2["Edad de los cónyuges"] != "Todas las edades"]  # type: ignore

        # df contains all total counts, df_2 contains breakdown by 'Estado civil anterior'
        df["Estado civil anterior"] = "Total"
        rows_to_add = df_2[df_2["Estado civil anterior"] != "Total"].copy()

        # Add rows from df_2 to df
        df = pd.concat(
            [
                df,
                rows_to_add.rename(
                    columns={
                        "Nacional y Provincias": "Provincias",
                        "Sexo del conyuge": "Sexo",
                        "Edad de los cónyuges": "Edad",
                    }
                ),
            ],
            ignore_index=True,
        )

        # Rename columns
        df.rename(
            columns={
                "Provincias": "provincia_id",
                "Sexo": "sexo",
                "Edad": "edad",
                "Periodo": "anio",
                "Total": "matrimonios",
                "Total Nacional": "es_residente_espania",
                "Estado civil anterior": "estado_civil_anterior",
            },
            inplace=True,
        )

        # Map values 'es_residente_espania' to boolean
        df["es_residente_espania"] = df["es_residente_espania"].apply(lambda x: x == "Total Nacional")  # type: ignore

        # Drop all rows with aggregated data (e.g., "TOTAL")
        df = df[~(df["provincia_id"].isna() & (df["es_residente_espania"]))]

        # Drop rows with missing values for 'matrimonios'
        df = df[df["matrimonios"].notna()]

        # Adapt to expected values
        df["edad"] = df["edad"].replace({"Menos de 15 años": "<15"})  # type: ignore

        # Normalize and validate columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})
        df["edad"] = apply_and_check(df["edad"], normalize_age_group)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["matrimonios"] = apply_and_check(df["matrimonios"], normalize_positive_integer)
        df["estado_civil_anterior"] = apply_and_check_dict(
            df["estado_civil_anterior"],
            {
                "Total": "Total",
                "Solteros/Solteras": "Solteros/Solteras",
                "Viudos/Viudas": "Viudos/Viudas",
                "Divorciados/Divorciadas": "Divorciados/Divorciadas",
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
