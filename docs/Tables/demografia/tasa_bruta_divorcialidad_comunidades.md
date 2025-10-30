# demografia.tasa_bruta_divorcialidad_comunidades

Crude divorce rate in Spain, disaggregated by autonomous community and year.

- **Time period**: 2005-2023, annually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_bruta_divorcialidad_comunidades_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| tasa_bruta_divorcialidad | float | NO | crude divorce rate per 1000 inhabitants |

## Table definition

```sql
CREATE TABLE
  demografia.tasa_bruta_divorcialidad_comunidades (
    tasa_bruta_divorcialidad_comunidades_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tasa_bruta_divorcialidad float NOT NULL CHECK (
      tasa_bruta_divorcialidad >= 0
      AND tasa_bruta_divorcialidad <= 1000
    )
  );
```

## Notable transformations

- Removed rows where `tasa_bruta_divorcialidad` was reported as `..` and converted the column to numeric values.
- Normalized `comunidad_autonoma_id`, `anio`, and `tasa_bruta_divorcialidad` using shared validation helpers.

## Source

Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25204&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consulted on 18 June 2025.
