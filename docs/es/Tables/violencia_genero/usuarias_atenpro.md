# violencia_genero.usuarias_atenpro

Número de usuarias activas, altas y bajas del servicio telefónico de atención y protección para víctimas de violencia contra las mujeres, Atenpro.

- **Periodo temporal**: 2005-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| usuarias_atenpro_id | serial | NO | primary key |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| altas | int | NO | número de altas |
| bajas | int | NO | número de bajas |
| usuarias_activas | int | NO | número total de usuarias activas |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.usuarias_atenpro (
    usuarias_atenpro_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    altas int NOT NULL CHECK (altas >= 0),
    bajas int NOT NULL CHECK (bajas >= 0),
    usuarias_activas int NOT NULL CHECK (usuarias_activas >= 0)
  );
```

## Transformaciones notables
Se eliminaron las entradas con valores negativos en `altas` y `bajas`.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "050 Usuarias de ATENPRO".
