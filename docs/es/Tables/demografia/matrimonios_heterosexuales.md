# demografia.matrimonios_heterosexuales

Número de matrimonios entre personas de diferente sexo en España, desagregados por provincia, sexo, grupo de edad de los cónyuges y estado civil anterior.

- **Periodo temporal**: 1975-2023, anual. El detalle de `estado_civil_anterior` está disponible desde 2010
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| matrimonios_heterosexuales_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| sexo | enums.sexo_enum | NO | sexo |
| edad | varchar | NO | grupo de edad |
| estado_civil_anterior | varchar | YES | estado civil anterior |
| matrimonios | int | NO | número de matrimonios |
| es_residente_espania | boolean | NO | residente en España |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.matrimonios_heterosexuales (
    matrimonios_heterosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    edad varchar NOT NULL CHECK (
      edad ~ '^\\d+$'
      OR edad ~ '^<\\d+$'
      OR edad ~ '^>\\d+$'
    ),
    estado_civil_anterior varchar CHECK (
      estado_civil_anterior IN (
        'Total',
        'Solteros/Solteras',
        'Viudos/Viudas',
        'Divorciados/Divorciadas'
      )
      OR estado_civil_anterior IS NULL
    ),
    matrimonios int NOT NULL CHECK (matrimonios >= 0),
    es_residente_espania boolean NOT NULL
  );
```

## Transformaciones notables

- El detalle de `estado_civil_anterior` fue fusionado a partir de 2010.
- Se eliminaron las filas con datos agregados para `provincia_id`.
- Se eliminaron las filas con valores faltantes en `matrimonios`.
- La columna `es_residente_espania` se mapeó a booleano.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=6532&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Datos de estado civil anterior extraídos de <a href="https://ine.es/jaxiT3/Tabla.htm?t=32879" target="_blank">Instituto Nacional de Estadística (INE)</a>

