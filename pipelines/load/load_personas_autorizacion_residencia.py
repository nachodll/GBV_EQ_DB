import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_personas_autorizacion_residencia(conn: Connection, df: pd.DataFrame) -> None:
    """Load personas_autorizacion_residencia table from a DataFrame."""

    # Get mapping from pais nombre to id (nan are mapped to None and saved as NULL in the database)
    result = conn.execute(text("SELECT pais, pais_id FROM paises"))
    rows = result.fetchall()
    nacionalidad_map = {row[0]: row[1] for row in rows}
    nacionalidad_map[np.nan] = None  # type: ignore

    # Check for unmapped nacionalidades before mapping (nan values are not in the map)
    unmapped = df[~df["nacionalidad"].isin(nacionalidad_map.keys())]["nacionalidad"].unique().tolist()  # type: ignore
    if len(unmapped) > 0:  # type: ignore
        raise ValueError(f"Unmapped nacionalidad values: {unmapped}")

    # Replace 'nacionalidad' in df with its corresponding id
    df = df.copy()
    df["nacionalidad"] = df["nacionalidad"].map(nacionalidad_map)  # type: ignore

    # Insert into table
    df.to_sql("personas_autorizacion_residencia", con=conn, if_exists="append", index=False)
