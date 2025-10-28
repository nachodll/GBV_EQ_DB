# violencia_genero.autorizaciones_residencia_trabajo_vvg

Number of residence and work permits granted to foreign women victims of gender based violence.

- **Time period**: 2005-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| autorizaciones_residencia_trabajo_vvg_id | serial | NO | primary key |
| provincia_id | int | YES | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |
| autorizaciones_concedidas | int | NO | total number of permits granted |

## Table definition

```sql
CREATE TABLE
  violencia_genero.autorizaciones_residencia_trabajo_vvg (
    autorizaciones_residencia_trabajo_vvg_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    autorizaciones_concedidas int NOT NULL CHECK (autorizaciones_concedidas >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "100 Concesiones de autorización de residencia y trabajo a mujeres extranjeras víctimas de violencia de género".
Consulted on 9 June 2025.
