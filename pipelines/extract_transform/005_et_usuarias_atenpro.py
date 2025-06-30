"""Extract and transform data
Sources:
    DGVG005
Target tables:
    usuarias_atenpro
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

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG005-050UsuariasATENPRO.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "usuarias_atenpro.csv"


def main():
    # Read file
    df = pd.read_csv(RAW_CSV_PATH)  # type: ignore

    # Delete spaces
    df.columns = df.columns.str.strip()

    # Rename columns
    df = df.rename(
        columns={
            "Año": "año",
            "Mes": "mes",
            "Provincia": "provincia_id",
            "Altas": "num_altas",
            "Bajas": "num_bajas",
            "Usuarias activas": "num_usuarias_activas",
        }
    )
    df = df.drop(columns=["Comunidad autónoma"])

    # Dropping rows with negative values in 'num_altas' or 'num_bajas'
    rows_before = len(df)
    df = df[df["num_altas"] >= 0]
    df = df[df["num_bajas"] >= 0]
    logging.warning(f"Dropped {rows_before - len(df)} rows with negative values in 'num_altas' or 'num_bajas'.")

    # Normalize and validate all columns
    df["año"] = apply_and_check(df["año"], normalize_year)
    df["mes"] = apply_and_check(df["mes"], normalize_month)
    df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
    df["num_usuarias_activas"] = apply_and_check(df["num_usuarias_activas"], normalize_positive_integer)
    df["num_altas"] = apply_and_check(df["num_altas"], normalize_positive_integer)
    df["num_bajas"] = apply_and_check(df["num_bajas"], normalize_positive_integer)

    # Save clean CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logging.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    setup_logging()
    main()
