"""Extract and transform data
Sources:
    BOE001
Target tables:
    legislacion
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_plain_text,
)

RAW_DIR_PATH = Path("data") / "raw" / "BOE" / "BOE001-LegislaciónVDG"
RAW_XLSX_PATH = RAW_DIR_PATH / "Leyes VG.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "politicas_publicas_igualdad_violencia" / "legislacion.csv"


def main():
    try:
        # Read xlsx file
        df = pd.read_excel(RAW_XLSX_PATH, sheet_name="Hoja1", usecols=range(8))

        # Rename columns
        df = df.rename(
            columns={
                "Comunidad Autónoma": "comunidad_autonoma_id",
                "Ley": "nombre",
                "ENLACE BOE": "enlace_boe",
                "TEMA": "tematica",
                "Fecha de Aprobación": "fecha_aprobacion",
                "Vigencia": "vigente",
                "Fecha derogación": "fecha_derogacion",
            }
        )
        df = df.drop(columns=["Pdf"], errors="ignore")

        # Transform column 'vigente' to boolean
        df["vigente"] = df["vigente"].apply(lambda x: False if str(x).strip().upper() == "DEROGADA" else True)

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["nombre"] = apply_and_check(df["nombre"], normalize_plain_text)
        df["enlace_boe"] = apply_and_check(df["enlace_boe"], normalize_plain_text)
        df["tematica"] = apply_and_check_dict(
            df["tematica"], {"VIOLENCIA": "Violencia de género", "IGUALDAD": "Igualdad"}
        )
        df["fecha_aprobacion"] = apply_and_check(df["fecha_aprobacion"], normalize_date)
        df["fecha_derogacion"] = apply_and_check(df["fecha_derogacion"], normalize_date)

        # Save to clean CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data successfully transformed and saved to {CLEAN_CSV_PATH}")

    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Could not parse: {e}")
        raise
    except ValueError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(f"Unexpected error processing: {e}")
        raise


if __name__ == "__main__":
    setup_logging()
    main()
