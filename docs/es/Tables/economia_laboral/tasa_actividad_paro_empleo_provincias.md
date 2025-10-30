# economia_laboral.tasa_actividad_paro_empleo_provincias

Tasas trimestrales de actividad, empleo y paro en España, desagregadas por provincia y sexo.

- **Periodo temporal**: 2002-2025, trimestral
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_actividad_paro_empleo_provincias_id | serial | NO | primary key |
| anio | int | NO | año |
| trimestre | int | NO | número de trimestre (1-4) |
| provincia_id | int | NO | referencia a geo.provincias |
| sexo | enums.sexo_enum | NO | sexo (`Hombre`, `Mujer`, `Total`) |
| tasa | text | NO | categoría de tasa (`Tasa de actividad`, `Tasa de empleo`, `Tasa de paro`) |
| total | float | NO | valor porcentual de la tasa seleccionada |

## Definición de la tabla

```sql
CREATE TABLE
  economia_laboral.tasa_actividad_paro_empleo_provincias (
    tasa_actividad_paro_empleo_provincias_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    tasa text NOT NULL CHECK (
      tasa IN (
        'Tasa de actividad',
        'Tasa de empleo',
        'Tasa de paro'
      )
    ),
    total float NOT NULL CHECK (
      total >= 0
      AND total <= 100
    )
  );
```

## Transformaciones notables

- Se dividió la columna `Periodo` en los campos `anio` y `trimestre`.
- Se eliminaron las filas con valores faltantes (`..`) y se convirtieron los porcentajes a formato numérico.
- Se normalizaron los identificadores de provincia, los años, los trimestres, las categorías de sexo y las etiquetas de tasa mediante utilidades compartidas de normalización.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=65349" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consultado el 16 de junio de 2025.
