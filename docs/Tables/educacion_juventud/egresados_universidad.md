# educacion_juventud.egresados_universidad

Number of university graduates by academic level, type of university, study mode, sex, and field of knowledge.

- **Time period**: 1985-2024, per academic year
- **Regional breakdown**: Comunidades

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| egresados_universidad_id | serial | NO | primary key |
| comunidad_autonoma_id | int | YES | references geo.comunidades_autonomas |
| nivel_academico | text | NO | academic level (`Total`, `Grado`, `1º y 2º ciclo`, `Máster`, `Doctorado`) |
| tipo_universidad | text | YES | type of university (`Total`, `Pública`, `Privada`) |
| modalidad_universidad | text | YES | university modality (`Total`, `Presencial`, `No Presencial`, `Especial`) |
| sexo | enums.sexo_enum | NO | sex |
| rama_conocimiento | text | NO | field of knowledge (`Total`, `Ciencias Sociales y Jurídicas`, `Ingeniería y Arquitectura`, `Artes y Humanidades`, `Ciencias de la Salud`, `Ciencias`) |
| curso | varchar | NO | academic year in `yyyy-yy` format |
| egresados | int | NO | number of graduates |

## Table definition

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

## Notable transformations

- Restructured the multi-level Excel source into a long table by iterating through academic level, university type, modality, sex, field of knowledge, and academic year combinations.
- Replaced `No desglosado` with null values for `comunidad_autonoma_id` and removed rows aggregated at the `Estado` level.
- 'No consta' values are stored as NULL.

## Source

Data extracted from <a href="https://estadisticas.universidades.gob.es/jaxiPx/Tabla.htm?path=/Universitaria/Alumnado/EEU_2024/Serie/TotalSUE//l0/&file=HIS_Egr_TotalSUE_Rama_CA.px&type=pcaxis&L=0" target="_blank">Ministerio de Ciencia Innovacion y Universidades.</a>
Consulted on 16 June 2025.
