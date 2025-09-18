# violencia_genero.macroencuesta_2019

Microdata from the 2019 "Macroencuesta de Violencia contra la Mujer" carried out by the Centro de Investigaciones Sociológicas (CIS). Each row stores the anonymised answers given by a single participant, consolidated as a JSON document together with the province identifier.

- **Time period**: 2019
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| macroencuesta_2019_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| variables_json | jsonb | NO | JSON document with the survey variables for the respondent |

## Table definition

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2019 (
    macroencuesta_2019_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Notable transformations

- The raw SAV file (study 3235) is read with `pyreadstat` so that labelled values are applied to the responses.
- Empty strings, "NaN" strings and numerical NaN values are replaced with nulls before serialising each record.
- All survey columns are grouped into a dictionary, serialised to UTF-8 JSON and stored in `variables_json`.
- Province identifiers are normalised against the reference table `geo.provincias` using the shared normalisation utilities in order to improve queries.

## Source
Data extracted from the <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14470" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Study 3235: Macroencuesta de Violencia contra la Mujer 2019.
