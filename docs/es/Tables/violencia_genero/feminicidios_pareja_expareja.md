# violencia_genero.feminicidios_pareja_expareja

Número agregado mensual de feminicidios por provincia cometidos por la pareja o expareja de la víctima. Número agregado mensual de huérfanos menores dejados por feminicidios cometidos por la pareja o expareja de la víctima por provincia. Los datos sobre huérfanos están disponibles solo desde 2013 y su valor se establece como NULL para las entradas sin datos.

- **Periodo temporal**: 2003-2025, mensual (huerfanos_menores desde 2013)
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| feminicidios_pareja_expareja_id | serial | NO | primary key |
| feminicidios | int | NO | número de feminicidios |
| huerfanos_menores | int | YES | número de huérfanos menores |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| victima_grupo_edad | varchar | YES | grupo de edad de la víctima |
| agresor_grupo_edad | varchar | YES | grupo de edad del agresor |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.feminicidios_pareja_expareja (
    feminicidios_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    huerfanos_menores int CHECK (huerfanos_menores >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    victima_grupo_edad varchar CHECK (
      victima_grupo_edad ~ '^\\d+-\\d+$'
      OR victima_grupo_edad ~ '^<\\d+$'
      OR victima_grupo_edad ~ '^>\\d+$'
    ),
    agresor_grupo_edad varchar CHECK (
      agresor_grupo_edad ~ '^\\d+-\\d+$'
      OR agresor_grupo_edad ~ '^<\\d+$'
      OR agresor_grupo_edad ~ '^>\\d+$'
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos. El proveedor de datos solo permite seleccionar 5 variables de análisis a la vez. Se pueden encontrar más variables de análisis disponibles en la fuente original.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "010 Feminicidios en la pareja o expareja".
