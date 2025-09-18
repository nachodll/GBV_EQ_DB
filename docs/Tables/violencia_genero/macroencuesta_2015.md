# violencia_genero.macroencuesta_2015

Microdata from the 2015 "Macroencuesta de Violencia contra la Mujer" collected by the Centro de Investigaciones Sociológicas (CIS). Each entry contains the anonymised answers given by one respondent, aggregated into a JSON document alongside the province identifier.

- **Time period**: 2015
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| macroencuesta_2015_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| variables_json | jsonb | NO | JSON document with the survey variables for the respondent |

## Table definition

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2015 (
    macroencuesta_2015_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Notable transformations

- The raw SAV file (study 3027) is read with `pyreadstat`, applying the labelled values defined in the survey metadata.
- Blank strings, explicit "NaN" literals and numerical NaN values are converted to nulls before serialising the records.
- All survey variables are combined into a dictionary and serialised to UTF-8 JSON, which is stored in `variables_json`.
- Province identifiers are harmonised through the shared `normalize_provincia` utility to match `geo.provincias` and improve queries.

## Source
Data extracted from the <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14084" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Study 3027: Macroencuesta de Violencia contra la Mujer 2015.
