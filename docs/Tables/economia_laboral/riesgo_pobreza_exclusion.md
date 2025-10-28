# economia_laboral.riesgo_pobreza_exclusion

Share of population at risk of poverty or social exclusion (AROPE) and its components, compiled by INE from the Living Conditions Survey.

- **Time period**: 2008-2024, annual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| riesgo_pobreza_exclusion_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| indicador | text | NO | indicator label within the AROPE framework |
| porcentaje | float | NO | percentage of population |

## Table definition

```sql
CREATE TABLE
  economia_laboral.riesgo_pobreza_exclusion (
    riesgo_pobreza_exclusion_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    indicador text NOT NULL CHECK (
      indicador IN (
        'Tasa de riesgo de pobreza o exclusión social (indicador AROPE)',
        'En riesgo de pobreza (renta año anterior a la entrevista)',
        'Con carencia material severa',
        'Viviendo en hogares con baja intensidad en el trabajo (de 0 a 59 años)'
      )
    ),
    porcentaje float NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=10011" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consulted on 23 October 2025.
