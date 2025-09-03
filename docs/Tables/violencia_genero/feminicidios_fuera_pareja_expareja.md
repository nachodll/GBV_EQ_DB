# violencia_genero.feminicidios_fuera_pareja_expareja

**Data loading script:** `pipelines/extract_transform/violencia_genero/002_et_feminicidios_fuera_pareja_expareja.py`

## Columns

- `feminicidios_fuera_pareja_expareja_id serial PRIMARY KEY`
- `feminicidios int NOT NULL CHECK (feminicidios >= 0)`
- `tipo_feminicidio enums.tipo_feminicidio_enum NOT NULL`
- `comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
