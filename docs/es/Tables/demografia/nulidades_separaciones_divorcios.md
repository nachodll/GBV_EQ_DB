# demografia.nulidades_separaciones_divorcios

Número de disoluciones matrimoniales en España, desagregadas por provincia, tipo de disolución y año. Los tipos de disolución considerados son nulidades, separaciones y divorcios.

- **Periodo temporal**: 1998-2023, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| nulidades_separaciones_divorcios_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | SÍ | referencia a geo.provincias |
| tipo_disolucion | varchar | NO | tipo de disolución matrimonial |
| disoluciones_matrimoniales | int | NO | número de disoluciones matrimoniales |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.nulidades_separaciones_divorcios (
    nulidades_separaciones_divorcios_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tipo_disolucion varchar NOT NULL CHECK (
      tipo_disolucion IN ('Nulidades', 'Separaciones', 'Divorcios')
    ),
    disoluciones_matrimoniales int NOT NULL CHECK (disoluciones_matrimoniales >= 0)
  );
```

## Transformaciones notables

- Se eliminaron las filas con datos agregados para `provincia_id` y `tipo_disolucion`.
- Se descartaron las entradas con `disoluciones_matrimoniales` faltantes.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=20173" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consultado el 9 de junio de 2025.
