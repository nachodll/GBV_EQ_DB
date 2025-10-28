# violencia_genero.denuncias_vg_pareja

Número de denuncias por violencia de género contra parejas o exparejas.

- **Periodo temporal**: 2009-2025, trimestral
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| denuncias_vg_pareja_id | serial | NO | primary key |
| origen_denuncia | enums.origen_denuncia_enum | NO | organización o persona que denunció los hechos |
| anio | int | NO | año |
| trimestre | int | NO | trimestre |
| provincia_id | int | NO | referencia a geo.provincias |
| denuncias | int | NO | número de denuncias |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.denuncias_vg_pareja (
    denuncias_vg_pareja_id serial PRIMARY KEY,
    origen_denuncia enums.origen_denuncia_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    denuncias int NOT NULL CHECK (denuncias >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "110 Denuncias por violencia de género en la pareja o expareja".
Consultado el 2 de junio de 2025.
