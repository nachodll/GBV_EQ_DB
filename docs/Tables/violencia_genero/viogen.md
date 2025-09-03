# violencia_genero.viogen

**Data loading script:** `pipelines/extract_transform/violencia_genero/008_et_viogen.py`

## Columns

- `viogen_id serial PRIMARY KEY`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `nivel_riesgo enums.nivel_riesgo_viogen_enum NOT NULL`
- `casos int NOT NULL CHECK (casos >= 0)`
- `casos_proteccion_policial int NOT NULL CHECK (casos_proteccion_policial >= 0)`
