# demografia.poblacion_grupo_edad

Población total de España, desagregada por sexo y grupo de edad.

- **Periodo temporal**: 1998-2022, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| poblacion_grupo_edad_id | serial | NO | primary key |
| nacionalidad | int | YES | referencia a geo.paises |
| sexo | enums.sexo_enum | NO | sexo |
| grupo_edad | varchar | NO | grupo de edad |
| anio | int | NO | año |
| poblacion | int | NO | población |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.poblacion_grupo_edad (
    poblacion_grupo_edad_id serial PRIMARY KEY,
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );
```

## Transformaciones notables

- Se eliminaron las entradas con datos agregados para `grupo_edad`.
- Se eliminaron las entradas con datos agregados para `nacionalidad`.
- Se eliminaron las entradas con datos agregados para `sexo`.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=01002.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consultado el 3 de junio de 2025.
