# economia_laboral.tasa_paro_comunidades

Quarterly unemployment rate in Spain, disaggregated by autonomous community and sex.

- **Time period**: 2002-2025, quarterly
- **Regional breakdown**: comunidades

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasa_paro_comunidades_id | serial | NO | primary key |
| anio | int | NO | year |
| trimestre | int | NO | quarter number (1-4) |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sex (`Hombre`, `Mujer`, `Total`) |
| tasa_paro | float | NO | unemployment rate (%) |

## Table definition

```sql
CREATE TABLE
  economia_laboral.tasa_paro_comunidades (
    tasa_paro_comunidades_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    tasa_paro float NOT NULL CHECK (
      tasa_paro >= 0
      AND tasa_paro <= 100
    )
  );
```

## Notable transformations

- Split the `Periodo` field into separate `anio` and `trimestre` columns.
- Filtered the dataset to keep the `Edad = 'Total'` aggregate and dropped the original `Edad` column.
- Removed rows with missing (`..`) unemployment rates and converted the percentages to numeric values.
## Source

Data extracted from the <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=65334" target="_blank">Instituto Nacional de Estadística (INE)</a>.

Consulted on 16 June 2025.

