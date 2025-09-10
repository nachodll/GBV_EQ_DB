# demografia.divorcios_segun_duracion_matrimonio

Percentage distribution of divorces in Spain by marriage duration, disaggregated by province and year. The results for the 2005-2010 period only take into account divorces of marriages between people of different sexes. It is also worth noticing that the 2005-2010 period uses different duration of marriage categories.

- **Time period**: 2005-2023, annually (only heterosexual marriages for the 2005-2010 period)
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| divorcios_segun_duracion_matrimonio_id | serial | NO | primary key |
| anio | int | NO | year |
| provincia_id | int | YES | references geo.provincias |
| duracion_matrimonio | varchar | NO | duration of marriage, ranges varies for different periods |
| porcentaje_divorcios | float | YES | percentage of divorces |

## Table definition

```sql
CREATE TABLE
  demografia.divorcios_segun_duracion_matrimonio (
    divorcios_segun_duracion_matrimonio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    duracion_matrimonio varchar NOT NULL CHECK (
      duracion_matrimonio IN (
        'Menos de 1 año',
        'De 1 año',
        'De 1 a 2 años',
        'De 2 a 4 años',
        'De 3 a 5 años',
        'De 5 a 9 años',
        'De 6 a 10 años',
        'De 10 a 14 años',
        'De 11 a 15 años',
        'De 15 a 19 años',
        'De 16 a 19 años',
        'De 20 a 29 años',
        '20 y más años',
        '30 y más años'
      )
    ),
    porcentaje_divorcios float CHECK (
      porcentaje_divorcios >= 0
      AND porcentaje_divorcios <= 100
    )
  );
```

## Notable transformations

- Merged datasets covering 2005-2010 and 2010-2023.
- Dropped rows with missing `porcentaje_divorcios`.
- Dropped rows with aggregated data for `provincia_id`.

## Source

Data for 2005-2010 extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25214&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Data for 2010-2023 extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25213&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>
