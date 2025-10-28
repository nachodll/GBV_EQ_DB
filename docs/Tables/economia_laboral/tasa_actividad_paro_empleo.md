# economia_laboral.tasa_actividad_paro_empleo

Quarterly activity, employment, and unemployment rates in Spain, disaggregated by province and sex.

- **Time period**: 2002-2025, quarterly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_actividad_paro_empleo_id | serial | NO | primary key |
| anio | int | NO | year |
| trimestre | int | NO | quarter number (1-4) |
| provincia_id | int | NO | references geo.provincias |
| sexo | enums.sexo_enum | NO | sex (`Hombre`, `Mujer`, `Total`) |
| tasa | text | NO | rate category (`Tasa de actividad`, `Tasa de empleo`, `Tasa de paro`) |
| total | float | NO | percentage value of the selected rate |

## Table definition

```sql
CREATE TABLE
  economia_laboral.tasa_actividad_paro_empleo (
    tasa_actividad_paro_empleo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    tasa text NOT NULL CHECK (
      tasa IN (
        'Tasa de actividad',
        'Tasa de empleo',
        'Tasa de paro'
      )
    ),
    total float NOT NULL CHECK (
      total >= 0
      AND total <= 100
    )
  );
```

## Notable transformations

- Split the `Periodo` column into separate `anio` and `trimestre` fields.
- Removed rows with missing (`..`) rate values and converted percentages to numeric format.
- Standardised province identifiers, years, quarters, sex categories, and rate labels using shared normalisation utilities.

## Source

Data extracted from the <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=65349" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consulted on 16 June 2025.
