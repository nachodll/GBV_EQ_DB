# demografia.matrimonios_homosexuales

Número de matrimonios entre personas del mismo sexo en España, desagregados por provincia, grupo de edad de los cónyuges y composición de sexo (hombres o mujeres).

- **Periodo temporal**: 2005-2023, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| matrimonios_homosexuales_id | serial | NO | primary key |
| anio | int | NO | año |
| provincia_id | int | YES | referencia a geo.provincias |
| conyuge_1_grupo_edad | varchar | NO | grupo de edad del cónyuge 1 |
| conyuge_2_grupo_edad | varchar | NO | grupo de edad del cónyuge 2 |
| matrimonios_hombres | int | NO | matrimonios entre hombres |
| matrimonios_mujeres | int | NO | matrimonios entre mujeres |
| es_residente_espania | boolean | NO | residente en España |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.matrimonios_homosexuales (
    matrimonios_homosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    conyuge_1_grupo_edad varchar NOT NULL CHECK (
      conyuge_1_grupo_edad ~ '^\\d+-\\d+$'
      OR conyuge_1_grupo_edad ~ '^<\\d+$'
      OR conyuge_1_grupo_edad ~ '^>\\d+$'
    ),
    conyuge_2_grupo_edad varchar NOT NULL CHECK (
      conyuge_2_grupo_edad ~ '^\\d+-\\d+$'
      OR conyuge_2_grupo_edad ~ '^<\\d+$'
      OR conyuge_2_grupo_edad ~ '^>\\d+$'
    ),
    matrimonios_hombres int NOT NULL CHECK (matrimonios_hombres >= 0),
    matrimonios_mujeres int NOT NULL CHECK (matrimonios_mujeres >= 0),
    es_residente_espania boolean NOT NULL
  );
```

## Transformaciones notables

- Se fusionaron las tablas de matrimonios entre hombres y entre mujeres.
- `es_residente_espania` se derivó a partir de `provincia_id`.
- Se reemplazaron los valores faltantes en `matrimonios_hombres` y `matrimonios_mujeres` por 0.
- Se elimnaron las filas con valores agregados para los campos `conyuge_1_grupo_edad`, `conyuge_2_grupo_edad` y `provincia_id`.

## Fuente

Datos de matrimonios entre hombres extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=9113&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>

Datos de matrimonios entre mujeres extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=9114&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>