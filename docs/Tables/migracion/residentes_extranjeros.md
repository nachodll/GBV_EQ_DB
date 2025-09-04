# migracion.residentes_extranjeros

Number of foreign residents in Spain with valid documentation.

- **Time period**: 1996-2024, anually before 2013 and quarterly after 2013
- **Regional breakdown**: provincias

Due to differences in source data, not every variable is available for every year. Below is a list of the years for which each variable is available. When not available, it will have a NULL value.

- `es_nacido_espania`: 2013-2024
- `grupo_edad`: 2010-2024
- `tipo_documentacion`: 2013-2024
- `regimen`: 2001-2024
- `sexo`: 1997-2024
- `nacionalidad`: 1996 and 2002-2024

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| residentes_extranjeros_id | serial | NO | primary key |
| provincia_id | int | YES | references geo.provincias |
| nacionalidad | int | YES | references geo.paises |
| sexo | enums.sexo_enum | YES | sex |
| es_nacido_espania | boolean | YES | born in Spain |
| grupo_edad | varchar | YES | age group |
| fecha | date | NO | date |
| residentes_extranjeros | int | NO | number of foreign residents |
| tipo_documentacion | enums.tipo_documentacino_enum | YES | 'Certificado de registro', 'Autorización' or 'TIE-Acuerdo de Retirada' |
| regimen | enums.tipo_regimen_enum | YES | 'Régimen General' or 'Régimen de libre circulación de la UE' |

## Table definition

```sql
CREATE TABLE
  migracion.residentes_extranjeros (
    residentes_extranjeros_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum,
    es_nacido_espania boolean,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    fecha date NOT NULL CHECK (
      fecha >= DATE '1900-01-01'
      AND fecha <= CURRENT_DATE
    ),
    residentes_extranjeros int NOT NULL CHECK (residentes_extranjeros >= 0),
    tipo_documentacion enums.tipo_documentacino_enum,
    regimen enums.tipo_regimen_enum
  );
```

## Notable transformations

- Data after 2013 belongs to two different merged tables: "Personas con autorización de residencia por provincia según sexo, grupo de edad, principales nacionalidades y lugar de nacimiento." for entries with `tipo_documentacion = 'Autorización'` and "Personas con certificado de registro o TIE-Acuerdo de Retirada por provincia según sexo, grupo de edad, principales nacionalidades y lugar de nacimiento." for entries with `tipo_documentacion = 'TIE-Acuerdo de Retirada' or 'Certificado de Registro'`.
- Data for 2012, 2011 and 2011 is distributed among several .xls files, one per province. Sheet 4 of these files was used and all of them were merged into a single dataset.
- Data for 2002-2009 was extracted from 2010 files, since sheet 1 contains a detailed historic evolution. It was merged into a single dataset.
- Data for 2001 was extracted from sheet 8 of its respective .xls file.
- Data for 1997-2000 was extracted from sheet 10 of their respective .xls file.
- Data for 1996 was extracted from sheet 1 of its respective .xls file.
- All previous datasets were merged into a single one.
- "-" values were replaced with 0.
- All other nationalities ('otros américa', 'otros asia'...) were unified into a single 'Otros' category.
- All entries with aggregated data for `provincia_id` were dropped.
- All entries with aggregated data for `country_id` were dropped.
- All entries with aggregated data for `tipo_documentacion` were dropped.
- All entries with aggregated data for `es_nacido_espania` were dropped.
- All entries with aggregated data for `grupo_edad` were dropped.
- All entries with aggregated data for `regimen` were dropped.

 
## Source
Data extracted from <a href="https://expinterweb.inclusion.gob.es/dynPx/inebase/index.htm?type=pcaxis&path=/Stock/&file=pcaxis" target="_blank">Observatorio Permanente de la Inmigración (OPI)</a>. 