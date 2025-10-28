# igualdad_formal.ganancia_por_hora_trabajo

Average hourly earnings (in euros) by sector of activity and sex across Spanish autonomous communities.

- **Time period**: 2004-2023, annually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ganancia_por_hora_trabajo_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sex |
| sector_actividad | text | NO | economic activity sector |
| ganancia_por_hora_trabajo | float | NO | average hourly earnings in euros |

## Table definition

```sql
CREATE TABLE
  igualdad_formal.ganancia_por_hora_trabajo (
    ganancia_por_hora_trabajo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    sector_actividad text NOT NULL CHECK (
      sector_actividad IN (
        'Todos los sectores',
        'Industria',
        'Construcción',
        'Servicios'
      )
    ),
    ganancia_por_hora_trabajo float NOT NULL CHECK (ganancia_por_hora_trabajo >= 0)
  );
```

## Notable transformations

- Combined two source files (2004-2007 and 2008-2023) into a single dataset.
- Filtered out records with missing hourly earnings.

## Source

Data extracted from the <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t22/p133/2004-2007/l0/&file=04001.px&L=0" target="_blank">Instituto Nacional de Estadística (INE) 2004-2007 series</a> and the <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28203&L=0" target="_blank">INE 2008-2023 series</a>.
Consulted on 3 June 2025.
