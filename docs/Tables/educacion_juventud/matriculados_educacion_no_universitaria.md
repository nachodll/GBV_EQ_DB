# educacion_juventud.matriculados_educacion_no_universitaria

**Data loading script:** `pipelines/extract_transform/educacion_juventud/001_et_matriculados_educacion_no_universitaria.py`

## Columns

- `matriculados_educacion_no_universitaria_id serial PRIMARY KEY`
- `titularidad enums.titularidad_centro_ensenanza_enum NOT NULL`
- `curso varchar NOT NULL CHECK ( curso ~ '^\d{4}-\d{2}$' AND ( substring(curso, 1, 4)::int BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) ) AND ( substring(curso, 6, 2)::int = (substring(curso, 3, 2)::int + 1) % 100 ) )`
- `sexo enums.sexo_enum`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
- `ensenianza varchar NOT NULL`
- `matriculados int NOT NULL CHECK (matriculados >= 0)`
