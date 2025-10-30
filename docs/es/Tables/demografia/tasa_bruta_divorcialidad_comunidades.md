# demografia.tasa_bruta_divorcialidad_comunidades

Tasa bruta de divorcialidad en España, desagregada por comunidad autónoma y año.

- **Periodo temporal**: 2005-2023, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_bruta_divorcialidad_comunidades_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| tasa_bruta_divorcialidad | float | NO | tasa bruta de divorcialidad por cada 1000 habitantes |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.tasa_bruta_divorcialidad_comunidades (
    tasa_bruta_divorcialidad_comunidades_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tasa_bruta_divorcialidad float NOT NULL CHECK (
      tasa_bruta_divorcialidad >= 0
      AND tasa_bruta_divorcialidad <= 1000
    )
  );
```

## Transformaciones notables

- Se eliminaron las filas donde `tasa_bruta_divorcialidad` aparecía como `..` y se convirtió la columna a valores numéricos.
- Se normalizaron `comunidad_autonoma_id`, `anio` y `tasa_bruta_divorcialidad` con las funciones de validación compartidas.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25204&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consultado el 18 de junio de 2025.
