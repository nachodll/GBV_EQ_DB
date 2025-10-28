# violencia_genero.viogen

Number of open cases in the Comprehensive Monitoring System for Gender Violence Cases (VioGen) of the Ministry of the Interior.

- **Time period**: 2013-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| viogen_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |
| nivel_riesgo | enums.nivel_riesgo_viogen_enum | NO | risk level: 'Extremo', 'Alto', 'Medio' or 'No apreciado' |
| casos | int | NO | number of cases |
| casos_proteccion_policial | int | NO | number of cases with police protection |

## Table definition

```sql
CREATE TABLE
  violencia_genero.viogen (
    viogen_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    nivel_riesgo enums.nivel_riesgo_viogen_enum NOT NULL,
    casos int NOT NULL CHECK (casos >= 0),
    casos_proteccion_policial int NOT NULL CHECK (casos_proteccion_policial >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "090 VioGén - Sistema de seguimiento integral de casos de VG".
Consulted on 17 June 2025.
