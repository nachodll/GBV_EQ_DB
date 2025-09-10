# demografia.matrimonios_heterosexuales

Number of heterosexual marriages in Spain, disaggregated by province, sex, age group of the spouses and previous marital status (from 2010).

- **Time period**: 1975-2023, annually. Detailed `estado_civil_anterior` available from 2010 onwards
- **Regional breakdown**: Provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| matrimonios_heterosexuales_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| sexo | enums.sexo_enum | NO | sex |
| edad | varchar | NO | age group |
| estado_civil_anterior | varchar | YES | previous marital status |
| matrimonios | int | NO | number of marriages |
| es_residente_espania | boolean | NO | resident in Spain |

## Table definition

```sql
CREATE TABLE
  demografia.matrimonios_heterosexuales (
    matrimonios_heterosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    edad varchar NOT NULL CHECK (
      edad ~ '^\\d+$'
      OR edad ~ '^<\\d+$'
      OR edad ~ '^>\\d+$'
    ),
    estado_civil_anterior varchar CHECK (
      estado_civil_anterior IN (
        'Total',
        'Solteros/Solteras',
        'Viudos/Viudas',
        'Divorciados/Divorciadas'
      )
      OR estado_civil_anterior IS NULL
    ),
    matrimonios int NOT NULL CHECK (matrimonios >= 0),
    es_residente_espania boolean NOT NULL
  );
```

## Notable transformations

- Previous marital status breakdown war merged into the dataset.
- Rows with aggregated data for `provincia_id` were dropped.
- Rows with missing values for `matrimonios` were dropped.
- Column `es_residente_espania` was mapped to boolean.

## Source
Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=6532&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Previous marital status data extracted from <a href="https://ine.es/jaxiT3/Tabla.htm?t=32879" target="_blank">Instituto Nacional de Estadística (INE)</a>