"""Extract and transform data
Sources:
    DGVG015
Target tables:
    centros_acogida_emergencia
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_PATH_DIR = Path("data") / "raw" / "DGVG" / "DGVG015-RecursosAutonómicos"
RAW_PATHS = {
    2022: {
        "Path": RAW_PATH_DIR / "2022" / "Capitulo-1.xlsx",
        "Sheet_centros": "Acogida de emergencia ",
        "Sheet_victimas": "Acogida de emergencia. Muj Víct",
    },
    2020: {
        "Path": RAW_PATH_DIR / "2020" / "DERA_2020_Dep_DEF-_Valores.xlsx",
        "Sheet_centros": "1A1",
        "Sheet_profesionales": "1A2",
        "Sheet_victimas": "1A4",
    },
    2017: {
        "Path": RAW_PATH_DIR / "2017" / "RecursosAsistencia_Social_5.xls",
        "Sheet_centros": "Centros de emergencia (1)",
        "Sheet_victimas": "Centros de emergencia (2)",
    },
}
CLEAN_CSV_PATH = Path("data") / "clean" / "politicas_publicas_igualdad_violencia" / "centros_acogida_emergencia.csv"


def load_2022_centros_data() -> pd.DataFrame:
    centros_df = pd.read_excel(RAW_PATHS[2022]["Path"], sheet_name=RAW_PATHS[2022]["Sheet_centros"])
    centros_df = centros_df.iloc[:, :-2]
    all_entries = []

    andalucia_idx = centros_df.index[centros_df.iloc[:, 0].str.strip().eq("Andalucía")][0]
    melilla_idx = centros_df.index[centros_df.iloc[:, 0].str.strip().eq("Melilla")][0]
    header = centros_df.iloc[7, :].tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        centros = None
        plazas = None
        profesionales = None

        for j in range(2, centros_df.shape[1]):
            if header[j].strip() == "Centros":
                centros = centros_df.iat[i, j]
            elif header[j].strip() == "Plazas":
                plazas = centros_df.iat[i, j]
            elif header[j].strip() == "Total":
                profesionales = centros_df.iat[i, j]

        entry = {
            "anio": 2022,
            "provincia_id": centros_df.iat[i, 1],
            "centros": centros,
            "plazas": plazas,
            "profesionales": profesionales,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    df = df.dropna(subset=["provincia_id"])

    return df


def load_2022_victimas_data() -> pd.DataFrame:
    victimas_df = pd.read_excel(RAW_PATHS[2022]["Path"], sheet_name=RAW_PATHS[2022]["Sheet_victimas"])
    all_entries = []

    andalucia_idx = victimas_df.index[victimas_df.iloc[:, 0].str.strip().eq("Andalucía")][0]
    melilla_idx = victimas_df.index[victimas_df.iloc[:, 0].str.strip().eq("Melilla")][0]
    first_header = victimas_df.iloc[4, :].ffill().tolist()
    second_header = victimas_df.iloc[5, :].ffill().tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        mujeres_acogidas = None
        hijos_a_cargo_acogidos = None

        for j in range(2, victimas_df.shape[1]):
            if first_header[j].strip() == "Mujeres y/o niñas víctimas de VCM" and second_header[j].strip() == "Total":
                mujeres_acogidas = victimas_df.iat[i, j]
            elif (
                first_header[j].strip() == "Hijos/as menores o con discapacidad a cargo de víctimas de VCM"
                and second_header[j].strip() == "Total"
            ):
                hijos_a_cargo_acogidos = victimas_df.iat[i, j]

        entry = {
            "anio": 2022,
            "provincia_id": victimas_df.iat[i, 1],
            "mujeres_acogidas": mujeres_acogidas,
            "hijos_a_cargo_acogidos": hijos_a_cargo_acogidos,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    df = df.dropna(subset=["provincia_id"])

    return df


def load_2020_centros_data() -> pd.DataFrame:
    centros_df = pd.read_excel(RAW_PATHS[2020]["Path"], sheet_name=RAW_PATHS[2020]["Sheet_centros"])
    all_entries = []

    andalucia_idx = centros_df.index[centros_df.iloc[:, 1].str.strip().eq("Andalucía")][0]
    melilla_idx = centros_df.index[centros_df.iloc[:, 1].str.strip().eq("Melilla")][0]
    first_header = centros_df.iloc[4, :].ffill().tolist()
    second_header = centros_df.iloc[6, :].ffill().tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        centros = None
        plazas = None

        for j in range(5, centros_df.shape[1]):
            if first_header[j].strip() == "Acogida de emergencia" and second_header[j].strip() == "Centros":
                centros = centros_df.iat[i, j]
            elif first_header[j].strip() == "Acogida de emergencia" and second_header[j].strip() == "Máximo de Plazas":
                plazas = centros_df.iat[i, j]

        entry = {
            "anio": 2020,
            "provincia_id": centros_df.iat[i, 3],
            "centros": centros,
            "plazas": plazas,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    df = df.dropna(subset=["provincia_id"])

    # Replace - with 0 in centros and plazas
    df["centros"] = df["centros"].replace("-", 0).astype(float)
    df["plazas"] = df["plazas"].replace("-", 0).astype(float)

    return df


def load_2020_profesionales_data() -> pd.DataFrame:
    profesionales_df = pd.read_excel(RAW_PATHS[2020]["Path"], sheet_name=RAW_PATHS[2020]["Sheet_profesionales"])
    all_entries = []

    andalucia_idx = profesionales_df.index[profesionales_df.iloc[:, 1].str.strip().eq("Andalucía")][0]
    melilla_idx = profesionales_df.index[profesionales_df.iloc[:, 1].str.strip().eq("Melilla")][0]
    first_header = profesionales_df.iloc[4, :].ffill().tolist()
    second_header = profesionales_df.iloc[6, :].ffill().tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        for j in range(5, profesionales_df.shape[1]):
            if first_header[j].strip() == "Acogida de emergencia" and second_header[j].strip() == "Total":
                entry = {
                    "anio": 2020,
                    "provincia_id": profesionales_df.iat[i, 3],
                    "profesionales": profesionales_df.iat[i, j],
                }
                all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    df = df.dropna(subset=["provincia_id"])

    # Replace - with 0 in profesionales
    df["profesionales"] = df["profesionales"].replace("-", 0).astype(float)

    return df


def load_2020_victimas_data() -> pd.DataFrame:
    victimas_df = pd.read_excel(RAW_PATHS[2020]["Path"], sheet_name=RAW_PATHS[2020]["Sheet_victimas"])
    all_entries = []

    andalucia_idx = victimas_df.index[victimas_df.iloc[:, 1].str.strip().eq("Andalucía")][0]
    melilla_idx = victimas_df.index[victimas_df.iloc[:, 1].str.strip().eq("Melilla")][0]
    first_header = victimas_df.iloc[3, :].ffill().tolist()
    second_header = victimas_df.iloc[4, :].ffill().tolist()
    third_header = victimas_df.iloc[6, :].ffill().tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        mujeres_hijos_acogidas = None
        hijos_a_cargo_acogidos = None

        for j in range(5, victimas_df.shape[1]):
            if first_header[j].strip() == "Acogida de emergencia" and second_header[j].strip() == "Total":
                if third_header[j].strip() == "Total víctimas acogidas (mujeres + hijas/os a cargo)":
                    mujeres_hijos_acogidas = victimas_df.iat[i, j]
                elif third_header[j].strip() == "Total Hijas/os a cargo":
                    hijos_a_cargo_acogidos = victimas_df.iat[i, j]

        entry = {
            "anio": 2020,
            "provincia_id": victimas_df.iat[i, 3],
            "mujeres_acogidas": mujeres_hijos_acogidas - hijos_a_cargo_acogidos,  # type: ignore
            "hijos_a_cargo_acogidos": hijos_a_cargo_acogidos,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    df = df.dropna(subset=["provincia_id"])

    return df


def load_2017_centros_data() -> pd.DataFrame:
    centros_df = pd.read_excel(RAW_PATHS[2017]["Path"], sheet_name=RAW_PATHS[2017]["Sheet_centros"])
    all_entries = []

    andalucia_idx = centros_df.index[centros_df.iloc[:, 1].str.strip().eq("Andalucía")][0]
    melilla_idx = centros_df.index[centros_df.iloc[:, 1].str.strip().eq("Melilla1")][0]
    header = centros_df.iloc[4, :].tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        centros = None
        plazas = None
        profesionales = None

        for j in range(1, centros_df.shape[1] - 3):
            if header[j].strip() == "Nº centros de emergencia":
                centros = centros_df.iat[i, j]
            elif header[j].strip() == "Nº especialistas":
                profesionales = centros_df.iat[i, j]
            elif header[j].strip() == "Nº plazas disponibles":
                plazas = centros_df.iat[i, j]

        entry = {
            "anio": 2017,
            "provincia_id": centros_df.iat[i, 1],
            "profesionales": profesionales,
            "centros": centros,
            "plazas": plazas,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)

    # Raplce .. with None in profesionales, centros and plazas
    df["profesionales"] = df["profesionales"].replace("..", None).astype(float)
    df["centros"] = df["centros"].replace("..", None).astype(float)
    df["plazas"] = df["plazas"].replace("..", None).astype(float)

    # Drop comunidades with multiple provinces and replace comunidades with one province with province name
    df = df[
        ~df["provincia_id"].isin(
            [
                "Andalucía",
                "Aragón",
                "Canarias",
                "Castilla y León",
                "Castilla-La Mancha",
                "Cataluña",
                "Comunitat Valenciana",
                "Extremadura",
                "Galicia",
                "País Vasco",
            ]
        )
    ].replace(
        {
            "Asturias, Principado de": "Asturias",
            "Balears, Illes1": "Balears, Illes",
            "Cantabria1": "Cantabria",
            "Madrid, Comunidad de": "Madrid",
            "Murcia, Región de": "Murcia",
            "Navarra, Comunidad Foral de": "Navarra",
        }
    )

    return df


def load_2017_victimas_data() -> pd.DataFrame:
    victimas_df = pd.read_excel(RAW_PATHS[2017]["Path"], sheet_name=RAW_PATHS[2017]["Sheet_victimas"])
    all_entries = []

    andalucia_idx = victimas_df.index[victimas_df.iloc[:, 1].str.strip().eq("Andalucía")][0]
    melilla_idx = victimas_df.index[victimas_df.iloc[:, 1].str.strip().eq("Melilla1")][0]
    first_header = victimas_df.iloc[3, :].ffill().tolist()
    second_header = victimas_df.iloc[4, :].ffill().tolist()

    for i in range(andalucia_idx, melilla_idx + 1):
        mujeres_acogidas = None
        hijos_a_cargo_acogidos = None

        for j in range(1, victimas_df.shape[1]):
            if first_header[j].strip() == "Mujeres" and second_header[j].strip() == "TOTAL mujeres":
                mujeres_acogidas = victimas_df.iat[i, j]
            elif (
                first_header[j].strip() == "Hijas/os menores o con discapacidad"
                and second_header[j].strip() == "TOTAL hijas/os"
            ):
                hijos_a_cargo_acogidos = victimas_df.iat[i, j]

        entry = {
            "anio": 2017,
            "provincia_id": victimas_df.iat[i, 1],
            "mujeres_acogidas": mujeres_acogidas,
            "hijos_a_cargo_acogidos": hijos_a_cargo_acogidos,
        }
        all_entries.append(entry)

    df = pd.DataFrame(all_entries)

    # Replace .. with None in mujeres_acogidas and hijos_a_cargo_acogidos
    df["mujeres_acogidas"] = df["mujeres_acogidas"].replace("..", None).astype(float)
    df["hijos_a_cargo_acogidos"] = df["hijos_a_cargo_acogidos"].replace("..", None).astype(float)

    # Drop comunidades with multiple provinces and replace comunidades with one province with province name
    df = df[
        ~df["provincia_id"].isin(
            [
                "Andalucía",
                "Aragón",
                "Canarias",
                "Castilla y León",
                "Castilla-La Mancha",
                "Cataluña",
                "Comunitat Valenciana",
                "Extremadura",
                "Galicia",
                "País Vasco",
            ]
        )
    ].replace(
        {
            "Asturias, Principado de": "Asturias",
            "Balears, Illes1": "Balears, Illes",
            "Cantabria1": "Cantabria",
            "Madrid, Comunidad de": "Madrid",
            "Murcia, Región de": "Murcia",
            "Navarra, Comunidad Foral de": "Navarra",
        }
    )

    return df


def main():
    try:
        # Read xlsx files for different years and concatenate data
        df_centros_2022 = load_2022_centros_data()
        df_victimas_2022 = load_2022_victimas_data()
        df_2022 = pd.merge(df_centros_2022, df_victimas_2022, on=["provincia_id", "anio"], how="outer")
        df_centros_2020 = load_2020_centros_data()
        df_profesionales_2020 = load_2020_profesionales_data()
        df_victimas_2020 = load_2020_victimas_data()
        df_2020 = pd.merge(df_centros_2020, df_profesionales_2020, on=["provincia_id", "anio"], how="outer")
        df_2020 = pd.merge(df_2020, df_victimas_2020, on=["provincia_id", "anio"], how="outer")
        df_centros_2017 = load_2017_centros_data()
        df_victimas_2017 = load_2017_victimas_data()
        df_2017 = pd.merge(df_centros_2017, df_victimas_2017, on=["provincia_id", "anio"], how="outer")
        df = pd.concat([df_2022, df_2020, df_2017], ignore_index=True)

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["centros"] = apply_and_check(df["centros"], normalize_positive_integer)
        df["plazas"] = apply_and_check(df["plazas"], normalize_positive_integer)
        df["profesionales"] = apply_and_check(df["profesionales"], normalize_positive_integer)
        df["mujeres_acogidas"] = apply_and_check(df["mujeres_acogidas"], normalize_positive_integer)
        df["hijos_a_cargo_acogidos"] = apply_and_check(df["hijos_a_cargo_acogidos"], normalize_positive_integer)

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
