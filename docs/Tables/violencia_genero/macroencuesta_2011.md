# violencia_genero.macroencuesta_2011

Microdata from the 2011 "Macroencuesta de Violencia contra la Mujer" conducted by the Centro de Investigaciones Sociológicas (CIS). Each row contains the anonymised answers from one respondent, stored as a JSON document together with the province identifier.

- **Time period**: 2011
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| macroencuesta_2011_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| variables_json | jsonb | NO | JSON document with the survey variables for the respondent |

## Table definition

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2011 (
    macroencuesta_2011_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Notable transformations

- The raw SAV file (study 2858) is ingested with `pyreadstat`, ensuring that labelled categorical values are available in the dataframe.
- Empty strings, "NaN" literals and numerical NaN values are replaced with nulls before serialising each observation.
- The full set of questionnaire variables is bundled into a dictionary, serialised to UTF-8 JSON and stored in `variables_json`.
- Province identifiers are normalised with the shared routines so they align with `geo.provincias` to make queries easier.

## Source
Data extracted from the <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=12144" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Study 2858: Macroencuesta de Violencia contra la Mujer 2011.
