# igualdad_formal.eige_indicadores

Indicadores utilizados para calcular el Índice de Igualdad de Género, puntuaciones de dominios y subdominios. Valores para España.

- **Periodo temporal**: 2013-2025, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| eige_indicador_id | serial | NO | primary key |
| anio | int | NO | año |
| pais_id | int | NO | referencia a geo.paises |
| indicador | text | NO | indicador |
| valor | int | NO | valor |
| sexo | enums.sexo_enum | NO | sexo |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
