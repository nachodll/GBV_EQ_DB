import os

import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine(
    (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST', 'localhost')}/"
        f"{os.getenv('DB_NAME')}"
    )
)

# Load CSVs
ccaa_df = pd.read_csv("data/static/ComunidadesAutónomas.csv")
prov_df = pd.read_csv("data/static/Provincias.csv")

# Insert into DB
with engine.begin() as conn:
    # Clear tables first (cascade to handle FK)
    conn.execute(text("TRUNCATE provincias RESTART IDENTITY CASCADE"))
    conn.execute(text("TRUNCATE comunidades_autonomas RESTART IDENTITY CASCADE"))

    # Load comunidades autónomas
    ccaa_df.to_sql(name="comunidades_autonomas", con=conn, if_exists="append", index=False)

    # Load provincias (FK comunidad_autonoma_id must already exist)
    prov_df.to_sql(name="provincias", con=conn, if_exists="append", index=False)

print("✅ Table 'comunidades_autonomas' loaded successfully.")
print("✅ Table 'provincias' loaded successfully.")
