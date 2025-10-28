# violencia_genero.denuncias_vg_pareja

Number of reports of gender based violence against partners or ex-partners.

- **Time period**: 2009-2025, quarterly
- **Regional breakdown**: provincias
  
## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| denuncias_vg_pareja_id | serial | NO | primary key |
| origen_denuncia | enums.origen_denuncia_enum | NO | organization or person who reported the events |
| anio | int | NO | year |
| trimestre | int | NO | quarter |
| provincia_id | int | NO | references geo.provincias |
| denuncias | int | NO | number of reports |

## Table definition

```sql
CREATE TABLE
  violencia_genero.denuncias_vg_pareja (
    denuncias_vg_pareja_id serial PRIMARY KEY,
    origen_denuncia enums.origen_denuncia_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    denuncias int NOT NULL CHECK (denuncias >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "110 Denuncias por violencia de género en la pareja o expareja".
Consulted on 2 June 2025.
