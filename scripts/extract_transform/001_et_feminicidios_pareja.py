"""Extract and transform data
Sources:
    DGVG001
Target tables:
    feminicios_pareja
"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_month, normalize_provincia

# Paths
RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG001-010FeminicidiosPareja.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "feminicidios_pareja.csv"

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
            "VM Grupo de edad": "edad_grupo_victima",
            "AG Grupo de edad": "edad_grupo_agresor",
            "Feminicidios pareja o expareja": "feminicidios",
            "Huérfanas y huérfanos menores de edad -1-": "huerfanos_menores",
        }
    )

    # Validate year and cast to integer
    df["año"] = pd.to_numeric(df["año"], errors="coerce")  # type: ignore
    df.loc[~df["año"].between(1900, 2050), "año"] = None  # type: ignore
    if df["año"].isnull().any():
        invalid_years = df[df["año"].isnull()]["año"].unique()  # type: ignore
        raise ValueError(f"Invalid year values found: {invalid_years}")
    df["año"] = df["año"].astype(int)

    # Normalize months
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    if df["mes"].isnull().any():
        missing_months = df[df["mes"].isnull()]["mes"].unique()  # type: ignore
        raise ValueError(f"Unmapped months found: {missing_months}")

    # Normalize provinces
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    if df["provincia_id"].isnull().any():
        missing = df[df["provincia_id"].isnull()]["provincia_id"].unique()  # type: ignore
        raise ValueError(f"Unmapped provinces found: {missing}")

    # Save cleaned CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logger.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
