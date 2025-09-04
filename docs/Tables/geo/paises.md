# geo.paises

Country names. Primary key is auto generated.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| pais_id | serial | NO | primary key |
| nombre | varchar | NO | unique |

## Table definition

```sql
CREATE TABLE
  geo.paises (
    pais_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```

## Source
Own elaboration