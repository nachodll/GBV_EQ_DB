# violencia_genero.denuncias_vg_pareja

**Data loading script:** `pipelines/extract_transform/violencia_genero/010_et_denuncias_vg_pareja.py`

## Columns

- `denuncias_vg_pareja_id serial PRIMARY KEY`
- `origen_denuncia enums.origen_denuncia_enum NOT NULL`
- `anio int NOT NULL CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) )`
- `trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4)`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `denuncias int NOT NULL CHECK (denuncias >= 0)`
