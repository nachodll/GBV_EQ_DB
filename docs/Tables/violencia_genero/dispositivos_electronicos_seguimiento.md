# violencia_genero.dispositivos_electronicos_seguimiento

**Data loading script:** `pipelines/extract_transform/violencia_genero/006_et_dispositivos_electronicos_seguimiento.py`

## Columns

- `dispositivos_electronicos_seguimiento_id serial PRIMARY KEY`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `instalaciones_acumuladas int NOT NULL CHECK (instalaciones_acumuladas >= 0)`
- `desinstalaciones_acumuladas int NOT NULL CHECK (desinstalaciones_acumuladas >= 0)`
- `dispositivos_activos int NOT NULL CHECK (dispositivos_activos >= 0)`
