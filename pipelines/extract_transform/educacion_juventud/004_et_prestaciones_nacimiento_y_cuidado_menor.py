"""Extract and tansform data
Sources:
    SS001
Target tables:
    prestaciones_nacimiento_y_cuidado_menor
"""

import logging
import re
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,
    normalize_positive_float,
    normalize_positive_integer,
    normalize_provincia,
    normalize_year,
)

RAW_XLSX_DIR = Path("data") / "raw" / "SS" / "SS001-MaternidadPaternidadCuidadoMenorYCuidadoFamiliares"
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "prestaciones_nacimiento_y_cuidado_menor.csv"


def get_df_from_all_excels(paths: list[Path]) -> pd.DataFrame:
    all_entries = []

    for path in paths:
        year = int(path.stem.split("-")[-1])
        sheet_name = "PNM-1" if year > 2020 else "PNM03"
        excel_df = pd.read_excel(path, header=None, sheet_name=sheet_name)

        prestaciones_header = excel_df.iloc[5, :].ffill().tolist()
        anio_header = excel_df.iloc[7, :].tolist()
        pat = re.compile(r"^\s*(\d{4})\s*\(\d+\)\s*$")
        anio_header = [int(m.group(1)) if isinstance(v, str) and (m := pat.match(v)) else v for v in anio_header]

        andalucia_idx = excel_df.index[excel_df[0].str.strip().eq("ANDALUCÍA")][0]
        melilla_idx = excel_df.index[excel_df[0].str.strip().eq("Melilla")][0]

        for i in range(andalucia_idx, melilla_idx + 1):
            if str(excel_df.iat[i, 0]) == "nan":
                continue

            primer_progenitor = None
            opcion_a_favor = None
            segundo_progenitor = None
            importe = None

            if year == 2019:
                for j in range(1, excel_df.shape[1]):
                    if j == 6:
                        opcion_a_favor = excel_df.iat[i, j]
                    elif j == 9:
                        primer_progenitor = excel_df.iat[i, j]
                    elif j == 11:
                        segundo_progenitor = excel_df.iat[i, j]
                    elif j == 13:
                        importe = excel_df.iat[i, j]
            else:
                for j in range(1, excel_df.shape[1]):
                    if anio_header[j] == year and prestaciones_header[j] != "TOTAL PRESTACIONES":
                        if prestaciones_header[j] == "Total primer progenitor":
                            primer_progenitor = excel_df.iat[i, j]
                        elif prestaciones_header[j] == "Total segundo progenitor":
                            segundo_progenitor = excel_df.iat[i, j]
                        elif prestaciones_header[j].lstrip()[:7] == "Importe":
                            importe = excel_df.iat[i, j]

            entry = {  #  type: ignore
                "anio": year,
                "provincia_id": str(excel_df.iat[i, 0]).strip(),
                "prestaciones_primer_progenitor": primer_progenitor,
                "opcion_a_favor_segundo_progenitor": opcion_a_favor,
                "prestaciones_segundo_progenitor": segundo_progenitor,
                "importe_miles_euros": importe,
            }
            all_entries.append(entry)

        excel_df.to_csv("data/debug/prestaciones.csv", index=False, sep=";")

    df = pd.DataFrame(all_entries)

    # Round to 2 decimals importe_miles_euros
    df["importe_miles_euros"] = pd.to_numeric(df["importe_miles_euros"], errors="coerce").round(2)

    # Drop rows with aggregate data for provincia_id and map comunidad_autonoma to their provincias
    df = df[
        ~df["provincia_id"].isin(
            [
                "ANDALUCÍA",
                "ARAGÓN",
                "CANARIAS",
                "CASTILLA-LA MANCHA",
                "CASTILLA Y LEÓN",
                "CATALUÑA",
                "COMUNITAT VALENCIANA",
                "EXTREMADURA",
                "GALICIA",
                "PAÍS VASCO",
            ]
        )
    ]
    df["provincia_id"] = df["provincia_id"].replace(
        {
            "NAVARRA (C. FORAL DE)": "Navarra",
            "ASTURIAS (PRINCIPADO DE)": "Asturias",
            "MADRID (COMUNIDAD DE)": "Madrid",
            "MURCIA (REGIÓN DE)": "Murcia",
        }
    )

    return df


def main():
    try:
        # Get all raw XLSX paths and load to df
        raw_xlsx_paths = sorted(RAW_XLSX_DIR.glob("*.xlsx"))
        raw_xlsx_paths = [p for p in raw_xlsx_paths if int(p.stem.split("-")[-1]) >= 2019]
        raw_xlsx_paths = [p for p in raw_xlsx_paths if not p.name.startswith(("~$", "._")) or p.name.endswith("~")]
        df = get_df_from_all_excels(raw_xlsx_paths)

        # Validate and normalize columns
        df["anio"] = apply_and_check(df["anio"], normalize_year)
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["prestaciones_primer_progenitor"] = apply_and_check(
            df["prestaciones_primer_progenitor"], normalize_positive_integer
        )
        df["prestaciones_segundo_progenitor"] = apply_and_check(
            df["prestaciones_segundo_progenitor"], normalize_positive_integer
        )
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
