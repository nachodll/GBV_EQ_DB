# violencia_genero.viogen

Número de casos abiertos en el Sistema de Seguimiento Integral en los casos de Violencia de Género (VioGén) del Ministerio del Interior.

- **Periodo temporal**: 2013-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| viogen_id | serial | NO | primary key |
| provincia_id | int | NO | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| nivel_riesgo | enums.nivel_riesgo_viogen_enum | NO | nivel de riesgo: 'Extremo', 'Alto', 'Medio' o 'No apreciado' |
| casos | int | NO | número de casos |
| casos_proteccion_policial | int | NO | número de casos con protección policial |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.viogen (
    viogen_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    nivel_riesgo enums.nivel_riesgo_viogen_enum NOT NULL,
    casos int NOT NULL CHECK (casos >= 0),
    casos_proteccion_policial int NOT NULL CHECK (casos_proteccion_policial >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "090 VioGén - Sistema de seguimiento integral de casos de VG".
Consultado el 17 de junio de 2025.
