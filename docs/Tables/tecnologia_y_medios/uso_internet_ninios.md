# tecnologia_y_medios.uso_internet_ninios

Percentages of kids (between 10 and 15 years old) according to type of internet use.

- **Time period**: 2006-2024, anually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| uso_internet_ninios_id | serial | NO | primary key |
| anio | int | NO | year |
| porcentaje | numeric | NO | percentage |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| tipo_uso | text | NO | type of internet use |

## Table definition

```sql
CREATE TABLE
  tecnologia_y_medios.uso_internet_ninios (
    uso_internet_ninios_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_uso text NOT NULL CHECK (
      tipo_uso IN (
        'Niños usuarios de Internet en los últimos 3 meses',
        'Niños que disponen de teléfono móvil',
        'Niños usuarios de ordenador en los últimos 3 meses'
      )
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset. 

## Source
Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?tpx=70472&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>. 
Consulted on 3 June 2025.
