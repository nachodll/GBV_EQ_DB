# educacion_juventud.nivel_formacion

Distribución porcentual de la población según nivel educativo alcanzado de acuerdo con la Clasificación Internacional Normalizada de la Educación (CINE/ISCED), elaborada por el INE a partir de la Encuesta de Población Activa.

- **Periodo temporal**: 2004-2023, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| nivel_formacion_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| grupo_edad | varchar | NO | grupo de edad ("25-64" or ">65") |
| nivel_formacion | text | NO | tramo educativo según la CINE |
| porcentaje | numeric | NO | porcentaje de población en el tramo |

### Correspondencia CINE
- **Nivel 0-2**: CINE 0-2 (educación infantil, primaria y primera etapa de secundaria).
- **Nivel 3-4**: CINE 3-4 (segunda etapa de secundaria y educación postsecundaria no terciaria).
- **Nivel 5-8**: CINE 5-8 (enseñanzas terciarias desde ciclos cortos hasta doctorados).
- **Nivel 3-8**: agregado de CINE 3-8, es decir, población con educación secundaria superior o superior.

## Definición de la tabla

```sql
CREATE TABLE
  educacion_juventud.nivel_formacion (
    nivel_formacion_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    nivel_formacion text NOT NULL CHECK (
      nivel_formacion IN (
        'Nivel 0-2',
        'Nivel 3-8',
        'Nivel 3-4',
        'Nivel 5-8'
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.


## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t00/ICV/dim4/l0/&file=41201.px&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.
