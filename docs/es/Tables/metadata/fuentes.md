# metadata.fuentes

Todas las organizaciones e instituciones utilizadas como fuentes.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| fuente_id | serial | NO | primary key |
| nombre | varchar | NO | único |

# Definición de la tabla

```sql
CREATE TABLE
  metadata.fuentes (
    fuente_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```
