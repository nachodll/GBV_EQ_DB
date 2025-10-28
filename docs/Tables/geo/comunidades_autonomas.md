# geo.comunidades_autonomas

All comunidades autonames in Spain. Primary keys are not auto generated, since they have unique code assigned by INE (CODAUTO). Special key 0 is used for national totals.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| comunidad_autonoma_id | int | NO | primary key |
| nombre | varchar | NO | unique |

## Table definition

```sql
CREATE TABLE
  geo.comunidades_autonomas (
    comunidad_autonoma_id int PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```

## Source
Data extracted from <a href="https://www.ine.es/daco/daco42/codmun/cod_ccaa.htm" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 2 June 2025.
