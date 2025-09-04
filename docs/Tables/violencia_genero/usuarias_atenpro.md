# violencia_genero.usuarias_atenpro

Number of active users, registered and deregistered users of the telephone service for attention and protection for victims of violence against women, Atenpro.

- **Time period**: 2005-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| usuarias_atenpro_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |
| altas | int | NO | number of registered users |
| bajas | int | NO | number of deregistered users |
| usuarias_activas | int | NO | total number of active users |

## Table definition

```sql
CREATE TABLE
  violencia_genero.usuarias_atenpro (
    usuarias_atenpro_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    altas int NOT NULL CHECK (altas >= 0),
    bajas int NOT NULL CHECK (bajas >= 0),
    usuarias_activas int NOT NULL CHECK (usuarias_activas >= 0)
  );
```

## Notable transformations
Entries with negative values for `altas` and `bajas` were dropped from the dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "050 Usuarias de ATENPRO".