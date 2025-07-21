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


def main():
    try:
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

        # Normalize values in 'ensenianza' column
        df["ensenianza"] = df["ensenianza"].str.replace(r"\s*\(\d+\)$", "", regex=True)  # type: ignore
        df["ensenianza"] = df["ensenianza"].replace(  # type: ignore
            {
                "E. Infantil Primer Ciclo": "E. Infantil - Primer ciclo",
                "E. Infantil Segundo Ciclo": "E. Infantil - Segundo ciclo",
                "CF FP Básica": "CF Grado Básico",
                "CF FP Grado Medio": "CF Grado Medio",
                "C.F. FP Grado Medio": "CF Grado Medio",
                "CF FP Grado Medio a distancia": "CF Grado Medio a distancia",
                "C.F. FP a distancia Grado Medio": "CF Grado Medio a distancia",
                "CF FP Grado Superior": "CF Grado Superior",
                "C.F. FP Grado Superior": "CF Grado Superior",
                "CF FP Grado Superior a distancia": "CF Grado Superior a distancia",
                "C.F. FP a distancia Grado Superior": "CF Grado Superior a distancia",
            }
        )

        # Drop numbers from provincia_id column
        df["provincia_id"] = df["provincia_id"].astype(str).str.replace(r"^\d+\s*", "", regex=True)

        # Replace comunidades autonomas with one provincia to the provincia name
        df["provincia_id"] = df["provincia_id"].replace(  # type: ignore
            {
                "MURCIA, REGIÓN DE": "MURCIA",
                "NAVARRA (Comunidad Foral de) (4)": "NAVARRA",
                "NAVARRA (Comunidad Foral de) (3)": "NAVARRA",
                "NAVARRA (Comunidad Foral de)": "NAVARRA",
                "NAVARRA, COMUNIDAD FORAL DE": "NAVARRA",
                "MADRID, COMUNIDAD DE": "MADRID",
                "ASTURIAS, PRINCIPADO DE": "ASTURIAS",
            }
        )

        # Drop rows with aggregated data for titularidad
        num_rows_before = len(df)
        df = df[~df["titularidad"].isin(["TODOS LOS CENTROS", "CENTROS PRIVADOS"])]  # type: ignore
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'titularidad'.")

        # Drop rows with aggregated data for sexo
        num_rows_before = len(df)
        df = df[df["sexo"] != "AMBOS SEXOS"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'sexo'.")

        # Drop rows with aggregated data for provincia
        num_rows_before = len(df)
        rows_to_drop = [
            "TOTAL",
            "ANDALUCÍA",
            "ARAGÓN",
            "CANARIAS",
            "CASTILLA Y LEÓN",
            "CASTILLA-LA MANCHA",
            "CATALUÑA",
            "COMUNITAT VALENCIANA",
            "EXTREMADURA",
            "GALICIA",
            "PAÍS VASCO",
        ]
        df = df[~df["provincia_id"].isin(rows_to_drop)]  # type: ignore
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'provincia'.")

        # Drop rows with aggregated data for ensenianza
        num_rows_before = len(df)
        df = df[df["ensenianza"] != "TOTAL"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'ensenianza'.")

        # Validate and normalize columns
        df["titularidad"] = apply_and_check_dict(
            df["titularidad"],
            {
                "CENTROS PÚBLICOS": "Público",
                "Enseñanza privada concertada": "Privado concertado",
                "Enseñanza privada no concertada": "Privado no concertado",
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
