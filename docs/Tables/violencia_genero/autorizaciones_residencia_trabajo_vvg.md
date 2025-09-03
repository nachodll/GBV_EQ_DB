# violencia_genero.autorizaciones_residencia_trabajo_vvg

**Data loading script:** `pipelines/extract_transform/violencia_genero/009_et_autorizaciones_residencia_trabajo_vvg.py`

## Columns

- `autorizaciones_residencia_trabajo_vvg_id serial PRIMARY KEY`
- `provincia_id int REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `autorizaciones_concedidas int NOT NULL CHECK (autorizaciones_concedidas >= 0)`

