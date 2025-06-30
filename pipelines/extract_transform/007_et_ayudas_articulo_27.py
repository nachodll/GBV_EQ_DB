"""Extract and transform data
Sources:
    DGVG007
Target tables:
    ayudas_articulo_27
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import normalize_comunidad_autonoma, normalize_positive_integer, normalize_year

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG007-070AyudasArtículo27.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "ayudas_articulo_27.csv"


def main():
    # Read file
    df = pd.read_csv(RAW_CSV_PATH)  # type: ignore

    # Delete spaces
    df.columns = df.columns.str.strip()

    # Rename columns
    df = df.rename(
        columns={
            "Año": "año",
            "Comunidad autónoma": "comunidad_autonoma_id",
            "Número de ayudas concedidas Art 27": "num_ayudas_concedidas",
        }
    )

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].map(normalize_comunidad_autonoma)  # type: ignore
    df["num_ayudas_concedidas"] = df["num_ayudas_concedidas"].map(normalize_positive_integer)  # type: ignore

    # Check for missing values in required columns
    required_columns = ["año", "num_ayudas_concedidas"]
    for column in required_columns:
        if df[column].isnull().any():
            logging.error(f"Missing values found in column '{column}'")
            raise ValueError(f"Missing values found in column '{column}'")

    # Save clean data
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logging.info(f"Clean data saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    setup_logging()
    main()
