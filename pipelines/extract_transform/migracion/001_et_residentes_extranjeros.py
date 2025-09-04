"""Extract and transform data
Sources:
    OPI001, (2013-present, autorización de residencia)
    OPI002, (2013-present, certificado de registro or acuerdo de retirada)
    OPI003, OPI004, OPI005, (2012, 2011, 2010 and 2002-2009 historic evolution)
    OPI006, OPI
Target tables:
    residentes_extranjeros
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
RAW_XLS_DIR_2012 = Path("data") / "raw" / "OPI" / "OPI003-2012"
RAW_XLS_DIR_2011 = Path("data") / "raw" / "OPI" / "OPI004-2011"
RAW_XLS_DIR_2010 = Path("data") / "raw" / "OPI" / "OPI005-2010"
RAW_XLS_PATH_2001 = Path("data") / "raw" / "OPI" / "OPI006-2001.xls"
RAW_XLS_PATH_2000 = Path("data") / "raw" / "OPI" / "OPI007-2000.xls"
RAW_XLS_PATH_1999 = Path("data") / "raw" / "OPI" / "OPI008-1999.xls"
RAW_XLS_PATH_1998 = Path("data") / "raw" / "OPI" / "OPI009-1998.xls"
RAW_XLS_PATH_1997 = Path("data") / "raw" / "OPI" / "OPI010-1997.xls"
RAW_XLS_PATH_1996 = Path("data") / "raw" / "OPI" / "OPI011-1996.xls"

CLEAN_CSV_PATH = Path("data") / "clean" / "migracion" / "residentes_extranjeros.csv"


def excel_1996_to_df(file: Path) -> pd.DataFrame:
    """Read an excel file and return a DataFrame with table 1. Used for year 1997."""
    try:
        excel_df = pd.read_excel(file, sheet_name="1", header=None)  # type: ignore

        # Extract headers
        year = file.name.split("-")[-1].split(".")[0]
        nationality_headers = excel_df.iloc[6].ffill().copy()  # type: ignore

        # Drop first 6 rows
        excel_df = excel_df.drop(index=excel_df.index[:7]).reset_index(drop=True)  # type: ignore

        # Replace '-' with 0 and convert to int
        excel_df.loc[:, excel_df.columns[1:]] = (
            excel_df.loc[:, excel_df.columns[1:]].replace("-", 0).infer_objects(copy=False)  # type: ignore
        )

        # Unify all "other nationalities" under a single category
        countries_to_unify = [
            "OTROS AMÉRICA",
            "OTROS  ASIA",
            "OTR. RES. AFR.",
            "OTROS OCEANÍA",
            "OTROS\nEUR. ESTE",
            "     OTROS",
        ]
        cols_to_unify = [col for col in excel_df.columns if nationality_headers[col] in countries_to_unify]
        new_column = excel_df.loc[:, cols_to_unify].sum(axis=1)  # type: ignore
        otros_idx = nationality_headers[nationality_headers == "     OTROS"].index[0]  # type: ignore
        excel_df.loc[:, otros_idx] = new_column  # type: ignore
        # Drop all columns that were unified into "otros" but "otros" itself
        cols_to_drop = [col for col in cols_to_unify if int(col) != int(otros_idx)]  # type: ignore
        excel_df.drop(columns=cols_to_drop, inplace=True)  # type: ignore
        nationality_headers = nationality_headers[~nationality_headers.index.isin(cols_to_drop)]  # type: ignore

        all_records = []
        for col in excel_df.columns[1:]:
            for row in excel_df.index:
                total = excel_df.loc[row, col]  # type: ignore
                all_records.append(  # type: ignore
                    {
                        "Provincia": excel_df.loc[row, 0],  # type: ignore
                        "Principales nacionalidades": nationality_headers[col],
                        "Fecha": f"{year}-12-31",
                        "Total": total,
                    }
                )
        df = pd.DataFrame(all_records)

        # Drop all ccaa aggregated data
        aggregated_to_drop = [
            "TOTALES",
            "ANDALUCÍA",
            "ARAGÓN",
            "CANARIAS",
            "CASTILLA-LEÓN",
            "CAST-LA MANCHA",
            "CATALUÑA",
            "COM.VALENCIANA",
            "EXTREMADURA",
            "GALICIA",
            "PAÍS VASCO",
        ]
        df = df[~df["Provincia"].isin(aggregated_to_drop)]  # type: ignore

        # Drop all countries aggregated data
        countries_to_drop = [
            "TOT. REST.EUROPA",
            "        TOTAL U.E.",
            "TOTAL ÁFRICA",
            "OTROS AMÉRICA",
            "TOTAL OCEANÍA",
            "TOTAL AMÉRICA",
            "TOT.IBEROAMÉRICA",
            "      TOTAL EUROPA",
            "TOT. ÁFRICA NORTE",
            "TOT. RES. AFR.",
            "TOTAL\nEUR. ESTE",
            "TOTAL RES. AMER.",
            "TOTAL ASIA",
        ]
        df = df[~df["Principales nacionalidades"].isin(countries_to_drop)]  # type: ignore

        # Adapt to the expected format
        df["Principales nacionalidades"] = df["Principales nacionalidades"].replace("APÁTRIDAS, NO CONSTA", "No consta")  # type: ignore
        df["Total"] = df["Total"].fillna(0)  # type: ignore

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file}")
    except Exception as e:
        raise ValueError(f"Error reading {file}: {e}")


def excel_2000_1997_to_df(file: Path) -> pd.DataFrame:
    """Read an excel file and return a DataFrame with table 10. Used for years 2000-1997."""

    try:
        excel_df = pd.read_excel(file, sheet_name="10", header=None)  # type: ignore

        # Remove column 4
        excel_df.drop(columns=[4], inplace=True)

        year = file.name.split("-")[-1].split(".")[0]
        sexo_headers = excel_df.iloc[6].ffill().copy()  # type: ignore

        all_records = []
        for col in excel_df.columns[1:]:
            for row in excel_df.index[8:]:
                total = excel_df.loc[row, col]  # type: ignore
                if total != "-":
                    all_records.append(  # type: ignore
                        {
                            "Provincia": excel_df.loc[row, 0],  # type: ignore
                            "Sexo": sexo_headers[col],
                            "Fecha": f"{year}-12-31",
                            "Total": total,
                        }
                    )

        df = pd.DataFrame(all_records)

        # Drop all columns with aggregated data
        aggregated_to_drop = [
            "TOTALES",
            "ANDALUCÍA",
            "ARAGÓN",
            "CANARIAS",
            "CASTILLA-LEÓN",
            "CAST-LA MANCHA",
            "CATALUÑA",
            "COM.VALENCIANA",
            "EXTREMADURA",
            "GALICIA",
            "PAÍS VASCO",
        ]
        df = df[~df["Provincia"].isin(aggregated_to_drop)]  # type: ignore

        # Adapt to the expected format
        df["Sexo"] = df["Sexo"].replace("VARONES", "Hombres")  # type: ignore
        df["Sexo"] = df["Sexo"].replace("MUJERES", "Mujeres")  # type: ignore

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file}")
    except Exception as e:
        raise ValueError(f"Error reading {file}: {e}")


def excel_2001_to_df(file: Path) -> pd.DataFrame:
    """Read an excel file and return a DataFrame with table 8. Used for year 2001."""

    try:
        excel_df = pd.read_excel(file, sheet_name="8", header=None)  # type: ignore

        # Remove columns 4 and 8 (percentages are not needed)
        excel_df.drop(columns=[4, 8], inplace=True)

        # Extract headers
        year = file.name.split("-")[-1].split(".")[0]
        regimen_headers = excel_df.iloc[6].ffill().copy()  # type: ignore
        sexo_headers = excel_df.iloc[7].ffill().copy()  # type: ignore

        all_records = []
        for col in excel_df.columns[1:]:
            for row in excel_df.index[8:]:
                total = excel_df.loc[row, col]  # type: ignore
                if total != "-":
                    all_records.append(  # type: ignore
                        {
                            "Provincia": excel_df.loc[row, 0],  # type: ignore
                            "Sexo": sexo_headers[col],
                            "Régimen": regimen_headers[col],
                            "Fecha": f"{year}-12-31",
                            "Total": total,
                        }
                    )

        df = pd.DataFrame(all_records)

        # Drop all columns with aggregated data
        aggregated_to_drop = [
            "TOTAL",
            "ANDALUCÍA",
            "ARAGÓN",
            "CANARIAS",
            "CASTILLA Y LEÓN",
            "CASTILLA - LA MANCHA",
            "CATALUÑA",
            "COM. VALENCIANA",
            "EXTREMADURA",
            "GALICIA",
            "PAÍS VASCO",
        ]
        df = df[~df["Provincia"].isin(aggregated_to_drop)]  # type: ignore

        # Adapt to the expected format
        df["Sexo"] = df["Sexo"].replace("VARONES", "Hombres")  # type: ignore
        df["Sexo"] = df["Sexo"].replace("MUJERES", "Mujeres")  # type: ignore
        df["Régimen"] = df["Régimen"].replace("RÉGIMEN COMUNITARIO", "Régimen de libre circulación UE")  # type: ignore
        df["Régimen"] = df["Régimen"].replace("RÉGIMEN GENERAL", "Régimen General")  # type: ignore

        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file}")
    except Exception as e:
        raise ValueError(f"Error reading {file}: {e}")


def excel_directory_to_df(dir: Path) -> pd.DataFrame:
    """Used for years 2012, 2011 and 2010.
    Read all excel files from a directory and return a DataFrame with table 4 of each one"""

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

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file}")
        except Exception as e:
            raise ValueError(f"Error reading {file}: {e}")

    return pd.DataFrame(all_records)


def excel_directory_historic_evolution_to_df(dir: Path) -> pd.DataFrame:
    """Used for years 2002-2009 data present in OPI005.
    Read all excel files from a directroy and return a DataFrame with table 1 of each one"""

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

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file}")
        except Exception as e:
            raise ValueError(f"Error reading {file}: {e}")
    return pd.DataFrame(all_records)


def csv_post_2013(path: Path) -> pd.DataFrame:
    """Read a csv file and return a DataFrame with the post 2013 data."""

    df = pd.read_csv(path, sep="\t", thousands=".")  # type: ignore

    if "Tipo de documentación" not in df.columns:
        df["Tipo de documentación"] = "Autorización"
        df["Régimen"] = "Régimen General"
    else:
        df["Régimen"] = "Régimen de libre circulación UE"

    return df


def main():
    try:
        # Read csvs files and concat into a DataFrame
        df_post_2013_1 = csv_post_2013(RAW_CSV_PATH_POST_2013_1)
        df_post_2013_2 = csv_post_2013(RAW_CSV_PATH_POST_2013_2)
        df_2012 = excel_directory_to_df(RAW_XLS_DIR_2012)
        df_2011 = excel_directory_to_df(RAW_XLS_DIR_2011)
        df_2010 = excel_directory_to_df(RAW_XLS_DIR_2010)
        df_2002_2009 = excel_directory_historic_evolution_to_df(RAW_XLS_DIR_2010)
        df_2001 = excel_2001_to_df(RAW_XLS_PATH_2001)
        df_2000 = excel_2000_1997_to_df(RAW_XLS_PATH_2000)
        df_1999 = excel_2000_1997_to_df(RAW_XLS_PATH_1999)
        df_1998 = excel_2000_1997_to_df(RAW_XLS_PATH_1998)
        df_1997 = excel_2000_1997_to_df(RAW_XLS_PATH_1997)
        df_1996 = excel_1996_to_df(RAW_XLS_PATH_1996)

        df = pd.concat(
            [
                df_post_2013_1,
                df_post_2013_2,
                df_2012,
                df_2011,
                df_2010,
                df_2002_2009,
                df_2001,
                df_2000,
                df_1999,
                df_1998,
                df_1997,
                df_1996,
            ],
            ignore_index=True,
        )

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
                "Total": "residentes_extranjeros",
                "Régimen": "regimen",
            },
            inplace=True,
        )

        # Drop all rows with aggregated data (e.g., "TOTAL")
        df = df[df["provincia_id"] != "Total nacional"]
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
        df = df[df["tipo_documentacion"] != "Total"]
        df = df[df["sexo"] != "Ambos sexos"]
        df = df[df["es_nacido_espania"] != "Total"]
        df = df[df["grupo_edad"] != "Total"]
        df = df[df["regimen"] != "Total"]

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
        df["residentes_extranjeros"] = apply_and_check(df["residentes_extranjeros"], normalize_positive_integer)
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
