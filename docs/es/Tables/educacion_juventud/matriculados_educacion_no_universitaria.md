# educacion_juventud.matriculados_educacion_no_universitaria

Número de estudiantes matriculados en educación no universitaria.

- **Periodo temporal**: 1999-2023, por curso académico
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| matriculados_educacion_no_universitaria_id | serial | NO | primary key |
| titularidad | enums.titularidad_centro_ensenanza_enum | NO | 'Privado' o 'Público' |
| curso | varchar | NO | curso académico |
| sexo | enums.sexo_enum | YES | sexo |
| provincia_id | int | NO | referencia a geo.provincias |
| ensenianza | varchar | NO | enseñanza |
| matriculados | int | NO | número de estudiantes matriculados |

## Definición de la tabla

```sql
CREATE TABLE
  educacion_juventud.matriculados_educacion_no_universitaria (
    matriculados_educacion_no_universitaria_id serial PRIMARY KEY,
    titularidad enums.titularidad_centro_ensenanza_enum NOT NULL,
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
    sexo enums.sexo_enum,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    ensenianza varchar NOT NULL,
    matriculados int NOT NULL CHECK (matriculados >= 0)
  );
```

## Transformaciones notables

- Los datos anteriores a 2011 están en formato .xls o .xlsx y a partir de 2011 en .csv. Para algunos años el formato varía ligeramente. Los diferentes conjuntos de datos de cada curso se fusionaron en uno solo.
- Se eliminaron las entradas con datos agregados para `titularidad`.
- Se eliminaron las entradas con datos agregados para `sexo`.
- Se eliminaron las entradas con datos agregados para `provincia_id`.
- Se eliminaron las entradas con datos agregados para `ensenianza`.
- Los valores ".." en `matriculados` se sustituyeron por 0.

## Fuente

Datos extraídos del <a href="https://www.educacionfpydeportes.gob.es/ca/servicios-al-ciudadano/estadisticas/no-universitaria/alumnado/matriculado.html" target="_blank">Ministerio de Educación, Formación Profesional y Deportes.</a>
Consultado el 2 de junio de 2025.
