# igualdad_formal.eige_violencia

Violence domain and sub-domain score are seen as satellite domains and therefore do not compute for the calculation of the Europeen Equality Index. Only data for 2 years is available.

- **Time period**: 2013 and 2024, anually
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| eige_violencia_id | serial | NO | primary key |
| anio | int | NO | year |
| pais_id | int | NO | references geo.paises |
| indicador | text | NO | indicator |
| valor | int | NO | value |

## Table definition

```sql
CREATE TABLE
  igualdad_formal.eige_violencia (
    eige_violencia_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int NOT NULL CHECK (valor >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.