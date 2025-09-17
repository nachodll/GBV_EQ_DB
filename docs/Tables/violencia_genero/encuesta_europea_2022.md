# violencia_genero.encuesta_europea_2022

Microdata from the 2022 European Union survey on gender-based violence carried out in Spain. Each record stores the anonymised responses provided by a single participant stored as a json object.

- **Time period**: 2022
- **Regional breakdown**: Spain

For more details on how the survey was conducted and information about the variables, check the <a href="https://ec.europa.eu/eurostat/documents/3859598/13484289/KS-GQ-21-009-EN-N.pdf#page=151" target="blank">Methodological manual for the EU survey on gender-based violence against women and other forms of inter-personal violence (EU-GBV)</a>

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| encuesta_europea_2022_id | serial | NO | primary key |
| variables_json | jsonb | NO | JSON document with the survey variables for the respondent |

## Table definition

```sql
CREATE TABLE
  violencia_genero.encuesta_europea_2022 (
    encuesta_europea_2022_id serial PRIMARY KEY,
    variables_json jsonb NOT NULL
  );
```

## Notable transformations

- The raw Eurostat CSV is read using a semicolon delimiter and missing values are converted to nulls prior to serialisation.
- Due to the large amount of variables and in order to preserve the entire variable set, all columns are aggregated into a dictionary and stored as a JSON string in `variables_json` so each row represents a full survey response.
- Data validation ensures the JSON string is well formed before loading it into the database.

## Source
Data extracted from <a href="https://ec.europa.eu/eurostat/web/microdata/gender-based-violence" target="_blank">Eurostat's European Union survey on gender-based violence (2022)</a>.
