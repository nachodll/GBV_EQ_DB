# educacion_juventud.egresados_universidad

Número de egresados universitarios según nivel académico, tipo de universidad, modalidad de estudio, sexo y rama de conocimiento.

- **Periodo temporal**: 1985-2024, por curso académico
- **Desagregación regional**: Comunidades

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| egresados_universidad_id | serial | NO | primary key |
| comunidad_autonoma_id | int | SÍ | referencia a geo.comunidades_autonomas |
| nivel_academico | text | NO | nivel académico (`Total`, `Grado`, `1º y 2º ciclo`, `Máster`, `Doctorado`) |
| tipo_universidad | text | SÍ | tipo de universidad (`Total`, `Pública`, `Privada`) |
| modalidad_universidad | text | SÍ | modalidad universitaria (`Total`, `Presencial`, `No Presencial`, `Especial`) |
| sexo | enums.sexo_enum | NO | sexo |
| rama_conocimiento | text | NO | rama de conocimiento (`Total`, `Ciencias Sociales y Jurídicas`, `Ingeniería y Arquitectura`, `Artes y Humanidades`, `Ciencias de la Salud`, `Ciencias`) |
| curso | varchar | NO | curso académico en formato `yyyy-yy` |
| egresados | int | NO | número de egresados |

## Definición de la tabla

```sql
CREATE TABLE
  educacion_juventud.egresados_universidad (
    egresados_universidad_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nivel_academico text NOT NULL CHECK (
      nivel_academico IN (
        'Total',
        'Grado',
        '1º y 2º ciclo',
        'Máster',
        'Doctorado'
      )
    ),
    tipo_universidad text CHECK (
      tipo_universidad IN ('Total', 'Pública', 'Privada')
    ),
    modalidad_universidad text CHECK (
      modalidad_universidad IN (
        'Total',
        'Presencial',
        'No Presencial',
        'Especial'
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    rama_conocimiento text NOT NULL CHECK (
      rama_conocimiento IN (
        'Total',
        'Ciencias Sociales y Jurídicas',
        'Ingeniería y Arquitectura',
        'Artes y Humanidades',
        'Ciencias de la Salud',
        'Ciencias'
      )
    ),
    curso varchar NOT NULL CHECK (
      curso ~ '^\\d{4}-\\d{2}$'
      AND (
        substring(curso, 1, 4)::int BETWEEN 1900 AND EXTRACT(
          YEAR
          FROM
            CURRENT_DATE
        )
      )
      AND (
        substring(curso, 6, 2)::int = (substring(curso, 3, 2)::int + 1) % 100
      )
    ),
    egresados int NOT NULL CHECK (egresados >= 0)
  );
```

## Transformaciones notables

- Reestructuración del Excel multinivel a una tabla en formato largo iterando por combinaciones de nivel académico, tipo y modalidad de universidad, sexo, rama de conocimiento y curso académico.
- Sustitución de `No desglosado` por valores nulos en `comunidad_autonoma_id` y eliminación de filas agregadas al nivel `Estado`.
- Los valores 'No consta' se almacenan como NULL.

## Fuente

Datos extraídos del <a href="https://estadisticas.universidades.gob.es/jaxiPx/Tabla.htm?path=/Universitaria/Alumnado/EEU_2024/Serie/TotalSUE//l0/&file=HIS_Egr_TotalSUE_Rama_CA.px&type=pcaxis&L=0" target="_blank">Ministerio de Ciencia Innovacion y Universidades.</a>
