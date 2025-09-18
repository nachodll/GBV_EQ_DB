"""Extract and transform data
Sources:
    CIS001, CIS002
Target tables:
    fusion_encuestas
"""

import logging
from pathlib import Path

import pandas as pd
import pyreadstat  # type: ignore

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_month,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_SAV_PATH_2015 = Path("data") / "raw" / "CIS" / "CIS002-Macroencuesta2015" / "3027.sav"
RAW_SAV_PATH_2019 = Path("data") / "raw" / "CIS" / "CIS001-Macroencuesta2019" / "3235.sav"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "fusion_encuestas.csv"


def main():
    try:
        # Read raw SAV files
        df_2015, _ = pyreadstat.read_sav(RAW_SAV_PATH_2015, apply_value_formats=True)  # type: ignore
        df_2019, _ = pyreadstat.read_sav(RAW_SAV_PATH_2019, apply_value_formats=True)  # type: ignore

        # Extract common variables and add metadata for both years
        df_2015_subset = df_2015[["PROV"]].copy()  # type: ignore
        df_2015_subset["codigo_estudio"] = 3027
        df_2015_subset["anio"] = 2014
        df_2015_subset["mes"] = "Septiembre"
        df_2019_subset = df_2019[["PROV"]].copy()  # type: ignore
        df_2019_subset["codigo_estudio"] = 3235
        df_2019_subset["anio"] = 2019
        df_2019_subset["mes"] = "Septiembre"

        # Define the variable mappings
        var_mapping_2019 = {
            "violencia_sexual_1_pareja": ["M1P5_0_4", "M2P5_0_4"],
            "violencia_sexual_2_pareja": ["M1P5_0_2", "M2P5_0_2"],
            "violencia_sexual_3_pareja": ["M1P5_0_8", "M2P5_0_8"],
            "violencia_sexual_1_fuera_pareja": ["M3P2_4"],
            "violencia_fisica_1_pareja": ["M1P4_0_1", "M2P4_0_1"],
            "violencia_fisica_2_pareja": ["M1P4_0_2", "M2P4_0_2"],
            "violencia_fisica_3_pareja": ["M1P4_0_3", "M2P4_0_3"],
            "violencia_fisica_4_pareja": ["M1P4_0_4", "M2P4_0_4"],
            "violencia_fisica_5_pareja": ["M1P4_0_5", "M2P4_0_5"],
            "violencia_fisica_6_pareja": ["M1P4_0_6", "M2P4_0_6"],
            "violencia_fisica_2_fuera_pareja": ["M3P1_2"],
            "violencia_fisica_5_fuera_pareja": ["M3P1_5"],
            "violencia_fisica_6_fuera_pareja": ["M3P1_6"],
        }

        var_mapping_2015 = {
            "violencia_sexual_1_pareja": ["P2201", "P3101"],
            "violencia_sexual_2_pareja": ["P2202", "P3102"],
            "violencia_sexual_3_pareja": ["P2203", "P3103"],
            "violencia_sexual_1_fuera_pareja": ["P52"],
            "violencia_fisica_1_pareja": ["P2101", "P3001"],
            "violencia_fisica_2_pareja": ["P2102", "P3002"],
            "violencia_fisica_3_pareja": ["P2103", "P3003"],
            "violencia_fisica_4_pareja": ["P2104", "P3004"],
            "violencia_fisica_5_pareja": ["P2105", "P3005"],
            "violencia_fisica_6_pareja": ["P2106", "P3006"],
            "violencia_fisica_2_fuera_pareja": ["P4803"],
            "violencia_fisica_5_fuera_pareja": ["P4804"],
            "violencia_fisica_6_fuera_pareja": ["P4805"],
        }

        # Apply conditions for 2019
        for var, columns in var_mapping_2019.items():
            df_2019_subset[var] = df_2019[columns].eq("Sí").any(axis=1)  # type: ignore

        # Apply conditions for 2015
        for var, columns in var_mapping_2015.items():
            df_2015_subset[var] = df_2015[columns].eq("Sí").any(axis=1)  # type: ignore

        # Concatenate the two subsets and rename columns
        df = pd.concat([df_2019_subset, df_2015_subset], ignore_index=True)  # type: ignore
        df.rename(
            columns={
                "PROV": "provincia_id",
                "codigo_estudio": "codigo_estudio",
                "anio": "anio",
                "mes": "mes",
            },
            inplace=True,
        )

        # Normalize and validate columns
        df["provincia_id"] = apply_and_check(df["provincia_id"].astype(str), normalize_provincia)
        df["codigo_estudio"] = apply_and_check(df["codigo_estudio"], normalize_positive_integer)
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["mes"] = apply_and_check(df["mes"], normalize_month)

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
