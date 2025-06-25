"""Extract and transform data
Sourceses:
    DGVG003
Target tables:
    menores_victimas_mortales"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import normalize_month, normalize_positive_integer, normalize_provincia, normalize_year

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG003-030MenoresVictimasMortales.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "menores_victimas_mortales.csv"


def main():
    # Read file
    df = pd.read_csv(str(RAW_CSV_PATH))  # type: ignore

    # Delete spaces
    df.columns = df.columns.str.strip()

    # Rename columns
    df = df.rename(
        columns={
            "Provincia (As)": "provincia_id",
            "Año": "año",
            "Mes": "mes",
            "VM Vicaria -1-": "es_victima_vicaria",
            "AG-VM Relación": "es_hijo_agresor",
            "Menores víctimas mortales vdg": "num_menores_victimas_mortales",
        }
    )

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    df["es_victima_vicaria"] = df["es_victima_vicaria"].map({"Sí vicaria": True, "No vicaria": False})  # type: ignore
    df["es_hijo_agresor"] = df["es_hijo_agresor"].map(  # type: ignore
        {"Padre biológico/adoptivo": True, "No padre biológico/adoptivo": False}
    )  # type: ignore
    df["num_menores_victimas_mortales"] = df["num_menores_victimas_mortales"].map(normalize_positive_integer)  # type: ignore

    # Check for missing values in required columns
    required_columns = [
        "provincia_id",
        "año",
        "mes",
        "es_victima_vicaria",
        "es_hijo_agresor",
        "num_menores_victimas_mortales",
    ]
    for column in required_columns:
        if df[column].isnull().any():
            logging.error(f"Missing values found in column '{column}'")
            raise ValueError(f"Missing values found in column '{column}'")

    # Save cleaned CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logging.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    setup_logging()
    main()
