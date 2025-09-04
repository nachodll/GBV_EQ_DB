# salud.ive_ccaa

Rate of voluntary pregnancy terminations by autonomous community of women between 15 and 44 years old.

- **Time period**: 2014-2023, annual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ive_ccaa_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| tasa | float | NO | rate per 1000 women |

## Table definition

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

## Notable transformations
Removed rows corresponding to the total and to the combined entry for Ceuta y Melilla.

## Source
Data extracted from <a href="https://www.sanidad.gob.es/areas/promocionPrevencion/embarazo/datosEstadisticos.htm#Tabla1" target="_blank">Ministerio de Sanidad</a>. Table: "Interrupciones voluntarias del embarazo".
