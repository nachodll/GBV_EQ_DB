# igualdad_formal.eige_violencia

**Data loading script:** `pipelines/extract_transform/igualdad_formal/004_et_eige_violencia.py`

## Columns

- `eige_violencia_id serial PRIMARY KEY`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `pais_id int NOT NULL REFERENCES geo.paises (pais_id)`
- `indicador text NOT NULL`
- `valor int NOT NULL CHECK (valor >= 0)`
