# violencia_genero.renta_activa_insercion

**Data loading script:** `pipelines/extract_transform/violencia_genero/012_et_renta_activa_insercion.py`

## Columns

- `renta_activa_insercion_id serial PRIMARY KEY`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `perceptoras int NOT NULL CHECK (perceptoras >= 0)`
