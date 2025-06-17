import os

import pandas as pd
import pyreadstat

from utils.normalization import normalize_comunidad_autonoma, normalize_provincia

output_dir = os.path.join("data", "preliminary-merge")

# PRE001 - Feminicidios pareja
pre001_path = os.path.join("data", "raw", "DGVG", "DGVG001-010FeminicidiosPareja.csv")
pre001 = pd.read_csv(pre001_path)
pre001.rename(columns={"Provincia (As)": "Provincia"}, inplace=True)
pre001["Provincia"] = pre001["Provincia"].apply(normalize_provincia)
pre001_csv_path = os.path.join(output_dir, "PRE001-FeminicidiosPareja.csv")
pre001.to_csv(pre001_csv_path, index=False)

# PRE002 - Feminicidios Fuera Pareja
pre002_path = os.path.join("data", "raw", "DGVG", "DGVG002-020FeminicidiosFueraParejaExpareja.csv")
pre002 = pd.read_csv(pre002_path)
pre002.rename(columns={"Comunidad autónoma (As)": "Comunidad autónoma"}, inplace=True)
pre002["Comunidad autónoma"] = pre002["Comunidad autónoma"].apply(normalize_comunidad_autonoma)
pre002_csv_path = os.path.join(output_dir, "PRE002-FeminicidiosFueraPareja.csv")
pre002.to_csv(pre002_csv_path, index=False)

# PRE003 - VioGen
pre003_path = os.path.join("data", "raw", "DGVG", "DGVG008-090VioGenSistemaSeguimientoIntegral.csv")
pre003 = pd.read_csv(pre003_path)
pre003["Comunidad autónoma"] = pre003["Comunidad autónoma"].apply(normalize_comunidad_autonoma)
pre003_csv_path = os.path.join(output_dir, "PRE003-VioGen.csv")
pre003.to_csv(pre003_csv_path, index=False)

# PRE004 - Servicio 016
pre004 = os.path.join("data", "raw", "DGVG", "DGVG004-040Servicio016.csv")
pre004 = pd.read_csv(pre004)
pre004["Provincia"] = pre004["Provincia"].apply(normalize_provincia)
pre004_csv_path = os.path.join(output_dir, "PRE004-Servicio016.csv")
pre004.to_csv(pre004_csv_path, index=False)

# PRE005 - Denuncias VDG Incoadas según Tipo de Infracción
pre005_path = os.path.join("data", "raw", "INE", "INE020-DenunciasIncoadasTipoInfracción.csv")
pre005 = pd.read_csv(pre005_path, sep=";")
pre005.rename(columns={"Comunidades y ciudades autónomas": "Comunidad autónoma"}, inplace=True)
pre005["Comunidad autónoma"] = pre005["Comunidad autónoma"].apply(normalize_comunidad_autonoma)
pre005_csv_path = os.path.join(output_dir, "PRE005-DenunciasVDG.csv")
pre005.to_csv(pre005_csv_path, index=False)

# PRE006 - Macroencuestas Violencia de Género
pre006_dir = os.path.join("data", "raw", "CIS")
pre006_path_2019 = os.path.join(pre006_dir, "CIS001-Macroencuesta2019", "3235.sav")
pre006_path_2015 = os.path.join(pre006_dir, "CIS002-Macroencuesta2015", "3027.sav")
pre006_2019, meta = pyreadstat.read_sav(pre006_path_2019, apply_value_formats=True)
pre006_2015, meta = pyreadstat.read_sav(pre006_path_2015, apply_value_formats=True)

# Extract common variables and add metadata for both years
pre006_2019_subset = pre006_2019[["CUES", "CCAA", "PROV"]].copy()
pre006_2019_subset["ESTUDIO"] = 3235
pre006_2019_subset["AÑO"] = 2019
pre006_2019_subset["MES"] = "Septiembre"
pre006_2015_subset = pre006_2015[["CUES", "CCAA", "PROV"]].copy()
pre006_2015_subset["ESTUDIO"] = 3027
pre006_2015_subset["AÑO"] = 2014
pre006_2015_subset["MES"] = "Septiembre"

# Define the variable mappings
var_mapping_2019 = {
    "VS1P": ["M1P5_0_4", "M2P5_0_4"],
    "VS2P": ["M1P5_0_2", "M2P5_0_2"],
    "VS3P": ["M1P5_0_8", "M2P5_0_8"],
    "VS1FP": ["M3P2_4"],
    "VF1P": ["M1P4_0_1", "M2P4_0_1"],
    "VF2P": ["M1P4_0_2", "M2P4_0_2"],
    "VF3P": ["M1P4_0_3", "M2P4_0_3"],
    "VF4P": ["M1P4_0_4", "M2P4_0_4"],
    "VF5P": ["M1P4_0_5", "M2P4_0_5"],
    "VF6P": ["M1P4_0_6", "M2P4_0_6"],
    "VF2FP": ["M3P1_2"],
    "VF5FP": ["M3P1_5"],
    "VF6FP": ["M3P1_6"],
}

var_mapping_2015 = {
    "VS1P": ["P2201", "P3101"],
    "VS2P": ["P2202", "P3102"],
    "VS3P": ["P2203", "P3103"],
    "VS1FP": ["P52"],
    "VF1P": ["P2101", "P3001"],
    "VF2P": ["P2102", "P3002"],
    "VF3P": ["P2103", "P3003"],
    "VF4P": ["P2104", "P3004"],
    "VF5P": ["P2105", "P3005"],
    "VF6P": ["P2106", "P3006"],
    "VF2FP": ["P4803"],
    "VF5FP": ["P4804"],
    "VF6FP": ["P4805"],
}

# Apply conditions for 2019
for var, columns in var_mapping_2019.items():
    pre006_2019_subset[var] = pre006_2019[columns].eq("Sí").any(axis=1)

# Apply conditions for 2015
for var, columns in var_mapping_2015.items():
    pre006_2015_subset[var] = pre006_2015[columns].eq("Sí").any(axis=1)

# Concatenate the two subsets and rename columns
pre006 = pd.concat([pre006_2019_subset, pre006_2015_subset], ignore_index=True)
pre006.rename(
    columns={
        "CCAA": "Comunidad autónoma",
        "PROV": "Provincia",
        "CUES": "Numero cuesionario",
        "ESTUDIO": "Código estudio",
        "AÑO": "Año",
        "MES": "Mes",
    },
    inplace=True,
)
pre006["Comunidad autónoma"] = pre006["Comunidad autónoma"].apply(normalize_comunidad_autonoma)
pre006["Provincia"] = pre006["Provincia"].apply(normalize_provincia)

pre006_csv_path = os.path.join(output_dir, "PRE006-MacroencuestasVDG.csv")
pre006.to_csv(pre006_csv_path, index=False)
