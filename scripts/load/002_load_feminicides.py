import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

FEMINICIDIOS_PAREJA_PATH = Path("data") / "clean" / "feminicidios_pareja.csv"
FEMINICIDIOS_NO_PAREJA_PATH = Path("data") / "clean" / "feminicidios_no_pareja.csv"


def main():
    # Load CSVs to dataframes
    feminicidios_pareja_df = pd.read_csv(FEMINICIDIOS_PAREJA_PATH)[
        ["feminicidios", "huerfanos_menores", "provincia_id", "año", "mes", "edad_grupo_victima", "edad_grupo_agresor"]
    ]
    feminicidios_no_pareja_df = pd.read_csv(FEMINICIDIOS_NO_PAREJA_PATH)[
        ["feminicidios", "tipo_feminicidio", "comunidad_autonoma_id", "año"]
    ]

    # Create database engine
    engine = create_engine(
        (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST', 'localhost')}/"
            f"{os.getenv('DB_NAME')}"
        )
    )

    # Insert with full transaction
    with engine.begin() as conn:
        # Clear existing data
        conn.execute(text("TRUNCATE feminicidios_pareja RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE feminicidios_no_pareja RESTART IDENTITY CASCADE"))

        # Load data
        feminicidios_pareja_df.to_sql("feminicidios_pareja", con=conn, if_exists="append", index=False)
        feminicidios_no_pareja_df.to_sql("feminicidios_no_pareja", con=conn, if_exists="append", index=False)

    print("✅ Tables 'feminicidios_pareja' loaded succesfully.")
    print("✅ Table 'feminicidios_no_pareja' loaded successfully.")


if __name__ == "__main__":
    main()
