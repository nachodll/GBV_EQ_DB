# geo.paises

Nombres de países. La primary key se autogenera.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| pais_id | serial | NO | primary key |
| nombre | varchar | NO | único |

## Definición de la tabla

```sql
CREATE TABLE
  geo.paises (
    pais_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```

## Fuente

Elaboración propia
