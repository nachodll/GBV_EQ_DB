# seguridad_criminalidad.tasas_homicidios_criminalidad

Tasas anuales de homicidios y de criminalidad general registradas por el Ministerio del Interior y armonizadas por el Instituto Nacional de Estadística (INE).

- **Periodo temporal**: 2010-2023, anual
- **Desagregación regional**: comunidades autónomas

> **⚠️ Importante:** Los denominadores de las tasas difieren entre indicadores:
>
> - **Tasas de homicidios**: tasa por **100,000** habitantes
> - **Tasa de criminalidad**: tasa por **1,000** habitantes

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| tasas_homicidios_criminalidad_id | serial | NO | primary key |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| anio | int | NO | año |
| tipo_tasa | text | NO | tipo de tasa ("Tasa de homicidios" o "Tasa de criminalidad") |
| total | float | NO | valor de la tasa (comprobar denominadores en la nota previa) |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.


## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t00/ICV/dim6/l0/&file=61101.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.
