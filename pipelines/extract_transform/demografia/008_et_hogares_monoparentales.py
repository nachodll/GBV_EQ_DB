"""Extract and transform data
Sources:
    INE010
Target tables:
    hogares_monoparentales
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
    normalize_plain_text,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE010-HogaresMonoparentales.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "hogares_monoparentales.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep="\t", thousands=".", decimal=",")

        # Rename columns
        df.rename(
            columns={
                "periodo": "anio",
                "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
                "Sexo": "sexo",
                "Edad": "grupo_edad",
                "Estado civil": "estado_civil",
                "Total": "hogares_monoparentales",
            },
            inplace=True,
        )
        df = df.drop(columns=["Total Nacional"], errors="ignore")

        # Drop columns with aggregated data
        df = df[df["comunidad_autonoma_id"].notna()]
        df = df[df["sexo"] != "Ambos sexos"]
        df = df[df["grupo_edad"] != "Total (edad)"]
        df = df[df["estado_civil"] != "Total (estado civil)"]

        # Adapt to expected values
        df["grupo_edad"] = df["grupo_edad"].str.replace("65 años o más", ">65", regex=False)
        df["grupo_edad"] = df["grupo_edad"].str.replace("Menos de 15 años", "<15", regex=False)

        # Replace missing values in 'hogares_monoparentales' with 0 and cast to float
        df["hogares_monoparentales"] = df["hogares_monoparentales"].replace("..", 0)
        df["hogares_monoparentales"] = (
            df["hogares_monoparentales"].astype(str).str.replace(",", ".", regex=False).astype(float)
        )

        # Normalize and validate columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombre": "Hombre", "Mujer": "Mujer"})
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["estado_civil"] = apply_and_check(df["estado_civil"], normalize_plain_text)
        df["hogares_monoparentales"] = apply_and_check(df["hogares_monoparentales"], normalize_positive_float)

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
