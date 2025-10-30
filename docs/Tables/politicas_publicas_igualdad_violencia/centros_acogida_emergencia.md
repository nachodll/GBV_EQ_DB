# politicas_publicas_igualdad_violencia.centros_acogida_emergencia

Emergency accommodation centres for women survivors of gender-based violence and their dependants, disaggregated by Spanish province. The dataset records available facilities, capacity, professional staff, and the number of women and children housed in the network of emergency shelters.

- **Time period**: 2017, 2020, 2022
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| centros_acogida_emergencia_id | serial | NO | primary key |
| anio | int | NO | reference year |
| provincia_id | int | NO | references geo.provincias |
| centros | int | YES | number of emergency accommodation centres |
| plazas | int | YES | available places in emergency centres |
| profesionales | int | YES | professional staff working in the centres |
| mujeres_acogidas | int | YES | women (over or under 18) accommodated during the year |
| hijos_a_cargo_acogidos | int | YES | accompanying children accommodated during the year |

## Table definition

```sql
CREATE TABLE
  politicas_publicas_igualdad_violencia.centros_acogida_emergencia (
    centros_acogida_emergencia_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    centros int CHECK (centros >= 0),
    plazas int CHECK (plazas >= 0),
    profesionales int CHECK (profesionales >= 0),
    mujeres_acogidas int CHECK (mujeres_acogidas >= 0),
    hijos_a_cargo_acogidos int CHECK (hijos_a_cargo_acogidos >= 0)
  );
```

## Notable transformations

- Limited the series to the three publication years currently released by the Delegación General contra la Violencia de Género; the source does provide null values for absent data points.

## Source

Data published by the <a href="https://violenciagenero.igualdad.gob.es/violenciaencifras/recursos-autonomicos/" target="_blank">Delegación General contra la Violencia de Género (DGVG)</a>.  Consulted on 28 October 2025.