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
    normalize_comunidad_autonoma,
    normalize_provincia,
)

RAW_SAV_DIR = Path("data") / "raw" / "CIS" / "CIS004-BarómetrosGenerales"
CLEAN_CSV_PATH = Path("data") / "clean" / "percepcion_social" / "barometros_generales.csv"
JSON_VARIABLE_MAP_PATH = Path("pipelines") / "extract_transform" / "percepcion_social" / "CIS_variable_mappings.json"
LOAD_FROM_RAW = False  # Set to True to load .sav files directly, False to load from pickle for debugging


def get_map_from_json() -> dict[int, dict[str, str]]:
    """Returns a dictionary mapping study codes to variable mappings from the JSON file."""
    with open(JSON_VARIABLE_MAP_PATH, "r", encoding="utf-8") as f:
        variable_mapps = json.load(f)
    return variable_mapps


def get_updated_map() -> dict[int, dict[str, str]]:
    """Updates the variable mapping with information that could not be automatically extracted."""
    variable_maps = get_map_from_json()

    for code, mapping in variable_maps.items():
        # comunidad_autonoma is alwasys mapped to "CCAA" except if its mapped to REGION in the JSON
        if not ("comunidad_autonoma" in mapping and mapping["comunidad_autonoma"] == "REGION"):
            mapping["comunidad_autonoma"] = "CCAA"

        # provincia is always mapped to "PROV"
        mapping["provincia"] = "PROV"

        # breakdown multiple answer questions into separate columns
        if "problemas_personales" in mapping:
            original_var = mapping.pop("problemas_personales")
            for i in range(1, 4):
                mapping[f"problemas_personales_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problemas_personales_{i}"] = f"PPERSONAL_{i}"

        if "problemas_generales" in mapping:
            original_var = mapping.pop("problemas_generales")
            for i in range(1, 4):
                mapping[f"problemas_generales_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problemas_generales_{i}"] = f"PESPANNA_{i}"

    return variable_maps


def load_all_sav_files(directory: Path) -> dict[str, pd.DataFrame]:
    """Load all .sav files from the given directory and return a dictionary of dataframes."""

    dataframes_dict = {}
    no_sav_subdirs = []
    corrupted_sav_files = []
    sorted_subdirs = sorted([d for d in directory.iterdir() if d.is_dir()])
    for subdir in sorted_subdirs:
        sav_files = [f for f in subdir.iterdir() if f.is_file() and f.suffix == ".sav"]
        if not sav_files:
            no_sav_subdirs.append(subdir)  #  type: ignore
            continue
        for sav_file in sav_files:
            try:
                df_study = pd.read_spss(sav_file, convert_categoricals=True)  # type: ignore
                study_code = subdir.name[2:6]
                if study_code.isdigit() and len(study_code) == 4:
                    dataframes_dict[study_code] = df_study
                else:
                    logging.warning(f"Skipping file with unexpected name: {sav_file}")
            except Exception as e:
                logging.error(f"Error processing file {sav_file}: {e}")
                corrupted_sav_files.append(subdir)  # type: ignore
                continue
    summary = (
        f"Number of subdirectories: {len(sorted_subdirs)}\n"
        f"Number of files processed: {len(dataframes_dict)}\n"  # type: ignore
        f"Number of subdirectories without .sav files: {len(no_sav_subdirs)}\n"  # type: ignore
        f"Number of corrupted .sav files: {len(corrupted_sav_files)}\n"  # type: ignore
        f"Subdirectories without .sav files: {[subdir.name for subdir in no_sav_subdirs]}\n"  # type: ignore
        f"Corrupted .sav files: {[subdir.name for subdir in corrupted_sav_files]}"  # type: ignore
    )
    print(summary)

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

        # Load variable mapping from JSON (with updates)
        studies_variable_map = get_updated_map()

        # For each dataframe, rename columns according to the mapping and concatenate
        all_dfs = []
        studies_with_missing_maps = []
        for code, df in df_dict.items():
            mapping = studies_variable_map.get(code)  # type: ignore
            df_study = pd.DataFrame()
            if not mapping:
                print("No mapping found for study code:", code)
                continue

            for standard_name, original_name in mapping.items():
                if standard_name not in ["fecha", "url"]:
                    if original_name in df.columns:
                        df_study[standard_name] = df[original_name]
                    elif standard_name.startswith("problemas_personales") or standard_name.startswith(
                        "problemas_generales"
                    ):  # type: ignore
                        variant_original_name = original_name.replace("_", "0")
                        if variant_original_name in df.columns:
                            df_study[standard_name] = df[variant_original_name]
                    elif original_name.lower() in df.columns:
                        df_study[standard_name] = df[original_name.lower()]
                    elif standard_name not in ["provincia", "comunidad_autonoma"]:
                        studies_with_missing_maps.append(code)  # type: ignore
                        print(f"Column '{original_name}' ({standard_name}) not found in study {code}")

            df_study["codigo_estudio"] = code
            df_study["fecha"] = mapping["fecha"]
            all_dfs.append(df_study)  # type: ignore

        df = pd.concat(all_dfs, ignore_index=True)  # type: ignore
        print(f"{len(studies_with_missing_maps)} missing columns in {len(set(studies_with_missing_maps))} studies")  # type: ignore

        # Delete all () and {} in comunidad_autonoma and account for typos
        df["comunidad_autonoma"] = df["comunidad_autonoma"].str.replace(r"[\(\{].*?[\)\}]", "", regex=True).str.strip()
        df["comunidad_autonoma"] = (
            df["comunidad_autonoma"]
            .str.replace("Exremadura", "Extremadura")
            .str.replace("E5remadura", "Extremadura")
            .str.replace("Castilla-Len", "Castilla y León")
        )

        # Delete all () and {} in provincia and fix typos and encoding issues
        df["provincia"] = df["provincia"].str.replace(r"[\(\{].*?[\)\}]", "", regex=True).str.strip()
        df["provincia"] = (
            df["provincia"]
            .str.replace("Logroño", "La Rioja")
            .str.replace("Logro�o", "La Rioja")
            .str.replace("Santander", "Cantabria")
            .str.replace("SANTANDER", "Cantabria")
            .str.replace("Santader", "Cantabria")
            .str.replace("Salamaca", "Salamanca")
            .str.replace("M laga", "Málaga")
            .str.replace("Almer�a", "Almería")
            .str.replace("Le�n", "León")
            .str.replace("OREN.S.E", "Ourense")
            .str.replace("Coru�a", "Coruña")
            .str.replace("Oviedo", "Asturias")
            .str.replace("OVIEDO", "Asturias")
            .str.replace("Ja�n", "Jaén")
            .str.replace("Guip�zcoa", "Guipúzcoa")
            .str.replace("�lava", "Álava")
            .str.replace("C�rdoba", "Córdoba")
            .str.replace("C�diz", "Cádiz")
            .str.replace("Castell�n de la Plana", "Castellón de la Plana")
            .str.replace("C�ceres", "Cáceres")
            .str.replace("M�laga", "Málaga")
        )

        # Validate and normalize columns
        df["comunidad_autonoma"] = apply_and_check(df["comunidad_autonoma"], normalize_comunidad_autonoma)
        df["provincia"] = apply_and_check(df["provincia"], normalize_provincia)

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
