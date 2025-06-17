import os

import pandas as pd

from utils.normalization import normalize_comunidad_autonoma

# Paths
raw_csv_path = os.path.join("data", "raw", "DGVG", "DGVG002-020FeminicidiosFueraParejaExpareja.csv")
clean_csv_path = os.path.join("data", "clean", "feminicidios_no_pareja.csv")

# Read file
df = pd.read_csv(raw_csv_path)

# Delete spaces
df.columns = df.columns.str.strip()

# Rename columns
df = df.rename(
    columns={
        "Comunidad autónoma (As)": "comunidad_autonoma_id",
        "Año": "año",
        "Tipo de feminicidio": "tipo_feminicidio",
        "Feminicidos fuera pareja o expareja": "feminicidios",
    }
)

# Validate year and cast to integer
df["año"] = pd.to_numeric(df["año"], errors="coerce")
df.loc[~df["año"].between(1900, 2050), "año"] = None
if df["año"].isnull().any():
    invalid_years = df[df["año"].isnull()]["año"].unique()
    raise ValueError(f"Invalid year values found: {invalid_years}")
df["año"] = df["año"].astype(int)

# Normalize provinces
df["comunidad_autonoma_id"] = df["comunidad_autonoma_id"].map(normalize_comunidad_autonoma)
if df["comunidad_autonoma_id"].isnull().any():
    missing = df[df["comunidad_autonoma_id"].isnull()]["comunidad_autonoma_id"].unique()
    raise ValueError(f"Unmapped provinces found: {missing}")

# Save cleaned CSV
os.makedirs(os.path.dirname(clean_csv_path), exist_ok=True)
df.to_csv(clean_csv_path, index=False)
print(f"Cleaned data saved to {clean_csv_path}")
