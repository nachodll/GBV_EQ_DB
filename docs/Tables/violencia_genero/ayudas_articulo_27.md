# violencia_genero.ayudas_articulo_27

Number of aids granted under Article 27.

- **Time period**: 2006-2025, monthly
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ayudas_articulo_27_id | serial | NO | primary key |
| comunidad_autonoma_id | int | YES | references geo.comunidades_autonomas |
| anio | int | NO | year |
| ayudas_concedidas | int | NO | number of aids granted |

## Table definition

```sql
CREATE TABLE
  violencia_genero.ayudas_articulo_27 (
    ayudas_articulo_27_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_concedidas int NOT NULL CHECK (ayudas_concedidas >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "070 Ayudas del artículo 27 - Ley integral 2004".
Consulted on 2 June 2025.
