# percepcion_social.encuesta_igualdad_2023

Microdatos del barómetro especial del CIS (Centro de Investigaciones Sociológicas) sobre percepciones de la igualdad entre hombres y mujeres (estudio 3428). Cada fila recoge una entrevista y conserva el cuestionario completo en un documento JSON, a la vez que armoniza los identificadores territoriales utilizados por el CIS. Es preciso desanidar o mapear esos atributos para trabajar con preguntas concretas, y las etiquetas categóricas se mantienen en español tal y como las ofrece el CIS. El diccionario de variables completo puede encontrarse en el enlace a la fuente original.

- **Periodo temporal**: 6 de noviembre de 2023
- **Desagregación regional**: Provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| encuesta_igualdad_2023_id | serial | NO | Clave primaria |
| codigo_estudio | varchar(4) | NO | Código de estudio del CIS de cuatro dígitos |
| fecha | date | NO | Fecha del estudio |
| cuestionario | int | NO | Número de cuestionario dentro del estudio |
| comunidad_autonoma_id | int | SÍ | Clave foránea a `geo.comunidades_autonomas` |
| provincia_id | int | SÍ | Clave foránea a `geo.provincias` |
| variables_json | jsonb | NO | Registro completo de la encuesta serializado en JSON, con todas las columnas originales y sus etiquetas de valor |

## Definición de la tabla

```sql
CREATE TABLE
  percepcion_social.encuesta_igualdad_2023 (
    encuesta_igualdad_2023_id serial PRIMARY KEY,
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

Datos extraídos del <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14756" target="_blank">barómetro especial del CIS sobre igualdad entre hombres y mujeres (estudio 3428)</a>.
Consultado el 10 de junio de 2025.
