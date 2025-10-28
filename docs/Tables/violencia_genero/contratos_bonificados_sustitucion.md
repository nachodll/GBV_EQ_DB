# violencia_genero.contratos_bonificados_sustitucion

Number of subsidized contracts and number of replacement contracts for victims of gender based violence.

- **Time period**: 2003-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| contratos_bonificados_sustitucion_id | serial | NO | primary key |
| contratos_bonificados | int | NO | number of subsidized contracts |
| contratos_sustitucion | int | NO | number of replacemet contracts |
| anio | int | NO | year |
| mes | int | NO | month |
| provincia_id | int | YES | references geo.provincias |
| colectivo | enums.colectivo_contratos_bonificados_sustitucion_enum | NO | colective |
| tipo_contrato | enums.tipo_contrato_enum | NO | type of contract |

## Table definition

```sql
CREATE TABLE
  violencia_genero.contratos_bonificados_sustitucion (
    contratos_bonificados_sustitucion_id serial PRIMARY KEY NOT NULL,
    contratos_bonificados int NOT NULL CHECK (contratos_bonificados >= 0),
    contratos_sustitucion int NOT NULL CHECK (contratos_sustitucion >= 0),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    colectivo enums.colectivo_contratos_bonificados_sustitucion_enum NOT NULL,
    tipo_contrato enums.tipo_contrato_enum NOT NULL
  );
```

## Notable transformations
No notable transformations were performed over this dataset. Source data provider only allows 5 analysis variable to be selected at time. More analysis variables are available at the original source. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "140 Contratos bonificados y de sustitución".
Consulted on 10 June 2025.
