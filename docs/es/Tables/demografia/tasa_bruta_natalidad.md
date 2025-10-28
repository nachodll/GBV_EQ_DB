# demografia.tasa_bruta_natalidad

Tasa bruta de natalidad en España, desagregada por provincia y año.

- **Periodo temporal**: 1975-2023, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasa_bruta_natalidad_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| tasa_bruta_natalidad | float | NO | tasa bruta de natalidad por 1000 habitantes |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.tasa_bruta_natalidad (
    tasa_bruta_natalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tasa_bruta_natalidad float NOT NULL CHECK (tasa_bruta_natalidad >= 0)
  );
```

## Transformaciones notables

- Se excluyeron las filas con datos agregados para `provincia_id`.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=1470&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Consultado el 3 de junio de 2025.
