"""Extract and tansform data
Sources:
    SS001
Target tables:
    excedencias_cuidado_hijos_familiares
"""

import logging
import unicodedata
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_XLSX_DIR = Path("data") / "raw" / "SS" / "SS001-MaternidadPaternidadCuidadoMenorYCuidadoFamiliares"
FILE_NAMES = [
    "PMA-2007-3.xls",
    "PMA-2007-4.xls",
    "PMA-2008-4.xls",
    "PMA-2008-5.xls",
    "PMA-2009-4.xls",
    "PMA-2009-5.xls",
    "PMA-2010-4.xls",
    "PMA-2010-5.xls",
    "PMA-2011-4.xls",
    "PMA-2011-5.xls",
    "PMA-2012-4.xls",
    "PMA-2012-5.xls",
    "PMA-2013-3.xls",
    "PMA-2014.xls",
    "PMA-2015.xls",
    "PMA-2016.xls",
    "PMA-2017.xlsx",
    "PMA-2018.xlsx",
    "PNM-2019.xlsx",
    "PNM-2020.xlsx",
    "PNM-2021.xlsx",
    "PNM-2022.xlsx",
    "PNM-2023.xlsx",
]
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "excedencias_cuidado_hijos_familiares.csv"

SHEET_NAME_DICT = {
    2007: " ",
    2008: " ",
    2009: " ",
    2010: " ",
    2011: " ",
    2012: " ",
    2013: " ",
    2014: "PMA03",
    2015: "PMA03",
    2016: "PMA03",
    2017: "PMA-3",
    2018: "PMA-3",
    2019: "PNM04",
    2020: "PNM04",
    2021: "PNM-2",
    2022: "PNM-2",
    2023: "PNM-2",
}


def _norm(s: str) -> str:
    s = "" if pd.isna(s) else str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s.strip()


def get_df_from_all_excels(paths: list[Path]) -> pd.DataFrame:
    all_entries = []

    for path in paths:
        year = int(path.stem.split("-")[1])
        excel_df = pd.read_excel(path, header=None, sheet_name=SHEET_NAME_DICT[year])

        # Fix wrong columns for specific years
        if year == 2017 or year == 2018:
            excel_df[10] = pd.NA
            excel_df[17] = pd.NA

        # Fix missing header for specific years
        if path.stem == "PMA-2008-4" or path.stem == "PMA-2007-3":
            motivo_header = excel_df.shape[1] * ["EXCEDENCIAS POR CUIDADO FAMILIAR: CUIDADO DE HIJOS"]
        elif path.stem == "PMA-2008-5" or path.stem == "PMA-2007-4":
            motivo_header = excel_df.shape[1] * ["EXCEDENCIAS POR CUIDADO FAMILIAR: CUIDADO DE FAMILIARES"]
        else:
            motivo_header_idx = 4 if year >= 2014 else 6
            motivo_header = excel_df.iloc[motivo_header_idx, :]
            motivo_header = motivo_header.replace("nan", "")
            motivo_header = motivo_header.ffill().tolist()
        sexo_header_idx = 5 if year >= 2014 else 7
        sexo_header = excel_df.iloc[sexo_header_idx, :].ffill().tolist()
        year_header = excel_df.iloc[sexo_header_idx + 1, :].tolist()  # only used before 2012

        excel_df[0] = excel_df[0].apply(_norm)
        andalucia_idx = excel_df.index[excel_df[0].eq("ANDALUCIA")][0]
        melilla_idx = excel_df.index[excel_df[0].eq("Melilla")][0]

        for i in range(andalucia_idx, melilla_idx + 1):
            for j in range(1, excel_df.shape[1]):
                if str(excel_df.iat[i, j]) == "nan" or excel_df.iat[i, j] is pd.NA:
                    continue
                if sexo_header[j].capitalize() not in ("Hombres", "Mujeres", "Varones"):
                    continue
                if motivo_header[j] in ("TOTAL"):
                    continue
                if year <= 2012 and year != year_header[j]:
                    continue
                if (year == 2007 or year == 2008) and excel_df.iat[i, 0] in [
                    "ASTURIAS",
                    "BALEARES",
                    "CANTABRIA",
                    "MADRID",
                    "MURCIA",
                    "NAVARRA",
                    "RIOJA (LA)",
                ]:
                    continue

                entry = {
                    "anio": year,
                    "provincia_id": excel_df.iat[i, 0],
                    "motivo": motivo_header[j],
                    "sexo": sexo_header[j],
                    "excedencias": excel_df.iat[i, j],
                }
                all_entries.append(entry)

    df = pd.DataFrame(all_entries)
    return df


def main():
    try:
        # Get all raw XLSX paths and load to df
        raw_xlsx_paths = [RAW_XLSX_DIR / fn for fn in FILE_NAMES]
        df = get_df_from_all_excels(raw_xlsx_paths)

        # Drop rows with aggregate data for provincia_id and map comunidad_autonoma to their provincias
        df = df[
            ~df["provincia_id"].isin(
                [
                    "ANDALUCIA",
                    "ARAGON",
                    "CANARIAS",
                    "CASTILLA-LA MANCHA",
                    "CASTILLA Y LEON",
                    "CATALUNA",
                    "COMUNIDAD VALENCIANA",
                    "COMUNITAT VALENCIANA",
                    "EXTREMADURA",
                    "GALICIA",
                    "PAIS VASCO",
                ]
            )
        ]
        df["provincia_id"] = df["provincia_id"].replace(
            {
                "NAVARRA (C. FORAL DE)": "Navarra",
                "ASTURIAS (PRINCIPADO DE)": "Asturias",
                "MADRID (COMUNIDAD DE)": "Madrid",
                "MURCIA (REGION DE)": "Murcia",
            }
        )

        # Count number of entries for each year
        logging.info(f"Number of entries per year:\n{df['anio'].value_counts()}")

        # Replace - with NULL for excedencias
        df["excedencias"] = df["excedencias"].replace("-", None)

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["motivo"] = apply_and_check_dict(
            df["motivo"],
            {
                "EXCEDENCIAS POR CUIDADO FAMILIAR: CUIDADO DE HIJOS": "Cuidado de hijos",
                "EXCEDENCIAS POR CUIDADO FAMILIAR: CUIDADO DE FAMILIARES": "Cuidado de familiares",
                "EXCEDENCIAS POR CUIDADO DE HIJOS": "Cuidado de hijos",
                "EXCEDENCIAS POR CUIDADO DE FAMILIARES": "Cuidado de familiares",
            },
        )
        df["sexo"] = apply_and_check_dict(
            df["sexo"],
            {"MUJERES": "Mujer", "VARONES": "Hombre", "Mujeres": "Mujer", "Varones": "Hombre"},
        )
        df["excedencias"] = apply_and_check(df["excedencias"], normalize_positive_integer)

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
