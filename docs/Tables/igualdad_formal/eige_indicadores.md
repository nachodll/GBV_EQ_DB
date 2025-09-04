# igualdad_formal.eige_indicadores

Indicators used to calculate the Gender Equality Index, domain and sub-domain scores. Values for Spain.

- **Time period**: 2013-2025, anually
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| eige_indicador_id | serial | NO | primary key |
| anio | int | NO | year |
| pais_id | int | NO | references geo.paises |
| indicador | text | NO | indicator |
| valor | int | NO | value |
| sexo | enums.sexo_enum | NO | sex |

## Table definition

```sql
CREATE TABLE
  igualdad_formal.eige_indicadores (
    eige_indicador_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int NOT NULL CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.