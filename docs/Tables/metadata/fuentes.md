# metadata.fuentes

All organizations and institutions used as sources.

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| fuente_id | serial | NO | primary key |
| nombre | varchar | NO | unique |

# Table definition

```sql
CREATE TABLE
  metadata.fuentes (
    fuente_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```
