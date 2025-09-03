# violencia_genero.ayudas_cambio_residencia

**Data loading script:** `pipelines/extract_transform/violencia_genero/014_et_ayudas_cambio_residencia.py`

## Columns

- `ayudas_cambio_residencia_id serial PRIMARY KEY`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `ayudas_cambio_residencia int NOT NULL CHECK (ayudas_cambio_residencia >= 0)`
