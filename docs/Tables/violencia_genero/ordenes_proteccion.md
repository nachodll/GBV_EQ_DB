# violencia_genero.ordenes_proteccion

**Data loading script:** `pipelines/extract_transform/violencia_genero/011_et_ordenes_proteccion.py`

## Columns

- `ordenes_proteccion_id serial PRIMARY KEY`
- `estado_proceso enums.estado_orden_proteccion_enum NOT NULL`
- `instancia enums.instancia_orden_proteccion_enum NOT NULL`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4)`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `ordenes_proteccion int NOT NULL CHECK (ordenes_proteccion >= 0)`
