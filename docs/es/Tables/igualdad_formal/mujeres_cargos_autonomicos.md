# igualdad_formal.mujeres_cargos_autonomicos

Número de escaños en los parlamentos autonómicos según sexo para las comunidades autónomas españolas.

- **Periodo temporal**: 1996-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| mujeres_cargos_autonomicos_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sexo |
| numero_cargos | int | NO | número de escaños |

## Definición de la tabla

```sql
CREATE TABLE
  igualdad_formal.mujeres_cargos_autonomicos (
    mujeres_cargos_autonomicos_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    numero_cargos int NOT NULL CHECK (numero_cargos >= 0)
  );
```

## Transformaciones notables

- Los datos fueron leídos del fichero excel y transformados y pivotados a una estructura tabular estandar.

## Fuente

Datos extraídos de <a href="https://www.inmujeres.gob.es/MujerCifras/PoderDecisiones/PoderLegislativo.htm" target="_blank">Mujeres en Cifras - Instituto de las Mujeres</a>.
