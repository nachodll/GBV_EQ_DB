"""Extract and tansform data
Sources:
    MINEDU001, (post 2011)
    MINEDU002  (pre 2011)
Target tables:
    matriculados_educacion_no_universitaria
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_plain_text,
    normalize_positive_integer,
    normalize_provincia,
)

RAW_CSV_DIR_POST_2011 = Path("data") / "raw" / "MINEDU" / "MINEDU001-AlumnadoNoUniversitario"
RAW_XLS_DIR_PRE_2011 = Path("data") / "raw" / "MINEDU" / "MINEDU002-AlumnadoNoUniversatarioPre2011"
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "matriculados_educacion_no_universitaria.csv"


def read_sheet_from_xls(file: Path, sheet_name: str) -> pd.DataFrame:
    """Read a specific sheet from an XLS file and return it as a DataFrame."""
    try:
        df = pd.read_excel(file, sheet_name=sheet_name, header=None)  # type: ignore
        if df.empty:
            raise ValueError(f"The sheet '{sheet_name}' in {file} is empty.")

        # Fill forward 'ensenianza' column
        df.iloc[3] = df.iloc[3].ffill()
        for col in df.columns:
            if df.iloc[3, col] == "Ciclos Formativos de FP" or df.iloc[3, col] == "Ciclos Formativos de F.P.":  # type: ignore
                df.iloc[3, col] = "CF FP " + df.iloc[4, col]  # type: ignore

        # Slice the DataFrame to extract headers and data
        start_idx = df[df[0].str.lower() == "total"].index[0]  # type: ignore
        end_idx = df[df[0].str.lower() == "melilla"].index[0]  # type: ignore
        ensenianza_x_header = df.iloc[3, 1:].copy()  # type: ignore
        ensenianza_x_header = ensenianza_x_header.astype(str).str.replace(r"[\r\n]+", " ", regex=True)
        provincia_y_header = df.iloc[start_idx : end_idx + 1, 0].copy()  # type: ignore
        numbers_df = df.iloc[start_idx : end_idx + 1, 1:].copy()

        all_records = []
        for col in numbers_df.columns:
            ensenianza = ensenianza_x_header[col]  # type: ignore
            for row in numbers_df.index:
                provincia = provincia_y_header[row]  # type: ignore
                matriculados = numbers_df[col][row]  # type: ignore
                all_records.append(  # type: ignore
                    {
                        "ensenianza": ensenianza,
                        "provincia_id": provincia,
                        "matriculados": matriculados,
                    }
                )
        return pd.DataFrame(all_records)
    except FileNotFoundError as e:
        logging.error(f"File not found: {file}. Error: {e}")
        raise
    except ValueError as e:
        logging.error(f"Could not read sheet '{sheet_name}' from {file}: {e}")
        raise


def read_pre_2011_data(directory: Path) -> pd.DataFrame:
    """Read pre-2011 XLS data from the xls files in the specified directory.
    Assumes each file name is the corresponding academic year (e.g., "2010-2011.xls")."""

    # Read all xls files in the first directory into a single DataFrame
    xls_files_pre_2011 = list(directory.glob("*.xls")) + list(directory.glob("*.xlsx"))
    xls_files_pre_2011 = [f for f in xls_files_pre_2011 if not f.name.startswith("~$")]
    if not xls_files_pre_2011:
        raise FileNotFoundError(f"No XLS files found in {directory}")

    sheet_names_dicts = {
        "2010-11": {
            "2. Alumnado Público": "Público",
            "3. Alumnado Privado": "Privado",
            "4. Alumnado Privado Concer": "Privado concertado",
            "5. Alumnado Privado No Concer ": "Privado no concertado",
        },
        "2009-10": {
            "2. Alumnado Público": "Público",
            "3. Alumnado Privado": "Privado",
            "4. Alumnado Privado Concer": "Privado concertado",
            "5. Alumnado Privado No Concer ": "Privado no concertado",
        },
        "2008-09": {
            "2. Alumnado Públicos": "Público",
            "3. Alumnado Privados": "Privado",
            "4. Alumnado Privados Conc.": "Privado concertado",
            "5. Alumnado Privados no Conc.": "Privado no concertado",
        },
        "2007-08": {
            "2. Alumnado Público": "Público",
            "3. Alumnado Privado": "Privado",
            "4. Alumnado Privado Concer": "Privado concertado",
            "5. Alumnado Privado No Concer ": "Privado no concertado",
        },
        "2006-07": {
            "Tabla 2": "Público",
            "Tabla 3": "Privado",
            "Tabla 4": "Privado concertado",
            "Tabla 5": "Privado no concertado",
        },
        "2005-06": {
            "2a. Alumnado Público": "Público",
            "2b. Alumnado Público": "Público",
            "3a. Alumnado Privado": "Privado",
            "3b. Alumnado Privado": "Privado",
            "4a. Alumnado Privado Concer": "Privado concertado",
            "4b. Alumnado Privado Concer": "Privado concertado",
            "5a. Alumnado Privado No Concer ": "Privado no concertado",
            "5b. Alumnado Privado No Concer": "Privado no concertado",
        },
        "2004-05": {
            "2a. Alumnado Público": "Público",
            "2b. Alumnado Público": "Público",
            "3a. Alumnado Privado": "Privado",
            "3b. Alumnado Privado": "Privado",
            "4a. Alumnado Privado Concer": "Privado concertado",
            "4b. Alumnado Privado Concer": "Privado concertado",
            "5a. Alumnado Privado No Concer ": "Privado no concertado",
            "5b. Alumnado Privado No Concer": "Privado no concertado",
        },
        "2003-04": {
            "2a. Alumnado Público": "Público",
            "2b. Alumnado Público": "Público",
            "3a. Alumnado Privado": "Privado",
            "3b. Alumnado Privado": "Privado",
            "4a. Alumnado Privado Concer": "Privado concertado",
            "4b. Alumnado Privado Concer": "Privado concertado",
            "5a. Alumnado Privado No Concer ": "Privado no concertado",
            "5b. Alumnado Privado No Concer": "Privado no concertado",
        },
        "2002-03": {
            "2a. Alumnado Público": "Público",
            "2b. Alumnado Público": "Público",
            "3a. Alumnado Privado": "Privado",
            "3b. Alumnado Privado": "Privado",
            "4a. Alumnado Privado Concer": "Privado concertado",
            "4b. Alumnado Privado Concer": "Privado concertado",
            "5a. Alumnado Privado No Concer ": "Privado no concertado",
            "5b. Alumnado Privado No Concer": "Privado no concertado",
        },
        "2001-02": {
            "Tabla 2": "Público",
            "Tabla 3": "Privado",
            "Tabla 4": "Privado concertado",
            "Tabla 5": "Privado no concertado",
        },
        "2000-01": {
            "Tabla 2a": "Público",
            "Tabla 2b": "Público",
            "Tabla 3a": "Privado",
            "Tabla 3b": "Privado",
            "Tabla 4a": "Privado concertado",
            "Tabla 4b": "Privado concertado",
            "Tabla 5a": "Privado no concertado",
            "Tabla 5b": "Privado no concertado",
        },
        "1999-00": {
            "Tabla 2": "Público",
            "Tabla 3": "Privado",
        },
    }

    dfs = []
    for file in xls_files_pre_2011:
        for sheet_name, titularidad in sheet_names_dicts[file.stem].items():
            sheet_df = read_sheet_from_xls(file, sheet_name)
            sheet_df["titularidad"] = titularidad
            sheet_df["curso"] = file.stem
            dfs.append(sheet_df)  # type: ignore

    df = pd.concat(dfs, ignore_index=True)  # type: ignore

    return df


def read_post_2011_data(directory: Path) -> pd.DataFrame:
    """Read post-2011 CSV data from the csvs in the specified directory.
    Assumes each file name is the corresponding academic year (e.g., "2012-2013.csv")."""

    # Read all csv files in the first directory into a single DataFrame
    csv_files_post_2011 = list(RAW_CSV_DIR_POST_2011.glob("*.csv"))
    if not csv_files_post_2011:
        raise FileNotFoundError(f"No CSV files found in {RAW_CSV_DIR_POST_2011}")
    dfs = []
    for file in csv_files_post_2011:
        df_file = pd.read_csv(file, sep=";", thousands=".")  # type: ignore
        df_file["curso"] = file.stem
        dfs.append(df_file)  # type: ignore
    df = pd.concat(dfs, ignore_index=True)  # type: ignore

    # Rename columns
    df.rename(
        columns={
            "Titularidad/financiación del centro": "titularidad",
            "Sexo": "sexo",
            "Comunidad autónoma/provincia": "provincia_id",
            "Enseñanza": "ensenianza",
            "Total": "matriculados",
        },
        inplace=True,
    )

    # Adapt 'titularidad' column to expected values
    df["titularidad"] = df["titularidad"].replace(  # type: ignore
        {
            "CENTROS PÚBLICOS": "Público",
            "CENTROS PRIVADOS": "Privado",
            "Enseñanza privada concertada": "Privado concertado",
            "Enseñanza privada no concertada": "Privado no concertado",
        }
    )

    # Normalize values in 'ensenianza' column
    df["ensenianza"] = df["ensenianza"].str.replace(r"\s*\(\d+\)$", "", regex=True)  # type: ignore

    # Strip numbers from provincia_id column
    df["provincia_id"] = df["provincia_id"].astype(str).str.replace(r"^\d+\s*", "", regex=True)

    # Drop rows with aggregated data
    df = df[~df["titularidad"].isin(["TODOS LOS CENTROS"])]  # type: ignore
    df = df[df["sexo"] != "AMBOS SEXOS"]

    return df


def main():
    try:
        df_post_2011 = read_post_2011_data(RAW_CSV_DIR_POST_2011)
        df_pre_2011 = read_pre_2011_data(RAW_XLS_DIR_PRE_2011)
        df = pd.concat([df_post_2011, df_pre_2011], ignore_index=True)  # type: ignore

        # Strip numbers (e.g.(4)) from 'provincia_id' values and 'ensenianza' values
        df["provincia_id"] = df["provincia_id"].str.replace(r"\s*\(\d+\)$", "", regex=True).str.strip()  # type: ignore
        df["ensenianza"] = df["ensenianza"].str.replace(r"\s*\(\d+\)$", "", regex=True).str.strip()  # type: ignore

        # Normalize 'ensenianza' values
        df["ensenianza"] = df["ensenianza"].replace(  # type: ignore
            {
                "E. Infantil Primer Ciclo": "E. Infantil - Primer ciclo",
                "E. Infantil Segundo Ciclo": "E. Infantil - Segundo ciclo",
                "Educación Infantil 1er Ciclo": "E. Infantil - Primer ciclo",
                "Educación Infantil 2º Ciclo": "E. Infantil - Segundo ciclo",
                "CF FP Básica": "CF Grado Básico",
                "CF FP Grado Medio": "CF Grado Medio",
                "C.F. FP Grado Medio": "CF Grado Medio",
                "C.F. Grado Medio": "CF Grado Medio",
                "CF FP Grado Medio a distancia": "CF Grado Medio a distancia",
                "CF FP Grado Medio distancia": "CF Grado Medio a distancia",
                "C.F. FP a distancia Grado Medio": "CF Grado Medio a distancia",
                "C.F. Grado Medio/ Mod. II a distancia": "CF Grado Medio a distancia",
                "CF FP Grado Superior": "CF Grado Superior",
                "C.F. FP Grado Superior": "CF Grado Superior",
                "C.F. Grado Superior": "CF Grado Superior",
                "CF FP Grado Superior a distancia": "CF Grado Superior a distancia",
                "CF FP Grado Superior distancia": "CF Grado Superior a distancia",
                "C.F. FP a distancia Grado Superior": "CF Grado Superior a distancia",
                "C.F. Grado Sup./ Mod. III a distancia": "CF Grado Superior a distancia",
                "C.F. Grado Sup./ Mod. III  a distancia": "CF Grado Superior a distancia",
                "Educación Primaria": "E. Primaria",
                "Educ. Especial": "Educación Especial",
                "E.S.O.": "ESO",
                "Programas de Garantía Social": "Programas Garantía Social",
                "Bachillerato a Distancia": "Bachillerato a distancia",
            }
        )

        # Comunidades with one province are transformed to its corresponding province
        uniprovince_list = ["asturias", "murcia", "navarra", "madrid"]
        df["provincia_id"] = df["provincia_id"].apply(  # type: ignore
            lambda x: next((prov for prov in uniprovince_list if prov in str(x).lower()), x)  # type: ignore
        )

        # Normalize 'matriculados' column 0 values
        df["matriculados"] = df["matriculados"].replace(["..", -1], 0)  # type: ignore

        # Drop rows with aggregated data for provincia
        rows_to_drop = [
            "total",
            "andalucía",
            "aragón",
            "canarias",
            "castilla y león",
            "castilla-la mancha",
            "cataluña",
            "valencia",
            "extremadura",
            "galicia",
            "país vasco",
        ]
        df = df[~df["provincia_id"].apply(lambda x: any(word in str(x).lower() for word in rows_to_drop))]  # type: ignore

        # Drop rows with aggregated data for ensenianza
        df = df[df["ensenianza"] != "TOTAL"]

        # Validate and normalize columns
        df["titularidad"] = apply_and_check_dict(
            df["titularidad"],
            {
                "Público": "Público",
                "Privado": "Privado",
                "Privado concertado": "Privado concertado",
                "Privado no concertado": "Privado no concertado",
            },
        )
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["ensenianza"] = apply_and_check(df["ensenianza"], normalize_plain_text)
        df["matriculados"] = apply_and_check(df["matriculados"], normalize_positive_integer)

        # Save cleaned CSV
        CLEAN_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(CLEAN_CSV_PATH, index=False, sep=";")
        logging.info(f"Data saved to {CLEAN_CSV_PATH}")

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
