# geo.municipios

Todos los municipios de España. Las claves primarias no se autogeneran; su código único se obtiene concatenando el código de municipio proporcionado por el INE con el código de provincia también dado por el INE (CPRO+CMUN).

**Nota**: esta tabla también contiene municipios históricos que ya no existen.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| municipio_id | int | NO | primary key |
| nombre | varchar | NO | nombre |
| provincia_id | int | NO | referencia a geo.provincias |

## Definición de la tabla

```sql
CREATE TABLE
  geo.municipios (
    municipio_id int PRIMARY KEY,
    nombre varchar NOT NULL,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)
  );
```

## Fuente

Datos extraídos del <a href="https://www.ine.es/dyngs/INEbase/en/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990" target="_blank">Instituto Nacional de Estadística (INE)</a>
