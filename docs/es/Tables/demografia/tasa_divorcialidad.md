# demografia.tasa_divorcialidad

Tasa de divorcios en España, desagregada por provincia, sexo, grupo de edad y año. Los resultados del periodo 2005-2010 solo tienen en cuenta divorcios de matrimonios entre personas de distinto sexo.


- **Periodo temporal**: 2005-2023, anual (solo matrimonios heterosexuales para el periodo 2005-2010)
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_divorcialidad_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| sexo | enums.sexo_enum | NO | sexo |
| grupo_edad | varchar | YES | grupo de edad |
| tasa_divorcialidad | float | NO | tasa de divorcios por 1000 personas |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.tasa_divorcialidad (
    tasa_divorcialidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    tasa_divorcialidad float NOT NULL CHECK (
      tasa_divorcialidad >= 0
      AND tasa_divorcialidad <= 1000
    )
  );
```

## Transformaciones notables

- Se fusionaron los conjuntos de datos de 2005-2010 y 2010-2023. El primer periodo no incluye divorcios entre personas del mismo sexo.
- Se excluyeron las filas con `tasa_divorcialidad` faltante.
- Se eliminaron las entradas con valores agregados para `sexo` y `provincia_id`.


## Fuente

 Datos para el periodo 2005-2010 extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25216&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Datos para el periodo 2010-2023 extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25217&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>