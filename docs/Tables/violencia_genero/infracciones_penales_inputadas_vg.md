# violencia_genero.infracciones_penales_inputadas_vg

Number of charged criminal offences in gender-based violence cases. Results related to matters (with precautionary measures issued) registered in the Registry throughout the reference period.

- **Time period**: 2011-2024, annual
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| infracciones_penales_inputadas_vg_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| tipo_infraccion | text | NO | offence type |
| infracciones_penales_inputadas | int | NO | number of charged offences |

## Table definition

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

## Notable transformations

- Dropped rows with missing values for `infracciones_penales_inputadas`.
- Dropped rows with aggregated data for `comunidad_autonoma_id` and `tipo_infraccion`.

## Source
Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28294&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.

Consulted on 2 June 2025.
