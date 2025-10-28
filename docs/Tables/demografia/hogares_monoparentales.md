# demografia.hogares_monoparentales

Number of thousands of single-parent households in Spain, disaggregated by autonomous community, sex, age group and marital status of the household head.

- **Time period**: 2014-2020, annually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| hogares_monoparentales_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sex |
| grupo_edad | varchar | YES | age group |
| estado_civil | varchar | YES | marital status |
| hogares_monoparentales | float | NO | number of thousands of single-parent households |

## Table definition

```sql
CREATE TABLE
  demografia.hogares_monoparentales (
    hogares_monoparentales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    estado_civil varchar CHECK (
      estado_civil IN (
        'Soltero/a',
        'Casado/a',
        'Viudo/a',
        'Separado/a',
        'Divorciado/a'
      )
      OR estado_civil IS NULL
    ),
    hogares_monoparentales float NOT NULL CHECK (hogares_monoparentales >= 0)
  );
```

## Notable transformations

- Filled missing `hogares_monoparentales` values with 0.
- Dropped columns with aggregated data for `comunidad_autonoma_id`, `sexo`, `grupo_edad` and `estado_civil`.

## Source

Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t20/p274/serie/def/p02/&file=02015.px" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 2 June 2025.
