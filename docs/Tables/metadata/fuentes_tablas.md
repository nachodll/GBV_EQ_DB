# metadata.fuentes_tablas

Indicates which sources each table is based on, pointing to the specific resource URL and tracking the last update date.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| fuentes_tablas_id | serial | NO | primary key |
| fuente_id | int | NO | references metadata.fuentes |
| nombre | varchar | NO | name |
| fecha_actualizacion | date | NO | last update |
| descripcion | int | YES | description |
| url | varchar | NO | link to the specific reasource |


## Table definition

```sql
CREATE TABLE
  metadata.fuentes_tablas (
    fuentes_tablas_id serial PRIMARY KEY,
    fuente_id int NOT NULL REFERENCES metadata.fuentes (fuente_id),
    nombre varchar NOT NULL,
    fecha_actualizacion date NOT NULL CHECK (
      fecha_actualizacion >= DATE '1900-01-01'
      AND fecha_actualizacion <= CURRENT_DATE
    ),
    descripcion text,
    url varchar NOT NULL
  );
```