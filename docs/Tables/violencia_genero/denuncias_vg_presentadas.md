# violencia_genero.denuncias_vg_presentadas

Number of gender-based violence reports filed.

- **Time period**: 2007-2024, annual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| denuncias_vg_presentadas_id | serial | NO | primary key |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| anio | int | NO | year |
| denuncias_presentadas | int | NO | number of reports filed |

## Table definition

```sql
CREATE TABLE
  violencia_genero.denuncias_vg_presentadas (
    denuncias_vg_presentadas_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    denuncias_presentadas int NOT NULL CHECK (denuncias_presentadas >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset.

## Source
Data extracted from <a href="https://www.inmujeres.gob.es/MujerCifras/Violencia/AmbitoJudicial.htm" target="_blank">Instituto de las Mujeres</a>. Table: "Denuncias por violencia de género según Comunidad Autónoma".
Consulted on 9 June 2025.
