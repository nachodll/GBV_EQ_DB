# violencia_genero.ayudas_articulo_27

**Data loading script:** `pipelines/extract_transform/violencia_genero/007_et_ayudas_articulo_27.py`

## Columns

- `ayudas_articulo_27_id serial PRIMARY KEY`
- `comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `ayudas_concedidas int NOT NULL CHECK (ayudas_concedidas >= 0)`
