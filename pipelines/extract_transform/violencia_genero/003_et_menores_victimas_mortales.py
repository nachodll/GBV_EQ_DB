"""Extract and transform data
Sources:
    DGVG003
Target tables:
    menores_victimas_mortales"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG003-030MenoresVictimasMortales.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "menores_victimas_mortales.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(str(RAW_CSV_PATH))  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Provincia (As)": "provincia_id",
                "Año": "anio",
                "Mes": "mes",
                "VM Vicaria -1-": "es_victima_vicaria",
                "AG-VM Relación": "es_hijo_agresor",
                "Menores víctimas mortales vdg": "menores_victimas_mortales",
            }
        )

        es_victima_vicaria_mapping = {
            "Sí vicaria": True,
            "No vicaria": False,
        }
        es_hijo_agresor_mapping = {
            "Padre biológico/adoptivo": True,
            "No padre biológico/adoptivo": False,
        }

        # Normalize and validate all columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["es_victima_vicaria"] = apply_and_check_dict(df["es_victima_vicaria"], es_victima_vicaria_mapping)
        df["es_hijo_agresor"] = apply_and_check_dict(df["es_hijo_agresor"], es_hijo_agresor_mapping)
        df["menores_victimas_mortales"] = apply_and_check(df["menores_victimas_mortales"], normalize_positive_integer)

        # Save cleaned CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")

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
