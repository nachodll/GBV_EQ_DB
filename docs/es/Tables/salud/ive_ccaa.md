# salud.ive_ccaa

Tasa de interrupciones voluntarias del embarazo por comunidad autónoma para mujeres de entre 15 y 44 años.

- **Periodo temporal**: 2014-2023, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ive_ccaa_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| tasa | float | NO | tasa por 1000 mujeres |

## Definición de la tabla

```sql
CREATE TABLE
  salud.ive_ccaa (
    ive_ccaa_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );
```

## Transformaciones notables
Se eliminaron las filas correspondientes al total y a la entrada combinada de Ceuta y Melilla.

## Fuente
Datos extraídos del <a href="https://www.sanidad.gob.es/areas/promocionPrevencion/embarazo/datosEstadisticos.htm#Tabla1" target="_blank">Ministerio de Sanidad</a>. Tabla: "Interrupciones voluntarias del embarazo".
Consultado el 16 de junio de 2025.
