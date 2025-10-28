# politica.elecciones_congreso

Recuentos de votos y escaños obtenidos por cada candidatura en las elecciones generales al Congreso de los Diputados.

- **Periodo temporal**: 1977-2023, por elección
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | ¿Nulo? | Descripción |
| --- | --- | --- | --- |
| elecciones_congreso_id | serial | NO | Clave primaria |
| anio | int | NO | Año de la elección |
| mes | int | NO | Mes de la elección |
| candidatura | varchar | NO | Nombre de la candidatura |
| votos | int | NO | Votos válidos recibidos por la candidatura |
| representantes | int | NO | Escaños obtenidos por la candidatura |

## Definición de la tabla

```sql
CREATE TABLE
  politica.elecciones_congreso (
    elecciones_congreso_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );
```

## Transformaciones destacadas

- El año y el mes de la elección se extraen del identificador `Id convocatoria` suministrado en los ficheros del Ministerio del Interior.
- **Los partidos políticos no están normalizados entre tablas. Los nombres de partidos y coaliciones se mantienen tal y como aparecen en la fuente, por lo que no deben usarse para análisis que requieran identificadores armonizados.**

## Fuente

Datos extraídos del <a href="https://infoelectoral.interior.gob.es/es/elecciones-celebradas/resultados-electorales" target="_blank">Ministerio del Interior</a>.
Consultado el 17 de junio de 2025.
