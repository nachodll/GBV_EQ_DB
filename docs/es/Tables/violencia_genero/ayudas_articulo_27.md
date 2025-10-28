# violencia_genero.ayudas_articulo_27

Número de ayudas concedidas en virtud del artículo 27.

- **Periodo temporal**: 2006-2025, mensual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| ayudas_articulo_27_id | serial | NO | primary key |
| comunidad_autonoma_id | int | YES | referencia a geo.comunidades_autonomas |
| anio | int | NO | año |
| ayudas_concedidas | int | NO | número de ayudas concedidas |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.ayudas_articulo_27 (
    ayudas_articulo_27_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_concedidas int NOT NULL CHECK (ayudas_concedidas >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "070 Ayudas del artículo 27 - Ley integral 2004".
Consultado el 2 de junio de 2025.
