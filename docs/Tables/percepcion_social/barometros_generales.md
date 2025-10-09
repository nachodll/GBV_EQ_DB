# percepcion_social.barometros_generales

Microdata from the CIS (Centro de Investigaciones Sociológicas) General Barometer surveys, harmonized to provide a consistent view of interview metadata and and the selected fixed variables of the barometers.

- **Time period**: 1979-2025, per survey interview
- **Regional breakdown**: Spain (national scope) with optional autonomous community and province identifiers

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| barometros_generales_id | serial | NO | Primary key |
| fecha | date | NO | Interview date inferred from the CIS study metadata |
| codigo_estudio | varchar(4) | NO | Four-digit CIS study code |
| cuestionario | int | YES | Questionnaire number within the study |
| comunidad_autonoma_id | int | YES | Foreign key to `geo.comunidades_autonomas` |
| provincia_id | int | YES | Foreign key to `geo.provincias` |
| edad | int | YES | Interviewee age |
| sexo | enums.sexo_enum | YES | Interviewee sex |
| ideologia | int | YES | Self-placement on the 1 (left) – 10 (right) ideological scale |
| religiosidad | varchar | YES | Harmonized religiosity category |
| problema_personal_1 | text | YES | First personally relevant problem reported |
| problema_personal_2 | text | YES | Second personally relevant problem reported |
| problema_personal_3 | text | YES | Third personally relevant problem reported |
| problema_espania_1 | text | YES | First most important problem in Spain |
| problema_espania_2 | text | YES | Second most important problem in Spain |
| problema_espania_3 | text | YES | Third most important problem in Spain |

## Table definition

```sql
CREATE TABLE
  percepcion_social.barometros_generales (
    barometros_generales_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    cuestionario int,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    edad int CHECK (edad BETWEEN 1 AND 150),
    sexo enums.sexo_enum,
    ideologia int CHECK (ideologia BETWEEN 1 AND 10),
    religiosidad varchar CHECK (
      religiosidad IN (
        'Ateo/a',
        'Agnóstico/a',
        'Indiferente, no creyente',
        'Católico/a',
        'Católico/a practicante',
        'Católico/a no practicante',
        'Creyente de otra religión'
      )
      OR religiosidad IS NULL
    ),
    problema_personal_1 text,
    problema_personal_2 text,
    problema_personal_3 text,
    problema_espania_1 text,
    problema_espania_2 text,
    problema_espania_3 text
  );
```

## Coverage and limitations

- As of 3 October 2025 the CIS website listed 501 General Barometer studies; 427 studies were ingested into the database. The remaining 74 were excluded because (a) 51 have no downloadable microdata, (b) 8 correspond to barometer mergers, (c) 14 lack `.sav` files (`MD1436`, `MD1444`, `MD2927`, `MD2932`, `MD2935`, `MD2941`, `MD2944`, `MD2948`, `MD2951`, `MD2954`, `MD2966`, `MD2972`, `MD3109`, `MD3347`), and (d) the `.sav` file for study `MD2023` is corrupted.
- Columns `religiosidad` and `ideologia` have been standardized across all studies to facilitate longitudinal analyses. However, it is important to consider that the wording of these questions in the original questionnaires has evolved over time, which may introduce subtle differences in interpretation. For example, in older surveys, the extremes of the ideological scale (0 and 10) were labeled "left" and "right," while in more recent studies they are described as "far left" and "far right," respectively. These changes in wording may influence responses and should be taken into account when interpreting temporal trends.
- Problem columns (`problema_*`) are not standardized across waves. Even after the value cleaning dictionary is applied, historical studies still use heterogeneous labels, so users must decide how to group or recode these categories for longitudinal analyses.

## Notable transformations

- <a href="https://github.com/nachodll/GBV_EQ_DB/blob/main/downloaders/CIS004_download.py"> Selenium automation</a> (CIS004_download.py) iterates through every CIS barometer page, records metadata, and stores provisional variable maps before downloading available ZIP archives.
- Variable mappings are first produced automatically by the CIS downloader and then patched during transformation to set consistent field names, account for missing mappings, and split multiple-answer questions into individual columns because the scraped JSON map is not fully reliable on its own.
- ZIP files are uncompressed and the directory structure is readjusted in case of nested directories.
- Target variables are extracted from each study and merged into a single dataframe. Variables are extracted only if they are part of the target variable set and there is a map for such study and such variable.
- During transformation the updated map enforces canonical variable names, fixes typos in territorial labels, normalizes questionnaire numbers, ages, sex, ideology, and religiosity, and maps textual problems through a curated dictionary before linking regions to the geographic dimension tables.

## Source

Data extracted from the <a href="https://www.cis.es/catalogo-estudios/resultados-definidos/barometros" target="_blank">Centro de Investigaciones Sociológicas (CIS) General Barometer portal</a>.
