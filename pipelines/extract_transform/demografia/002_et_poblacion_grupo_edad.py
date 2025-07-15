"""Extract and transform data
Sources:
    INE002
Target tables:
    poblacion_grupo_edad
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_nationality,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE002-PoblaciónEdadSexo.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "poblacion_grupo_edad.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep="\t")  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Edad (grupos quinquenales)": "grupo_edad",
                "Españoles/Extranjeros": "nacionalidad",
                "Sexo": "sexo",
                "Año": "anio",
                "Total": "poblacion",
            },
            inplace=True,
        )

        # Drop all rows with aggregated data (e.g., "TOTAL")
        num_rows_before = len(df)
        df = df[df["grupo_edad"] != "TOTAL EDADES"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'grupo_edad'.")
        num_rows_before = len(df)
        df = df[df["nacionalidad"] != "TOTAL"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'nacionalidad'.")
        num_rows_before = len(df)
        df = df[df["sexo"] != "Ambos sexos"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'sexo'.")

        # Remove thousands separator dots from poblacion
        df["poblacion"] = df["poblacion"].astype(str).str.replace(".", "", regex=False)

        # Normalize and validate columns
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["nacionalidad"] = apply_and_check(df["nacionalidad"], normalize_nationality)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["poblacion"] = apply_and_check(df["poblacion"], normalize_positive_integer)

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
