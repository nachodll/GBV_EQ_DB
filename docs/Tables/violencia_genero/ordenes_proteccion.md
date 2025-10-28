# violencia_genero.ordenes_proteccion

Number of protection orders issued for cases of gender violence.

- **Time period**: 2009-2025, quarterly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ordenes_proteccion_id | serial | NO | primary key |
| estado_proceso | enums.estado_orden_proteccion_enum | NO | status of the judicial process |
| instancia | enums.instancia_orden_proteccion_enum | NO | who requested the protection order |
| anio | int | NO | year |
| trimestre | int | NO | quarter |
| provincia_id | int | NO | references geo.provincias |
| ordenes_proteccion | int | NO | number of protection orders |

## Table definition

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

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "120 Órdenes de protección".
Consulted on 10 June 2025.
