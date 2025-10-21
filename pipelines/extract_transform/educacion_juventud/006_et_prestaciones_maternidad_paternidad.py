"""Extract and tansform data
Sources:
    SS001
Target tables:
    prestaciones_maternidad_paternidad
"""

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    apply_and_check_dict,
    normalize_positive_float,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_XLSX_DIR = Path("data") / "raw" / "SS" / "SS001-MaternidadPaternidadCuidadoMenorYCuidadoFamiliares"
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "prestaciones_maternidad_paternidad.csv"
FILE_DICTIONARIES = {
    2019: {
        "maternidad": {
            "file": "PNM-2019.xlsx",
            "sheet": "PNM01",
        },
        "paternidad": {
            "file": "PNM-2019.xlsx",
            "sheet": "PNM02",
        },
    },
    2018: {
        "maternidad": {
            "file": "PMA-2018.xlsx",
            "sheet": "PMA-1",
        },
        "paternidad": {
            "file": "PMA-2018.xlsx",
            "sheet": "PMA-2",
        },
    },
    2017: {
        "maternidad": {
            "file": "PMA-2017.xlsx",
            "sheet": "PMA-1",
        },
        "paternidad": {
            "file": "PMA-2017.xlsx",
            "sheet": "PMA-2",
        },
    },
    2016: {
        "maternidad": {
            "file": "PMA-2016.xls",
            "sheet": "PMA01",
        },
        "paternidad": {
            "file": "PMA-2016.xls",
            "sheet": "PMA02",
        },
    },
    2015: {
        "maternidad": {
            "file": "PMA-2015.xls",
            "sheet": "PMA01",
        },
        "paternidad": {
            "file": "PMA-2015.xls",
            "sheet": "PMA02",
        },
    },
    2014: {
        "maternidad": {
            "file": "PMA-2014.xls",
            "sheet": "PMA01",
        },
        "paternidad": {
            "file": "PMA-2014.xls",
            "sheet": "PMA02",
        },
    },
    2013: {
        "maternidad": {
            "file": "PMA-2013-1.xls",
            "sheet": "PMA-1",
        },
        "paternidad": {
            "file": "PMA-2013-2.xls",
            "sheet": "PMA-2",
        },
    },
    2012: {
        "maternidad": {
            "file": "PMA-2012-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2012-2.xls",
            "sheet": " ",
        },
    },
    2011: {
        "maternidad": {
            "file": "PMA-2011-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2011-2.xls",
            "sheet": " ",
        },
    },
    2010: {
        "maternidad": {
            "file": "PMA-2010-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2010-2.xls",
            "sheet": " ",
        },
    },
    2009: {
        "maternidad": {
            "file": "PMA-2009-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2009-2.xls",
            "sheet": " ",
        },
    },
    2008: {
        "maternidad": {
            "file": "PMA-2008-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2008-2.xls",
            "sheet": " ",
        },
    },
    2007: {
        "maternidad": {
            "file": "PMA-2007-1.xls",
            "sheet": " ",
        },
        "paternidad": {
            "file": "PMA-2007-1.xls",
            "sheet": " ",
        },
    },
    2006: {
        "maternidad": {
            "file": "PMA-2006-1.xls",
            "sheet": " ",
        },
    },
    2005: {
        "maternidad": {
            "file": "PMA-2006-1.xls",
            "sheet": " ",
        },
    },
    2004: {
        "maternidad": {
            "file": "PMA-2004.xls",
            "sheet": " ",
        },
    },
    2003: {
        "maternidad": {
            "file": "PMA-2004.xls",
            "sheet": " ",
        },
    },
    2002: {
        "maternidad": {
            "file": "PMA-2004.xls",
            "sheet": " ",
        },
    },
}


def _norm(s: str) -> str:
    s = "" if pd.isna(s) else str(s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"\([^)]*\)", "", s)
    return s.strip()


def _coerce_year_token(v: Any) -> Any:
    if isinstance(v, str):
        pat = re.compile(r"^\s*(\d{4})\s*\(\s*(?:\d+|\*)\s*\)\s*$")
        m = pat.match(v)
        if m:
            return int(m.group(1))
        try:
            f = float(v)
            if f.is_integer():
                return int(f)
        except Exception:
            pass
        return v
    if isinstance(v, (float, np.floating)) and float(v).is_integer():
        return int(v)
    return v


def get_maternidad_entries(excel_df: pd.DataFrame, year: int) -> List[Dict[str, Any]]:
    all_entries: List[Dict[str, Any]] = []
    if year >= 2014:
        perceptor_idx = 5
    elif year >= 2010:
        perceptor_idx = 6
    else:
        perceptor_idx = 7
    if year >= 2007:
        perceptor_header_1 = excel_df.iloc[perceptor_idx, :].ffill().tolist()
        perceptor_header_2 = excel_df.iloc[perceptor_idx + 1, :].ffill().tolist()
        perceptor_header = [f"{_norm(h1)}: {_norm(h2)}" for h1, h2 in zip(perceptor_header_1, perceptor_header_2)]
        anio_idx = perceptor_idx + 2
    else:
        perceptor_header = excel_df.iloc[perceptor_idx, :].str.strip().ffill().tolist()
        anio_idx = perceptor_idx + 1
    anio_header = excel_df.iloc[anio_idx, :].ffill().tolist()
    anio_header = [_coerce_year_token(x) for x in anio_header]

    excel_df[0] = excel_df[0].apply(_norm)
    andalucia_idx = excel_df.index[excel_df[0].str.strip().eq("ANDALUCIA")][0]
    melilla_idx = excel_df.index[excel_df[0].str.strip().eq("Melilla")][0]

    for i in range(andalucia_idx, melilla_idx + 1):
        if str(excel_df.iat[i, 0]) == "":
            continue

        madre = None
        padre = None
        importe = None
        for j in range(1, excel_df.shape[1]):
            # Cells to skip
            if str(excel_df.iat[i, j]) == "nan" or excel_df.iat[i, j] is pd.NA or excel_df.iat[i, j] == "":
                continue
            if anio_header[j] != year:
                continue

            # Cells to unfold
            if perceptor_header[j].lower().startswith("percibidas por la madre"):
                madre = excel_df.iat[i, j]
            elif perceptor_header[j].startswith("Percibidas por el padre: Prestaciones"):
                padre = excel_df.iat[i, j]
            elif year <= 2006 and perceptor_header[j].startswith("PERCIBIDAS POR EL PADRE"):
                padre = excel_df.iat[i, j]
            elif perceptor_header[j].startswith("Importe"):
                importe = excel_df.iat[i, j]

        entry = {
            "anio": year,
            "provincia_id": excel_df.iat[i, 0],
            "tipo": "Maternidad",
            "percibidas_madre": madre,
            "percibidas_padre": padre,
            "importe_miles_euros": importe,
        }
        all_entries.append(entry)
    return all_entries


def get_paternidad_entries(excel_df: pd.DataFrame, year: int) -> List[Dict[str, Any]]:
    all_entries: List[Dict[str, Any]] = []
    if year >= 2011:
        prestaciones_idx = 5
    elif year >= 2008:
        prestaciones_idx = 6
    else:
        prestaciones_idx = 7
    prestaciones_header = excel_df.iloc[prestaciones_idx, :].ffill().tolist()
    anio_idx = prestaciones_idx + 1 if year >= 2008 else prestaciones_idx + 2
    anio_header = excel_df.iloc[anio_idx, :].tolist()
    anio_header = [_coerce_year_token(x) for x in anio_header]

    excel_df[0] = excel_df[0].apply(_norm)
    andalucia_idx = excel_df.index[excel_df[0].str.strip().eq("ANDALUCIA")][0]
    melilla_idx = excel_df.index[excel_df[0].str.strip().eq("Melilla")][0]

    for i in range(andalucia_idx, melilla_idx + 1):
        if str(excel_df.iat[i, 0]) == "":
            continue

        prestaciones = None
        importe = None
        for j in range(1, excel_df.shape[1]):
            # Cells to skip
            if str(excel_df.iat[i, j]) == "nan" or excel_df.iat[i, j] is pd.NA or excel_df.iat[i, j] == "":
                continue
            if anio_header[j] != year:
                continue

            # Cells to unfold
            if prestaciones_header[j].startswith("Prestaciones"):
                prestaciones = excel_df.iat[i, j]
            elif prestaciones_header[j].startswith("Importe"):
                importe = excel_df.iat[i, j]

        entry = {
            "anio": year,
            "provincia_id": excel_df.iat[i, 0],
            "tipo": "Paternidad",
            "percibidas_madre": None,
            "percibidas_padre": prestaciones,
            "importe_miles_euros": importe,
        }
        all_entries.append(entry)

    return all_entries


def get_df_from_excels() -> pd.DataFrame:
    all_entries = []

    for year, pat_mat_dict in FILE_DICTIONARIES.items():
        for tipo, file_dict in pat_mat_dict.items():
            path = RAW_XLSX_DIR / file_dict["file"]
            sheet = file_dict["sheet"]
            excel_df = pd.read_excel(path, sheet_name=sheet, header=None)

            if tipo == "maternidad":
                if year == 2007:
                    excel_df = excel_df.iloc[:, :-4]
                new_entries = get_maternidad_entries(excel_df, year)
            elif tipo == "paternidad":
                if year == 2007:
                    excel_df = excel_df.iloc[:, [0, -3, -2, -1]]
                new_entries = get_paternidad_entries(excel_df, year)

            # Filter out aggregate rows for column provincia_id
            AGGREGATES = {
                "ANDALUCIA",
                "ARAGON",
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
            }
            if year <= 2008:
                AGGREGATES.update(
                    {
                        "ASTURIAS",
                        "BALEARES",
                        "CANTABRIA",
                        "MADRID",
                        "MURCIA",
                        "NAVARRA",
                        "RIOJA (LA)",
                        "RIOJA",
                    }
                )
            new_entries = [e for e in new_entries if str(e.get("provincia_id", "")).strip() not in AGGREGATES]  # type: ignore

            all_entries.extend(new_entries)

    return pd.DataFrame(all_entries)


def main():
    try:
        # Get all raw XLSX paths and load to df
        df = get_df_from_excels()

        # Round importe to 2 decimal places
        df["importe_miles_euros"] = pd.to_numeric(df["importe_miles_euros"], errors="coerce").round(2)

        # Validate and normalize data
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["tipo"] = apply_and_check_dict(
            df["tipo"],
            {
                "Maternidad": "Maternidad",
                "Paternidad": "Paternidad",
            },
        )
        df["percibidas_madre"] = apply_and_check(df["percibidas_madre"], normalize_positive_integer)
        df["percibidas_padre"] = apply_and_check(df["percibidas_padre"], normalize_positive_integer)
        df["importe_miles_euros"] = apply_and_check(df["importe_miles_euros"], normalize_positive_float)

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
