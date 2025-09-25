# politica.elecciones_parlamentos_autonomicos

Recuentos de votos y escaños obtenidos por cada candidatura en las elecciones a los parlamentos autonómicos.

- **Periodo temporal**: 1980-2025, por elección
- **Desagregación regional**: Comunidades

## Columnas

| Nombre | Tipo de dato | ¿Nulo? | Descripción |
| --- | --- | --- | --- |
| elecciones_parlamentos_autonomicos_id | serial | NO | Clave primaria |
| fecha | date | NO | Fecha de la elección |
| comunidad_autonoma_id | int | NO | Referencia a `geo.comunidades_autonomas` |
| candidatura | varchar | NO | Nombre de la candidatura |
| votos | int | NO | Votos válidos recibidos por la candidatura |
| representantes | int | NO | Escaños obtenidos por la candidatura |

## Definición de la tabla

```sql
CREATE TABLE
  politica.elecciones_parlamentos_autonomicos (
    elecciones_parlamentos_autonomicos_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );
```

## Transformaciones destacadas

- El valor del campo `votos` para las elecciones al Parlmento de Canarias de 2023 y 2019 es la suma de los votos obtenidos por cada candidatura en las circunscriptciones insulares y la circunscripción autonómica.
- **Los partidos políticos no están normalizados. Los nombres de partidos y coaliciones se mantienen tal y como los publica la Junta Electoral Central, por lo que no deben usarse para análisis que requieran identificadores armonizados.**

## Fuente

Datos extraídos de la <a href="https://www.juntaelectoralcentral.es/cs/jec/elecciones/autonomicas" target="_blank">Junta Electoral Central (JEC)</a>.
