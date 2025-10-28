# violencia_genero.menores_victimas_mortales

Monthly aggregate of minors fatalities per province by cause of a gender based violence crime. It is considered to be a vicarious victim only if the mother was not has not been killed in the same event.

- **Time period**: 2013-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| menores_victimas_mortales_id | serial | NO | primary key |
| es_hijo_agresor | boolean | NO | whether the victim was the biological or adopted child of the aggressor or not |
| es_victima_vicaria | boolean | NO | it is considered to be a vicarious victim only if the mother was not has not been killed in the same event |
| menores_victimas_mortales | int | NO | number of minors fatalities |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |

## Table definition

```sql
CREATE TABLE
  violencia_genero.menores_victimas_mortales (
    menores_victimas_mortales_id serial PRIMARY KEY,
    es_hijo_agresor boolean NOT NULL,
    es_victima_vicaria boolean NOT NULL,
    menores_victimas_mortales int NOT NULL CHECK (menores_victimas_mortales >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)
  );
```

## Notable transformations
Text fields "VM Vicaria -1-" and "AG-VM Relación" were mapped to boolean values `es_victima_vicaria` and `es_hijo_agresor`, respectively.

Source data provider only allows 5 analysis variable to be selected at time. More analysis variables are available at the original source. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "030 Menores víctimas mortales".
Consulted on 2 June 2025.
