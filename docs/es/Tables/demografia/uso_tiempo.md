# demografia.uso_tiempo

Tiempo promedio por día, en horas y minutos, dedicado a los principales grupos de actividad, desagregado por sexo y comunidad autónoma. Datos de la Encuesta de Empleo del Tiempo 2009-2010 y la Encuesta de Empleo del Tiempo 2002-2003, ambas realizadas por el INE.

- **Periodo temporal**: 2002-2003 y 2009-2010
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| uso_tiempo_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| sexo | enums.sexo_enum | NO | sexo |
| actividad | varchar | NO | actividad |
| horas | int | NO | horas |
| minutos | int | NO | minutos |

## Definición de la tabla

```sql
CREATE TABLE
  demografia.uso_tiempo (
    uso_tiempo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    actividad varchar NOT NULL CHECK (
      actividad IN (
        '0 Cuidados personales',
        '1 Trabajo remunerado',
        '2 Estudios',
        '3 Hogar y familia',
        '4 Trabajo voluntario y reuniones',
        '5 Vida social y diversión',
        '6 Deportes y actividades al aire libre',
        '7 Aficiones e informática',
        '8 Medios de comunicación',
        '9 Trayectos y empleo del tiempo no especificado'
      )
    ),
    horas int NOT NULL CHECK (
      horas >= 0
      AND horas <= 24
    ),
    minutos int NOT NULL CHECK (
      minutos >= 0
      AND minutos < 60
    )
  );
```

## Transformaciones notables

- Se pivotó la fuente de 2009 para separar las columnas de horas y minutos.
- Se convirtieron las hojas de Excel de 2002 al mismo formato que los datos de 2009.
- Se eliminaron filas con totales nacionales y entradas para ambos sexos.
- Se estandarizaron los identificadores de comunidad y las etiquetas de sexo.

## Fuente

Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?path=/t25/e447/a2009-2010/p07/l0/&file=7.3a.px&L=0" target="_blank">Instituto Nacional de Estadística (INE) - encuesta 2009</a> y del <a href="https://www.ine.es/daco/daco42/empleo/dacoeet.htm" target="_blank">Instituto Nacional de Estadística (INE) - encuesta 2002</a>
Consultado el 2 de junio de 2025.
