# violencia_genero.infracciones_penales_inputadas_vg

Número de infracciones penales imputadas en casos de violencia de género. Resultados referidos a asuntos (con medidas cautelares dictadas) inscritos en el Registro a lo largo del periodo de referencia

- **Periodo temporal**: 2011-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| infracciones_penales_inputadas_vg_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| tipo_infraccion | text | NO | tipo de infracción |
| infracciones_penales_inputadas | int | NO | número de infracciones imputadas |

## Definición de la tabla

```sql
CREATE TABLE
  violencia_genero.infracciones_penales_inputadas_vg (
    infracciones_penales_inputadas_vg_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_infraccion text NOT NULL CHECK (
      tipo_infraccion IN (
        'Delitos',
        'Homicidio y sus formas',
        'Lesiones',
        'Detenciones ilegales y secuestro',
        'Amenazas',
        'Coacciones',
        'Torturas e integridad moral',
        'Agresiones sexuales',
        'Abusos sexuales',
        'Abusos y agresiones sexuales a menores de 16 años',
        'Allanamiento de morada',
        'Injurias',
        'Daños',
        'Quebrantamiento de condena',
        'Otros delitos sin especificar',
        'Faltas',
        'Faltas contra las personas',
        'Otras faltas sin especificar'
      )
    ),
    infracciones_penales_inputadas int NOT NULL CHECK (infracciones_penales_inputadas >= 0)
  );
```

## Transformaciones notables

- Se eliminaron las entradas con valores faltantes para `infracciones_penales_inputadas`.
- Se eliminaron las entradas con datos agregados para `comunidad_autonoma_id` y `tipo_infraccion`.

## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28294&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.

Consultado el 2 de junio de 2025.
