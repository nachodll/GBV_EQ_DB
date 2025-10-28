# demografia.tasa_bruta_natalidad

Crude birth rate in Spain, disaggregated by province and year.

- **Time period**: 1975-2023, annually
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_bruta_natalidad_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| tasa_bruta_natalidad | float | NO | crude birth rate per 1000 inhabitants |

## Table definition

```sql
CREATE TABLE
  demografia.tasa_bruta_natalidad (
    tasa_bruta_natalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tasa_bruta_natalidad float NOT NULL CHECK (tasa_bruta_natalidad >= 0)
  );
```

## Notable transformations

- Dropped entries with aggregated data for `provincia_id`.

## Source

Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=1470&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consulted on 3 June 2025.
