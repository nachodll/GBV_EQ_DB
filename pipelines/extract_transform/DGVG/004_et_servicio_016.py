"""Extract and transform data
Sources:
    DGVG004
Target tables:
    servicio_016
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG004-040Servicio016.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "servicio_016.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Año": "anio",
                "Mes": "mes",
                "Provincia": "provincia_id",
                "Persona que consulta": "persona_consulta",
                "Tipo violencia": "tipo_violencia",
                "Llamadas pertinentes": "llamadas",
                "WhatsApp pertinentes": "whatsapps",
                "Correos electrónicos pertinentes": "emails",
                "Chats pertinentes": "chats",
            }
        )
        df = df.drop(columns=["Total consultas pertinentes"])

        persona_consulta_mapping: dict[str, Optional[str]] = {
            "Usuaria": "Usuaria",
            "Familiares/Personas allegadas": "Familiares/Allegados",
            "Otras personas": "Otras personas",
        }

        tipo_violencia_mapping: dict[str, Optional[str]] = {
            "V. pareja o expareja": "Pareja/Expareja",
            "Violencia no desagregada": None,
            "V. familiar": "Familiar",
            "V. sexual (LOGILS)": "Sexual",
            "Otras violencias": "Otras violencias",
        }

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["persona_consulta"] = apply_and_check_dict(df["persona_consulta"], persona_consulta_mapping)
        df["tipo_violencia"] = apply_and_check_dict(df["tipo_violencia"], tipo_violencia_mapping)
        df["llamadas"] = apply_and_check(df["llamadas"], normalize_positive_integer)
        df["whatsapps"] = apply_and_check(df["whatsapps"], normalize_positive_integer)
        df["emails"] = apply_and_check(df["emails"], normalize_positive_integer)
        df["chats"] = apply_and_check(df["chats"], normalize_positive_integer)

        # Save cleaned CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data cleaned and saved to {CLEAN_CSV_PATH}")

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
