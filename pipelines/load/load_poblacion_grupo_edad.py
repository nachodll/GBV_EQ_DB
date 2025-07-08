import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_poblacion_grupo_edad(conn: Connection, df: pd.DataFrame) -> None:
    """Load poblacion_grupo_edad table from a DataFrame."""

    # Get mapping from pais nombre to id
    result = conn.execute(text("SELECT pais, pais_id FROM paises"))
    rows = result.fetchall()
    nacionalidad_map = {row[0]: row[1] for row in rows}

    # Replace 'nacionalidad' in df with its corresponding id
    df = df.copy()
    df["nacionalidad"] = df["nacionalidad"].map(nacionalidad_map)  # type: ignore

    # Check for unmapped nacionalidades
    unmapped = df[df["nacionalidad"].isna()]["nacionalidad"].unique().tolist()  # type: ignore
    unmapped_original = df[~df["nacionalidad"].isin(nacionalidad_map.keys())]["nacionalidad"].unique()  # type: ignore
    if len(unmapped) > 0:  # type: ignore
        raise ValueError(f"Unmapped nacionalidad values: {unmapped_original}")

    # Insert into table
    df.to_sql("poblacion_grupo_edad", con=conn, if_exists="append", index=False)
