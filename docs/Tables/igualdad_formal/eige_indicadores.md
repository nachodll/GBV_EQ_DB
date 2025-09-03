# igualdad_formal.eige_indicadores

**Data loading script:** `pipelines/extract_transform/igualdad_formal/002_et_eige_indicadores.py`

## Columns

- `eige_indicador_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `pais_id int NOT NULL REFERENCES geo.paises (pais_id)`
- `indicador text NOT NULL`
- `valor int NOT NULL CHECK (valor >= 0)`
- `sexo enums.sexo_enum NOT NULL`
