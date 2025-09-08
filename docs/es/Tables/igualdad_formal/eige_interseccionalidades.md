# igualdad_formal.eige_interseccionalidades

Valores de los indicadores del EIGE al cruzar distintos tipos de desigualdades o violencia. Valores para España.

- **Periodo temporal**: 2017-2024, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| eige_interseccionalidad_id | serial | NO | primary key |
| anio | int | NO | año |
| pais_id | int | NO | referencia a geo.paises |
| indicador | text | NO | indicador |
| valor | int | YES | valor |
| sexo | enums.sexo_enum | NO | sexo |
| interseccionalidad | enums.eige_interseccionalidades_enum | NO | interseccionalidad |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
