# violencia_genero.renta_activa_insercion

Number of recipients of active insertion income.

- **Time period**: 2006-2025, anually
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| renta_activa_insercion_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| perceptoras | int | NO | number of recipients |

## Table definition

```sql
CREATE TABLE
  violencia_genero.renta_activa_insercion (
    renta_activa_insercion_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    perceptoras int NOT NULL CHECK (perceptoras >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "130 Renta Activa de Inserción".
