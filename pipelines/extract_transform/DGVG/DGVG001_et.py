import os

import pandas as pd

from utils.normalization import normalize_month, normalize_provincia

# Paths
raw_csv_path = os.path.join("data", "raw", "DGVG", "DGVG001-010FeminicidiosPareja.csv")
clean_csv_path = os.path.join("data", "clean", "feminicidios_pareja.csv")

# Read file
df = pd.read_csv(raw_csv_path)

# Delete spaces
df.columns = df.columns.str.strip()

# Rename columns
df = df.rename(
    columns={
        "Provincia (As)": "provincia_id",
        "Año": "año",
        "Mes": "mes",
        "VM Grupo de edad": "edad_grupo_victima",
        "AG Grupo de edad": "edad_grupo_agresor",
        "Feminicidios pareja o expareja": "feminicidios",
        "Huérfanas y huérfanos menores de edad -1-": "huerfanos_menores",
    }
)

# Validate year and cast to integer
df["año"] = pd.to_numeric(df["año"], errors="coerce")
df.loc[~df["año"].between(1900, 2050), "año"] = None
if df["año"].isnull().any():
    invalid_years = df[df["año"].isnull()]["año"].unique()
    raise ValueError(f"Invalid year values found: {invalid_years}")
df["año"] = df["año"].astype(int)

# Normalize months
df["mes"] = df["mes"].map(normalize_month)
if df["mes"].isnull().any():
    missing_months = df[df["mes"].isnull()]["mes"].unique()
    raise ValueError(f"Unmapped months found: {missing_months}")

# Normalize provinces
df["provincia_id"] = df["provincia_id"].map(normalize_provincia)
if df["provincia_id"].isnull().any():
    missing = df[df["provincia_id"].isnull()]["provincia_id"].unique()
    raise ValueError(f"Unmapped provinces found: {missing}")

# Save cleaned CSV
os.makedirs(os.path.dirname(clean_csv_path), exist_ok=True)
df.to_csv(clean_csv_path, index=False)
print(f"Cleaned data saved to {clean_csv_path}")
