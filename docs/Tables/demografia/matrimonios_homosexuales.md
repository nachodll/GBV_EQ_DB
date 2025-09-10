# demografia.matrimonios_homosexuales

Number of same-sex marriages in Spain, broken down by province, age group of the spouses and sex composition (men or women).

- **Time period**: 2005-2023, annually
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| matrimonios_homosexuales_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| conyuge_1_grupo_edad | varchar | NO | age group of spouse 1 |
| conyuge_2_grupo_edad | varchar | NO | age group of spouse 2 |
| matrimonios_hombres | int | NO | marriages between men |
| matrimonios_mujeres | int | NO | marriages between women |
| es_residente_espania | boolean | NO | resident in Spain |

## Table definition

```sql
CREATE TABLE
  demografia.matrimonios_homosexuales (
    matrimonios_homosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    conyuge_1_grupo_edad varchar NOT NULL CHECK (
      conyuge_1_grupo_edad ~ '^\\d+-\\d+$'
      OR conyuge_1_grupo_edad ~ '^<\\d+$'
      OR conyuge_1_grupo_edad ~ '^>\\d+$'
    ),
    conyuge_2_grupo_edad varchar NOT NULL CHECK (
      conyuge_2_grupo_edad ~ '^\\d+-\\d+$'
      OR conyuge_2_grupo_edad ~ '^<\\d+$'
      OR conyuge_2_grupo_edad ~ '^>\\d+$'
    ),
    matrimonios_hombres int NOT NULL CHECK (matrimonios_hombres >= 0),
    matrimonios_mujeres int NOT NULL CHECK (matrimonios_mujeres >= 0),
    es_residente_espania boolean NOT NULL
  );
```

## Notable transformations

- Data from tables for marriages between men and between women were merged.
- `es_residente_espania` was derived from `provincia_id`.
- Missing values in `matrimonios_hombres` and `matrimonios_mujeres` were set to 0.
- Rows with aggregated data for columns `conyuge_1_grupo_edad`, `conyuge_2_grupo_edad` and `provincia_id` were dropped


## Source

Men marriage's data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=9113&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Women marriage's data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=9114&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>