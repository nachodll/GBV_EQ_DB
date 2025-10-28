# percepcion_social.encuesta_violencia_genero_2012

Microdata from the CIS barometer on social perceptions of gender-based violence (study 2968). Interviews from the November 2012 wave are stored as JSON documents to preserve all questionnaire variables while harmonizing territorial identifiers. Analysts need to unnest or map those attributes to work with individual questions, and categorical labels remain in Spanish as provided by the CIS. A complete variable dictionary can be found at the source url.


- **Time period**: 19 November 2012
- **Regional breakdown**: Provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| encuesta_violencia_genero_2012_id | serial | NO | Primary key |
| codigo_estudio | varchar(4) | NO | Four-digit CIS study code |
| fecha | date | NO | Date of the study |
| cuestionario | int | NO | Questionnaire number within the study |
| comunidad_autonoma_id | int | YES | Foreign key to `geo.comunidades_autonomas` |
| provincia_id | int | YES | Foreign key to `geo.provincias` |
| variables_json | jsonb | NO | Complete survey record serialized as JSON, including all original columns and labels |

## Table definition

```sql
CREATE TABLE
  percepcion_social.encuesta_violencia_genero_2012 (
    encuesta_violencia_genero_2012_id serial PRIMARY KEY,
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    cuestionario int NOT NULL,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Notable transformations

- The transformation script reads the original `.sav` file, converts categorical responses to strings, and serializes every interview as JSON to preserve all questionnaire variables.
- Territorial identifiers for autonomous communities and provinces are standardized through the shared normalization utilities before loading into the database.

## Source

Data extracted from the <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14086" target="_blank">CIS barometer on social perceptions of gender-based violence (study 2968)</a>.
Consulted on 3 June 2025.
