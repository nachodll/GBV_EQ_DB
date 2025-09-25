# politica.elecciones_congreso

Vote counts and seats obtained by each candidacy in Spanish general elections to the Congress of Deputies.

- **Time period**: 1977-2023, per election
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| elecciones_congreso_id | serial | NO | Primary key |
| anio | int | NO | Election year |
| mes | int | NO | Election month |
| candidatura | varchar | NO | Name of the electoral candidacy |
| votos | int | NO | Valid votes received by the candidacy |
| representantes | int | NO | Seats obtained by the candidacy |

## Table definition

```sql
CREATE TABLE
  politica.elecciones_congreso (
    elecciones_congreso_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );
```

## Notable transformations

- The election year and month are parsed from the `Id convocatoria` identifier provided by the Ministerio del Interior files.
- **Political parties are not normalized accross tables. Party and coalition names remain as published by the source, so they should not be used for analyses that require harmonized party identifiers.**

## Source

Data extracted from <a href="https://infoelectoral.interior.gob.es/es/elecciones-celebradas/resultados-electorales" target="_blank">Ministerio del Interior</a>.
