# educacion_juventud.matriculados_educacion_no_universitaria

Number of enroled students in non-university education.

- **Time period**: 1999-2023, per academic year
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| matriculados_educacion_no_universitaria_id | serial | NO | primary key |
| titularidad | enums.titularidad_centro_ensenanza_enum | NO | 'Privado' or 'Público' |
| curso | varchar | NO | academic year |
| sexo | enums.sexo_enum | YES | sex |
| provincia_id | int | NO | references geo.provincias |
| ensenianza | varchar | NO | education |
| matriculados | int | NO | number of enroled students |

## Table definition

```sql
CREATE TABLE
  educacion_juventud.matriculados_educacion_no_universitaria (
    matriculados_educacion_no_universitaria_id serial PRIMARY KEY,
    titularidad enums.titularidad_centro_ensenanza_enum NOT NULL,
    curso varchar NOT NULL CHECK (
      curso ~ '^\d{4}-\d{2}$'
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
    sexo enums.sexo_enum,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    ensenianza varchar NOT NULL,
    matriculados int NOT NULL CHECK (matriculados >= 0)
  );
```

## Notable transformations

- Data before 2011 has .xls or .xlsx format and after 2011 it has .csv format. For some years the format varies slightly. The different datasets for each course were merged into a single one.
- Entries with aggregated data for `titularidad` were dropped.
- Entries with aggregated data for `sexo` were dropped.
- Entries with aggregated data for `provincia_id` were dropped.
- Entries with aggregated data for `ensenianza` were dropped.
- ".." values for `matriculados` are replaced by 0.

## Source
Data extracted from <a href="https://www.educacionfpydeportes.gob.es/ca/servicios-al-ciudadano/estadisticas/no-universitaria/alumnado/matriculado.html" target="_blank">Ministerio de Educación, Formación Profesional y Deportes.</a>
Consulted on 2 June 2025.
