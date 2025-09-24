"""Extract and transform data
Sources:
    MONCLOA001
Target tables:
    presidentes_espania
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_date,
    normalize_plain_text,
)

RAW_XLSX_PATH = Path("data") / "raw" / "MONCLOA" / "MONCLOA001-PresidentesEspaña.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "politica" / "presidentes_espania.csv"


def main():
    try:
        # Read xlsx file
        df = pd.read_excel(RAW_XLSX_PATH, sheet_name="Hoja1", nrows=22)  # type: ignore

        # Rename columns
        df = df.rename(
            columns={
                "Legislatura": "legislatura",
                "Presidente": "presidente",
                "Nombramiento": "nombramiento",
                "Cese": "cese",
                "Partidos en el gobierno": "partidos_gobierno",
                "Tipo de mayoría": "tipo_mayoria",
            }
        )
        df = df.drop(columns=["Observaciones"])

        # Validate and normalize columns
        df["legislatura"] = apply_and_check(df["legislatura"], normalize_plain_text)
        df["presidente"] = apply_and_check(df["presidente"], normalize_plain_text)
        df["nombramiento"] = apply_and_check(df["nombramiento"], normalize_date)
        df["cese"] = apply_and_check(df["cese"], normalize_date)
        df["partidos_gobierno"] = apply_and_check(df["partidos_gobierno"], normalize_plain_text)
        df["tipo_mayoria"] = apply_and_check_dict(
            df["tipo_mayoria"],
            {
                "Mayoría simple": "Simple",
                "Mayoría absoluta": "Absoluta",
                "En funciones": "En funciones",
                "Minoría": "Minoría",
            },
        )

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
