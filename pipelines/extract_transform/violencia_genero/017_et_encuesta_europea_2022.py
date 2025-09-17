"""Extract and transform data
Sources:
    EUROSTAT001
Target tables:
    encuesta_europea_2022
"""

import csv
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    normalize_json_string,
    normalize_positive_integer,
)

RAW_CSV_PATH = (
    Path("data") / "raw" / "EUROSTAT" / "EUROSTAT001-EncuestaEuropeaViolenciaGénero" / "encuesta_europea_GBV.csv"
)
CLEAN_CSV_PATH = Path("data") / "clean" / "violencia_genero" / "encuesta_europea_2022.csv"


def main():
    try:
        # Read raw CSV
        df = pd.read_csv(RAW_CSV_PATH, sep=";")  # type: ignore

        # Replace NaN with None for JSON serialization
        df = df.replace({np.nan: None})  # type: ignore

        # Aggregate all columns except PERS_ID_R into a dict, then to JSON
        df_json = pd.DataFrame(
            {
                "encuestado_id": df["PERS_ID_R"],
                "variables_json": df.drop(columns=["PERS_ID_R"]).apply(lambda x: x.to_dict(), axis=1).apply(json.dumps),  # type: ignore
            }
        )

        # Validate and normalize columns
        df_json["encuestado_id"] = apply_and_check(df_json["encuestado_id"], normalize_positive_integer)
        df_json["variables_json"] = apply_and_check(df_json["variables_json"], normalize_json_string)

        # Save to CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df_json.to_csv(CLEAN_CSV_PATH, index=False, sep=";", quoting=csv.QUOTE_NONE, escapechar="\\")
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
