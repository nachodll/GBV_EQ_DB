# politicas_publicas_igualdad_violencia.legislacion

Catalogue of regional legislation on gender equality and gender-based violence across the Spanish autonomous communities.

- **Time period**: 2001-2025
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| legislacion_id | serial | NO | primary key |
| comunidad_autonoma_id | int | YES | references geo.comunidades_autonomas; 0 for national laws |
| nombre | text | NO | official title of the law |
| fecha_aprobacion | date | NO | approval date |
| enlace_boe | text | NO | URL to the law in the Boletín Oficial del Estado |
| tematica | text | NO | thematic focus: either "Violencia de género" or "Igualdad" |
| vigente | boolean | NO | whether the law is currently in force |
| fecha_derogacion | date | YES | repeal date, if applicable |

## Table definition

```sql
CREATE TABLE
  politicas_publicas_igualdad_violencia.legislacion (
    legislacion_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    fecha_aprobacion date NOT NULL CHECK (fecha_aprobacion <= CURRENT_DATE),
    enlace_boe text NOT NULL,
    tematica text NOT NULL CHECK (tematica IN ('Violencia de género', 'Igualdad')),
    vigente boolean NOT NULL,
    fecha_derogacion date CHECK (
      fecha_derogacion <= CURRENT_DATE
      AND fecha_derogacion >= fecha_aprobacion
    )
  );
```

## Notable transformations

- Manually curated dataset consolidating laws published in the BOE and harmonising community identifiers and thematic labels.

## Source

Self-produced dataset based on the <a href="https://www.boe.es/" target="_blank">Boletín Oficial del Estado (BOE)</a>.
