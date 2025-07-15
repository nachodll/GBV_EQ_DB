"""Extract and transform data
Sources:
    DGVG013
Target tables:
    contratos_bonificados_sustitucion
"""

import logging
from pathlib import Path

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

RAW_CSV_PATH = Path("data") / "raw" / "DGVG" / "DGVG013-140ContratosBonificadosSustitución.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "contratos_bonificados_sustitucion.csv"


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
                "Colectivo": "colectivo",
                "Tipo de contrato": "tipo_contrato",
                "Número de contratos bonificados": "contratos_bonificados",
                "Número de contratos de sustitución": "contratos_sustitucion",
            }
        )

        colectivo_mapping = {
            "Contratos de sustitución VG": "Contratos de sustitución por vg",
            "Transformación en indefinidos de contratos de víctimas de violencia de género*": "Transformación en indefinidos de contratos de vvg",  # noqa: E501
            "Trata y mujeres en contexto de prostitución**": "Trata y mujeres en contexto de prostitución",
            "Violencia de género": "Violencia de genero",
            "Violencia doméstica*": "Violencia domestica",
            "Contrato de sustitución V. Sexual***": "Contrato de sustitución por violencia sexual",
            "Transformación en indefinidos de contratos de víctimas de violencia doméstica*": "Transformación en indefinidos de contratos de vdomestica",  # noqa: E501
            "Violencia Sexual***": "Violencia sexual",
            "Cargas familiares de violencia doméstica": "Cargas familiares de vdomestica",
        }
        tipo_contrato_mapping = {
            "Temporal": "Temporal",
            "Indefinido": "Indefinido",
        }

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["colectivo"] = apply_and_check_dict(df["colectivo"], colectivo_mapping)
        df["tipo_contrato"] = apply_and_check_dict(df["tipo_contrato"], tipo_contrato_mapping)
        df["contratos_bonificados"] = apply_and_check(df["contratos_bonificados"], normalize_positive_integer)
        df["contratos_sustitucion"] = apply_and_check(df["contratos_sustitucion"], normalize_positive_integer)

        # Save to CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Cleaned data saved to {CLEAN_CSV_PATH}")

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
