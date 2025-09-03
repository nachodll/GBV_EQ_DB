# geo.municipios

**Data loading script:** Not available

## Columns

- `municipio_id int PRIMARY KEY`
- `nombre varchar NOT NULL`
- `provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)`
