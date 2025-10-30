# politicas_publicas_igualdad_violencia.centros_acogida_emergencia

Centros de acogida de emergencia para mujeres supervivientes de violencia de género y sus personas dependientes, desagregados por provincia. El conjunto de datos recoge los recursos disponibles, la capacidad, el personal profesional y el número de mujeres e hijos e hijas atendidos en la red de acogida urgente. 

- **Periodo temporal**: 2017, 2020, 2022
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| centros_acogida_emergencia_id | serial | NO | clave primaria |
| anio | int | NO | año de referencia |
| provincia_id | int | NO | referencia a geo.provincias |
| centros | int | SÍ | número de centros de acogida de emergencia |
| plazas | int | SÍ | plazas disponibles en los centros de emergencia |
| profesionales | int | SÍ | personal profesional que trabaja en los centros |
| mujeres_acogidas | int | SÍ | mujeres (mayores o menores de 18) acogidas durante el año |
| hijos_a_cargo_acogidos | int | SÍ | hijos menores o con discapacidad a cargo acogidos durante el año |

## Definición de la tabla

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

## Transformaciones notables

- La serie se limita a los tres años publicados por la Delegación General contra la Violencia de Género; la fuente proporciona valores nulos cuando no existe información.

## Fuente

Datos publicados por la <a href="https://violenciagenero.igualdad.gob.es/violenciaencifras/recursos-autonomicos/" target="_blank">Delegación General contra la Violencia de Género (DGVG)</a>. Consultado a 28 de octubre de 2025.
