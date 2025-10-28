# educacion_juventud.prestaciones_maternidad_paternidad

Prestaciones concedidas en los antiguos regímenes de maternidad y paternidad, desagregadas por tipo de prestación, persona perceptora y provincia.

- **Periodo temporal**: 2002-2019, anual
- **Desagregación regional**: provincias

Las prestaciones de maternidad podían cederse parcialmente al otro progenitor, mientras que las de paternidad eran intransferibles. Por ello, las filas con `tipo = 'Maternidad'` pueden contener valores en `percibidas_madre` y en `percibidas_padre`, mientras que las filas con `tipo = 'Paternidad'` presentan siempre `percibidas_madre = NULL`. Las prestaciones de paternidad se crearon con la Ley Orgánica 3/2007 (en vigor desde el 24 de marzo de 2007), por lo que no existen registros de paternidad antes de 2007. Los importes económicos solo están disponibles desde ese año.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| prestaciones_maternidad_paternidad_id | serial | NO | clave primaria |
| anio | int | NO | año |
| provincia_id | int | NO | referencia a geo.provincias |
| tipo | text | NO | tipo de prestación (`Maternidad`, `Paternidad`) |
| percibidas_madre | int | SÍ | número de prestaciones percibidas por la madre |
| percibidas_padre | int | NO | número de prestaciones percibidas por el padre |
| importe_miles_euros | float | SÍ | importe abonado en miles de euros (disponible desde 2007) |

## Definición de la tabla

```sql
CREATE TABLE
  educacion_juventud.prestaciones_maternidad_paternidad (
    prestaciones_maternidad_paternidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    tipo text NOT NULL CHECK (tipo IN ('Maternidad', 'Paternidad')),
    percibidas_madre int CHECK (percibidas_madre >= 0),
    percibidas_padre int NOT NULL CHECK (percibidas_padre >= 0),
    importe_miles_euros float CHECK (importe_miles_euros >= 0)
  );
```

## Transformaciones notables

- Se interpretaron hojas separadas de maternidad y paternidad para cada año y se desplegaron los encabezados multinivel hasta obtener un formato largo.
- Se filtraron las filas agregadas (totales nacionales y regionales) y se homogeneizaron los nombres provinciales antes de la normalización.
- Se convirtieron los importes monetarios a valores numéricos con dos decimales y se normalizaron los recuentos de prestaciones como enteros no negativos, manteniendo los nulos históricos cuando no se informaron importes o perceptores.

## Fuente

Anuarios Estadísticos del Ministerio de Trabajo y Economía Social (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
Consultado el 10 de junio de 2025.
