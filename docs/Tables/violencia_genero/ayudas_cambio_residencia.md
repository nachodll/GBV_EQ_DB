# violencia_genero.ayudas_cambio_residencia

Number of aids programs for change of residence for victims of gender based violence.

- **Time period**: 2005-2025, anually
- **Regional breakdown**: provincias


## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| ayudas_cambio_residencia_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias|
| anio | int | NO | year |
| ayudas_cambio_residencia | int | NO | number of aids |

## Table definition

```sql
CREATE TABLE
  violencia_genero.ayudas_cambio_residencia (
    ayudas_cambio_residencia_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_cambio_residencia int NOT NULL CHECK (ayudas_cambio_residencia >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.
## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "150 Ayudas para cambio de residencia".