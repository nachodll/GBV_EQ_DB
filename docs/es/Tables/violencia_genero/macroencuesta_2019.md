# violencia_genero.macroencuesta_2019

Microdatos de la "Macroencuesta de Violencia contra la Mujer" de 2019 realizada por el Centro de Investigaciones Sociológicas (CIS). Cada fila almacena las respuestas anonimizadas de una persona participante, consolidadas en un documento JSON junto con el identificador de provincia.

- **Periodo temporal**: 2019
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| macroencuesta_2019_id | serial | NO | clave primaria |
| provincia_id | int | NO | referencia a geo.provincias |
| variables_json | jsonb | NO | documento JSON con las variables de la encuesta para la persona encuestada |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.macroencuesta_2019 (
    macroencuesta_2019_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );
```

## Transformaciones notables

- El fichero SAV bruto (estudio 3235) se lee con `pyreadstat` para aplicar las etiquetas de valores a las respuestas.
- Las cadenas vacías, los literales "NaN" y los valores numéricos NaN se sustituyen por nulos antes de serializar cada registro.
- Todas las columnas de la encuesta se agrupan en un diccionario, se serializan a JSON en UTF-8 y se almacenan en `variables_json`.
- Los identificadores provinciales se normalizan con la tabla de referencia `geo.provincias` mediante las utilidades de normalización compartidas para facilitar las consultas.

## Fuente
Datos extraídos del <a href="https://www.cis.es/detalle-ficha-estudio?origen=estudio&idEstudio=14470" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Estudio 3235: Macroencuesta de Violencia contra la Mujer 2019.
