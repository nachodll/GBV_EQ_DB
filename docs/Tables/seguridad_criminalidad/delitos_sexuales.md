# seguridad_criminalidad.delitos_sexuales

Sexual offence counts recorded by the Ministry of the Interior and published by INE, broken down by Penal Code classification and sex.

- **Time period**: 2017-2024, annual
- **Regional breakdown**: Spain (national total)

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| delitos_sexuales_id | serial | NO | primary key |
| sexo | enums.sexo_enum | NO | sex of recorded victims/offenders aggregate (Hombre, Mujer, Total) |
| anio | int | NO | year |
| nivel_2 | text | NO | Penal Code level 2 category (always "8 Contra la libertad e indemnidad sexuales") |
| nivel_3 | text | YES | Penal Code level 3 category |
| nivel_4 | text | YES | Penal Code level 4 category |
| delitos | int | NO | number of recorded offences |

## Table definition

```sql
CREATE TABLE
  seguridad_criminalidad.delitos_sexuales (
    delitos_sexuales_id serial PRIMARY KEY,
    sexo enums.sexo_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    nivel_2 text NOT NULL CHECK (
      nivel_2 IN ('8 Contra la libertad e indemnidad sexuales')
    ),
    nivel_3 text CHECK (
      nivel_3 IN (
        '8.1 Agresiones sexuales',
        '8.2 Abusos sexuales',
        '8.2 BIS Abusos y agresiones sexuales a menores de 16 años',
        '8.3 Acoso sexual',
        '8.4 Exhibicionismo y provocación sexual',
        '8.5 Prostitución y corrupción menores'
      )
    ),
    nivel_4 text CHECK (
      nivel_4 IN ('8.1.1 Agresión sexual', '8.1.2 Violación')
    ),
    delitos int NOT NULL CHECK (delitos >= 0)
  );
```

## Notable transformations
- Dropped records without total offences.

## Source
Data extracted from <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28750" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consulted on 23 October 2025.
