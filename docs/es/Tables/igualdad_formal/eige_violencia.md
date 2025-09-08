# igualdad_formal.eige_violencia

Las puntuaciones del dominio de violencia y sus subdominios se consideran dominios satélite y, por lo tanto, no se computan para el cálculo del Índice Europeo de Igualdad. Solo hay datos para 2 años.

- **Periodo temporal**: 2013 y 2024, anual
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| eige_violencia_id | serial | NO | primary key |
| anio | int | NO | año |
| pais_id | int | NO | referencia a geo.paises |
| indicador | text | NO | indicador |
| valor | int | NO | valor |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://eige.europa.eu/gender-statistics/dgs/browse/index" target="_blank">European Institute for Gender Equality (EIGE)</a>.
