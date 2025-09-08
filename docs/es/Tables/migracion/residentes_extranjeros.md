# migracion.residentes_extranjeros

Número de residentes extranjeros en España con documentación vigente.

- **Periodo temporal**: 1996-2024, anual antes de 2013 y trimestral después de 2013
- **Desagregación regional**: provincias

Debido a diferencias en los datos de origen, no todas las variables están disponibles para todos los años. A continuación se muestra una lista de los años para los que cada variable está disponible. Cuando una variable no esté disponible en una entrada, tendrá un valor NULL.

- `es_nacido_espania`: 2013-2024
- `grupo_edad`: 2010-2024
- `tipo_documentacion`: 2013-2024
- `regimen`: 2001-2024
- `sexo`: 1997-2024
- `nacionalidad`: 1996 y 2002-2024

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| residentes_extranjeros_id | serial | NO | primary key |
| provincia_id | int | YES | referencia a geo.provincias |
| nacionalidad | int | YES | referencia a geo.paises |
| sexo | enums.sexo_enum | YES | sexo |
| es_nacido_espania | boolean | YES | nacido en España |
| grupo_edad | varchar | YES | grupo de edad |
| fecha | date | NO | fecha |
| residentes_extranjeros | int | NO | número de residentes extranjeros |
| tipo_documentacion | enums.tipo_documentacino_enum | YES | 'Certificado de registro', 'Autorización' o 'TIE-Acuerdo de Retirada' |
| regimen | enums.tipo_regimen_enum | YES | 'Régimen General' o 'Régimen de libre circulación de la UE' |

## Definición de la tabla

```sql
CREATE TABLE
  migracion.residentes_extranjeros (
    residentes_extranjeros_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum,
    es_nacido_espania boolean,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\\d+-\\d+$'
      OR grupo_edad ~ '^<\\d+$'
      OR grupo_edad ~ '^>\\d+$'
    ),
    fecha date NOT NULL CHECK (
      fecha >= DATE '1900-01-01'
      AND fecha <= CURRENT_DATE
    ),
    residentes_extranjeros int NOT NULL CHECK (residentes_extranjeros >= 0),
    tipo_documentacion enums.tipo_documentacino_enum,
    regimen enums.tipo_regimen_enum
  );
```

## Transformaciones notables

- Los datos posteriores a 2013 pertenecen a dos tablas diferentes fusionadas: "Personas con autorización de residencia por provincia según sexo, grupo de edad, principales nacionalidades y lugar de nacimiento" para las entradas con `tipo_documentacion = 'Autorización'` y "Personas con certificado de registro o TIE-Acuerdo de Retirada por provincia según sexo, grupo de edad, principales nacionalidades y lugar de nacimiento" para las entradas con `tipo_documentacion = 'TIE-Acuerdo de Retirada'` o `'Certificado de Registro'`.
- Los datos de 2012, 2011 y 2010 están distribuidos en varios archivos .xls, uno por provincia. Se utilizó la hoja 4 de estos archivos y todos se fusionaron en un único conjunto de datos.
- Los datos de 2002-2009 se extrajeron de los archivos de 2010, ya que la hoja 1 contiene una evolución histórica detallada. Se fusionaron en un único conjunto.
- Los datos de 2001 se extrajeron de la hoja 8 de su archivo .xls correspondiente.
- Los datos de 1997-2000 se extrajeron de la hoja 10 de sus archivos .xls correspondientes.
- Los datos de 1996 se extrajeron de la hoja 1 de su archivo .xls correspondiente.
- Todos los conjuntos de datos anteriores se fusionaron en uno solo.
- Los valores "-" se reemplazaron por 0.
- Todas las nacionalidades categorizadas como otros ('otros américa', 'otros asia', ...) se unificaron en una única categoría 'Otros'.
- Se eliminaron todas las entradas con datos agregados para `provincia_id`.
- Se eliminaron todas las entradas con datos agregados para `country_id`.
- Se eliminaron todas las entradas con datos agregados para `tipo_documentacion`.
- Se eliminaron todas las entradas con datos agregados para `es_nacido_espania`.
- Se eliminaron todas las entradas con datos agregados para `grupo_edad`.
- Se eliminaron todas las entradas con datos agregados para `regimen`.

## Fuente

Datos extraídos del <a href="https://expinterweb.inclusion.gob.es/dynPx/inebase/index.htm?type=pcaxis&path=/Stock/&file=pcaxis" target="_blank">Observatorio Permanente de la Inmigración (OPI)</a>.
