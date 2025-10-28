# demografia.nulidades_separaciones_divorcios

Number of marital dissolutions in Spain broken down by province, type of dissolution and year. The types of dissolution considered are nullities, separations and divorces.

- **Time period**: 1998-2023, annually
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| nulidades_separaciones_divorcios_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| tipo_disolucion | varchar | NO | marital dissolution type |
| disoluciones_matrimoniales | int | NO | number of marital dissolutions |

## Table definition

```sql
CREATE TABLE
  demografia.nulidades_separaciones_divorcios (
    nulidades_separaciones_divorcios_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tipo_disolucion varchar NOT NULL CHECK (
      tipo_disolucion IN ('Nulidades', 'Separaciones', 'Divorcios')
    ),
    disoluciones_matrimoniales int NOT NULL CHECK (disoluciones_matrimoniales >= 0)
  );
```

## Notable transformations

- Removed rows with aggregated totals for `provincia_id` and `tipo_disolucion`.
- Discarded entries with missing `disoluciones_matrimoniales`.

## Source

Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=20173" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 9 June 2025.
