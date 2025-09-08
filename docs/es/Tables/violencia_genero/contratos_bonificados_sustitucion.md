# violencia_genero.contratos_bonificados_sustitucion

Número de contratos bonificados y número de contratos de sustitución para víctimas de violencia de género.

- **Periodo temporal**: 2003-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| contratos_bonificados_sustitucion_id | serial | NO | primary key |
| contratos_bonificados | int | NO | número de contratos bonificados |
| contratos_sustitucion | int | NO | número de contratos de sustitución |
| anio | int | NO | año |
| mes | int | NO | mes |
| provincia_id | int | YES | referencia a geo.provincias |
| colectivo | enums.colectivo_contratos_bonificados_sustitucion_enum | NO | colectivo |
| tipo_contrato | enums.tipo_contrato_enum | NO | tipo de contrato |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.contratos_bonificados_sustitucion (
    contratos_bonificados_sustitucion_id serial PRIMARY KEY NOT NULL,
    contratos_bonificados int NOT NULL CHECK (contratos_bonificados >= 0),
    contratos_sustitucion int NOT NULL CHECK (contratos_sustitucion >= 0),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    colectivo enums.colectivo_contratos_bonificados_sustitucion_enum NOT NULL,
    tipo_contrato enums.tipo_contrato_enum NOT NULL
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos. El proveedor de datos solo permite seleccionar 5 variables de análisis a la vez. Existen más variables de análisis en la fuente original.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "140 Contratos bonificados y de sustitución".
