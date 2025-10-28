# geo.comunidades_autonomas

Todas las comunidades autónomas de España. Las claves primarias no se autogeneran, ya que tienen un código único asignado por el INE (CODAUTO). Se utiliza la clave especial 0 para los totales nacionales.

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| comunidad_autonoma_id | int | NO | primary key |
| nombre | varchar | NO | único |

## Definición de la tabla

```sql
CREATE TABLE
  geo.comunidades_autonomas (
    comunidad_autonoma_id int PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );
```

## Fuente

Datos extraídos del <a href="https://www.ine.es/daco/daco42/codmun/cod_ccaa.htm" target="_blank">Instituto Nacional de Estadística (INE)</a>
Consultado el 2 de junio de 2025.
