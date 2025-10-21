"""Extract and transform data
Sources:
    INMUJERES002
Target tables:
    mujeres_cargos_autonomicos
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_positive_integer,
    normalize_year,
)

RAW_XLS_PATH = Path("data") / "raw" / "INMUJERES" / "INMUJERES002-MujeresCargosAutonómicos.xls"
CLEAN_CSV_PATH = Path("data") / "clean" / "igualdad_formal" / "mujeres_cargos_autonomicos.csv"


def format_data_per_sex(df: pd.DataFrame, year_headers: pd.Series, sex: str) -> pd.DataFrame:
    all_entries = []
    for row in range(0, df.shape[0]):
        for col in range(2, df.shape[1]):
            entry = {
                "comunidad_autonoma_id": df.iat[row, 1],
                "anio": year_headers.iat[col],
                "numero_cargos": df.iat[row, col],
                "sexo": sex,
            }
            all_entries.append(entry)

    return pd.DataFrame(all_entries)


def main():
    try:
        # Read xls file
        excel_df = pd.read_excel(RAW_XLS_PATH, sheet_name="Evo w95", header=None)

        # Get year headers
        year_headers = excel_df.iloc[2]

        # Divide the dataframe into multiple dataframes, one for each sex
        df_ambos_sexos = excel_df.iloc[30:49, :].copy()
        df_mujeres = excel_df.iloc[53:72, :].copy()
        df_hombres = excel_df.iloc[76:95, :].copy()

        # Adapt format
        df_ambos_sexos = format_data_per_sex(df_ambos_sexos, year_headers, "Total")
        df_mujeres = format_data_per_sex(df_mujeres, year_headers, "Mujer")
        df_hombres = format_data_per_sex(df_hombres, year_headers, "Hombre")

        # Merge all dataframes
        df = pd.concat([df_ambos_sexos, df_mujeres, df_hombres], ignore_index=True)

        # Valiedate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["numero_cargos"] = apply_and_check(df["numero_cargos"], normalize_positive_integer)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombre": "Hombre", "Mujer": "Mujer", "Total": "Total"})

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
