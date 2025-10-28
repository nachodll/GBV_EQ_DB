# demografia.hogares_monoparentales

Número de miles de hogares monoparentales en España, desagregado por comunidad autónoma, sexo, grupo de edad y estado civil de la persona cabeza de hogar.

- **Periodo temporal**: 2014-2020, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| hogares_monoparentales_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sexo |
| grupo_edad | varchar | YES | grupo de edad |
| estado_civil | varchar | YES | estado civil |
| hogares_monoparentales | float | NO | número de miles de hogares monoparentales |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.hogares_monoparentales (
    hogares_monoparentales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    estado_civil varchar CHECK (
      estado_civil IN (
        'Soltero/a',
        'Casado/a',
        'Viudo/a',
        'Separado/a',
        'Divorciado/a'
      )
      OR estado_civil IS NULL
    ),
    hogares_monoparentales float NOT NULL CHECK (hogares_monoparentales >= 0)
  );
```

## Transformaciones notables

- Se rellenaron con 0 los valores faltantes de `hogares_monoparentales`.
- Descartadas entradas con valores agregados para los campos `comunidad_autonoma_id`, `sexo`, `grupo_edad` y `estado_civil`.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t20/p274/serie/def/p02/&file=02015.px" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consultado el 2 de junio de 2025.
