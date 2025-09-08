# violencia_genero.ordenes_proteccion

Número de órdenes de protección emitidas en casos de violencia de género.

- **Periodo temporal**: 2009-2025, trimestral
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ordenes_proteccion_id | serial | NO | primary key |
| estado_proceso | enums.estado_orden_proteccion_enum | NO | estado del proceso judicial |
| instancia | enums.instancia_orden_proteccion_enum | NO | quién solicitó la orden de protección |
| anio | int | NO | año |
| trimestre | int | NO | trimestre |
| provincia_id | int | NO | referencia a geo.provincias |
| ordenes_proteccion | int | NO | número de órdenes de protección |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.ordenes_proteccion (
    ordenes_proteccion_id serial PRIMARY KEY,
    estado_proceso enums.estado_orden_proteccion_enum NOT NULL,
    instancia enums.instancia_orden_proteccion_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    ordenes_proteccion int NOT NULL CHECK (ordenes_proteccion >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "120 Órdenes de protección".
