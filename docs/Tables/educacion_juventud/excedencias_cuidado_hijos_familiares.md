# educacion_juventud.excedencias_cuidado_hijos_familiares

Number of unpaid leave requests for child or family care, disaggregated by sex and reason for the leave.

- **Time period**: 2007-2023, annual
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| excedencias_cuidado_hijos_familiares_id | serial | NO | primary key |
| anio | int | NO | year |
| sexo | enums.sexo_enum | NO | sex (`Hombre`, `Mujer`, `Total`) |
| motivo | text | NO | leave reason (`Cuidado de hijos`, `Cuidado de familiares`) |
| provincia_id | int | NO | references geo.provincias |
| excedencias | int | YES | number of approved unpaid leaves |

## Table definition

```sql
CREATE TABLE
  educacion_juventud.excedencias_cuidado_hijos_familiares (
    excedencias_cuidado_hijos_familiares_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    motivo text NOT NULL CHECK (
      motivo IN ('Cuidado de hijos', 'Cuidado de familiares')
    ),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    excedencias int CHECK (excedencias >= 0)
  );
```

## Notable transformations

- Consolidated annual spreadsheets with changing layouts into a single long-form table.
- Removed regional aggregate rows and harmonised province labels before normalisation.
- Normalised sex categories and leave reasons to shared enums and dictionaries, and coerced missing or placeholder values to nulls.

## Source

Statistics Yearbooks of the Ministry of Labor and Social Economy (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
Consulted on 11 June 2025.
