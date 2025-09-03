# tecnologia_y_medios.uso_internet_ninios

**Data loading script:** `pipelines/extract_transform/tecnologia_y_medios/003_et_uso_internet_ninios.py`

## Columns

- `uso_internet_ninios_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `porcentaje numeric NOT NULL CHECK ( porcentaje >= 0 AND porcentaje <= 100 )`
- `comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
- `tipo_uso text NOT NULL CHECK ( tipo_uso IN ( 'Niños usuarios de Internet en los últimos 3 meses', 'Niños que disponen de teléfono móvil', 'Niños usuarios de ordenador en los últimos 3 meses' ) )`
