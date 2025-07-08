import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_poblacion_grupo_edad(conn: Connection, df: pd.DataFrame) -> None:
    """Load poblacion_grupo_edad table from a DataFrame."""

    # Get mapping from nacionalidad nombre to id
    result = conn.execute(text("SELECT nacionalidad, nacionalidad_id FROM nacionalidades"))
    rows = result.fetchall()
    nacionalidad_map = {row[0]: row[1] for row in rows}

    # Replace 'nacionalidad' in df with its corresponding id
    df = df.copy()
    df["nacionalidad_id"] = df["nacionalidad"].map(nacionalidad_map)  # type: ignore

    # Check for unmapped nacionalidades
    unmapped = df[df["nacionalidad_id"].isna()]["nacionalidad"].unique().tolist()  # type: ignore
    if len(unmapped) > 0:  # type: ignore
        raise ValueError(f"Unmapped nacionalidad values: {unmapped}")

    # Drop the original nacionalidad column
    df.drop(columns=["nacionalidad"], inplace=True)  # type: ignore

    # Insert into table
    df.to_sql("poblacion_grupo_edad", con=conn, if_exists="append", index=False)
