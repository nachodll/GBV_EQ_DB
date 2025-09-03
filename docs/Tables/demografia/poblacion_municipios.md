# demografia.poblacion_municipios

**Data loading script:** `pipelines/extract_transform/demografia/001_et_poblacion_municipios.py`

## Columns

- `poblacion_municipios_id serial PRIMARY KEY`
- `municipio_id int NOT NULL REFERENCES geo.municipios (municipio_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `sexo enums.sexo_enum NOT NULL`
- `poblacion int NOT NULL CHECK (poblacion >= 0)`
