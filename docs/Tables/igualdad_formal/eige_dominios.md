# igualdad_formal.eige_dominios

**Data loading script:** `pipelines/extract_transform/igualdad_formal/001_et_eige_dominios.py`

## Columns

- `eige_dominio_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `pais_id int NOT NULL REFERENCES geo.paises (pais_id)`
- `dominio_subdominio enums.eige_dominio_subdominio_enum NOT NULL`
- `valor numeric NOT NULL CHECK (valor >= 0)`
