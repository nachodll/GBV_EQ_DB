# demografia.tasa_bruta_divorcialidad_provincias

Crude divorce rate in Spain, disaggregated by province and year.

- **Time period**: 2005-2023, annually
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_bruta_divorcialidad_provincias_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| tasa_bruta_divorcialidad | float | NO | crude divorce rate per 1000 inhabitants |

## Table definition

```sql
CREATE TABLE
  demografia.tasa_bruta_divorcialidad_provincias (
    tasa_bruta_divorcialidad_provincias_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tasa_bruta_divorcialidad float NOT NULL CHECK (
      tasa_bruta_divorcialidad >= 0
      AND tasa_bruta_divorcialidad <= 1000
    )
  );
```

## Notable transformations

- Removed rows where `tasa_bruta_divorcialidad` was reported as `..` and converted the column to numeric values.
- Normalized `provincia_id`, `anio`, and `tasa_bruta_divorcialidad` using shared validation helpers.

## Source

Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25212&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consulted on 18 June 2025.
