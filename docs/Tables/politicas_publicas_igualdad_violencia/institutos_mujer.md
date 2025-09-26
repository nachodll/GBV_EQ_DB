# politicas_publicas_igualdad_violencia.institutos_mujer

Directory of regional women's institutes and equality bodies in the Spanish autonomous communities. The autonomous communities not listed do not have an autonomous women's institute.

- **Time period**: 1983-2025
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| institutos_mujer_id | serial | NO | primary key |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| nombre | text | NO | official name of the institute |
| anio_fundacion | int | YES | foundation year |
| enlace | text | YES | official website or reference URL |

## Table definition

```sql
CREATE TABLE
  politicas_publicas_igualdad_violencia.institutos_mujer (
    institutos_mujer_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    anio_fundacion int CHECK (
      anio_fundacion BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    enlace text
  );
```

## Notable transformations

- Manual compilation of organisational details from the Instituto de las Mujeres directory, standardising names and regional identifiers.

## Source

Data gathered from the <a href="https://www.inmujeres.gob.es/servRecursos/OrganismosIgualdad/AmbitoEstatal/AmbitoEstatal.htm" target="_blank">Instituto de las Mujeres</a>.
