"""Extract and transform data
Sources:
    INE024
Target tables:
    delitos_sexuales
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "INE" / "INE024-DelitosSexuales.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "seguridad_criminalidad" / "delitos_sexuales.csv"


def main():
    try:
        # Read csv file into a DataFrame
        df = pd.read_csv(RAW_CSV_PATH, sep=";", decimal=",")

        # Rename columns
        df = df.rename(
            columns={
                "Periodo": "anio",
                "Sexo": "sexo",
                "Total": "delitos",
                "Delitos: Nivel 2": "nivel_1",
                "Delitos: Nivel 3": "nivel_2",
                "Delitos: Nivel 4": "nivel_3",
            }
        )
        df = df.drop(columns=["Delitos: Nivel 1"], errors="ignore")

        # Drop rows with missing values in 'nivel_1' column (duplicated totals)
        df = df.dropna(subset=["nivel_1"])

        # Drop rows with missing values in 'delitos' column
        df = df.dropna(subset=["delitos"])

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["sexo"] = apply_and_check_dict(
            df["sexo"],
            {"Hombres": "Hombre", "Mujeres": "Mujer", "Total": "Total"},
        )
        df["delitos"] = apply_and_check(df["delitos"], normalize_positive_integer)
        df["nivel_1"] = apply_and_check_dict(
            df["nivel_1"], {"8 Contra la libertad e indemnidad sexuales": "8 Contra la libertad e indemnidad sexuales"}
        )
        df["nivel_2"] = apply_and_check_dict(
            df["nivel_2"],
            {
                "8.1 Agresiones sexuales": "8.1 Agresiones sexuales",
                "8.2 Abusos sexuales": "8.2 Abusos sexuales",
                "8.2 BIS Abusos y agresiones sexuales a menores de 16 años": "8.2 BIS Abusos y agresiones sexuales a menores de 16 años",  # noqa: E501
                "8.3 Acoso sexual": "8.3 Acoso sexual",
                "8.4 Exhibicionismo y provocación sexual": "8.4 Exhibicionismo y provocación sexual",
                "8.5 Prostitución y corrupción menores": "8.5 Prostitución y corrupción menores",
            },
        )
        df["nivel_3"] = apply_and_check_dict(
            df["nivel_3"], {"8.1.1 Agresión sexual": "8.1.1 Agresión sexual", "8.1.2 Violación": "8.1.2 Violación"}
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
