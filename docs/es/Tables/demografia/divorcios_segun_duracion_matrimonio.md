# demografia.divorcios_segun_duracion_matrimonio

Porcentaje de divorcios en España según la duración del matrimonio, desagregado por provincia y año. Los resultados del periodo 2005-2010 solo tienen en cuenta divorcios de matrimonios entre personas de distinto sexo. También vale la pena mencionar que en el periodo 2005-2010 se utilizan categorías diferentes para los rangos de duraciones del matrimonio.

- **Periodo temporal**: 2005-2023, anual (solo matrimonios heterosexuales para el periodo 2005-2010)
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| divorcios_segun_duracion_matrimonio_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| duracion_matrimonio | varchar | NO | duración del matrimonio |
| porcentaje_divorcios | float | YES | porcentaje de divorcios |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.divorcios_segun_duracion_matrimonio (
    divorcios_segun_duracion_matrimonio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    duracion_matrimonio varchar NOT NULL CHECK (
      duracion_matrimonio IN (
        'Menos de 1 año',
        'De 1 año',
        'De 1 a 2 años',
        'De 2 a 4 años',
        'De 3 a 5 años',
        'De 5 a 9 años',
        'De 6 a 10 años',
        'De 10 a 14 años',
        'De 11 a 15 años',
        'De 15 a 19 años',
        'De 16 a 19 años',
        'De 20 a 29 años',
        '20 y más años',
        '30 y más años'
      )
    ),
    porcentaje_divorcios float CHECK (
      porcentaje_divorcios >= 0
      AND porcentaje_divorcios <= 100
    )
  );
```

## Transformaciones notables

- Se fusionaron los conjuntos de datos de 2005-2010 y 2010-2023.
- Se eliminaron las filas con `porcentaje_divorcios` faltante.
- Se eliminaron las filas con datos agregados para `provincia_id`.

## Fuente

Datos para el periodo 2005-2010 extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25214&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Datos para el periodo 2010-2023 extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=25213&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>
