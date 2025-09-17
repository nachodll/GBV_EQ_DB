# violencia_genero.encuesta_europea_2022

Microdatos de la encuesta de la Unión Europea sobre violencia de género realizada en España en 2022. Cada registro almacena las respuestas anonimizadas de una persona participante como objeto json.

- **Periodo temporal**: 2022
- **Desagregación regional**: España

Para más detalles acerca de la enconcuesta y las variables utilizadas, consultar <a href="https://ec.europa.eu/eurostat/documents/3859598/13484289/KS-GQ-21-009-EN-N.pdf#page=151" target="blank">Methodological manual for the EU survey on gender-based violence against women and other forms of inter-personal violence (EU-GBV)</a>

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| encuesta_europea_2022_id | serial | NO | primary key |
| encuestado_id | int | NO | identificador de la persona encuestada proporcionado en los microdatos originales |
| variables_json | jsonb | NO | documento JSON con el resto de variables de la encuesta para la persona encuestada |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.encuesta_europea_2022 (
    encuesta_europea_2022_id serial PRIMARY KEY,
    encuestado_id int NOT NULL,
    variables_json jsonb NOT NULL
  );
```

## Transformaciones notables

- El CSV de Eurostat se lee utilizando punto y coma como separador y los valores ausentes se convierten en nulos antes de la serialización.
- Debido a la gran cantidad de varibles y con el objetivo de preservar todas ellas, todas las columnas distintas del identificador de la persona encuestada (`PERS_ID_R`) se agrupan en un diccionario y se almacenan como cadena JSON en `variables_json`, de modo que cada fila representa una respuesta completa de la encuesta.
- Se valida que el identificador de la persona encuestada sea un entero positivo y que la cadena JSON esté bien formada antes de cargarla en la base de datos.

## Fuente
Datos extraídos de la <a href="https://ec.europa.eu/eurostat/web/microdata/gender-based-violence" target="_blank">encuesta de la Unión Europea sobre violencia de género de Eurostat (2022)</a>.
