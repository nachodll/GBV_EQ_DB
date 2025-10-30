# demografia.tasa_bruta_divorcialidad_provincias

Tasa bruta de divorcialidad en España, desagregada por provincia y año.

- **Periodo temporal**: 2005-2023, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_bruta_divorcialidad_provincias_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| tasa_bruta_divorcialidad | float | NO | tasa bruta de divorcialidad por cada 1000 habitantes |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.tasa_bruta_divorcialidad_provincias (
    tasa_bruta_divorcialidad_provincias_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tasa_bruta_divorcialidad float NOT NULL CHECK (
      tasa_bruta_divorcialidad >= 0
      AND tasa_bruta_divorcialidad <= 1000
    )
  );
```

## Transformaciones notables

- Se eliminaron las filas donde `tasa_bruta_divorcialidad` aparecía como `..` y se convirtió la columna a valores numéricos.
- Se normalizaron `provincia_id`, `anio` y `tasa_bruta_divorcialidad` con las funciones de validación compartidas.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25212&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consultado el 18 de junio de 2025.
