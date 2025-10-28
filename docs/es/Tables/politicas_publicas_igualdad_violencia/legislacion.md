# politicas_publicas_igualdad_violencia.legislacion

Catálogo de normativa autonómica sobre igualdad y violencia de género en las comunidades autónomas españolas.

- **Periodo temporal**: 2001-2025
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| legislacion_id | serial | NO | clave primaria |
| comunidad_autonoma_id | int | SÍ | referencia a geo.comunidades_autonomas; 0 para leyes estatales |
| nombre | text | NO | título oficial de la norma |
| fecha_aprobacion | date | NO | fecha de aprobación |
| enlace_boe | text | NO | URL a la publicación en el Boletín Oficial del Estado |
| tematica | text | NO | ámbito temático: "Violencia de género" o "Igualdad" |
| vigente | boolean | NO | indica si la norma está en vigor |
| fecha_derogacion | date | SÍ | fecha de derogación, si aplica |

## Definición de la tabla

```sql
CREATE TABLE
  politicas_publicas_igualdad_violencia.legislacion (
    legislacion_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    fecha_aprobacion date NOT NULL CHECK (fecha_aprobacion <= CURRENT_DATE),
    enlace_boe text NOT NULL,
    tematica text NOT NULL CHECK (tematica IN ('Violencia de género', 'Igualdad')),
    vigente boolean NOT NULL,
    fecha_derogacion date CHECK (
      fecha_derogacion <= CURRENT_DATE
      AND fecha_derogacion >= fecha_aprobacion
    )
  );
```

## Transformaciones notables

- Conjunto de datos elaborado manualmente a partir de las publicaciones del BOE, homogeneizando identificadores autonómicos y temáticas.

## Fuente

Datos de elaboración propia a partir del <a href="https://www.boe.es/" target="_blank">Boletín Oficial del Estado (BOE)</a>.

Consultado el 3 de junio de 2025.
