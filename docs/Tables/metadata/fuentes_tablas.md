# metadata.fuentes_tablas

**Data loading script:** Not available

## Columns

- `fuentes_tablas_id serial PRIMARY KEY`
- `fuente_id int NOT NULL REFERENCES metadata.fuentes (fuente_id)`
- `nombre varchar NOT NULL`
- `fecha_actualizacion date NOT NULL CHECK ( fecha_actualizacion >= DATE '1900-01-01' AND fecha_actualizacion <= CURRENT_DATE )`
- `descripcion text`
- `url varchar NOT NULL`
