from typing import Dict

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_fuentes(conn: Connection, df: pd.DataFrame) -> None:
    """Load fuentes and fuentes_tablas tables from a single CSV."""

    # Check tabla_nombre existence in db
    table_names = set(df["tabla_nombre"].unique())  # type: ignore
    placeholders = ", ".join([f":t{i}" for i in range(len(table_names))])
    query = (
        f"SELECT table_name FROM information_schema.tables "
        f"WHERE table_schema = 'public' AND table_name IN ({placeholders})"
    )
    params = {f"t{i}": name for i, name in enumerate(table_names)}
    result = conn.execute(text(query), params)
    existing_tables = {row[0] for row in result.fetchall()}
    missing_tables = table_names - existing_tables
    if missing_tables:
        raise RuntimeError(f"The following tables are not in the database: {missing_tables}")

    fuentes_df = (
        df[["fuente_nombre", "descripcion", "url"]]
        .drop_duplicates(subset="fuente_nombre")
        .rename(columns={"fuente_nombre": "nombre"})
    )

    # Insert fuentes into the database retrieving their ids
    fuente_ids: Dict[str, int] = {}
    for _, row in fuentes_df.iterrows():  # type: ignore
        result = conn.execute(
            text(("INSERT INTO fuentes (nombre) VALUES (:nombre) RETURNING fuente_id")),
            {"nombre": row["nombre"]},
        )
        fuente_ids[row["nombre"]] = result.scalar_one()

    # Insert fuentes_tablas with the corresponding fuente_id
    for _, row in df.iterrows():  # type: ignore
        conn.execute(
            text(
                "INSERT INTO fuentes_tablas (fuente_id, nombre, fecha_actualizacion, descripcion, url) "
                "VALUES (:fuente_id, :nombre, :fecha_actualizacion, :descripcion, :url)"
            ),
            {
                "fuente_id": fuente_ids[row["fuente_nombre"]],
                "nombre": row["tabla_nombre"],
                "fecha_actualizacion": row["fecha_actualizacion"],
                "descripcion": row["descripcion"] if pd.notnull(row["descripcion"]) else None,  # type: ignore
                "url": row["url"],
            },
        )
