# violencia_genero.dispositivos_electronicos_seguimiento

Número de instalaciones y desinstalaciones de dispositivos electrónicos de seguimiento, así como el número de dispositivos activos.

- **Periodo temporal**: 2009-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| dispositivos_electronicos_seguimiento_id | serial | NO | primary key |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| instalaciones_acumuladas | int | NO | número de instalaciones acumuladas |
| desinstalaciones_acumuladas | int | NO | número de desinstalaciones acumuladas |
| dispositivos_activos | int | NO | número de dispositivos activos |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.dispositivos_electronicos_seguimiento (
    dispositivos_electronicos_seguimiento_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    instalaciones_acumuladas int NOT NULL CHECK (instalaciones_acumuladas >= 0),
    desinstalaciones_acumuladas int NOT NULL CHECK (desinstalaciones_acumuladas >= 0),
    dispositivos_activos int NOT NULL CHECK (dispositivos_activos >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "060 Dispositivos electrónicos de seguimiento".
