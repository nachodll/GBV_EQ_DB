# violencia_genero.denuncias_vg_presentadas

Número de denuncias por violencia de género presentadas.

- **Periodo temporal**: 2007-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| denuncias_vg_presentadas_id | serial | NO | primary key |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| anio | int | NO | año |
| denuncias_presentadas | int | NO | número de denuncias presentadas |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://www.inmujeres.gob.es/MujerCifras/Violencia/AmbitoJudicial.htm" target="_blank">Instituto de las Mujeres</a>. Tabla: "Denuncias por violencia de género según Comunidad Autónoma".
