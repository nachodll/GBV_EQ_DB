"""Extract and transform data
Sources:
    INE001
Target tables:
    poblacion_municipios
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_DIR = Path("data") / "raw" / "INE" / "INE001-PoblaciónMunicipios"
CLEAN_CSV_PATH = Path("data") / "clean" / "poblacion_municipios.csv"


def main():
    try:
        # Read all csv files in the directory into a single DataFrame
        csv_files = list(RAW_CSV_DIR.glob("*.csv"))
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {RAW_CSV_DIR}")
        df = pd.concat((pd.read_csv(file, sep="\t") for file in csv_files), ignore_index=True)  # type: ignore

        # Rename columns
        df.rename(
            columns={
                "Municipios": "municipio_id",
                "Periodo": "anio",
                "Sexo": "sexo",
                "Total": "total_poblacion",
            },
            inplace=True,
        )

        # Extract municipio_id and drop if it's province_id (less 5 digits)
        df["municipio_id"] = df["municipio_id"].astype(str).str.split(" ").str[0]
        df = df[df["municipio_id"].str.match(r"^\d{5}$")]  # type: ignore

        # Drop rows with missing values in total_poblacion
        num_rows_before = len(df)
        df.dropna(subset=["total_poblacion"], inplace=True)  # type: ignore
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with missing 'total_poblacion' values.")

        # Normalize and validate all columns (municipio_id is already validated)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["sexo"] = apply_and_check_dict(
            df["sexo"],
            {
                "Hombres": "Hombre",
                "Mujeres": "Mujer",
                "Total": "Total",
            },
        )
        df["total_poblacion"] = df["total_poblacion"].astype(str).str.replace(".", "", regex=False)
        df["total_poblacion"] = apply_and_check(df["total_poblacion"], normalize_positive_integer)

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
