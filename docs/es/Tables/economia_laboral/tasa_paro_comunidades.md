# economia_laboral.tasa_paro_comunidades

Tasa trimestral de paro en España, desagregada por comunidad autónoma y sexo.

- **Periodo temporal**: 2002-2025, trimestral
- **Desagregación regional**: comunidades

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_paro_comunidades_id | serial | NO | primary key |
| anio | int | NO | año |
| trimestre | int | NO | número de trimestre (1-4) |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sexo (`Hombre`, `Mujer`, `Total`) |
| tasa_paro | float | NO | tasa de paro (%) |

## Definición de la tabla

```sql
CREATE TABLE
  economia_laboral.tasa_paro_comunidades (
    tasa_paro_comunidades_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    tasa_paro float NOT NULL CHECK (
      tasa_paro >= 0
      AND tasa_paro <= 100
    )
  );
```

## Transformaciones notables

- Se dividió el campo `Periodo` en las columnas `anio` y `trimestre`.
- Se filtró el conjunto de datos para mantener el agregado `Edad = 'Total'` y se eliminó la columna original `Edad`.
- Se eliminaron las filas con tasas de paro faltantes (`..`) y se convirtieron los porcentajes a valores numéricos.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=65334" target="_blank">Instituto Nacional de Estadística (INE)</a>.

Consultado el 16 de junio de 2025.

