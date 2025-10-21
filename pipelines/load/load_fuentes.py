from typing import Dict

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Connection


def load_fuentes(conn: Connection, df: pd.DataFrame) -> None:
    """Load fuentes and fuentes_tablas tables from a single CSV."""

    # Check tabla_nombre existence in db
    table_names = set(df["tabla_nombre"].unique())
    schema_table_pairs = [tuple(name.split(".", 1)) if "." in name else ("public", name) for name in table_names]
    placeholders = ", ".join([f"(:s{i}, :t{i})" for i in range(len(schema_table_pairs))])
    query = (
        f"SELECT table_schema, table_name FROM information_schema.tables "
        f"WHERE table_schema NOT IN ('pg_catalog', 'information_schema') "
        f"AND (table_schema, table_name) IN ({placeholders})"
    )
    params = {}
    for i, (schema, table) in enumerate(schema_table_pairs):
        params[f"s{i}"] = schema
        params[f"t{i}"] = table
    result = conn.execute(text(query), params)
    existing_pairs = {(row[0], row[1]) for row in result.fetchall()}
    missing_pairs = set(schema_table_pairs) - existing_pairs
    if missing_pairs:
        raise RuntimeError(f"The following tables are not in the database: {missing_pairs}")

    fuentes_df = (
        df[["fuente_nombre", "descripcion", "url"]]
        .drop_duplicates(subset="fuente_nombre")
        .rename(columns={"fuente_nombre": "nombre"})
    )

    # Insert fuentes into the database retrieving their ids
    fuente_ids: Dict[str, int] = {}
    for _, row in fuentes_df.iterrows():
        result = conn.execute(
            text(("INSERT INTO metadata.fuentes (nombre) VALUES (:nombre) RETURNING fuente_id")),
            {"nombre": row["nombre"]},
        )
        fuente_ids[row["nombre"]] = result.scalar_one()

    # Insert fuentes_tablas with the corresponding fuente_id
    for _, row in df.iterrows():
        conn.execute(
            text(
                "INSERT INTO metadata.fuentes_tablas (fuente_id, nombre, fecha_actualizacion, descripcion, url) "
                "VALUES (:fuente_id, :nombre, :fecha_actualizacion, :descripcion, :url)"
            ),
            {
                "fuente_id": fuente_ids[row["fuente_nombre"]],
                "nombre": row["tabla_nombre"],
                "fecha_actualizacion": row["fecha_actualizacion"],
                "descripcion": row["descripcion"] if pd.notnull(row["descripcion"]) else None,
                "url": row["url"],
            },
        )
