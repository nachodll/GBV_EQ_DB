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
    apply_and_check_dict,  # type: ignore
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_plain_text,
    normalize_positive_integer,
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

        # cues is always mapped to "CUES"
        mapping["cuestionario"] = "CUES"

        # ideologia is not extracted for studies before 1320 due to different scale
        if int(code) < 1320 and "ideologia" in mapping:
            mapping.pop("ideologia")

        # breakdown multiple answer questions into separate columns
        if "problemas_personales" in mapping:
            original_var = mapping.pop("problemas_personales")
            for i in range(1, 4):
                mapping[f"problemas_personal_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problemas_personal_{i}"] = f"PPERSONAL_{i}"

        if "problemas_generales" in mapping:
            original_var = mapping.pop("problemas_generales")
            for i in range(1, 4):
                mapping[f"problemas_espania_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problemas_espania_{i}"] = f"PESPANNA_{i}"

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

        # For each dataframe, select the target columns and rename according to the mapping
        all_dfs = []
        studies_with_missing_maps = []
        for code, df in df_dict.items():
            mapping = studies_variable_map.get(code)  # type: ignore
            df_study = pd.DataFrame()
            if not mapping:
                logging.warning(f"No mapping found for study code: {code}")
                continue

            for standard_name, original_name in mapping.items():
                if standard_name not in ["fecha", "url"]:
                    if original_name in df.columns:
                        df_study[standard_name] = df[original_name]
                    elif standard_name.startswith("problemas_personal") or standard_name.startswith(
                        "problemas_espania"
                    ):
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

        # Drop floating points in cuestionario
        df["cuestionario"] = df["cuestionario"].apply(lambda x: str(x).split(".")[0] if pd.notnull(x) else x)  # type: ignore

        # Replace age ranges with None and cast to integer
        age_pattern = r"De 41 a 60 años|De 26 a 40 años|Más de 60|De 18 a 25 años|N.C.|N.S."
        df["edad"] = df["edad"].astype(str).replace("nan", None).str.replace(age_pattern, "", regex=True)  # type: ignore
        df["edad"] = df["edad"].replace("", None)  # type: ignore
        df["edad"] = df["edad"].astype(float).astype("Int64")  # type: ignore

        # Replace sexo values that are not 1 or 2 with 'hombre' and 'mujer' respectively
        df["sexo"] = df["sexo"].replace(  # type: ignore
            {1.0: "Hombre", 2.0: "Mujer", "NC": None, "N.C.": None, 98.0: None, 99.0: None}
        )

        # For ideologia, izquierda=1, derecha=10, nsnc=None and remove floating points
        ns_nc_values = ["N.S.", "N.S", "N.C", "N.C.", "No sabe", "No contesta", 98.0, 99.0]  # type: ignore
        df["ideologia"] = df["ideologia"].replace(ns_nc_values, None)  # type: ignore
        df["ideologia"] = df["ideologia"].replace(  # type: ignore
            {r"(?i).*extrema izquierda.*": 1, r"(?i).*extrema derecha.*": 10}, regex=True
        )
        df["ideologia"] = df["ideologia"].replace(  # type: ignore
            {r"(?i).*izquierda.*": 1, r"(?i).*derecha.*": 10}, regex=True
        )
        df["ideologia"] = df["ideologia"].apply(lambda x: str(x).split(".")[0] if pd.notnull(x) else x)  # type: ignore

        # Dictionary to map values for religiosidad
        religiosidad_map = {  # type: ignore
            "Ateo/a": "Ateo/a",
            "Ateo": "Ateo/a",
            "Ateo/a (Niegan la existencia de Dios)": "Ateo/a",
            "Ateo/a (niegan la existencia de Dios)": "Ateo/a",
            4.0: "Ateo/a",
            "Agnóstico/a": "Agnóstico/a",
            "Agnóstico/a (No niegan la existencia de Dios pero tampoco la": "Agnóstico/a",
            "Agnóstico/a (no niegan la existencia de Dios pero tampoco la": "Agnóstico/a",
            "Agnóstico/a (no niegan la existencia de Dios pero tampoco la descartan)": "Agnóstico/a",
            "Indiferente, no creyente": "Indiferente, no creyente",
            "No creyente": "Indiferente, no creyente",
            "No creyente {No crey.}": "Indiferente, no creyente",
            "Indiferente": "Indiferente, no creyente",
            "Indiferente {Indif.}": "Indiferente, no creyente",
            3.0: "Indiferente, no creyente",
            "Católico/a": "Católico/a",
            "Católico": "Católico/a",
            "Católico {Cat.}": "Católico/a",
            1.0: "Católico/a",
            "Católico/a practicante": "Católico/a practicante",
            "Católico practicante": "Católico/a practicante",
            "Muy buen católico": "Católico/a practicante",
            "Católico poco prácticamente": "Católico/a practicante",
            "Católico/a no practicante": "Católico/a no practicante",
            "Católico no practicante": "Católico/a no practicante",
            "Creyente de otra religión": "Creyente de otra religión",
            "Creyente de otras religiones": "Creyente de otra religión",
            "Creyente otra religión": "Creyente de otra religión",
            "Creyente de otra religión {Crey.}": "Creyente de otra religión",
            "Creyente practicante de otras religiones": "Creyente de otra religión",
            "Creyente no practicante de otras religiones": "Creyente de otra religión",
            "Otras religiones": "Creyente de otra religión",
            2.0: "Creyente de otra religión",
            "Otra respuesta": None,
            "Otras respuestas": None,
            "Otra respuesta {Otra}": None,
            "N.C.": None,
            "N.C": None,
            "N.S.": None,
            9.0: None,
        }

        # Rename some columns
        df = df.rename(columns={"provincia": "provincia_id", "comunidad_autonoma": "comunidad_autonoma_id"})

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["fecha"] = apply_and_check(df["fecha"], normalize_date)
        df["codigo_estudio"] = apply_and_check(df["codigo_estudio"], normalize_plain_text)
        df["cuestionario"] = apply_and_check(df["cuestionario"], normalize_positive_integer)
        df["edad"] = apply_and_check(df["edad"], normalize_positive_integer)
        df["sexo"] = apply_and_check_dict(
            df["sexo"], {"Hombre": "Hombre", "Mujer": "Mujer", "hombre": "Hombre", "mujer": "Mujer"}
        )
        df["ideologia"] = apply_and_check(df["ideologia"], normalize_positive_integer)
        df["religiosidad"] = apply_and_check_dict(df["religiosidad"], religiosidad_map)  # type: ignore

        # keep only some columns
        target_columns = [
            "comunidad_autonoma_id",
            "provincia_id",
            "fecha",
            "codigo_estudio",
            "cuestionario",
            "edad",
            "sexo",
            "ideologia",
            "religiosidad",
        ]
        df = df[target_columns]

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
