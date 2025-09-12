"""Extract and transform data
Sources:
    INMUJERES003
Target tables:
    denuncias_vg_presentadas
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_positive_integer,
    normalize_year,
)

RAW_XLS_PATH = Path("data") / "raw" / "INMUJERES" / "INMUJERES003-DenunciasVDG.xls"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "denuncias_vg_presentadas.csv"


def main():
    try:
        excel_df = pd.read_excel(RAW_XLS_PATH, sheet_name="Evo w852", skiprows=3, header=None)  # type: ignore

        # Extract data from excel into desired format
        all_entries = []
        for row in range(3, 20):
            for col in range(1, 19):
                entry = {  # type: ignore
                    "anio": excel_df.iat[0, col],  # type: ignore
                    "comunidad_autonoma_id": excel_df.iat[row, 0],  # type: ignore
                    "denuncias_presentadas": excel_df.iat[row, col],  # type: ignore
                }
                all_entries.append(entry)  # type: ignore
        df = pd.DataFrame(all_entries)

        # Normalize and validate all columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["denuncias_presentadas"] = apply_and_check(df["denuncias_presentadas"], normalize_positive_integer)

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
