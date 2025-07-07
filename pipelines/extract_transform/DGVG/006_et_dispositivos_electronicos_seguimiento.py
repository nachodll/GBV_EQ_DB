"""Extract and transform data
Sources:
    DGVG006
Target tables:
    dispositivos_electronicos_seguimiento
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG006-060DispositivosElectrónicoSeguimiento.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "dispositivos_electronicos_seguimiento.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Mes": "mes",
                "Provincia": "provincia_id",
                "Instalaciones acumuladas": "instalaciones_acumuladas",
                "Desinstalaciones acumuladas": "desinstalaciones_acumuladas",
                "Dispositivos activos": "dispositivos_activos",
            }
        )
        df = df.drop(columns=["Comunidad autónoma"])

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["instalaciones_acumuladas"] = apply_and_check(df["instalaciones_acumuladas"], normalize_positive_integer)
        df["desinstalaciones_acumuladas"] = apply_and_check(
            df["desinstalaciones_acumuladas"], normalize_positive_integer
        )
        df["dispositivos_activos"] = apply_and_check(df["dispositivos_activos"], normalize_positive_integer)

        # Save clean CSV
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
