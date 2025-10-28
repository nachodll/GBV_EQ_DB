# educacion_juventud.prestaciones_nacimiento_y_cuidado_menor

Benefits granted under the unified birth and childcare leave scheme, disaggregated by parent and province.

- **Time period**: 2019-2023, annual
- **Regional breakdown**: provincias

The 2019 data only cover the period after the new law entered into force on 1 April 2019. The reform merged previous maternity and paternity leave schemes into a single benefit. The "first parent" refers to the first caregiver to take the leave (most often the mother). For information on the former separate schemes, consult the table `educacion_juventud.prestaciones_maternidad_paternidad`. The column `opcion_a_favor_segundo_progenitor` was a temporary measure available during part of 2019 and must be subtracted from `prestaciones_primer_progenitor` in that year to obtain the net benefits effectively used by the first parent.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| prestaciones_nacimiento_y_cuidado_menor_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | NO | references geo.provincias |
| prestaciones_primer_progenitor | int | NO | number of benefits accessed by the first parent |
| opcion_a_favor_segundo_progenitor | int | YES | transfers ceded to the second parent (only applicable in 2019) |
| prestaciones_segundo_progenitor | int | NO | number of benefits accessed by the second parent |
| importe_miles_euros | float | NO | amount paid in thousands of euros |

## Table definition

```sql
CREATE TABLE
  educacion_juventud.prestaciones_nacimiento_y_cuidado_menor (
    prestaciones_nacimiento_y_cuidado_menor_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    prestaciones_primer_progenitor int NOT NULL CHECK (prestaciones_primer_progenitor >= 0),
    opcion_a_favor_segundo_progenitor int CHECK (opcion_a_favor_segundo_progenitor >= 0),
    prestaciones_segundo_progenitor int NOT NULL CHECK (prestaciones_segundo_progenitor >= 0),
    importe_miles_euros float NOT NULL CHECK (importe_miles_euros >= 0)
  );
```

## Notable transformations

- Parsed evolving spreadsheet layouts (including the 2019 transition year) to isolate first-parent, transfer option, and second-parent totals.
- Removed aggregate rows (national and regional totals) and harmonised province names prior to applying shared normalisation utilities.
- Cast monetary amounts to numeric values rounded to two decimals and enforced non-negative integer checks for benefit counts.

## Source

Statistics Yearbooks of the Ministry of Labor and Social Economy (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
Consulted on 2 June 2025.
