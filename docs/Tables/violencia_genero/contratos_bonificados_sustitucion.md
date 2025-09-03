# violencia_genero.contratos_bonificados_sustitucion

**Data loading script:** `pipelines/extract_transform/violencia_genero/013_et_contratos_bonificados_sustitucion.py`

## Columns

- `contratos_bonificados_sustitucion_id serial PRIMARY KEY NOT NULL`
- `contratos_bonificados int NOT NULL CHECK (contratos_bonificados >= 0)`
- `contratos_sustitucion int NOT NULL CHECK (contratos_sustitucion >= 0)`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)`
- `provincia_id int REFERENCES geo.provincias (provincia_id)`
- `colectivo enums.colectivo_contratos_bonificados_sustitucion_enum NOT NULL`
- `tipo_contrato enums.tipo_contrato_enum NOT NULL`
