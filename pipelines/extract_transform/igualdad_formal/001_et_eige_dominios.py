"""Extract and transform data
Sources:
    EIGE001
Target tables:
    eige_dominios
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_nationality,
    normalize_positive_float,
    normalize_year,
)

RAW_CSV_PATH = Path("data") / "raw" / "EIGE" / "EIGE001-DomainsSubdomains.csv"
CLEAN_CSV_PATH = Path("data") / "clean" / "igualdad_formal" / "eige_dominios.csv"


def main():
    try:
        # Read file
        df = pd.read_csv(RAW_CSV_PATH)  # type: ignore
        df.columns = df.columns.str.strip()

        # Rename columns
        df = df.rename(
            columns={
                "Time": "anio",
                "Geographic region": "pais_id",
                "Value": "valor",
                "(Sub-) Domain Scores": "dominio_subdominio",
            }
        )

        dominio_subdominio_mapping = {
            v: v
            for v in [
                "Access to health structures (Subdomain score)",
                "Attainment and participation (Subdomain score)",
                "Care activities (Subdomain score)",
                "Economic power (Subdomain score)",
                "Economic situation (Subdomain score)",
                "Financial resources (Subdomain score)",
                "Health (Domain score)",
                "Health status (Subdomain score)",
                "Healthy behaviour (Subdomain score)",
                "Knowledge (Domain score)",
                "Money (Domain score)",
                "Overall Gender Equality Index",
                "Participation in work (Subdomain score)",
                "Political power (Subdomain score)",
                "Power (Domain score)",
                "Segregation (Subdomain score)",
                "Segregation and quality of work (Subdomain score)",
                "Social activities (Subdomain score)",
                "Social power (Subdomain score)",
                "Time (Domain score)",
                "Work (Domain score)",
            ]
        }

        # Normalize and valitate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["pais_id"] = apply_and_check(df["pais_id"], normalize_nationality)
        df["dominio_subdominio"] = apply_and_check_dict(df["dominio_subdominio"], dominio_subdominio_mapping)
        df["valor"] = apply_and_check(df["valor"], normalize_positive_float)

        # Save to clean data
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")  # type: ignore
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
