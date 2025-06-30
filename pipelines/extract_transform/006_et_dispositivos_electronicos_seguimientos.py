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
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

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
    df["año"] = apply_and_check(df["año"], normalize_year)
    df["mes"] = apply_and_check(df["mes"], normalize_month)
    df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
    df["num_instalaciones_acumuladas"] = apply_and_check(df["num_instalaciones_acumuladas"], normalize_positive_integer)
    df["num_desinstalaciones_acumuladas"] = apply_and_check(
        df["num_desinstalaciones_acumuladas"], normalize_positive_integer
    )
    df["num_dispositivos_activos"] = apply_and_check(df["num_dispositivos_activos"], normalize_positive_integer)

    # Save clean CSV
    CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_CSV_PATH, index=False)
    logging.info(f"Cleaned data saved to {CLEAN_CSV_PATH}")


if __name__ == "__main__":
    setup_logging()
    main()
