# demografia.uso_tiempo

Average time per day, in hours and minutes, spent on main activity groups, disaggregated by sex and autonomous community. Data from the 2009-2010 Time Use Survey and the 2002-2003 Time Use Survey, both conducted by the INE.

- **Time period**: 2002-2003 and 2009-2010
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| uso_tiempo_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sex |
| actividad | varchar | NO | activity |
| horas | int | NO | hours |
| minutos | int | NO | minutes |

## Table definition

```sql
CREATE TABLE
  demografia.uso_tiempo (
    uso_tiempo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    actividad varchar NOT NULL CHECK (
      actividad IN (
        '0 Cuidados personales',
        '1 Trabajo remunerado',
        '2 Estudios',
        '3 Hogar y familia',
        '4 Trabajo voluntario y reuniones',
        '5 Vida social y diversión',
        '6 Deportes y actividades al aire libre',
        '7 Aficiones e informática',
        '8 Medios de comunicación',
        '9 Trayectos y empleo del tiempo no especificado'
      )
    ),
    horas int NOT NULL CHECK (
      horas >= 0
      AND horas <= 24
    ),
    minutos int NOT NULL CHECK (
      minutos >= 0
      AND minutos < 60
    )
  );
```

## Notable transformations

- Pivoted the 2009 source so hours and minutes became separate columns.
- Converted 2002 Excel sheets to the same structure as the 2009 data.
- Dropped rows with aggregated data for national totals and `sexo`.
- Standardized community identifiers and sex labels.

## Source

Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t25/e447/a2009-2010/p07/l0/&file=7.3a.px&L=0" target="_blank">Instituto Nacional de Estadística (INE) - 2009 survey</a> and <a href="https://www.ine.es/daco/daco42/empleo/dacoeet.htm" target="_blank">Instituto Nacional de Estadística (INE) - 2002 survey</a>
Consulted on 2 June 2025.
