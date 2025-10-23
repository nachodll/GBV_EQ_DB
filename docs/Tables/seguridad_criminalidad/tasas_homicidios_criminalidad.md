# seguridad_criminalidad.tasas_homicidios_criminalidad

Annual homicide and overall crime rates reported by the Ministry of the Interior and harmonised by the National Statistics Institute (INE).

- **Time period**: 2010-2023, annual
- **Regional breakdown**: comunidades autónomas

> **⚠️ Important:** Rate denominators differ by indicator type:
> 
> - **Tasa de homicidios**: rate per **100,000** inhabitants
> - **Tasa de criminalidad**: rate per **1,000** inhabitants

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| tasas_homicidios_criminalidad_id | serial | NO | primary key |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| anio | int | NO | year |
| tipo_tasa | text | NO | rate type ("Tasa de homicidios" or "Tasa de criminalidad") |
| total | float | NO | rate value (see note above for denominators) |

## Table definition

```sql
CREATE TABLE
  seguridad_criminalidad.tasas_homicidios_criminalidad (
    tasas_homicidios_criminalidad_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    tipo_tasa text NOT NULL CHECK (
      tipo_tasa IN ('Tasa de homicidios', 'Tasa de criminalidad')
    ),
    total float NOT NULL CHECK (total >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t00/ICV/dim6/l0/&file=61101.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>