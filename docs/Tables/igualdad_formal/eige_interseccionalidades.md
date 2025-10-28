# igualdad_formal.eige_interseccionalidades

EIGE indicator values when intersecting different types of inequalities or violence. Values for Spain.

- **Time period**: 2017-2024, anually
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| eige_interseccionalidad_id | serial | NO | primary key |
| anio | int | NO | yaer |
| pais_id | int | NO | references geo.paises |
| indicador | text | NO | indicator |
| valor | int | YES | value |
| sexo | enums.sexo_enum | NO | sex |
| interseccionalidad | enums.eige_interseccionalidades_enum | NO | intersection |

## Table definition

```sql
CREATE TABLE
  igualdad_formal.eige_interseccionalidades (
    eige_interseccionalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL,
    interseccionalidad enums.eige_interseccionalidades_enum NOT NULL
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
Consulted on 2 June 2025.
