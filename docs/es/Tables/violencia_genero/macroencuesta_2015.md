# violencia_genero.macroencuesta_2015

Microdatos de la "Macroencuesta de Violencia contra la Mujer" de 2015 recopilados por el Centro de Investigaciones Sociológicas (CIS). Cada registro contiene las respuestas anonimizadas de una persona encuestada, agregadas en un documento JSON junto al identificador de provincia.

- **Periodo temporal**: 2015
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| macroencuesta_2015_id | serial | NO | clave primaria |
| provincia_id | int | NO | referencia a geo.provincias |
| variables_json | jsonb | NO | documento JSON con las variables de la encuesta para la persona encuestada |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2015 (
    macroencuesta_2015_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Transformaciones notables

- El fichero SAV bruto (estudio 3027) se procesa con `pyreadstat`, aplicando las etiquetas de valores definidas en la encuesta.
- Las cadenas vacías, los literales "NaN" y los valores numéricos NaN se convierten en nulos antes de serializar los registros.
- Todas las variables del cuestionario se agrupan en un diccionario y se serializan a JSON en UTF-8, que se almacena en `variables_json`.
- Los identificadores provinciales se armonizan mediante la utilidad compartida `normalize_provincia` para que coincidan con `geo.provincias` y facilitar las consultas.

## Fuente
Datos extraídos del <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14084" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Estudio 3027: Macroencuesta de Violencia contra la Mujer 2015.
Consultado el 10 de junio de 2025.
