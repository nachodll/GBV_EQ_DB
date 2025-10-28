# tecnologia_y_medios.uso_internet_personas

Porcentajes de personas según el tipo de uso de Internet.

- **Periodo temporal**: 2006-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| uso_internet_personas_id | serial | NO | primary key |
| anio | int | NO | año |
| porcentaje | numeric | NO | porcentaje |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| tipo_uso | text | NO | tipo de uso de Internet |

## Definición de la tabla

```sql
CREATE TABLE
  tecnologia_y_medios.uso_internet_personas (
    uso_internet_personas_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_uso text NOT NULL CHECK (
      tipo_uso IN (
        'Personas que han utilizado Internet en los últimos 3 meses',
        'Personas que han utilizado Internet diariamente (al menos 5 días a la semana)',
        'Personas que han comprado a través de Internet en los últimos 3 meses',
        'Personas que usan el teléfono móvil'
      )
    )
  );
```

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?tpx=70471&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consultado el 3 de junio de 2025.
