# demografia.poblacion_grupo_edad

**Data loading script:** `pipelines/extract_transform/demografia/002_et_poblacion_grupo_edad.py`

## Columns

- `poblacion_grupo_edad_id serial PRIMARY KEY`
- `nacionalidad int REFERENCES geo.paises (pais_id)`
- `sexo enums.sexo_enum NOT NULL`
- `grupo_edad varchar NOT NULL CHECK ( grupo_edad ~ '^\d+-\d+$' OR grupo_edad ~ '^<\d+$' OR grupo_edad ~ '^>\d+$' )`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `poblacion int NOT NULL CHECK (poblacion >= 0)`
