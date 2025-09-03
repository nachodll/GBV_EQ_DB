# violencia_genero.usuarias_atenpro

**Data loading script:** `pipelines/extract_transform/violencia_genero/005_et_usuarias_atenpro.py`

## Columns

- `usuarias_atenpro_id serial PRIMARY KEY`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `altas int NOT NULL CHECK (altas >= 0)`
- `bajas int NOT NULL CHECK (bajas >= 0)`
- `usuarias_activas int NOT NULL CHECK (usuarias_activas >= 0)`
