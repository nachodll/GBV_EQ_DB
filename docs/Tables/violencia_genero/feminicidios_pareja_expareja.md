# violencia_genero.feminicidios_pareja_expareja

**Data loading script:** `pipelines/extract_transform/violencia_genero/001_et_feminicidios_pareja_expareja.py`

## Columns

- `feminicidios_pareja_expareja_id serial PRIMARY KEY`
- `feminicidios int NOT NULL CHECK (feminicidios >= 0)`
- `huerfanos_menores int NOT NULL CHECK (huerfanos_menores >= 0)`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `victima_grupo_edad varchar CHECK ( victima_grupo_edad ~ '^\d+-\d+$' OR victima_grupo_edad ~ '^<\d+$' OR victima_grupo_edad ~ '^>\d+$' )`
- `agresor_grupo_edad varchar CHECK ( agresor_grupo_edad ~ '^\d+-\d+$' OR agresor_grupo_edad ~ '^<\d+$' OR agresor_grupo_edad ~ '^>\d+$' )`
