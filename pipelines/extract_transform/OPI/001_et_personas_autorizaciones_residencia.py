"""Extract and transform data
Sources:
    OPI001,
    OPI002
Target tables:
    personas_autorizaciones_residencia
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_date,
    normalize_nationality,
    normalize_positive_integer,
    normalize_provincia,
)

RAW_CSV_PATH_1 = Path("data") / "raw" / "OPI" / "OPI001-PersonasAutorizaciónResidencia.csv"
RAW_CSV_PATH_2 = Path("data") / "raw" / "OPI" / "OPI002-PersonasCertificadoRegistroOAcuerdoRetirada.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "personas_autorizaciones_residencia.csv"


def main():
    try:
        # Read both csvs files and concat into a DataFrame
        df1 = pd.read_csv(RAW_CSV_PATH_1, sep="\t")  # type: ignore
        df1["Tipo de documentación"] = "Autorización"
        df2 = pd.read_csv(RAW_CSV_PATH_2, sep="\t")  # type: ignore
        df = pd.concat([df1, df2], ignore_index=True)

        # Rename columns
        df.rename(
            columns={
                "Provincia": "provincia_id",
                "Principales nacionalidades": "nacionalidad",
                "Tipo de documentación": "tipo_documentacion",
                "Sexo": "sexo",
                "Lugar de nacimiento": "es_nacido_espania",
                "Grupo de edad": "grupo_edad",
                "Fecha": "fecha",
                "Total": "personas_autorizacion_residencia",
            },
            inplace=True,
        )

        # Drop all rows with aggregated data (e.g., "TOTAL")
        num_rows_before = len(df)
        df = df[df["provincia_id"] != "Total nacional"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'provincia_id'.")
        num_rows_before = len(df)
        df = df[df["nacionalidad"] != "Todas las nacionalidades"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'nacionalidad'.")
        num_rows_before = len(df)
        df = df[df["tipo_documentacion"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'tipo_documentacion'.")
        num_rows_before = len(df)
        df = df[df["sexo"] != "Ambos sexos"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'sexo'.")
        num_rows_before = len(df)
        df = df[df["es_nacido_espania"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'es_nacido_espania'.")
        num_rows_before = len(df)
        df = df[df["grupo_edad"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'grupo_edad'.")

        # Remove thousands separator dots from personas_autorizacion_residencia
        df["personas_autorizacion_residencia"] = (
            df["personas_autorizacion_residencia"].astype(str).str.replace(".", "", regex=False)
        )

        # Normalize and validate columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["nacionalidad"] = apply_and_check(df["nacionalidad"], normalize_nationality)
        df["tipo_documentacion"] = apply_and_check_dict(
            df["tipo_documentacion"],
            {v: v for v in ["Autorización", "Certificado de registro", "TIE-Acuerdo de Retirada"]},
        )
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})
        df["es_nacido_espania"] = apply_and_check_dict(
            df["es_nacido_espania"],
            {"España": True, "Extranjero": False},
        )
        df["fecha"] = apply_and_check(df["fecha"], normalize_date)
        df["personas_autorizacion_residencia"] = apply_and_check(
            df["personas_autorizacion_residencia"], normalize_positive_integer
        )

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
