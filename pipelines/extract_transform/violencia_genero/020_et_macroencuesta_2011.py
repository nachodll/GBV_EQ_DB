"""Extract and transform data
Sources:
    CIS003
Target tables:
    macroencuesta_2011
"""

import csv
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat  # type: ignore

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_json_string,
)

RAW_SAV_PATH = Path("data") / "raw" / "CIS" / "CIS003-Macroencuesta2011" / "2858.sav"
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "macroencuesta_2011.csv"


def main():
    try:
        # Read raw SAV
        df, meta = pyreadstat.read_sav(RAW_SAV_PATH)  # type: ignore

        # Replace NaN with None for JSON serialization
        df = df.replace({np.nan: None})  # type: ignore

        # Aggregate all columns except PERS_ID_R into a dict, then to JSON
        df_json = pd.DataFrame(
            {
                "variables_json": df.apply(lambda x: x.to_dict(), axis=1).apply(json.dumps),  # type: ignore
            }
        )

        # Validate and normalize columns
        df_json["variables_json"] = apply_and_check(df_json["variables_json"], normalize_json_string)

        # Save to CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df_json.to_csv(CLEAN_CSV_PATH, index=False, sep=";", quoting=csv.QUOTE_NONE)
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
