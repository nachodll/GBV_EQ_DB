# violencia_genero.servicio_016

**Data loading script:** `pipelines/extract_transform/violencia_genero/004_et_servicio_016.py`

## Columns

- `servicio_016_id serial PRIMARY KEY`
- `provincia_id int REFERENCES geo.provincias (provincia_id)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `persona_consulta enums.persona_consulta_enum`
- `tipo_violencia enums.tipo_violencia_enum`
- `llamadas int NOT NULL CHECK (llamadas >= 0)`
- `whatsapps int NOT NULL CHECK (whatsapps >= 0)`
- `emails int NOT NULL CHECK (emails >= 0)`
- `chats int NOT NULL CHECK (chats >= 0)`
