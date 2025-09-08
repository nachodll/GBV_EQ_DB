# demografia.poblacion_municipios

Población total por municipio español, desagregada por sexo.

- **Periodo temporal**: 1996-2024, anual
- **Desagregación regional**: municipios

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| poblacion_municipios_id | serial | NO | primary key |
| municipio_id | int | NO | referencia a geo.municipios |
| anio | int | NO | año |
| sexo | enums.sexo_enum | NO | sexo |
| poblacion | int | NO | población |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.poblacion_municipios (
    poblacion_municipios_id serial PRIMARY KEY,
    municipio_id int NOT NULL REFERENCES geo.municipios (municipio_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );
```

## Transformaciones notables

- Se combinaron los conjuntos de datos de todos los municipios.
- Se eliminaron las entradas con datos agregados para `provincia_id`.
- Se eliminaron las entradas con valores faltantes en `poblacion`.
- Se eliminaron las entradas con datos agregados totales para `sexo`.

## Fuente

Datos extraídos del <a href="https://www.ine.es/dynt3/inebase/index.htm?padre=525#" target="_blank">Instituto Nacional de Estadística (INE)</a>
