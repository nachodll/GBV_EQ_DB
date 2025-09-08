# metadata.fuentes_tablas

Indica en qué fuentes se basa cada tabla, señalando la URL del recurso específico y registrando la fecha de la última actualización.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| fuentes_tablas_id | serial | NO | primary key |
| fuente_id | int | NO | referencia a metadata.fuentes |
| nombre | varchar | NO | nombre |
| fecha_actualizacion | date | NO | última actualización |
| descripcion | int | YES | descripción |
| url | varchar | NO | enlace al recurso específico |

## Definición de la tabla

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
