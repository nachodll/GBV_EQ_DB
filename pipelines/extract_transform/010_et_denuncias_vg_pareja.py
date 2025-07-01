"""Extract and transform data
Sources:
    DGVG010
Target tables:
    denuncias_vg_pareja
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_positive_integer,
    normalize_provincia,
    normalize_quarter,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG010-110DenunciasVDGPareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "denuncias_vg_pareja.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "año",
                "Trimestre": "trimestre",
                "Provincia": "provincia_id",
                "Origen de la denuncia": "origen_denuncia",
                "Número de denuncias por violencia de género": "num_denuncias",
            }
        )

        origen_denuncia_mapping = {
            "Presentada directamente por victima": "Presentada directamente por víctima",
            "Presentada directamente por familiares": "Presentada directamente por familiares",
            "Atestados policiales - con denuncia victima": "Atestados policiales - con denuncia víctima",
            "Atestados policiales - con denuncia familiar": "Atestados policiales - con denuncia familiar",
            "Atestados policiales - por intervención directa policial": "Atestados policiales - por intervención directa policial",  # noqa: E501
            "Parte de lesiones": "Parte de lesiones",
            "Servicios asistencia-Terceros  en general": "Servicios asistencia - Terceros en general",
        }

        # Normalize and validate all columns
        df["año"] = apply_and_check(df["año"], normalize_year)
        df["trimestre"] = apply_and_check(df["trimestre"], normalize_quarter)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["num_denuncias"] = apply_and_check(df["num_denuncias"], normalize_positive_integer)
        df["origen_denuncia"] = apply_and_check_dict(df["origen_denuncia"], origen_denuncia_mapping)

        # Save clean CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False)
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
