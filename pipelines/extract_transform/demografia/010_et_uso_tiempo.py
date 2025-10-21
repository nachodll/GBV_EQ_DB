"""Extract and transform data
Sources:
    INE018 - 2009
    INE019 - 2002
Target tables:
    uso_tiempo
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_positive_integer,
    normalize_year,
)

RAW_CSV_PATH_2009 = Path("data") / "raw" / "INE" / "INE018-UsoTiempo2009.csv"
RAW_XLS_PATH_2002 = Path("data") / "raw" / "INE" / "INE019-UsoTiempo2002.xls"
CLEAN_CSV_PATH = Path("data") / "clean" / "demografia" / "uso_tiempo.csv"


def extract_2009() -> pd.DataFrame:
    """Extract data from 2009 source"""

    # Read csv file into a DataFrame
    df = pd.read_csv(RAW_CSV_PATH_2009, sep=";")

    # Pivot so horas/minutos become columns
    df = df.pivot_table(
        index=["Sexo", "Total Nacional", "Comunidades y Ciudades Autónomas", "Actividades principales (1 dígito)"],
        columns="Promedio: Seleccionar horas y minutos",
        values="Total",
        aggfunc="first",
    ).reset_index()

    # Rename columns
    df.rename(
        columns={
            "Sexo": "sexo",
            "Comunidades y Ciudades Autónomas": "comunidad_autonoma_id",
            "Actividades principales (1 dígito)": "actividad",
        },
        inplace=True,
    )
    df = df.drop(columns=["Total Nacional"], errors="ignore")

    # Set year for dataset
    df["anio"] = 2009

    # Drop rows with aggregated data
    df = df[df["comunidad_autonoma_id"].notna()]
    df = df[df["sexo"] != "Ambos sexos"]

    # Replace - in column horas and minutos with ""
    df["horas"] = df["horas"].astype(str).str.replace(".", "0", regex=False)
    df["horas"] = df["horas"].str.replace("-", "", regex=False).astype(int)
    df["minutos"] = df["minutos"].str.replace("-", "", regex=False).astype(int)

    return df


def excel_to_dataframe(excel_df: pd.DataFrame, sexo: str, anio: int) -> pd.DataFrame:
    """Convert excel data to DataFrame"""

    activity_dictionary = {
        "0": "0 Cuidados personales",
        "1": "1 Trabajo remunerado",
        "2": "2 Estudios",
        "3": "3 Hogar y familia",
        "4": "4 Trabajo voluntario y reuniones",
        "5": "5 Vida social y diversión",
        "6": "6 Deportes y actividades al aire libre",
        "7": "7 Aficiones e informática",
        "8": "8 Medios de comunicación",
        "9": "9 Trayectos y empleo del tiempo no especificado",
    }

    # Iterate over all rows and columns to create a list of entries
    all_entries = []
    for row in range(2, 19):
        for col in range(2, 20):
            time = excel_df.iat[row, col]
            if pd.notna(time):
                entry = {
                    "anio": anio,
                    "comunidad_autonoma_id": excel_df.iat[row, 0],
                    "actividad": activity_dictionary.get(str(excel_df.iat[0, col])),
                    "sexo": sexo,
                    "horas": time.hour,  # type: ignore
                    "minutos": time.minute,  # type: ignore
                }
                all_entries.append(entry)

    return pd.DataFrame(all_entries)


def extract_2002() -> pd.DataFrame:
    """Extract data from 2002 source"""

    # Read both sheets into DataFrames
    excel_df_men = pd.read_excel(RAW_XLS_PATH_2002, sheet_name="9.2", skiprows=3, header=None)
    excel_df_women = pd.read_excel(RAW_XLS_PATH_2002, sheet_name="9.3", skiprows=3, header=None)

    # Convert both DataFrames to the desired format
    df_men = excel_to_dataframe(excel_df_men, "Varones", 2002)
    df_women = excel_to_dataframe(excel_df_women, "Mujeres", 2002)

    df = pd.concat([df_men, df_women], ignore_index=True)

    return df


def main():
    try:
        # Get data from both sources and merge them into a single DataFrame
        df_2009 = extract_2009()
        df_2002 = extract_2002()
        df = pd.concat([df_2009, df_2002], ignore_index=True)

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Varones": "Hombre", "Mujeres": "Mujer"})
        df["actividad"] = apply_and_check(df["actividad"], normalize_plain_text)
        df["horas"] = apply_and_check(df["horas"], normalize_positive_integer)
        df["minutos"] = apply_and_check(df["minutos"], normalize_positive_integer)
        df["anio"] = apply_and_check(df["anio"], normalize_year)

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
