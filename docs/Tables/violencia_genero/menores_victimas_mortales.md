# violencia_genero.menores_victimas_mortales

**Data loading script:** `pipelines/extract_transform/violencia_genero/003_et_menores_victimas_mortales.py`

## Columns

- `menores_victimas_mortales_id serial PRIMARY KEY`
- `es_hijo_agresor boolean NOT NULL`
- `es_victima_vicaria boolean NOT NULL`
- `menores_victimas_mortales int NOT NULL CHECK (menores_victimas_mortales >= 0)`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
