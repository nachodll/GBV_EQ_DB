# igualdad_formal.ganancia_por_hora_trabajo

Ganancia media por hora (en euros) según sector de actividad y sexo en las comunidades autónomas españolas.

- **Periodo temporal**: 2004-2023, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ganancia_por_hora_trabajo_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sexo |
| sector_actividad | text | NO | sector de actividad económica |
| ganancia_por_hora_trabajo | float | NO | ganancia media por hora en euros |

## Definición de la tabla

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

## Transformaciones notables

- Se combinaron los dos ficheros fuente (2004-2007 y 2008-2023) en un único conjunto de datos.
- Se eliminaron los registros sin información de ganancia.

## Fuente

Datos extraídos de la <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t22/p133/2004-2007/l0/&file=04001.px&L=0" target="_blank">serie 2004-2007 del Instituto Nacional de Estadística (INE)</a> y de la <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28203&L=0" target="_blank">serie 2008-2023 del INE</a>.
