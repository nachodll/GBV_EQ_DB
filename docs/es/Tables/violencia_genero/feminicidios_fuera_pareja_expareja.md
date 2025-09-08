# violencia_genero.feminicidios_fuera_pareja_expareja

Número agregado anual de feminicidios por comunidad autónoma cometidos por un agresor que no es la pareja o expareja de la víctima.

- **Periodo temporal**: 2022-2025, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| feminicidios_fuera_pareja_expareja_id | serial | NO | primary key |
| feminicidios | int | NO | número de feminicidios |
| tipo_feminicidio | enums.tipo_feminicidio_enum | NO | 'Familiar', 'Sexual', 'Social' o 'Vicario' |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| anio | int | NO | año |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.feminicidios_fuera_pareja_expareja (
    feminicidios_fuera_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    tipo_feminicidio enums.tipo_feminicidio_enum NOT NULL,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "020 Feminicidios fuera de la pareja o expareja".
