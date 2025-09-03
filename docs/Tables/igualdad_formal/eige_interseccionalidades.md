# igualdad_formal.eige_interseccionalidades

**Data loading script:** `pipelines/extract_transform/igualdad_formal/003_et_eige_interseccionalidades.py`

## Columns

- `eige_interseccionalidad_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `pais_id int NOT NULL REFERENCES geo.paises (pais_id)`
- `indicador text NOT NULL`
- `valor int CHECK (valor >= 0)`
- `sexo enums.sexo_enum NOT NULL`
- `interseccionalidad enums.eige_interseccionalidades_enum NOT NULL`
