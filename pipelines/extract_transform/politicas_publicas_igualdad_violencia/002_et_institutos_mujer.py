"""Extract and transform data
Sources:
    INMUJERES001
Target tables:
    institutos_mujer
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_year,
)

RAW_XLSX_PATH = Path("data") / "raw" / "INMUJERES" / "INMUJERES001-InstitutosMujer.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "politicas_publicas_igualdad_violencia" / "institutos_mujer.csv"


def main():
    try:
        # Read xlsx file
        df = pd.read_excel(RAW_XLSX_PATH, sheet_name="Institutos")

        # Rename columns
        df = df.rename(
            columns={
                "Región": "comunidad_autonoma_id",
                "Instituto": "nombre",
                "Fecha de Fundación": "anio_fundacion",
                "URL": "enlace",
            }
        )

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["nombre"] = apply_and_check(df["nombre"], normalize_plain_text)
        df["anio_fundacion"] = apply_and_check(df["anio_fundacion"], normalize_year)
        df["enlace"] = apply_and_check(df["enlace"], normalize_plain_text)

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
