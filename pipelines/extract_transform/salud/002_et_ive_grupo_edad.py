"""Extract and transform data
Sources:
    MINSANIDAD001
Target tables
    ive_grupo_edad
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_age_group,
    normalize_positive_float,
    normalize_year,
)

RAW_XLSX_PATH = Path("data") / "raw" / "MINSANIDAD" / "MINSANIDAD001-InterrupcionesVoluntariasEmbarazo.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "salud" / "ive_grupo_edad.csv"


def main():
    try:
        # Read xlsx file into a DataFrame
        excel_df = pd.read_excel(RAW_XLSX_PATH, sheet_name="Tabla 2", header=1)

        # Reshape excel to df
        all_records = []
        for row in excel_df.itertuples(index=False):
            for cell in row[1:]:
                all_records.append(
                    {
                        "grupo_edad": excel_df.columns[row.index(cell)],
                        "anio": row[0],
                        "tasa": cell,
                    }
                )
        df = pd.DataFrame(all_records)

        # Replace "19 y menos años" with "<19"
        df["grupo_edad"] = df["grupo_edad"].replace("19 y menos años", "<19", regex=True)

        # Normalize and validate columns
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["tasa"] = apply_and_check(df["tasa"], normalize_positive_float)

        # Save to CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data saved to {CLEAN_CSV_PATH}")

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
