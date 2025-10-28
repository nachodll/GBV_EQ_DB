# igualdad_formal.eige_dominios

Europeen Gender Equality Index scores, domain scores and sub-domains scores for Spain.

- **Time period**: 2013-2024, anually
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| eige_dominio_id | serial | NO | primary key |
| anio | int | NO | year |
| pais_id | int | NO | references geo.paises |
| dominio_subdominio | enums.eige_dominio_subdominio_enum | NO | domain or subdomain |
| valor | numeric | NO | domain or sub-domain score |

## Table definition

```sql
CREATE TABLE
  igualdad_formal.eige_dominios (
    eige_dominio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    dominio_subdominio enums.eige_dominio_subdominio_enum NOT NULL,
    valor numeric NOT NULL CHECK (valor >= 0)
  );
```


## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
Consulted on 11 June 2025.
