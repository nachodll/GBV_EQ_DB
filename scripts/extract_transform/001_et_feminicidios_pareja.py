"""Extract and transform data
Sources:
    DGVG001
Target tables:
    feminicios_pareja"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import (
    normalize_age_group,
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG001-010FeminicidiosPareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_pareja_expareja.csv"

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
            "VM Grupo de edad": "victima_grupo_edad",
            "AG Grupo de edad": "agresor_grupo_edad",
            "Feminicidios pareja o expareja": "num_feminicidios",
            "Huérfanas y huérfanos menores de edad -1-": "num_huerfanos_menores",
        }
    )

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    df["victima_grupo_edad"] = df["victima_grupo_edad"].map(normalize_age_group)  # type: ignore
    df["agresor_grupo_edad"] = df["agresor_grupo_edad"].map(normalize_age_group)  # type: ignore
    df["num_feminicidios"] = df["num_feminicidios"].map(normalize_positive_integer)  # type: ignore
    df["num_huerfanos_menores"] = df["num_huerfanos_menores"].map(normalize_positive_integer)  # type: ignore

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
