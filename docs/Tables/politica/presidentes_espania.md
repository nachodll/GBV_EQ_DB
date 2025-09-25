# politica.presidentes_espania

List of the Presidents of the Government of Spain, including their mandate dates, coalition partners, and parliamentary majority type.

- **Time period**: 1979-2023
- **Regional breakdown**: Spain

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| presidentes_espania_id | serial | NO | Primary key |
| legislatura | varchar | NO | Legislative term in Roman numerals |
| presidente | varchar | NO | Name of the president |
| nombramiento | date | NO | Date of investiture |
| cese | date | YES | Date of leaving office |
| partidos_gobierno | text | NO | Parties forming the government |
| tipo_mayoria | text | NO | Type of parliamentary majority |

## Table definition

```sql
CREATE TABLE
  politica.presidentes_espania (
    presidentes_espania_id serial PRIMARY KEY,
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    cese date CHECK (
      cese <= CURRENT_DATE
      AND cese >= nombramiento
    ),
    partidos_gobierno text NOT NULL,
    tipo_mayoria text NOT NULL CHECK (
      tipo_mayoria IN ('Absoluta', 'Simple', 'Minoría', 'En funciones')
    )
  );
```

## Notable transformations

- Majority types are standardized to a controlled vocabulary (Absoluta, Simple, Minoría, En funciones).
- A NULL value for `cese` means the president remains in office.
- **Political parties are not normalized accross tables. Government party names stay as provided by La Moncloa, so they should not be used for analyses that require harmonized party identifiers.**

## Source

Data extracted from <a href="https://www.lamoncloa.gob.es/Paginas/index.aspx" target="_blank">La Moncloa</a>.
