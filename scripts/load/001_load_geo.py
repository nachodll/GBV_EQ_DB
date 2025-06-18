"""Load static geographical data into the database.
Target tables:
    comunidades_autonomas
    provincias
"""

import logging
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

CCAA_PATH = Path("data") / "static" / "ComunidadesAutónomas.csv"
PROV_PATH = Path("data") / "static" / "Provincias.csv"

# Logger setup
logger = logging.getLogger(__name__)


def main():
    # Load csvs to dataframes
    ccaa_df = pd.read_csv(CCAA_PATH)  # type: ignore
    prov_df = pd.read_csv(PROV_PATH)  # type: ignore

    # Create database engine
    engine = create_engine(
        (
            f"postgresql://{os.getenv('DB_USER')}:"
            f"{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST', 'localhost')}/"
            f"{os.getenv('DB_NAME')}"
        )
    )

    # Insert into DB
    with engine.begin() as conn:
        # Clear tables first (cascade to handle FK)
        conn.execute(text("TRUNCATE provincias RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE comunidades_autonomas RESTART IDENTITY CASCADE"))

        # Load comunidades autónomas
        ccaa_df.to_sql(name="comunidades_autonomas", con=conn, if_exists="append", index=False)

        # Load provincias (FK comunidad_autonoma_id must already exist)
        prov_df.to_sql(name="provincias", con=conn, if_exists="append", index=False)

    logger.info("Table 'comunidades_autonomas' loaded successfully.")
    logger.info("Table 'provincias' loaded successfully.")


if __name__ == "__main__":
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    main()
