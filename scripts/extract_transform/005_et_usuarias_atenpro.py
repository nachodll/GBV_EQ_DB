"""Extract and transform data
Sources:
    DGVG005
Target tables:
    usuarias_atenpro
"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_month, normalize_positive_integer, normalize_provincia, normalize_year

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG005-050UsuariasATENPRO.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "usuarias_atenpro.csv"

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
            "Año": "año",
            "Mes": "mes",
            "Provincia": "provincia_id",
            "Altas": "num_altas",
            "Bajas": "num_bajas",
            "Usuarias activas": "num_usuarias_activas",
        }
    )
    df = df.drop(columns=["Comunidad autónoma"])

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    df["num_altas"] = df["num_altas"].map(normalize_positive_integer)  # type: ignore
    df["num_bajas"] = df["num_bajas"].map(normalize_positive_integer)  # type: ignore
    df["num_usuarias_activas"] = df["num_usuarias_activas"].map(normalize_positive_integer)  # type: ignore

    # Drop rows with any NaN values in column num_altas or num_bajas
    df = df.dropna(subset=["num_altas", "num_bajas"])  # type: ignore

    # Check for missing values in required columns
    required_columns = ["provincia_id", "año", "mes", "num_altas", "num_bajas", "num_usuarias_activas"]
    for column in required_columns:
        if df[column].isnull().any():
            logger.error(f"Missing values found in column '{column}'")
            raise ValueError(f"Missing values found in column '{column}'")

    # Save clean CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logger.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    main()
