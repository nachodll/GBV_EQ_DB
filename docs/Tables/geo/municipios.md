# geo.municipios

All municipios in Spain. Primary keys are not auto generated, its unique code is obtained concatenating the municipio code provided by INE with the province code also given by INE (CPRO+CMUN).

**Note**: this table also contain historic municipalities that do not exist anymore.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| municipio_id | int | NO | primary key |
| nombre | varchar | NO | name |
| provincia_id | int | NO | references geo.provincias |

## Table definition

```sql
CREATE TABLE
  geo.municipios (
    municipio_id int PRIMARY KEY,
    nombre varchar NOT NULL,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)
  );
```

## Source
Data extracted from <a href="https://www.ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 2 June 2025.
