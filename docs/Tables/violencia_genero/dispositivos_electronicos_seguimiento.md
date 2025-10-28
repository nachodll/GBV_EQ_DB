# violencia_genero.dispositivos_electronicos_seguimiento

Number of installs and uninstalls of electronic tracking devices, as well as the number of active devices.

- **Time period**: 2009-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| dispositivos_electronicos_seguimiento_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |
| instalaciones_acumuladas | int | NO | number of accumulated installs |
| desinstalaciones_acumuladas | int | NO | number of accumulated uninstalls |
| dispositivos_activos | int | NO | number of active devices |

## Table definition

```sql
CREATE TABLE
  violencia_genero.dispositivos_electronicos_seguimiento (
    dispositivos_electronicos_seguimiento_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    instalaciones_acumuladas int NOT NULL CHECK (instalaciones_acumuladas >= 0),
    desinstalaciones_acumuladas int NOT NULL CHECK (desinstalaciones_acumuladas >= 0),
    dispositivos_activos int NOT NULL CHECK (dispositivos_activos >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.  

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "060 Dispositivos electrónicos de seguimiento".
Consulted on 17 June 2025.
