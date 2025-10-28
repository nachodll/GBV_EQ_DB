# geo.provincias

Todas las provincias de España. Las claves primarias no se autogeneran, ya que tienen un código único asignado por el INE (CPRO).

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| provincia_id | int | NO | primary key |
| nombre | varchar | NO | único |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |

## Definición de la tabla

```sql
CREATE TABLE
  geo.provincias (
    provincia_id int PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)
  );
```

## Fuente

Datos extraídos del <a href="https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consultado el 3 de junio de 2025.
