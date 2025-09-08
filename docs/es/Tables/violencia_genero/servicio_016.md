# violencia_genero.servicio_016

Total mensual de consultas realizadas por distintos medios al servicio 016 por provincia.

- **Periodo temporal**: 2007-2025, mensual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| servicio_016_id | serial | NO | primary key |
| provincia_id | int | YES | referencia a geo.provincias |
| anio | int | NO | año |
| mes | int | NO | mes |
| persona_consulta | enums.persona_consulta_enum | YES | persona que realizó la consulta |
| tipo_violencia | enums.tipo_violencia_enum | YES | 'Pareja/Expareja', 'Familiar' o 'Sexual' |
| llamadas | int | NO | número de consultas vía teléfono |
| whatsapps | int | NO | número de consultas vía whatsapp |
| emails | int | NO | número de consultas vía correo electrónico |
| chats | int | NO | número de consultas vía chat |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.servicio_016 (
    servicio_016_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    persona_consulta enums.persona_consulta_enum,
    tipo_violencia enums.tipo_violencia_enum,
    llamadas int NOT NULL CHECK (llamadas >= 0),
    whatsapps int NOT NULL CHECK (whatsapps >= 0),
    emails int NOT NULL CHECK (emails >= 0),
    chats int NOT NULL CHECK (chats >= 0)
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos. El proveedor de datos solo permite seleccionar 5 variables de análisis a la vez. Se pueden encontrar más variables de análisis disponibles en la fuente original.

## Fuente
Datos extraídos del <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadístico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Tabla: "040 Servicio 016".
