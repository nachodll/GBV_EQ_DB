# violencia_genero.feminicidios_fuera_pareja_expareja

Aggregate number of anual feminicides per autonomous community committed by an agressor who is not victim's partner or ex-partner.

- **Time period**: 2022-2025, anual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| feminicidios_fuera_pareja_expareja_id | serial | NO | primary key |
| feminicidios | int | NO | number of feminicides |
| tipo_feminicidio | enums.tipo_feminicidio_enum | NO | 'Familiar', 'Sexual', 'Social' or 'Vicario' |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| anio | int | NO | year |

## Table definition

```sql
CREATE TABLE
  violencia_genero.feminicidios_fuera_pareja_expareja (
    feminicidios_fuera_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    tipo_feminicidio enums.tipo_feminicidio_enum NOT NULL,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "020 Feminicidios fuera de la pareja o expareja".