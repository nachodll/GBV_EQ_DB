# educacion_juventud.nivel_formacion

Population shares by educational attainment level according to the International Standard Classification of Education (ISCED), compiled by INE from the Labour Force Survey.

- **Time period**: 2004-2023, annual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| nivel_formacion_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| grupo_edad | varchar | NO | age group ("25-64" or ">65") |
| nivel_formacion | text | NO | attainment bracket following ISCED |
| porcentaje | numeric | NO | share of population in the bracket |

### ISCED mapping
- **Nivel 0-2**: ISCED 0-2 (early childhood, primary and lower secondary education).
- **Nivel 3-4**: ISCED 3-4 (upper secondary and post-secondary non-tertiary education).
- **Nivel 5-8**: ISCED 5-8 (tertiary programmes from short-cycle to doctoral levels).
- **Nivel 3-8**: aggregate of ISCED 3-8, i.e. population with upper secondary or higher attainment.

## Table definition

```sql
CREATE TABLE
  educacion_juventud.nivel_formacion (
    nivel_formacion_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    nivel_formacion text NOT NULL CHECK (
      nivel_formacion IN (
        'Nivel 0-2',
        'Nivel 3-8',
        'Nivel 3-4',
        'Nivel 5-8'
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t00/ICV/dim4/l0/&file=41201.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consulted on 23 October 2025.
