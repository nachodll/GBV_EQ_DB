# igualdad_formal.eige_dominios

Puntuaciones del Índice Europeo de Igualdad de Género, dominios y subdominios para España.

- **Periodo temporal**: 2013-2024, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| eige_dominio_id | serial | NO | primary key |
| anio | int | NO | año |
| pais_id | int | NO | referencia a geo.paises |
| dominio_subdominio | enums.eige_dominio_subdominio_enum | NO | dominio o subdominio |
| valor | numeric | NO | puntuación del dominio o subdominio |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
