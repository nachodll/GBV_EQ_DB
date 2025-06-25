"""Extract and transform data
Sources:
    DGVG002
Target tables:
    feminicios_no_pareja
"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_comunidad_autonoma, normalize_positive_integer, normalize_year

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG002-020FeminicidiosFueraParejaExpareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_fuera_pareja_expareja.csv"

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
            "Feminicidos fuera pareja o expareja": "num_feminicidios",
        }
    )
    tipo_feminicidio_mapping = {
        "F. vicario -1-": "Vicario",
        "F. familiar": "Familiar",
        "F. sexual": "Sexual",
        "F. social": "Social",
    }

    # Normalize and validate all columns
    df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].map(normalize_comunidad_autonoma)  # type: ignore
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["num_feminicidios"] = df["num_feminicidios"].map(normalize_positive_integer)  # type: ignore
    df["tipo_feminicidio"] = df["tipo_feminicidio"].map(tipo_feminicidio_mapping)  # type: ignore

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
