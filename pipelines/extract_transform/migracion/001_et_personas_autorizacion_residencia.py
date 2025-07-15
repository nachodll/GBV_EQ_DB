"""Extract and transform data
Sources:
    OPI001, (2013-present, autorización de residencia)
    OPI002, (2013-present, certificado de registro or acuerdo de retirada)
    OPI003, OPI004, OPI005, (2012, 2011, 2010 and 2002-2009 historic evolution)
Target tables:
    personas_autorizacion_residencia
"""

import logging
from pathlib import Path

import pandas as pd

from utils.logging import setup_logging
from utils.normalization import (
    apply_and_check,  # type: ignore
    apply_and_check_dict,  # type: ignore
    normalize_age_group,
    normalize_date,
    normalize_nationality,
    normalize_positive_integer,
    normalize_provincia,
)

RAW_CSV_PATH_POST_2013_1 = Path("data") / "raw" / "OPI" / "OPI001-PersonasAutorizaciónResidencia.csv"
RAW_CSV_PATH_POST_2013_2 = Path("data") / "raw" / "OPI" / "OPI002-PersonasCertificadoRegistroOAcuerdoRetirada.csv"
RAW_CSV_DIR_2012 = Path("data") / "raw" / "OPI" / "OPI003-2012"
RAW_CSV_DIR_2011 = Path("data") / "raw" / "OPI" / "OPI004-2011"
RAW_CSV_DIR_2010 = Path("data") / "raw" / "OPI" / "OPI005-2010"
CLEAN_CSV_PATH = Path("data") / "clean" / "migracion" / "personas_autorizacion_residencia.csv"


def excel_directory_to_df(dir: Path) -> pd.DataFrame:
    """Read all excel files from a directory and return a DataFrame with table 4 of each one"""

    all_records = []
    for file in dir.glob("*.xls"):
        try:
            excel_df = pd.read_excel(file, sheet_name="4", header=None)  # type: ignore

            # Special case for a file with a different format, make it match the other files format
            if file.name == "Extranjeros_con_certificado_RD_PROV_18_Granada_2010.xls":
                excel_df.drop(columns=excel_df.columns[-24:], inplace=True)
                excel_df = excel_df.drop(index=3).reset_index(drop=True)  # type: ignore
                excel_df.replace("AELC-EFTA (1)", "AELC1", inplace=True)  # type: ignore
                excel_df.replace("Apátridas y No consta", "No consta", inplace=True)  # type: ignore
                excel_df.replace("Régimen Comunitario", "Régimen de libre circulación UE", inplace=True)  # type: ignore
                excel_df = pd.concat([excel_df, pd.DataFrame([[""] * len(excel_df.columns)])], ignore_index=True)

            # Extract constant variables
            date = excel_df.iloc[0].iloc[0].split(" ")[-1]  # type: ignore
            provincia = excel_df.iloc[1].iloc[0]  # type: ignore

            # Extract regimen and grupo_edad headers and fill forward excel unmerged cells
            regimen_headers = excel_df.iloc[3].ffill().copy()  # type: ignore
            grupo_edad_headers = excel_df.iloc[4].ffill().copy()  # type: ignore

            # Drop average age columns (even columns but 0)
            cols_to_drop = [col for col in excel_df.columns if col != 0 and col % 2 == 0]  # type: ignore
            excel_df.drop(columns=cols_to_drop, inplace=True)

            # Replace all cels with '-' with 0
            excel_df.replace("-", 0, inplace=True)  # type: ignore

            # Split the dataframe in 3 parts, 1 per sex
            ambos_sexos_index = excel_df[0].eq("Ambos sexos").idxmax()  # type: ignore
            hombres_index = excel_df[0].eq("Hombres").idxmax()  # type: ignore
            mujeres_index = excel_df[0].eq("Mujeres").idxmax()  # type: ignore
            dfs_per_sex = {
                "Ambos sexos": excel_df.iloc[ambos_sexos_index + 1 : hombres_index],  # type: ignore
                "Hombres": excel_df.iloc[hombres_index + 1 : mujeres_index],  # type: ignore
                "Mujeres": excel_df.iloc[mujeres_index + 1 : -8],  # type: ignore
            }

            # Unify all "other nationalities" under a single category
            for key, df_sex in dfs_per_sex.items():
                categories_to_unify = [
                    "Otros Oceanía",
                    "Otros Resto de Europa",
                    "Otros África",
                    "Otros Asia",
                    "Otros América Central y del Sur",
                ]

                # Calculate the sum of the rows that match the categories to unify
                rows_to_unify = df_sex[df_sex[0].isin(categories_to_unify)].copy()  # type: ignore
                summed = rows_to_unify.iloc[:, 1:].sum()  # type: ignore
                new_row = pd.Series(["Otros"] + summed.tolist(), index=df_sex.columns)

                # Remove the rows that match the categories to unify and add the new row
                df_sex = df_sex[~df_sex[0].isin(categories_to_unify)].copy()  # type: ignore
                df_sex = pd.concat([df_sex, pd.DataFrame([new_row])], ignore_index=True)
                dfs_per_sex[key] = df_sex

            # Iterate over each cell in the dataframes and create a record for each one
            for key, df in dfs_per_sex.items():
                sex = key
                for col in df.columns[1:]:
                    regimen = regimen_headers[col]  # type: ignore
                    grupo_edad = grupo_edad_headers[col]  # type: ignore
                    for _, row in df.iterrows():  # type: ignore
                        nacionalidad = row[0]  # type: ignore
                        total = row[col]  # type: ignore
                        all_records.append(  # type: ignore
                            {
                                "Provincia": provincia,
                                "Sexo": sex,
                                "Principales nacionalidades": nacionalidad,
                                "Régimen": regimen,
                                "Grupo de edad": grupo_edad,
                                "Fecha": date,
                                "Total": total,
                            }
                        )
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")

    return pd.DataFrame(all_records)


def excel_directory_historic_evolution_to_df(dir: Path) -> pd.DataFrame:
    """Read all excel files from a directroy and return a DataFrame with table 1 of each one"""

    all_records = []
    for file in dir.glob("*.xls"):
        try:
            excel_df = pd.read_excel(file, sheet_name="1", header=None)  # type: ignore

            # Remove '\xa0' characters from the dataframe
            excel_df[excel_df.columns[0]] = (
                excel_df[excel_df.columns[0]].astype(str).str.replace("\xa0", "", regex=False).str.lstrip()
            )

            # Special case for a file with a different format, make it match the other files format
            if file.name == "Extranjeros_con_certificado_RD_PROV_18_Granada_2010.xls":
                excel_df.replace("AELC-EFTA (*)", "AELC1", inplace=True)  # type: ignore
                excel_df.replace("Apátridas y No consta", "No consta", inplace=True)  # type: ignore
                excel_df.replace(  # type: ignore
                    r".*Régimen Comunitario.*", "Régimen de libre circulación UE", regex=True, inplace=True
                )
                excel_df.iloc[3], excel_df.iloc[4] = excel_df.iloc[4], excel_df.iloc[3]  # type: ignore
                excel_df = pd.concat([excel_df, pd.DataFrame([[""] * len(excel_df.columns)])], ignore_index=True)

            # Drop last 48 columns (they are not needed)
            excel_df.drop(columns=excel_df.columns[-48:], inplace=True)

            # Extract provincia and headers
            provincia = excel_df.iloc[1].iloc[0]  # type: ignore
            regimen_headers = excel_df.iloc[3].ffill().copy()  # type: ignore
            regimen_headers = regimen_headers.str.strip()  # type: ignore
            anio_headers = excel_df.iloc[5].ffill().copy()  # type: ignore
            excel_df.to_csv("data/debug/granada_raw.csv", index=False, sep=";")  # type: ignore

            # Replace all cels with '-' with 0
            for col in excel_df.columns:
                excel_df[col] = excel_df[col].map(lambda x: 0 if x == "-" else x)  # type: ignore

            # Split the dataframe in 3 parts, 1 per sex
            ambos_sexos_index = excel_df[0].eq("Ambos sexos").idxmax()  # type: ignore
            hombres_index = excel_df[0].eq("Hombres").idxmax()  # type: ignore
            mujeres_index = excel_df[0].eq("Mujeres").idxmax()  # type: ignore
            dfs_per_sex = {
                "Ambos sexos": excel_df.iloc[ambos_sexos_index + 1 : hombres_index],  # type: ignore
                "Hombres": excel_df.iloc[hombres_index + 1 : mujeres_index],  # type: ignore
                "Mujeres": excel_df.iloc[mujeres_index + 1 : -11],  # type: ignore
            }
            for key, df in dfs_per_sex.items():
                df.to_csv(f"data/debug/{key}.csv", index=False, sep=";")  # type: ignore

            # Unify all "other nationalities" under a single category
            for key, df_sex in dfs_per_sex.items():
                categories_to_unify = [
                    "Otros Oceanía",
                    "Otros Resto de Europa",
                    "Otros África",
                    "Otros Asia",
                    "Otros América Central y del Sur",
                ]

                # Calculate the sum of the rows that match the categories to unify
                rows_to_unify = df_sex[df_sex[0].isin(categories_to_unify)].copy()  # type: ignore
                summed = rows_to_unify.iloc[:, 1:].sum()  # type: ignore
                new_row = pd.Series(["Otros"] + summed.tolist(), index=df_sex.columns)

                # Remove the rows that match the categories to unify and add the new row
                df_sex = df_sex[~df_sex[0].isin(categories_to_unify)].copy()  # type: ignore
                df_sex = pd.concat([df_sex, pd.DataFrame([new_row])], ignore_index=True)
                dfs_per_sex[key] = df_sex

            # Iterate over each cell in the dataframes and create a record for each one
            for key, df in dfs_per_sex.items():
                sex = key
                for col in df.columns[1:]:
                    regimen = regimen_headers[col]  # type: ignore
                    for _, row in df.iterrows():  # type: ignore
                        nacionalidad = row[0]  # type: ignore
                        total = row[col]  # type: ignore
                        anio = anio_headers[col]  # type: ignore
                        if isinstance(anio, str):
                            anio = anio.split(" ")[0]
                        if anio != 2010:
                            all_records.append(  # type: ignore
                                {
                                    "Provincia": provincia,
                                    "Sexo": sex,
                                    "Principales nacionalidades": nacionalidad,
                                    "Régimen": regimen,
                                    "Fecha": f"{int(anio)}-12-31",  # type: ignore
                                    "Total": total,
                                }
                            )
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
    pd.DataFrame(all_records).to_csv("data/debug/opi_cleaned.csv", index=False, sep=";")
    return pd.DataFrame(all_records)


def main():
    try:
        # Read csvs files and concat into a DataFrame
        df_post_2013_1 = pd.read_csv(RAW_CSV_PATH_POST_2013_1, sep="\t")  # type: ignore
        df_post_2013_1["Tipo de documentación"] = "Autorización"
        df_post_2013_1["Régimen"] = "Régimen General"
        df_post_2013_2 = pd.read_csv(RAW_CSV_PATH_POST_2013_2, sep="\t")  # type: ignore
        df_post_2013_2["Régimen"] = "Régimen de libre circulación UE"
        df_2012 = excel_directory_to_df(RAW_CSV_DIR_2012)
        df_2012["Tipo de documentación"] = None
        df_2012["Lugar de nacimiento"] = None
        df_2011 = excel_directory_to_df(RAW_CSV_DIR_2011)
        df_2011["Tipo de documentación"] = None
        df_2011["Lugar de nacimiento"] = None
        df_2010 = excel_directory_to_df(RAW_CSV_DIR_2010)
        df_2010["Tipo de documentación"] = None
        df_2010["Lugar de nacimiento"] = None
        df_2002_2009 = excel_directory_historic_evolution_to_df(RAW_CSV_DIR_2010)
        df = pd.concat([df_post_2013_1, df_post_2013_2, df_2012, df_2011, df_2010, df_2002_2009], ignore_index=True)

        # Rename columns
        df.rename(
            columns={
                "Provincia": "provincia_id",
                "Principales nacionalidades": "nacionalidad",
                "Tipo de documentación": "tipo_documentacion",
                "Sexo": "sexo",
                "Lugar de nacimiento": "es_nacido_espania",
                "Grupo de edad": "grupo_edad",
                "Fecha": "fecha",
                "Total": "personas_autorizacion_residencia",
                "Régimen": "regimen",
            },
            inplace=True,
        )

        # Drop all rows with aggregated data (e.g., "TOTAL")
        num_rows_before = len(df)
        df = df[df["provincia_id"] != "Total nacional"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'provincia_id'.")

        num_rows_before = len(df)
        groups_to_drop = [
            "Europa",
            "UE-15",
            "UE-25",
            "UE-27",
            "Unión Europea",
            "AELC1",
            "Resto de Europa",
            "África",
            "América del Norte",
            "América Central y del Sur",
            "Asia",
            "Oceanía",
            "Todas las nacionalidades",
            "Total",
        ]
        df = df[~df["nacionalidad"].isin(groups_to_drop)]  # type: ignore
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'nacionalidad'.")

        num_rows_before = len(df)
        df = df[df["tipo_documentacion"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'tipo_documentacion'.")

        num_rows_before = len(df)
        df = df[df["sexo"] != "Ambos sexos"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'sexo'.")

        num_rows_before = len(df)
        df = df[df["es_nacido_espania"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'es_nacido_espania'.")

        num_rows_before = len(df)
        df = df[df["grupo_edad"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'grupo_edad'.")

        num_rows_before = len(df)
        df = df[df["regimen"] != "Total"]
        logging.warning(f"Dropped {num_rows_before - len(df)} rows with aggregated data for 'regimen'.")

        # Remove thousands separator dots from personas_autorizacion_residencia
        df["personas_autorizacion_residencia"] = (
            df["personas_autorizacion_residencia"].astype(str).str.replace(".", "", regex=False)
        )

        # Convert nan to None
        df = df.where(pd.notnull(df), None)  # type: ignore

        # Normalize and validate columns
        df["provincia_id"] = apply_and_check(df["provincia_id"], normalize_provincia)
        df["nacionalidad"] = apply_and_check(df["nacionalidad"], normalize_nationality)
        df["tipo_documentacion"] = apply_and_check_dict(
            df["tipo_documentacion"],
            {v: v for v in ["Autorización", "Certificado de registro", "TIE-Acuerdo de Retirada"]},
        )
        df["sexo"] = apply_and_check_dict(df["sexo"], {"Hombres": "Hombre", "Mujeres": "Mujer"})
        df["es_nacido_espania"] = apply_and_check_dict(
            df["es_nacido_espania"],
            {"España": True, "Extranjero": False},
        )
        df["grupo_edad"] = apply_and_check(df["grupo_edad"], normalize_age_group)
        df["fecha"] = apply_and_check(df["fecha"], normalize_date)
        df["personas_autorizacion_residencia"] = apply_and_check(
            df["personas_autorizacion_residencia"], normalize_positive_integer
        )
        df["regimen"] = apply_and_check_dict(
            df["regimen"],
            {v: v for v in ["Régimen General", "Régimen de libre circulación UE"]},
        )

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
