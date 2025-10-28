# demografia.poblacion_grupo_edad

Total population of Spain, disaggrated by sex and age group.

- **Time period**: 1998-2022, anually
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| poblacion_grupo_edad_id | serial | NO | primary key |
| nacionalidad | int | YES | references geo.paises |
| sexo | enums.sexo_enum | NO | sex |
| grupo_edad | varchar | NO | age group |
| anio | int | NO | year |
| poblacion | int | NO | population |

## Table definition

```sql
CREATE TABLE
  demografia.poblacion_grupo_edad (
    poblacion_grupo_edad_id serial PRIMARY KEY,
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );
```

## Notable transformations

- Entries with aggregated data for `grupo_edad` were dropped.
- Entries with aggregated data for `nacionalidad` were dropped.
- Entries with aggregated data for `sex` were dropped.

## Source
Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=01002.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 3 June 2025.
