# tecnologia_y_medios.uso_internet_personas

**Data loading script:** `pipelines/extract_transform/tecnologia_y_medios/002_et_uso_internet_personas.py`

## Columns

- `uso_internet_personas_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `porcentaje numeric NOT NULL CHECK ( porcentaje >= 0 AND porcentaje <= 100 )`
- `comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
- `tipo_uso text NOT NULL CHECK ( tipo_uso IN ( 'Personas que han utilizado Internet en los últimos 3 meses', 'Personas que han utilizado Internet diariamente (al menos 5 días a la semana)', 'Personas que han comprado a través de Internet en los últimos 3 meses', 'Personas que usan el teléfono móvil' ) )`
