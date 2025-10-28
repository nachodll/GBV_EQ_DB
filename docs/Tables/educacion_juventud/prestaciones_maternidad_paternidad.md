# educacion_juventud.prestaciones_maternidad_paternidad

Benefits granted under the former maternity and paternity leave schemes, disaggregated by type of benefit, recipient, and province.

- **Time period**: 2002-2019, annual
- **Regional breakdown**: provincias

Maternity benefits could be partially transferred to the other parent, whereas paternity benefits were non-transferable. As a result, rows with `tipo = 'Maternidad'` may contain values in both `percibidas_madre` and `percibidas_padre`, while rows with `tipo = 'Paternidad'` always have `percibidas_madre = NULL`. Paternity benefits were introduced by Organic Law 3/2007 (effective 24 March 2007), so no paternity records exist before 2007. Monetary amounts are only available from 2007 onwards.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| prestaciones_maternidad_paternidad_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | NO | references geo.provincias |
| tipo | text | NO | benefit type (`Maternidad`, `Paternidad`) |
| percibidas_madre | int | YES | number of benefits received by the mother |
| percibidas_padre | int | NO | number of benefits received by the father |
| importe_miles_euros | float | YES | amount paid in thousands of euros (available from 2007) |

## Table definition

```sql
CREATE TABLE
  educacion_juventud.prestaciones_maternidad_paternidad (
    prestaciones_maternidad_paternidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    tipo text NOT NULL CHECK (tipo IN ('Maternidad', 'Paternidad')),
    percibidas_madre int CHECK (percibidas_madre >= 0),
    percibidas_padre int NOT NULL CHECK (percibidas_padre >= 0),
    importe_miles_euros float CHECK (importe_miles_euros >= 0)
  );
```

## Notable transformations

- Parsed separate maternity and paternity spreadsheets for each year, unfolding multi-level headers into a tidy long format.
- Filtered out aggregate rows (national and regional totals) and harmonised province labels prior to normalisation.
- Coerced monetary amounts to numeric values with two decimals and normalised benefit counts to non-negative integers, preserving historical nulls where amounts or recipients were not reported.

## Source

Statistics Yearbooks of the Ministry of Labor and Social Economy (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
Consulted on 10 June 2025.
