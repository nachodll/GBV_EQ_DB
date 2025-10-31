# politica.presidentes_espania

Listado de los presidentes del Gobierno de España, con las fechas de mandato, los partidos que integran el ejecutivo y el tipo de mayoría parlamentaria.

- **Periodo temporal**: 1979-2023
- **Desagregación regional**: España

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| presidentes_espania_id | serial | NO | Clave primaria |
| legislatura | varchar | NO | Legislatura en números romanos |
| presidente | varchar | NO | Nombre del presidente |
| nombramiento | date | NO | Fecha de investidura |
| cese | date | SÍ | Fecha de cese |
| partidos_gobierno | text | NO | Partidos que forman el gobierno |
| tipo_mayoria | text | NO | Tipo de mayoría parlamentaria |

## Definición de la tabla

```sql
CREATE TABLE
  politica.presidentes_espania (
    presidentes_espania_id serial PRIMARY KEY,
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    cese date CHECK (
      cese <= CURRENT_DATE
      AND cese >= nombramiento
    ),
    partidos_gobierno text NOT NULL,
    tipo_mayoria text NOT NULL CHECK (
      tipo_mayoria IN ('Absoluta', 'Simple', 'Minoría', 'En funciones')
    )
  );
```

## Transformaciones destacadas

- Los tipos de mayoría se homogeneizan a un vocabulario controlado (Absoluta, Simple, Minoría, En funciones).
- El valor NULL en el campo `cese` indica que el presidente sigue en el cargo.
- **Los partidos políticos no están normalizados entre tablas. Los nombres de los partidos de gobierno se mantienen tal y como los publica La Moncloa, por lo que no deben usarse para análisis que requieran identificadores armonizados.**

## Fuente

Datos extraídos de <a href="https://www.lamoncloa.gob.es/Paginas/index.aspx" target="_blank">La Moncloa</a>.
Consultado el 17 de junio de 2025.
