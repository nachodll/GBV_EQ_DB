"""Extract and transform data
Sources:
    DGVG006
Target tables:
    dispositivos_electronicos_seguimiento
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import normalize_month, normalize_positive_integer, normalize_provincia, normalize_year

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG006-060DispositivosElectrónicoSeguimiento.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "dispositivos_electronicos_seguimientos.csv"


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
            "Instalaciones acumuladas": "num_instalaciones_acumuladas",
            "Desinstalaciones acumuladas": "num_desinstalaciones_acumuladas",
            "Dispositivos activos": "num_dispositivos_activos",
        }
    )
    df = df.drop(columns=["Comunidad autónoma"])

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    df["num_instalaciones_acumuladas"] = df["num_instalaciones_acumuladas"].map(normalize_positive_integer)  # type: ignore
    df["num_desinstalaciones_acumuladas"] = df["num_desinstalaciones_acumuladas"].map(normalize_positive_integer)  # type: ignore
    df["num_dispositivos_activos"] = df["num_dispositivos_activos"].map(normalize_positive_integer)  # type: ignore

    # Check for missing values in required columns
    required_columns = [
        "provincia_id",
        "año",
        "mes",
        "num_instalaciones_acumuladas",
        "num_desinstalaciones_acumuladas",
        "num_dispositivos_activos",
    ]
    for column in required_columns:
        if df[column].isnull().any():
            logging.error(f"Missing values found in column '{column}'")
            raise ValueError(f"Missing values found in column '{column}'")

    # Save clean CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logging.info(f"Cleaned data saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    setup_logging()
    main()
