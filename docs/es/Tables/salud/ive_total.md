# salud.ive_total

Total de interrupciones voluntarias del embarazo, centros notificadores y tasa por 1000 mujeres.

- **Periodo temporal**: 2014-2023, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ive_total_id | serial | NO | primary key |
| anio | int | NO | año |
| centros_notificadores | int | NO | número de centros notificadores |
| ives | int | NO | número de interrupciones |
| tasa | float | NO | tasa por 1000 mujeres |

## Definición de la tabla

```sql
CREATE TABLE
  salud.ive_total (
    ive_total_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    centros_notificadores int NOT NULL CHECK (centros_notificadores >= 0),
    ives int NOT NULL CHECK (ives >= 0),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://www.sanidad.gob.es/areas/promocionPrevencion/embarazo/datosEstadisticos.htm#Tabla1" target="_blank">Ministerio de Sanidad</a>.
