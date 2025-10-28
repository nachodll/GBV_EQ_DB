# educacion_juventud.prestaciones_nacimiento_y_cuidado_menor

Prestaciones concedidas dentro del régimen unificado de nacimiento y cuidado de menor, desagregadas por progenitor y provincia.

- **Periodo temporal**: 2019-2023, anual
- **Desagregación regional**: provincias

Los datos de 2019 solo abarcan el periodo posterior a la entrada en vigor de la nueva ley (1 de abril de 2019), que integró los antiguos permisos de maternidad y paternidad en una única prestación. El "primer progenitor" es la primera persona cuidadora que disfruta del permiso (habitualmente la madre). Para consultar las series históricas de los regímenes anteriores, véase la tabla `educacion_juventud.prestaciones_maternidad_paternidad`. La columna `opcion_a_favor_segundo_progenitor` fue una medida temporal disponible durante parte de 2019 y debe restarse de `prestaciones_primer_progenitor` en ese año para obtener las prestaciones netas disfrutadas por el primer progenitor.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| prestaciones_nacimiento_y_cuidado_menor_id | serial | NO | clave primaria |
| anio | int | NO | año |
| provincia_id | int | NO | referencia a geo.provincias |
| prestaciones_primer_progenitor | int | NO | número de prestaciones disfrutadas por el primer progenitor |
| opcion_a_favor_segundo_progenitor | int | SÍ | cesiones a favor del segundo progenitor (solo aplica en 2019) |
| prestaciones_segundo_progenitor | int | NO | número de prestaciones disfrutadas por el segundo progenitor |
| importe_miles_euros | float | NO | importe abonado en miles de euros |

## Definición de la tabla

```sql
CREATE TABLE
  educacion_juventud.prestaciones_nacimiento_y_cuidado_menor (
    prestaciones_nacimiento_y_cuidado_menor_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    prestaciones_primer_progenitor int NOT NULL CHECK (prestaciones_primer_progenitor >= 0),
    opcion_a_favor_segundo_progenitor int CHECK (opcion_a_favor_segundo_progenitor >= 0),
    prestaciones_segundo_progenitor int NOT NULL CHECK (prestaciones_segundo_progenitor >= 0),
    importe_miles_euros float NOT NULL CHECK (importe_miles_euros >= 0)
  );
```

## Transformaciones notables

- Se interpretaron estructuras de hojas de cálculo cambiantes (incluido el año transitorio 2019) para aislar los totales del primer progenitor, la opción a favor y el segundo progenitor.
- Se eliminaron filas agregadas (totales nacionales y regionales) y se armonizaron los nombres provinciales antes de aplicar las utilidades de normalización compartidas.
- Se convirtieron los importes monetarios a valores numéricos con dos decimales y se aplicaron comprobaciones de no negatividad a los recuentos de prestaciones.

## Fuente

Anuarios Estadísticos del Ministerio de Trabajo y Economía Social (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
Consultado el 2 de junio de 2025.
