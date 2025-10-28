# salud.ive_grupo_edad

Rate per 1000 women of voluntary pregnancy terminations by age group.

- **Time period**: 2014-2023, annual
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ive_grupo_edad_id | serial | NO | primary key |
| anio | int | NO | year |
| grupo_edad | varchar | NO | age group |
| tasa | float | NO | rate per 1000 women |

## Table definition

```sql
CREATE TABLE
  salud.ive_grupo_edad (
    ive_grupo_edad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );
```

## Notable transformations
Replaced "19 y menos años" with "<19" in age group labels.

## Source
Data extracted from <a href="https://www.sanidad.gob.es/areas/promocionPrevencion/embarazo/datosEstadisticos.htm#Tabla1" target="_blank">Ministerio de Sanidad</a>. 
Consulted on 10 June 2025.
