# violencia_genero.renta_activa_insercion

Número de perceptoras de la renta activa de inserción.

- **Periodo temporal**: 2006-2025, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| renta_activa_insercion_id | serial | NO | primary key |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| perceptoras | int | NO | número de perceptoras |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.renta_activa_insercion (
    renta_activa_insercion_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    perceptoras int NOT NULL CHECK (perceptoras >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "130 Renta Activa de Inserción".
