# violencia_genero.ayudas_cambio_residencia

Número de ayudas para cambio de residencia para víctimas de violencia de género concedidas.

- **Periodo temporal**: 2005-2025, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ayudas_cambio_residencia_id | serial | NO | primary key |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| ayudas_cambio_residencia | int | NO | número de ayudas |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.ayudas_cambio_residencia (
    ayudas_cambio_residencia_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_cambio_residencia int NOT NULL CHECK (ayudas_cambio_residencia >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "150 Ayudas para cambio de residencia".
