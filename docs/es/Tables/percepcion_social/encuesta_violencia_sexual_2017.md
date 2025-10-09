# percepcion_social.encuesta_violencia_sexual_2017

Microdatos del barómetro del CIS sobre percepciones sociales de la violencia sexual (estudio 3182). Las entrevistas realizadas en julio de 2017 se consolidan en documentos JSON para conservar el cuestionario completo y enlazar los territorios con el catálogo de provincias. Es preciso desanidar o mapear esos atributos para trabajar con preguntas concretas, y las etiquetas categóricas se mantienen en español tal y como las ofrece el CIS. El diccionario de variables completo puede encontrarse en el enlace a la fuente original.

- **Periodo temporal**: 5 de julio de 2017
- **Desagregación regional**: Provincias

## Columnas

| Nombre | Tipo de dato | ¿Nulo? | Descripción |
| --- | --- | --- | --- |
| encuesta_violencia_sexual_2017_id | serial | NO | Clave primaria |
| codigo_estudio | varchar(4) | NO | Código de estudio del CIS de cuatro dígitos |
| fecha | date | NO | Fecha del estudio |
| cuestionario | int | NO | Número de cuestionario dentro del estudio |
| comunidad_autonoma_id | int | SÍ | Clave foránea a `geo.comunidades_autonomas` |
| provincia_id | int | SÍ | Clave foránea a `geo.provincias` |
| variables_json | jsonb | NO | Registro completo de la encuesta serializado en JSON, con todas las columnas originales y etiquetas |

## Definición de la tabla

```sql
CREATE TABLE
  percepcion_social.encuesta_violencia_sexual_2017 (
    encuesta_violencia_sexual_2017_id serial PRIMARY KEY,
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    cuestionario int NOT NULL,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Transformaciones destacadas

- El script de transformación lee el fichero `.sav` original, convierte las respuestas categóricas a cadenas y serializa cada entrevista en JSON para preservar todas las variables del cuestionario.
- Los identificadores territoriales de comunidades autónomas y provincias se estandarizan mediante las utilidades de normalización compartidas antes de cargar los datos en la base de datos.

## Fuente

Datos extraídos del <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14354" target="_blank">barómetro del CIS sobre percepciones sociales de la violencia sexual (estudio 3182)</a>.
