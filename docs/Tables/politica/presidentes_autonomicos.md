# politica.presidentes_autonomicos

List of the presidents of the autonomous communities, including their legislature, appointment date, and party affiliation.

- **Time period**: 1980-2025
- **Regional breakdown**: Comunidades

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| presidentes_autonomicos_id | serial | NO | Primary key |
| comunidad_autonoma_id | int | NO | References `geo.comunidades_autonomas` |
| legislatura | varchar | NO | Legislative term |
| presidente | varchar | NO | Name of the regional president |
| nombramiento | date | NO | Appointment date |
| partido | text | NO | Political party of the president |

## Table definition

```sql
CREATE TABLE
  politica.presidentes_autonomicos (
    presidentes_autonomicos_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    partido text NOT NULL
  );
```

## Notable transformations

- **Political parties are not normalized. Party names remain exactly as provided by the Senado de España, so they should not be used for analyses that require harmonized party identifiers.**

## Source

Data extracted from the <a href="https://www.senado.es/web/conocersenado/biblioteca/dossieresareastematicas/detalledossier/index.html?lang=es_ES&id=DOSSIER_CCAA1&parte=CCAA1_PLANES" target="_blank">Senado de España</a>.
Consulted on 2 June 2025.
