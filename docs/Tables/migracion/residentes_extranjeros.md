# migracion.residentes_extranjeros

**Data loading script:** `pipelines/extract_transform/migracion/001_et_residentes_extranjeros.py`

## Columns

- `residentes_extranjeros_id serial PRIMARY KEY`
- `provincia_id int REFERENCES geo.provincias (provincia_id)`
- `nacionalidad int REFERENCES geo.paises (pais_id)`
- `sexo enums.sexo_enum`
- `es_nacido_espania boolean`
- `grupo_edad varchar CHECK ( grupo_edad ~ '^\d+-\d+$' OR grupo_edad ~ '^<\d+$' OR grupo_edad ~ '^>\d+$' )`
- `fecha date NOT NULL CHECK ( fecha >= DATE '1900-01-01' AND fecha <= CURRENT_DATE )`
- `residentes_extranjeros int NOT NULL CHECK (residentes_extranjeros >= 0)`
- `tipo_documentacion enums.tipo_documentacino_enum`
- `regimen enums.tipo_regimen_enum`
