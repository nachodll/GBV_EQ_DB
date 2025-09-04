# demografia.poblacion_municipios

Total population per spanish municipio, disaggregated by sex.

- **Time period**: 1996-2024, anually
- **Regional breakdown**: municipios

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| poblacion_municipios_id | serial | NO | primary key |
| municipio_id | int | NO | references geo.municipios |
| anio | int | NO | year |
| sexo | enums.sexo_enum | NO | sex |
| poblacion | int | NO | population |

## Table definition

```sql
CREATE TABLE
  demografia.poblacion_municipios (
    poblacion_municipios_id serial PRIMARY KEY,
    municipio_id int NOT NULL REFERENCES geo.municipios (municipio_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );
```

## Notable transformations

- All dataset from all municipios were merged.
- Entries with aggregated data for province totals were dropped.
- Entries with missing values for `poblacion` were dropped.
- Entries with total aggregated data for `sex` were dropped.

## Source
Data extracted from <a href="https://www.ine.es/dynt3/inebase/index.htm?padre=525#" target="_blank">Instituto Nacional de Estadística (INE)</a>