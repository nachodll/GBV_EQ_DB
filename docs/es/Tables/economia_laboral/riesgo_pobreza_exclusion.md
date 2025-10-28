# economia_laboral.riesgo_pobreza_exclusion

Proporción de población en riesgo de pobreza o exclusión social (AROPE) y sus componentes, elaborada por el INE a partir de la Encuesta de Condiciones de Vida.

- **Periodo temporal**: 2008-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| riesgo_pobreza_exclusion_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| indicador | text | NO | etiqueta del indicador dentro del marco AROPE |
| porcentaje | float | NO | porcentaje de población |

## Definición de la tabla

```sql
CREATE TABLE
  economia_laboral.riesgo_pobreza_exclusion (
    riesgo_pobreza_exclusion_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    indicador text NOT NULL CHECK (
      indicador IN (
        'Tasa de riesgo de pobreza o exclusión social (indicador AROPE)',
        'En riesgo de pobreza (renta año anterior a la entrevista)',
        'Con carencia material severa',
        'Viviendo en hogares con baja intensidad en el trabajo (de 0 a 59 años)'
      )
    ),
    porcentaje float NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.


## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=10011" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consultado el 23 de octubre de 2025.
