# politica.elecciones_parlamentos_autonomicos

Vote counts and seats obtained by each candidacy in autonomous parliamentary elections.

- **Time period**: 1980-2025, per election
- **Regional breakdown**: Comunidades

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| elecciones_parlamentos_autonomicos_id | serial | NO | Primary key |
| fecha | date | NO | Election date |
| comunidad_autonoma_id | int | NO | References `geo.comunidades_autonomas` |
| candidatura | varchar | NO | Name of the electoral candidacy |
| votos | int | NO | Valid votes received by the candidacy |
| representantes | int | NO | Seats obtained by the candidacy |

## Table definition

```sql
CREATE TABLE
  politica.elecciones_parlamentos_autonomicos (
    elecciones_parlamentos_autonomicos_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );
```

## Notable transformations

- The value of the `votes` field for the 2023 and 2019 Canary Islands Parliament elections is the sum of the votes obtained by each candidate in the island constituencies and the regional constituency.
- **Political parties are not normalized. Party and coalition names remain as published by the Junta Electoral Central, so they should not be used for analyses that require harmonized party identifiers.**

## Source

Data extracted from the <a href="https://www.juntaelectoralcentral.es/cs/jec/elecciones/autonomicas" target="_blank">Junta Electoral Central (JEC)</a>.
