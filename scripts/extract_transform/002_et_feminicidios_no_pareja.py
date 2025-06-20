"""Extract and transform data
Sources:
    DGVG002
Target tables:
    feminicios_no_pareja
"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_comunidad_autonoma

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG002-020FeminicidiosFueraParejaExpareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_no_pareja.csv"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    # Read file
    df = pd.read_csv(RAW_CSV_PATH)  # type: ignore

    # Delete spaces
    df.columns = df.columns.str.strip()

    # Rename columns
    df = df.rename(
        columns={
            "Comunidad autónoma (As)": "comunidad_autonoma_id",
            "Año": "año",
            "Tipo de feminicidio": "tipo_feminicidio",
            "Feminicidos fuera pareja o expareja": "feminicidios",
        }
    )

    # Validate year and cast to integer
    df["año"] = pd.to_numeric(df["año"], errors="coerce")  # type: ignore
    df.loc[~df["año"].between(1900, 2050), "año"] = None  # type: ignore
    if df["año"].isnull().any():
        invalid_years = df[df["año"].isnull()]["año"].unique()  # type: ignore
        raise ValueError(f"Invalid year values found: {invalid_years}")
    df["año"] = df["año"].astype(int)

    # Normalize provinces
    df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].map(normalize_comunidad_autonoma)  # type: ignore
    if df["comunidad_autonoma_id"].isnull().any():
        missing = df[df["comunidad_autonoma_id"].isnull()]["comunidad_autonoma_id"].unique()  # type: ignore
        raise ValueError(f"Unmapped provinces found: {missing}")

    # Save cleaned CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logger.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
