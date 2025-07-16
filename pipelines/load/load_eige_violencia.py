import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_eige_violencia(conn: Connection, df: pd.DataFrame) -> None:
    """Load eige_violencia table from a DataFrame."""

    # Get mapping from pais_id to id (nan are mapped to None and saved as NULL in the database)
    result = conn.execute(text("SELECT nombre, pais_id FROM geo.paises"))
    rows = result.fetchall()
    pais_map = {row[0]: row[1] for row in rows}
    pais_map[np.nan] = None  # type: ignore

    # Check for unmapped pais_id before mapping (nan values are not in the map)
    unmapped = df[~df["pais_id"].isin(pais_map.keys())]["pais_id"].unique().tolist()  # type: ignore
    if len(unmapped) > 0:  # type: ignore
        raise ValueError(f"Unmapped pais_id values: {unmapped}")

    # Replace 'pais_id' in df with its corresponding id
    df = df.copy()
    df["pais_id"] = df["pais_id"].map(pais_map)  # type: ignore

    # Insert into table
    df.to_sql("eige_violencia", schema="igualdad_formal", con=conn, if_exists="append", index=False)
