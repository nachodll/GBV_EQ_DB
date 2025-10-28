# percepcion_social.barometros_generales

Microdatos de los barómetros generales del CIS (Centro de Investigaciones Sociológicas), armonizados para ofrecer una visión consistente de los metadatos de las entrevistas y las variables fijas seleccionadas de los barómetros. Está fusión incluye todos los barómetros generales a los que se tiene acceso desde 1979.

- **Periodo temporal**: 1979-2025, por entrevista
- **Desagregación regional**: España (ámbito estatal) con identificadores opcionales de comunidad autónoma y provincia

## Columnas

| Nombre | Tipo de dato | ¿Nulo? | Descripción |
| --- | --- | --- | --- |
| barometros_generales_id | serial | NO | Clave primaria |
| fecha | date | NO | Fecha de la entrevista inferida a partir de la ficha del estudio del CIS |
| codigo_estudio | varchar(4) | NO | Código de estudio del CIS de cuatro dígitos |
| cuestionario | int | SÍ | Número de cuestionario dentro del estudio |
| comunidad_autonoma_id | int | SÍ | Clave foránea a `geo.comunidades_autonomas` |
| provincia_id | int | SÍ | Clave foránea a `geo.provincias` |
| edad | int | SÍ | Edad de la persona entrevistada |
| sexo | enums.sexo_enum | SÍ | Sexo de la persona entrevistada |
| ideologia | int | SÍ | Autoubicación ideológica en la escala 1 (izquierda) – 10 (derecha) |
| religiosidad | varchar | SÍ | Categoría de religiosidad armonizada |
| problema_personal_1 | text | SÍ | Primer problema señalado como personalmente relevante |
| problema_personal_2 | text | SÍ | Segundo problema señalado como personalmente relevante |
| problema_personal_3 | text | SÍ | Tercer problema señalado como personalmente relevante |
| problema_espania_1 | text | SÍ | Primer problema considerado más importante en España |
| problema_espania_2 | text | SÍ | Segundo problema considerado más importante en España |
| problema_espania_3 | text | SÍ | Tercer problema considerado más importante en España |

## Definición de la tabla

```sql
CREATE TABLE
  percepcion_social.barometros_generales (
    barometros_generales_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    cuestionario int,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    edad int CHECK (edad BETWEEN 1 AND 150),
    sexo enums.sexo_enum,
    ideologia int CHECK (ideologia BETWEEN 1 AND 10),
    religiosidad varchar CHECK (
      religiosidad IN (
        'Ateo/a',
        'Agnóstico/a',
        'Indiferente, no creyente',
        'Católico/a',
        'Católico/a practicante',
        'Católico/a no practicante',
        'Creyente de otra religión'
      )
      OR religiosidad IS NULL
    ),
    problema_personal_1 text,
    problema_personal_2 text,
    problema_personal_3 text,
    problema_espania_1 text,
    problema_espania_2 text,
    problema_espania_3 text
  );
```

## Cobertura y limitaciones

- A 3 de octubre de 2025 la web del CIS listaba 501 barómetros generales; 427 estudios se incorporaron a la base de datos. Los 74 restantes se descartaron porque (a) 51 no disponen de microdatos descargables, (b) 8 corresponden a barómetros fusionados, (c) 14 no incluyen ficheros `.sav` (`MD1436`, `MD1444`, `MD2927`, `MD2932`, `MD2935`, `MD2941`, `MD2944`, `MD2948`, `MD2951`, `MD2954`, `MD2966`, `MD2972`, `MD3109`, `MD3347`) y (d) el fichero `.sav` del estudio `MD2023` está dañado.
- Las columnas `religiosidad` e `ideologia` han sido estandarizadas entre todos los estudios para facilitar análisis longitudinales. Sin embargo, es importante considerar que la formulación de estas preguntas en los cuestionarios originales ha evolucionado a lo largo del tiempo, lo que puede introducir diferencias sutiles en la interpretación. Por ejemplo, en las encuestas más antiguas los extremos de la escala ideológica (0 y 10) se etiquetaban como "izquierda" y "derecha", mientras que en estudios más recientes se describen como "extrema izquierda" y "extrema derecha" respectivamente. Estos cambios en la formulación pueden influir en las respuestas y deben tenerse en cuenta al interpretar tendencias temporales.
- Las columnas de problemas (`problema_*`) no están estandarizadas entre oleadas. Incluso tras aplicar el diccionario de limpieza, los estudios históricos mantienen etiquetas heterogéneas, por lo que corresponde a la persona usuaria reagrupar o recodificar las categorías para análisis longitudinales.

## Transformaciones destacadas

- <a href="https://github.com/nachodll/GBV_EQ_DB/blob/main/downloaders/CIS004_download.py"> La automatización con Selenium </a>(CIS004_download.py) recorre cada página de barómetros del CIS, registra la metadata y almacena mapeos provisionales de variables antes de descargar los ZIP disponibles.
- Los mapeos de variables se obtienen automáticamente con el descargador del CIS y se corrigen durante la transformación para fijar nombres consistentes, cubrir ausencias y dividir las preguntas de respuesta múltiple, dado que el JSON generado en el scraping no es plenamente fiable.
- Los ficheros ZIP son descomprimidos y la estructura de directorios es reajustada en caso de directorios anidados.
- Las variables objetivo se extraen de cada estudio y se fusionan en un único dataframe. Las variables se extraen solo si forman parte del conjunto de variables objetivo y existe un mapa para dicho estudio y dicha variable.
- Durante la transformación se aplican los nombres canónicos de las variables, se corrigen fallos tipográficos en los territorios, se normalizan cuestionarios, edades, sexo, ideología y religiosidad, y se depuran los problemas con un diccionario específico antes de enlazar los territorios con las tablas geográficas.


## Fuente

Datos extraídos del <a href="https://www.cis.es/catalogo-estudios/resultados-definidos/barometros" target="_blank">portal de Barómetros Generales del Centro de Investigaciones Sociológicas (CIS)</a>.
Consultado el 3 de octubre de 2025.
