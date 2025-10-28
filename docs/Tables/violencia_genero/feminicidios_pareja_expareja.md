# violencia_genero.feminicidios_pareja_expareja

Aggregate number of monthly feminicides per province committed by the victim's partner or ex-partner. Aggregate number of monthly orphans left by feminicides committed by the victim's partner or ex-partner per province. Data for number of orphans is only available from 2013, its value is set as NULL for entries with no data.

- **Time period**: 2003-2025, monthly (huerfanos_menores from 2013 on)
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| feminicidios_pareja_expareja_id | serial | NO | primary key |
| feminicidios | int | NO | number of feminicides |
| huerfanos_menores | int | YES | number of orphan left by feminicides |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month|
| victima_grupo_edad | varchar | YES | victim's group of age |
| agresor_grupo_edad | varchar | YES | aggresor's group of age |

## Table definition

```sql
CREATE TABLE
  violencia_genero.feminicidios_pareja_expareja (
    feminicidios_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    huerfanos_menores int CHECK (huerfanos_menores >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    victima_grupo_edad varchar CHECK (
      victima_grupo_edad ~ '^\d+-\d+$'
      OR victima_grupo_edad ~ '^<\d+$'
      OR victima_grupo_edad ~ '^>\d+$'
    ),
    agresor_grupo_edad varchar CHECK (
      agresor_grupo_edad ~ '^\d+-\d+$'
      OR agresor_grupo_edad ~ '^<\d+$'
      OR agresor_grupo_edad ~ '^>\d+$'
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset. Source data provider only allows 5 analysis variable to be selected at time. More analysis variables are available at the original source. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "010 Feminicidios en la pareja o expareja".
Consulted on 9 June 2025.
