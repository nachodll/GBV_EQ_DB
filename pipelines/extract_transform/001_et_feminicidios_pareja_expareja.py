"""Extract and transform data
Sources:
    DGVG001
Target tables:
    feminicios_pareja"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_age_group,
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG001-010FeminicidiosPareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_pareja_expareja.csv"


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
                "VM Grupo de edad": "victima_grupo_edad",
                "AG Grupo de edad": "agresor_grupo_edad",
                "Feminicidios pareja o expareja": "num_feminicidios",
                "Huérfanas y huérfanos menores de edad -1-": "num_huerfanos_menores",
            }
        )

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["victima_grupo_edad"] = apply_and_check(df["victima_grupo_edad"], normalize_age_group)
        df["agresor_grupo_edad"] = apply_and_check(df["agresor_grupo_edad"], normalize_age_group)
        df["num_feminicidios"] = apply_and_check(df["num_feminicidios"], normalize_positive_integer)
        df["num_huerfanos_menores"] = apply_and_check(df["num_huerfanos_menores"], normalize_positive_integer)

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
