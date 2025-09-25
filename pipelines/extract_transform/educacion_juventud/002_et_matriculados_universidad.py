"""Extract and tansform data
Sources:
    MINCIU001
Target tables:
    matriculados_universidad
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,
    normalize_comunidad_autonoma,
    normalize_plain_text,
    normalize_positive_integer,
)

RAW_XLSX_PATH = Path("data") / "raw" / "MINCIU" / "MINCIU001-MatriculadosUniversidad.xlsx"
CLEAN_CSV_PATH = Path("data") / "clean" / "educacion_juventud" / "matriculados_universidad.csv"


def main():
    try:
        # Read raw XLSX
        excel_df = pd.read_excel(RAW_XLSX_PATH, dtype=str, header=None)  # type: ignore

        # General headers for the entire dataframe
        sexo_header = excel_df.iloc[6, :].ffill().tolist()
        rama_conocimiento_header = excel_df.iloc[7, :].ffill().tolist()
        curso_header = excel_df.iloc[8, :].ffill().tolist()

        # Iterate over each comunidad autonoma (block of 126 rows)
        all_entries = []
        for ccaa_idx in range(9, excel_df.shape[0] - 126, 126):
            comunidad_autonoma = excel_df.iloc[ccaa_idx, 0]
            ccaa_df = excel_df.iloc[ccaa_idx : ccaa_idx + 126, :].copy().reset_index(drop=True)

            # Iterate over each 'nivel_academico' (block of 25 rows)
            for na_idx in range(1, 126, 25):
                nivel_academico = ccaa_df.iloc[na_idx, 0]
                na_df = ccaa_df.iloc[na_idx : na_idx + 25, :].copy().reset_index(drop=True)

                # Iterate over each 'tipo_universidad' (block of 6 rows)
                for tu_idx in range(1, 25, 6):
                    tipo_universidad = na_df.iloc[tu_idx, 0]
                    tu_df = na_df.iloc[tu_idx : tu_idx + 6, :].copy().reset_index(drop=True)

                    # Melt the dataframe to long format
                    for i in range(1, tu_df.shape[0]):
                        for j in range(1, tu_df.shape[1]):
                            entry = {  #  type: ignore
                                "comunidad_autonoma_id": comunidad_autonoma,
                                "nivel_academico": nivel_academico,
                                "tipo_universidad": tipo_universidad,
                                "modalidad_universidad": tu_df.iat[i, 0],
                                "sexo": sexo_header[j],
                                "rama_conocimiento": rama_conocimiento_header[j],
                                "curso": curso_header[j],
                                "matriculados": tu_df.iat[i, j],
                            }
                            all_entries.append(entry)  # type: ignore

        df = pd.DataFrame(all_entries)  # type: ignore

        # Replace "No desglosado" with None for comunidad_autonoma
        df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].replace("No desglosado", None)  # type: ignore
        # Drop all rows with "Estado" in comunidad_autonoma
        df = df[df["comunidad_autonoma_id"] != "Estado"]
        # Adapt curso from yyyy-yyyy to yyyy-yy format
        df["curso"] = df["curso"].str.replace(r"(\d{4})-\d{2}(\d{2})", r"\1-\2", regex=True)

        # Validate and normalize columns
        df["comunidad_autonoma_id"] = apply_and_check(df["comunidad_autonoma_id"], normalize_comunidad_autonoma)
        df["nivel_academico"] = apply_and_check(df["nivel_academico"], normalize_plain_text)
        df["tipo_universidad"] = apply_and_check(df["tipo_universidad"], normalize_plain_text)
        df["modalidad_universidad"] = apply_and_check(df["modalidad_universidad"], normalize_plain_text)
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer", "Ambos sexos": "Total"})
        df["rama_conocimiento"] = apply_and_check(df["rama_conocimiento"], normalize_plain_text)
        df["curso"] = apply_and_check(df["curso"], normalize_plain_text)
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
