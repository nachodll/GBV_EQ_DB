# demografia.tasa_divorcialidad

Divorce rate in Spain, disaggregated by province, sex, age group and year. The results for the 2005-2010 period only take into account divorces of marriages between people of different sexes. Age groups categories are slightly different for periods 2005-2010 and 2010-2023.

- **Time period**: 2005-2023, annually (only heterosexual marriages for the 2005-2010 period)
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_divorcialidad_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| sexo | enums.sexo_enum | NO | sex |
| grupo_edad | varchar | YES | age group, categories varies slightly accross periods |
| tasa_divorcialidad | float | NO | divorce rate per 1000 people |

## Table definition

```sql
CREATE TABLE
  demografia.tasa_divorcialidad (
    tasa_divorcialidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    tasa_divorcialidad float NOT NULL CHECK (
      tasa_divorcialidad >= 0
      AND tasa_divorcialidad <= 1000
    )
  );
```

## Notable transformations

- Merged datasets covering 2005-2010 and 2010-2023. First period does not include same sex marriages.
- Excluded entries with missing `tasa_divorcialidad`.
- Dropped rows with aggregated data for `sexo` and `provincia_id`

## Source

Data for 2005-2010 extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25216&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Data for 2010-2023 extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25217&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>
