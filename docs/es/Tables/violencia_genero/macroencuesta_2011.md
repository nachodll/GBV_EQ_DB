# violencia_genero.macroencuesta_2011

Microdatos de la "Macroencuesta de Violencia contra la Mujer" de 2011 realizada por el Centro de Investigaciones Sociológicas (CIS). Cada fila contiene las respuestas anonimizadas de una persona encuestada, almacenadas como un documento JSON junto con el identificador de provincia.

- **Periodo temporal**: 2011
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| macroencuesta_2011_id | serial | NO | clave primaria |
| provincia_id | int | NO | referencia a geo.provincias |
| variables_json | jsonb | NO | documento JSON con las variables de la encuesta para la persona encuestada |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2011 (
    macroencuesta_2011_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Transformaciones notables

- El fichero SAV bruto (estudio 2858) se ingiere con `pyreadstat`, garantizando que las etiquetas de las categorías estén disponibles en el dataframe.
- Las cadenas vacías, los literales "NaN" y los valores numéricos NaN se sustituyen por nulos antes de serializar cada observación.
- El conjunto completo de variables del cuestionario se agrupa en un diccionario, se serializa a JSON en UTF-8 y se almacena en `variables_json`.
- Los identificadores provinciales se normalizan con las rutinas compartidas para que coincidan con `geo.provincias` para facilitar las consultas.

## Fuente
Datos extraídos del <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=12144" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Estudio 2858: Macroencuesta de Violencia contra la Mujer 2011.
