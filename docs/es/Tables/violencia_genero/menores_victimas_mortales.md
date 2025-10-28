# violencia_genero.menores_victimas_mortales

Agregado mensual de menores fallecidos por provincia según la causa de un delito de violencia de género. Se considera víctima vicaria solo si la madre no ha sido asesinada en el mismo evento.

- **Periodo temporal**: 2013-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| menores_victimas_mortales_id | serial | NO | primary key |
| es_hijo_agresor | boolean | NO | si la víctima era hijo biológico o adoptado del agresor |
| es_victima_vicaria | boolean | NO | se considera víctima vicaria solo si la madre no ha sido asesinada en el mismo evento |
| menores_victimas_mortales | int | NO | número de menores fallecidos |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.menores_victimas_mortales (
    menores_victimas_mortales_id serial PRIMARY KEY,
    es_hijo_agresor boolean NOT NULL,
    es_victima_vicaria boolean NOT NULL,
    menores_victimas_mortales int NOT NULL CHECK (menores_victimas_mortales >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)
  );
```

## Transformaciones notables
Los campos de texto "VM Vicaria -1-" y "AG-VM Relación" se mapearon a los valores booleanos `es_victima_vicaria` y `es_hijo_agresor`, respectivamente.

El proveedor de datos solo permite seleccionar 5 variables de análisis a la vez. Se pueden encontrar más variables de análisis disponibles en la fuente original.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "030 Menores víctimas mortales".
Consultado el 2 de junio de 2025.
