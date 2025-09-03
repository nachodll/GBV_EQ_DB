# geo.provincias

**Data loading script:** Not available

## Columns

- `provincia_id int PRIMARY KEY`
- `nombre varchar UNIQUE NOT NULL`
- `comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)`
