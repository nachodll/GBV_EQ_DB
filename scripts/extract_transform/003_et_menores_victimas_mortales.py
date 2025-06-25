"""Extract and transform data
Sourceses:
    DGVG003
Target tables:
    menores_victimas_mortales"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_month, normalize_positive_integer, normalize_provincia, normalize_year

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG003-030MenoresVictimasMortales.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "menores_victimas_mortales.csv"

# Logger setup
logger = logging.getLogger(__name__)


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

    # Check for missing values (according to the schema constraints)
    for column in df.columns:
        if df[column].isnull().any():
            logger.error(f"Missing values found in column '{column}'")
            raise ValueError(f"Missing values found in column '{column}'")

    # Save cleaned CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logger.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
