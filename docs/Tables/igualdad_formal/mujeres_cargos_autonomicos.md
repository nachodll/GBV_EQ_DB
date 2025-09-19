# igualdad_formal.mujeres_cargos_autonomicos

Number of seats held in regional parliaments by sex across Spanish autonomous communities.

- **Time period**: 1996-2024, annually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| mujeres_cargos_autonomicos_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sex |
| numero_cargos | int | NO | number of seats |

## Table definition

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

## Notable transformations

- Read the Excel source, isolating the three sex-specific blocks and converting them into a common tabular structure.

## Source

Data extracted from <a href="https://www.inmujeres.gob.es/MujerCifras/PoderDecisiones/PoderLegislativo.htm" target="_blank">Mujeres en Cifras - Instituto de las Mujeres</a>.
