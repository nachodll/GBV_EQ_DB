"""Extract and transform data
Sources:
    CIS004
Target tables:
    barometros_generales
"""

import json
import logging
import pickle
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
)

RAW_SAV_DIR = Path("data") / "raw" / "CIS" / "CIS004-BarómetrosGenerales"
CLEAN_CSV_PATH = Path("data") / "clean" / "percepcion_social" / "barometros_generales.csv"
JSON_VARIABLE_MAP_PATH = Path("data") / "raw" / "CIS" / "CIS004-BarómetrosGenerales" / "CIS_variable_mappings.json"
LOAD_FROM_RAW = True  # Set to True to load .sav files directly, False to load from pickle for debugging


def get_map_from_json() -> dict[int, dict[str, str]]:
    """Returns a dictionary mapping study codes to variable mappings from the JSON file."""
    with open(JSON_VARIABLE_MAP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data)
    return data


def load_all_sav_files(directory: Path) -> dict[str, pd.DataFrame]:
    """Load all .sav files from the given directory and return a dictionary of dataframes."""

    dataframes_dict = {}
    no_sav_subdirs = []
    corrupted_sav_files = []
    for subdir in sorted(directory.iterdir()):
        if subdir.is_dir():
            sav_files = [f for f in subdir.iterdir() if f.is_file() and f.suffix == ".sav"]
            if not sav_files:
                no_sav_subdirs.append(subdir)  #  type: ignore
            for sav_file in sav_files:
                try:
                    df_study = pd.read_spss(sav_file)
                    study_code = subdir.name[2:6]
                    if study_code.isdigit() and len(study_code) == 4:
                        dataframes_dict[study_code] = df_study
                    else:
                        logging.warning(f"Skipping file with unexpected name: {sav_file}")
                except Exception as e:
                    logging.error(f"Error processing file {sav_file}: {e}")
                    corrupted_sav_files.append(subdir)  # type: ignore
                    continue

    print(f"Number of subdirectories: {len(list(directory.iterdir()))}")
    print(f"Number of files processed: {len(dataframes_dict)}")  # type: ignore
    print(f"Number of subdirectories without .sav files: {len(no_sav_subdirs)}")  # type: ignore
    print(f"Number of corrupted .sav files: {len(corrupted_sav_files)}")  # type: ignore
    print(f"Subdirectories without .sav files: {[subdir.name for subdir in no_sav_subdirs]}")  # type: ignore
    print(f"Corrupted .sav files: {[subdir.name for subdir in corrupted_sav_files]}")  # type: ignore

    return dataframes_dict  # type: ignore


def main():
    try:
        # Load data from .sav files or from pickle for debugging
        if LOAD_FROM_RAW:
            df_dict = load_all_sav_files(RAW_SAV_DIR)
            with open("data/debug/barometros_generales_dict.pkl", "wb") as f:
                pickle.dump(df_dict, f)
        else:
            with open("data/debug/barometros_generales_dict.pkl", "rb") as f:
                df_dict = pickle.load(f)

        # Load variable mapping from JSON. Each study code maps to a dict of {standard_name: original_name}
        studies_variable_map = get_map_from_json()

        # For each dataframe, rename columns according to the mapping and concatenate
        all_dfs = []
        for code, df in df_dict.items():
            mapping = studies_variable_map.get(code)  # type: ignore
            df_study = pd.DataFrame()
            if not mapping:
                # print("No mapping found for study code:", code)
                continue

            print(f"Processing study code: {code}")

            for standard_name, original_name in mapping.items():
                if original_name in df.columns:
                    df_study[standard_name] = df[original_name]

            df_study["codigo_estudio"] = code
            df_study["fecha"] = mapping["fecha"]

            all_dfs.append(df_study)  # type: ignore

        df = pd.concat(all_dfs, ignore_index=True)  # type: ignore

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
