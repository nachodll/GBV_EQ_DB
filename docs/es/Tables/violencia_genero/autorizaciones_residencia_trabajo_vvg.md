# violencia_genero.autorizaciones_residencia_trabajo_vvg

Número de autorizaciones de residencia y trabajo concedidas a mujeres extranjeras víctimas de violencia de género.

- **Periodo temporal**: 2005-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| autorizaciones_residencia_trabajo_vvg_id | serial | NO | primary key |
| provincia_id | int | YES | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| autorizaciones_concedidas | int | NO | número total de permisos concedidos |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.autorizaciones_residencia_trabajo_vvg (
    autorizaciones_residencia_trabajo_vvg_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    autorizaciones_concedidas int NOT NULL CHECK (autorizaciones_concedidas >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "100 Concesiones de autorización de residencia y trabajo a mujeres extranjeras víctimas de violencia de género".
Consultado el 9 de junio de 2025.
