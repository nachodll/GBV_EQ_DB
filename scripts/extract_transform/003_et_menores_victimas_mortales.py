"""Extract and transform data
Sourceses:
    DGVG003
Target tables:
    menores_victimas_mortales"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_month, normalize_provincia

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
        missing_provincias = df[df["provincia_id"].isnull()]["provincia_id"].unique()  # type: ignore
        raise ValueError(f"Unmapped provinces found: {missing_provincias}")

    # Map es_victima_vicaria to boolean
    df["es_victima_vicaria"] = df["es_victima_vicaria"].map({"Sí vicaria": True, "No vicaria": False})  # type: ignore
    if df["es_victima_vicaria"].isnull().any():
        missing_vicaria = df[df["es_victima_vicaria"].isnull()]["es_victima_vicaria"].unique()  # type: ignore
        raise ValueError(f"Unmapped es_victima_vicaria values found: {missing_vicaria}")

    # Map es_hijo_agresor to boolean
    df["es_hijo_agresor"] = df["es_hijo_agresor"].map(  # type: ignore
        {"Padre biológico/adoptivo": True, "No padre biológico/adoptivo": False}
    )  # type: ignore

    # Validate num_menores_victimas_mortales and cast to integer
    df["num_menores_victimas_mortales"] = pd.to_numeric(df["num_menores_victimas_mortales"], errors="coerce")  # type: ignore
    if df["num_menores_victimas_mortales"].isnull().any():
        invalid_victimas = df[df["num_menores_victimas_mortales"].isnull()]["num_menores_victimas_mortales"].unique()  # type: ignore
        raise ValueError(f"Invalid num_menores_victimas_mortales values found: {invalid_victimas}")

    # Save cleaned CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logger.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
