"""Extract and transform data
Sources:
    CIS004 - Each subdirectory is a barometro general study containing a .sav file
    CIS_variable_mappings.json - Mapping of standard variable names to original variable names for each study,
        scrapped from the questionnaires in the CIS website. Check downloaders/CIS004_downloader.py
Target tables:
    barometros_generales
"""

import json
import logging

# import pickle
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_date,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_provincia,
)

RAW_SAV_DIR = Path("data") / "raw" / "CIS" / "CIS004-BarómetrosGenerales"
CLEAN_CSV_PATH = Path("data") / "clean" / "percepcion_social" / "barometros_generales.csv"
PROVINCIAS_CSV_PATH = Path("data") / "clean" / "geo" / "provincias.csv"
JSON_VARIABLE_MAP_PATH = Path("pipelines") / "extract_transform" / "percepcion_social" / "CIS_variable_mappings.json"
LOAD_FROM_RAW = True  # Set to True to load .sav files directly, False to load from pickle for debugging


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
                mapping[f"problema_personal_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problema_personal_{i}"] = f"PPERSONAL{i}"

        if "problemas_generales" in mapping:
            original_var = mapping.pop("problemas_generales")
            for i in range(1, 4):
                mapping[f"problema_espania_{i}"] = f"{original_var[:-2]}_{i}"

                # starting from study 3309, problems are mapped to standard names
                if int(code) >= 3309:
                    mapping[f"problema_espania_{i}"] = f"PESPANNA{i}"

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
                df_study = pd.read_spss(sav_file, convert_categoricals=True)
                study_code = subdir.name[2:6]
                if study_code.isdigit() and len(study_code) == 4:
                    dataframes_dict[study_code] = df_study
                else:
                    logging.warning(f"Skipping file with unexpected name: {sav_file}")
            except Exception as e:
                logging.warning(f"Error processing file {sav_file}: {e}")
                corrupted_sav_files.append(subdir)
                continue
    # summary = (
    #     f"Number of subdirectories: {len(sorted_subdirs)}\n"
    #     f"Number of files processed: {len(dataframes_dict)}\n"
    #     f"Number of subdirectories without .sav files: {len(no_sav_subdirs)}\n"
    #     f"Number of corrupted .sav files: {len(corrupted_sav_files)}\n"
    #     f"Subdirectories without .sav files: {[subdir.name for subdir in no_sav_subdirs]}\n"
    #     f"Corrupted .sav files: {[subdir.name for subdir in corrupted_sav_files]}"
    # )
    # print(summary)

    return dataframes_dict


def main():
    try:
        # Load data from .sav files or from pickle for debugging
        if LOAD_FROM_RAW:
            df_dict = load_all_sav_files(RAW_SAV_DIR)
        #     with open("data/debug/barometros_generales_dict.pkl", "wb") as f:
        #         pickle.dump(df_dict, f)
        # else:
        #     with open("data/debug/barometros_generales_dict.pkl", "rb") as f:
        #         df_dict = pickle.load(f)

        # Load variable mapping from JSON (with updates)
        studies_variable_map = get_updated_map()

        # For each dataframe, select the target columns and rename according to the mapping
        all_dfs = []
        studies_with_missing_maps = []
        for code, df in df_dict.items():  # type: ignore
            mapping = studies_variable_map.get(code)  # type: ignore
            df_study = pd.DataFrame()
            if not mapping:
                logging.warning(f"No mapping found for study code: {code}")
                continue

            for standard_name, original_name in mapping.items():
                if standard_name not in ["fecha", "url"]:
                    if original_name in df.columns:
                        df_study[standard_name] = df[original_name]
                    elif standard_name.startswith("problema_personal") or standard_name.startswith("problema_espania"):
                        variant_original_name = original_name.replace("_", "0")
                        if variant_original_name in df.columns:
                            df_study[standard_name] = df[variant_original_name]
                    elif original_name.lower() in df.columns:
                        df_study[standard_name] = df[original_name.lower()]
                    elif standard_name not in ["provincia", "comunidad_autonoma"]:
                        studies_with_missing_maps.append(code)
                        logging.warning(f"Column '{original_name}' ({standard_name}) not found in study {code}")

            df_study["codigo_estudio"] = code
            df_study["fecha"] = mapping["fecha"]
            all_dfs.append(df_study)

        df = pd.concat(all_dfs, ignore_index=True)
        # print(f"{len(studies_with_missing_maps)} missing columns in {len(set(studies_with_missing_maps))} studies")

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
        df["cuestionario"] = df["cuestionario"].apply(lambda x: str(x).split(".")[0] if pd.notnull(x) else x)

        # Replace age ranges with None and cast to integer
        age_pattern = r"De 41 a 60 años|De 26 a 40 años|Más de 60|De 18 a 25 años|N.C.|N.S."
        df["edad"] = df["edad"].astype(str).replace("nan", None).str.replace(age_pattern, "", regex=True)
        df["edad"] = df["edad"].replace("", None)
        df["edad"] = df["edad"].astype(float).astype("Int64")

        # Replace sexo values that are not 1 or 2 with 'hombre' and 'mujer' respectively
        df["sexo"] = df["sexo"].replace({1.0: "Hombre", 2.0: "Mujer", "NC": None, "N.C.": None, 98.0: None, 99.0: None})

        # For ideologia, izquierda=1, derecha=10, nsnc=None and remove floating points
        ns_nc_values = ["N.S.", "N.S", "N.C", "N.C.", "No sabe", "No contesta", 98.0, 99.0]
        df["ideologia"] = df["ideologia"].replace(ns_nc_values, None)
        df["ideologia"] = df["ideologia"].replace(
            {r"(?i).*extrema izquierda.*": 1, r"(?i).*extrema derecha.*": 10}, regex=True
        )
        df["ideologia"] = df["ideologia"].replace({r"(?i).*izquierda.*": 1, r"(?i).*derecha.*": 10}, regex=True)
        df["ideologia"] = df["ideologia"].apply(lambda x: str(x).split(".")[0] if pd.notnull(x) else x)

        # Dictionary to map values for religiosidad
        religiosidad_map = {
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

        # Map for problema_espania (study 3164 has numerical codes)
        problemas_mapping = {
            1: "El paro",
            2: "Las drogas",
            3: "La inseguridad ciudadana",
            4: "El terrorismo, ETA",
            5: "Las infraestructuras",
            6: "La sanidad",
            7: "La vivienda",
            8: "Los problemas de índole económica",
            9: "Los problemas relacionados con la calidad del empleo",
            10: "Los problemas de la agricultura, ganadería y pesca",
            11: "La corrupción y el fraude",
            12: "Las pensiones",
            13: "Los/as políticos/as en general, los partidos y la política",
            14: "Las guerras en general",
            15: "La Administración de Justicia",
            16: "Los problemas de índole social",
            17: "El racismo",
            18: "La inmigración",
            19: "La violencia contra la mujer",
            20: "Los problemas relacionados con la juventud",
            21: "La crisis de valores",
            22: "La educación",
            23: "Los problemas medioambientales",
            24: "El Gobierno y partidos o políticos/as concretos/as",
            25: "El funcionamiento de los servicios públicos",
            26: "Los nacionalismos",
            27: "Los problemas relacionados con la mujer",
            28: "El terrorismo internacional",
            29: "Las preocupaciones y situaciones personales",
            30: "Estatutos de autonomía",
            31: "Las negociaciones con ETA",
            32: "Reforma Laboral",
            33: '"Los recortes"',
            34: "Los bancos",
            35: "La subida del IVA",
            36: "Los desahucios",
            37: "El fraude fiscal",
            38: "Las hipotecas",
            39: "La Monarquía",
            40: "Las excarcelaciones",
            41: "La Ley del aborto",
            42: "Subida de tarifas energéticas",
            43: "Ébola",
            44: "Refugiados/as",
            45: "Independencia de Cataluña",
            46: "La falta de acuerdos. Situación política. Inestabilidad política",
            47: "Emigración",
            48: "Problemas relacionados con autónomos/as",
            49: "Falta de inversión en industrias e I+D",
            96: "Otras respuestas",
            97: "Ninguno",
            98: None,
            99: None,
            "N.C.": None,
            "N.S.": None,
            "N.S": None,
            "N.S/N.C.": None,
            "N.S/N.C..": None,
            "N.S./N.C.": None,
            "N.S./N.C..": None,
            "No_contesta": None,
            "No_sabe": None,
            "Otras respuestas": "Otros",
            "Otro/s": "Otros",
            "Otros problemas": "Otros",
            "Ninguno en especial": "Ninguno",
            "Ningún problema": "Ninguno",
            '"Vacas locas"': "Vacas locas",
            "'Vacas locas'": "Vacas locas",
            'El problema de las "vacas locas"': "Vacas locas",
            '"Los recortes"': "Los recortes",
            "'Los recortes'": "Los recortes",
            "Delincuencia, inseguridad ciudadana": "Delincuencia e inseguridad ciudadana",
            "Delincuencia, inseguridad ciudadana, violencia": "Delincuencia e inseguridad ciudadana, violencia",
            "Delincuencia. Inseguridad ciudadana": "Delincuencia e inseguridad ciudadana",
            "Delincuencia/inseguridad ciudadana": "Delincuencia e inseguridad ciudadana",
            "Delincuencia/inseguridad ciudadana/violencia": "Delincuencia e inseguridad ciudadana, violencia",
            "Droga": "Las drogas",
            "Drogas": "Las drogas",
            "Droga, alcoholismo": "Las drogas",
            "El peligro de la droga": "Las drogas",
            "El problema de la droga": "Las drogas",
            "Déficits de valores sociales": "Déficit de valores sociales",
            "Economía, crisis económica. Reconversión": "Económica, crisis económica. Reconversión",
            "El Gobierno y partidos o políticos concretos": "El Gobierno y partidos o políticos/as concretos",
            "El Gobierno y partidos o políticos/as concretos/as": "El Gobierno y partidos o políticos/as concretos",
            "El Gobierno, los políticos y los partidos": "El Gobierno y partidos o políticos/as concretos",
            "El Gobierno, los políticos y los partidos concretos": "El Gobierno y partidos o políticos/as concretos",
            "El Gobierno, mala gestión del COVID del Gobierno, falta de i": "El Gobierno, mala gestión del COVID del Gobierno, falta de información",  # noqa: E501
            "El orden público y seguridad ciudadana": "El orden público y la seguridad ciudadana",
            "Corrupción, fraude": "Corrupción y fraude",
            "Demasiados políticos, cargos públicos: no profesionales, muc": "Demasiados políticos, cargos públicos: no profesionales, mucho gasto",  # noqa: E501
            "El Sida": "El sida",
            "SIDA": "El sida",
            "El terrorismo. ETA": "El terrorismo, ETA",
            "Terrorismo, ETA": "El terrorismo, ETA",
            "Terrorismo": "El terrorismo",
            "emigración)": "La emigración",
            "Emigración": "La emigración",
            "Escasez y mal funcionamiento de los servicios públicos": "Escasez y/o mal funcionamiento de los servicios públicos",  # noqa: E501
            "Euro": "El euro",
            "Falta claridad en las informaciones y medidas relacionadas c": "Falta claridad en las informaciones y medidas relacionadas con la COVID-19",  # noqa: E501
            "Falta de acuerdo entre los/as políticos/as, entre el Gobiern": "Falta de acuerdo entre los/as políticos/as, entre el Gobierno central y autonómicos",  # noqa: E501
            "Fraude fiscal": "El fraude fiscal",
            "El funcionamiento/cobertura de los servicios públicos": "Funcionamiento y cobertura de los servicios públicos",  # noqa: E501
            "Funcionamiento, cobertura de los servicios públicos": "Funcionamiento y cobertura de los servicios públicos",  # noqa: E501
            "Funcionamiento/cobertura de los servicios públicos": "Funcionamiento y cobertura de los servicios públicos",  # noqa: E501
            "Impuestos, Declaración de la renta, fiscalidad": "Impuestos, declaración de la renta, fiscalidad",
            "Infraestructuras": "Infraestructura",
            "Paro": "El paro",
            "Pensiones": "Las pensiones",
            "La pensiones": "Las pensiones",
            "La contaminación; el medio ambiente": "Contaminación, medio ambiente",
            "Medio ambiente, contaminación": "Contaminación, medio ambiente",
            "Medio Ambiente": "El medio ambiente",
            "Medio ambiente": "El medio ambiente",
            "Medioambiente": "El medio ambiente",
            "Bancos": "Los bancos",
            "Monarquía": "La Monarquía",
            "La ley del aborto": "La Ley del aborto",
            "Corrupción política": "La corrupción política",
            "Corrupción y fraude": "La corrupción y el fraude",
            "Crisis de valores": "La crisis de valores",
            "La crisis económica, los problemas de índole económica": "La crisis económica, los problemas de índole económicos",  # noqa: E501
            "La crisis energética": "Crisis energética",
            "Crisis política": "La crisis política",
            "Crisis de valores sociales": "Déficit de valores sociales",
            "Racismo": "El racismo",
            "Escasez de agua/sequía": "Escasez de agua, sequía",
            "La sequía": "Escasez de agua, sequía",
            "Hipotecas": "Las hipotecas",
            "Sanidad": "La sanidad",
            "Seguridad social, pensiones, sanidad": "Seguridad Social, pensiones, sanidad",
            "Las desigualdades, incluida la de género, las diferencias de": "Las desigualdades, incluida la de género, las diferencias de clases, la pobreza",  # noqa: E501
            "La inseguridad ciudadana, la delincuencia, la falta de civis": "La inseguridad ciudadana, la delincuencia, la falta de civismo",  # noqa: E501
            "Los cambios de hábitos en mi vida cotidiana (no hacer vida n": "Los cambios de hábitos en mi vida cotidiana (no hacer vida normal, etc.)",  # noqa: E501
            "Los ciudadanos/as, el comportamiento, egoísmo, poco cívicos,": "Los ciudadanos/as, el comportamiento, egoísmo, poco cívicos, bulos",  # noqa: E501
            "Los deshaucios": "Los desahucios",
            "Los peligros para la salud: COVID-19. El coronavirus. Falta": "Los peligros para la salud: COVID-19. El coronavirus. Falta de recursos suficientes para hacer frente a la pandemia",  # noqa: E501
            "Los problemas relacionados con la juventud. Falta de apoyo y": "Los problemas relacionados con la juventud. Falta de apoyo y oportunidades a los/as jóvenes",  # noqa: E501
            "Los problemas relacionados con la mujer. La violencia de gén": "Los problemas relacionados con la mujer. La violencia de género",  # noqa: E501
            "Los problemas sobre la gestión de la vacunación, lentitud, r": "Los problemas sobre la gestión de la vacunación, lentitud, retraso",  # noqa: E501
            "Los/as ciudadanos/as, comportamiento, egoísmo, cada uno/a a": "Los/as ciudadanos/as, comportamiento, egoísmo, cada uno/a a lo suyo/poco cívicos, bulos",  # noqa: E501
            "Poca conciencia ciudadana (falta de civismo, de sentido espí": "Poca conciencia ciudadana (falta de civismo, de sentido espíritu cívico)",  # noqa: E501
            "Problemas psicológicos derivados de la pandemia (preocupacio": "Problemas psicológicos derivados de la pandemia (preocupaciones, soledad, tristeza,  desamparo, etc.)",  # noqa: E501
            "Limitaciones en las relaciones sociales, familiares, amigos/": "Limitaciones en las relaciones sociales, familiares, amigos",  # noqa: E501
        }

        problemas_columns = [
            "problema_espania_1",
            "problema_espania_2",
            "problema_espania_3",
            "problema_personal_1",
            "problema_personal_2",
            "problema_personal_3",
        ]

        # Remove {} and trailing spaces and map values in problemas columns
        for column in problemas_columns:
            df[column] = df[column].str.replace(r"\{.*$", "", regex=True).str.strip()
            df[column] = df[column].str.strip().replace(problemas_mapping)

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
        df["religiosidad"] = apply_and_check_dict(df["religiosidad"], religiosidad_map)
        df["problema_espania_1"] = apply_and_check(df["problema_espania_1"], normalize_plain_text)
        df["problema_espania_2"] = apply_and_check(df["problema_espania_2"], normalize_plain_text)
        df["problema_espania_3"] = apply_and_check(df["problema_espania_3"], normalize_plain_text)
        df["problema_personal_1"] = apply_and_check(df["problema_personal_1"], normalize_plain_text)
        df["problema_personal_2"] = apply_and_check(df["problema_personal_2"], normalize_plain_text)
        df["problema_personal_3"] = apply_and_check(df["problema_personal_3"], normalize_plain_text)

        # Fill up comunidad_autonoma_id for entries with provincia_id but missing comunidad_autonoma_id
        provincias_df = pd.read_csv(PROVINCIAS_CSV_PATH, sep=";")
        provincia_to_ccaa = dict(zip(provincias_df["provincia_id"], provincias_df["comunidad_autonoma_id"]))
        mask = df["comunidad_autonoma_id"].isna() & df["provincia_id"].notna()
        df.loc[mask, "comunidad_autonoma_id"] = df.loc[mask, "provincia_id"].map(provincia_to_ccaa)

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
