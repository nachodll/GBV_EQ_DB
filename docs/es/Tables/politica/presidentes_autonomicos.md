# politica.presidentes_autonomicos

Listado de los presidentes de las comunidades autónomas, con su legislatura, fecha de nombramiento y afiliación partidista.

- **Periodo temporal**: 1980-2025
- **Desagregación regional**: Comunidades

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| presidentes_autonomicos_id | serial | NO | Clave primaria |
| comunidad_autonoma_id | int | NO | Referencia a `geo.comunidades_autonomas` |
| legislatura | varchar | NO | Legislatura |
| presidente | varchar | NO | Nombre del presidente autonómico |
| nombramiento | date | NO | Fecha de nombramiento |
| partido | text | NO | Partido del presidente |

## Definición de la tabla

```sql
CREATE TABLE
  politica.presidentes_autonomicos (
    presidentes_autonomicos_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    partido text NOT NULL
  );
```

## Transformaciones destacadas

- **Los partidos políticos no están normalizados. Los nombres de los partidos se mantienen tal y como los facilita el Senado de España, por lo que no deben usarse para análisis que requieran identificadores armonizados.**

## Fuente

Datos extraídos del <a href="https://www.senado.es/web/conocersenado/biblioteca/dossieresareastematicas/detalledossier/index.html?lang=es_ES&id=DOSSIER_CCAA1&parte=CCAA1_PLANES" target="_blank">Senado de España</a>.
Consultado el 2 de junio de 2025.
