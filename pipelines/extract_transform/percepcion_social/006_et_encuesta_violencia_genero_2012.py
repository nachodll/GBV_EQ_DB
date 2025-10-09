"""Extract and transform data
Sources:
    CIS009
Target tables:
    encuesta_violencia_genero_2012
"""

import csv
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_json_string,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_provincia,
)

RAW_SAV_PATH = Path("data") / "raw" / "CIS" / "CIS009-PercepciónSocioalViolenciaGénero" / "2968.sav"
CLEAN_CSV_PATH = Path("data") / "clean" / "percepcion_social" / "encuesta_violencia_genero_2012.csv"


def main():
    try:
        # Load sav file
        df = pd.read_spss(RAW_SAV_PATH, convert_categoricals=True)

        # Replace NaN with None for JSON serialization
        df = df.replace({np.nan: None})  # type: ignore

        # Convert categorical columns to strings to avoid encoding issues
        for col in df.columns:
            if df[col].dtype.name == "category":
                df[col] = df[col].astype(str)

        # Extract relevant variables
        df_json = pd.DataFrame()
        df_json["codigo_estudio"] = df["ESTU"].astype(int).astype(str)
        df_json["fecha"] = "19-11-2012"
        df_json["comunidad_autonoma_id"] = df["CCAA"].astype(str)
        df_json["provincia_id"] = df["PROV"].astype(str)
        df_json["cuestionario"] = df["CUES"].astype(int)

        # Aggregate all columns into a dict, then to JSON
        df_json["variables_json"] = df.apply(lambda x: x.to_dict(), axis=1).apply(json.dumps)  # type: ignore

        # Normalize and validate columns
        df_json["variables_json"] = apply_and_check(df_json["variables_json"], normalize_json_string)
        df_json["comunidad_autonoma_id"] = apply_and_check(
            df_json["comunidad_autonoma_id"], normalize_comunidad_autonoma
        )
        df_json["provincia_id"] = apply_and_check(df_json["provincia_id"], normalize_provincia)
        df_json["codigo_estudio"] = apply_and_check(df_json["codigo_estudio"], normalize_plain_text)
        df_json["cuestionario"] = apply_and_check(df_json["cuestionario"], normalize_positive_integer)
        df_json["fecha"] = apply_and_check(df_json["fecha"], normalize_date)

        # Save to clean CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df_json.to_csv(CLEAN_CSV_PATH, index=False, sep=";", quoting=csv.QUOTE_NONE, escapechar="\\")
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
