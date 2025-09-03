# tecnologia_y_medios.acceso_internet_viviendas

**Data loading script:** `pipelines/extract_transform/tecnologia_y_medios/001_et_acceso_internet_viviendas.py`

## Columns

- `acceso_internet_viviendas_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
- `tipo_equipamiento text NOT NULL CHECK ( tipo_equipamiento IN ( 'Viviendas con algún tipo de ordenador', 'Viviendas que disponen de acceso a Internet', 'Viviendas con conexión de Banda Ancha  (ADSL, Red de cable, etc.)', 'Viviendas con teléfono fijo', 'Viviendas con teléfono móvil' ) )`
- `porcentaje numeric NOT NULL CHECK ( porcentaje >= 0 AND porcentaje <= 100 )`
