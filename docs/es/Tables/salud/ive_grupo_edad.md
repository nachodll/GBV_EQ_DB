# salud.ive_grupo_edad

Interrupciones voluntarias del embarazo por grupo de edad, tasa por cada 1000 mujeres.

- **Periodo temporal**: 2014-2023, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ive_grupo_edad_id | serial | NO | primary key |
| anio | int | NO | año |
| grupo_edad | varchar | NO | grupo de edad |
| tasa | float | NO | tasa por 1000 mujeres |

## Definición de la tabla

```sql
CREATE TABLE
  salud.ive_grupo_edad (
    ive_grupo_edad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );
```

## Transformaciones notables
Se sustituyó "19 y menos años" por "<19" en las etiquetas de grupo de edad.

## Fuente
Datos extraídos del <a href="https://www.sanidad.gob.es/areas/promocionPrevencion/embarazo/datosEstadisticos.htm#Tabla1" target="_blank">Ministerio de Sanidad</a>.
