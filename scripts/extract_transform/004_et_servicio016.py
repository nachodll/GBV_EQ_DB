"""Extract and transform data
Sources:
    DGVG004
Target tables:
    servicio_016
"""

import logging
from pathlib import Path

import pandas as pd

from utils.normalization import normalize_month, normalize_positive_integer, normalize_provincia, normalize_year

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG004-040Servicio016.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "servicio_016.csv"

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
            "Persona que consulta": "persona_consulta",
            "Tipo violencia": "tipo_violencia",
            "Total consultas pertinentes": "total_consultas",
            "Llamadas pertinentes": "num_llamadas",
            "WhatsApp pertinentes": "num_whatsapps",
            "Correos electrónicos pertinentes": "num_emails",
            "Chats pertinentes": "num_chats",
        }
    )

    persona_consulta_mapping = {
        "Usuaria": "Usuaria",
        "Familiares/Personas allegadas": "Familiares/Allegados",
        "Otras personas": "Otras personas",
        "No consta": "No consta",
    }
    tipo_violencia_mapping = {
        "V. pareja o expareja": "Pareja/Expareja",
        "Violencia no desagregada": "No desagregada",
        "V. familiar": "Familiar",
        "V. sexual (LOGILS)": "Sexual",
        "Otras violencias": "Otras violencias",
    }

    # Normalize and validate all columns
    df["año"] = df["año"].map(normalize_year)  # type: ignore
    df["mes"] = df["mes"].map(normalize_month)  # type: ignore
    df["provincia_id"] = df["provincia_id"].map(normalize_provincia)  # type: ignore
    df["persona_consulta"] = df["persona_consulta"].map(persona_consulta_mapping)  # type: ignore
    df["tipo_violencia"] = df["tipo_violencia"].map(tipo_violencia_mapping)  # type: ignore
    df["total_consultas"] = df["total_consultas"].map(normalize_positive_integer)  # type: ignore
    df["num_llamadas"] = df["num_llamadas"].map(normalize_positive_integer)  # type: ignore
    df["num_whatsapps"] = df["num_whatsapps"].map(normalize_positive_integer)  # type: ignore
    df["num_emails"] = df["num_emails"].map(normalize_positive_integer)  # type: ignore
    df["num_chats"] = df["num_chats"].map(normalize_positive_integer)  # type: ignore

    # Check for missing values (according to the schema constraints)
    for column in df.columns:
        if column != "provincia_id":
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
