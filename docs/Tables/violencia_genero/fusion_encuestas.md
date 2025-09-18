# violencia_genero.fusion_encuestas

Binary indicators derived from the 2015 and 2019 "Macroencuesta de Violencia contra la Mujer" surveys conducted by the Centro de Investigaciones Sociológicas (CIS). Each row represents a respondent and summarises whether different forms of sexual or physical violence were reported, together with survey metadata and the province identifier.

- **Time period**: 2015, 2019
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| fusion_encuestas_id | serial | NO | primary key |
| provincia_id | int | NO | references geo.provincias |
| codigo_estudio | int | NO | CIS study code that identifies the survey wave |
| anio | int | NO | year recorded for the survey fieldwork |
| mes | int | NO | month of the fieldwork (numeric month) |
| violencia_sexual_1_pareja | boolean | NO | has any partner ever forced her to have sex when she did not want to |
| violencia_sexual_1_fuera_pareja | boolean | NO | has any person (non partner) ever forced her to have sex when she did not want to |
| violencia_sexual_2_pareja | boolean | NO | has any partner ever made her have sex when she was unable to refuse because she was under the influence of alcohol or drugs  |
| violencia_sexual_3_pareja | boolean | NO | has any partner ever forced her to perform any other sexual practice not yet mentioned |
| violencia_fisica_1_pareja | boolean | NO | has any partner ever slapped her or thrown her something that could hurt |
| violencia_fisica_2_pareja | boolean | NO | has any partner ever pushed, grabbed or pulled her hair |
| violencia_fisica_2_fuera_pareja | boolean | NO | has any person (non partner) ever pushed, grabbed or pulled her hair |
| violencia_fisica_3_pareja | boolean | NO | has any partner ever hit her with their fist or something else that could hurt her |
| violencia_fisica_4_pareja | boolean | NO | has any partner ever kicked, dragged or beaten her |
| violencia_fisica_5_pareja | boolean | NO | has any partner ever tried to suffocate or burn her on purpose |
| violencia_fisica_5_fuera_pareja | boolean | NO | has any person (non partner) ever tried to suffocate or burn her on purpose |
| violencia_fisica_6_pareja | boolean | NO | has any partner ever threatened to use or has used a gun, knife or other weapon or dangerous substance against her |
| violencia_fisica_6_fuera_pareja | boolean | NO | has any person (non partner) ever threatened to use or has used a gun, knife or other weapon or dangerous substance against her |

## Table definition

```sql
CREATE TABLE
  violencia_genero.fusion_encuestas (
    fusion_encuestas_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    codigo_estudio int NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    violencia_sexual_1_pareja boolean NOT NULL,
    violencia_sexual_1_fuera_pareja boolean NOT NULL,
    violencia_sexual_2_pareja boolean NOT NULL,
    violencia_sexual_3_pareja boolean NOT NULL,
    violencia_fisica_1_pareja boolean NOT NULL,
    violencia_fisica_2_pareja boolean NOT NULL,
    violencia_fisica_2_fuera_pareja boolean NOT NULL,
    violencia_fisica_3_pareja boolean NOT NULL,
    violencia_fisica_4_pareja boolean NOT NULL,
    violencia_fisica_5_pareja boolean NOT NULL,
    violencia_fisica_5_fuera_pareja boolean NOT NULL,
    violencia_fisica_6_pareja boolean NOT NULL,
    violencia_fisica_6_fuera_pareja boolean NOT NULL
  );
```

## Notable transformations

- The 2015 (study 3027) and 2019 (study 3235) SAV files are read with `pyreadstat`, selecting the province identifier and questions related to physical and sexual violence.
- Metadata columns (`codigo_estudio`, `anio`, `mes`) are added manually to record the CIS study number and fieldwork date for each wave; the 2015 wave corresponds to fieldwork performed in September 2014.
- `violencia_sexual_1_pareja`
      1. 2019: answered affirmatively to M1P5_0_4 or M2P5_0_4.
      2. 2015: answered affirmatively to P2201 or P3101.
- `violencia_sexual_1_fuera_pareja`
      1. 2019: answered affirmatively to M3P2_4.
      2. 2015: answered affirmatively to P52.
- `violencia_sexual_2_pareja`
      1. 2019: answered affirmatively to M1P5_0_2 or M2P5_0_2.
      2. 2015: answered affirmatively to P2202 or P3102.
- `violencia_sexual_3_pareja`
      1. 2019: answered affirmatively to M1P5_0_8 or M2P5_0_8.
      2. 2015: answered affirmatively to P2203 or P3103.
- `violencia_fisica_1_pareja`
      1. 2019: answered affirmatively to M1P4_0_1 or M2P4_0_1.
      2. 2015: answered affirmatively to P2101 or P3001.
- `violencia_fisica_2_pareja`
      1. 2019: answered affirmatively to M1P4_0_2 or M2P4_0_2.
      2. 2015: answered affirmatively to P2102 or P3002.
- `violencia_fisica_2_fuera_pareja`
      1. 2019: answered affirmatively to M3P1_2.
      2. 2015: answered affirmatively to P4803.
- `violencia_fisica_3_pareja`
      1. 2019: answered affirmatively to M1P4_0_3 or M2P4_0_3.
      2. 2015: answered affirmatively to P2103 or P3003.
- `violencia_fisica_4_pareja`
      1. 2019: answered affirmatively to M1P4_0_4 or M2P4_0_4.
      2. 2015: answered affirmatively to P2104 or P3004.
- `violencia_fisica_5_pareja`
      1. 2019: answered affirmatively to M1P4_0_5 or M2P4_0_5.
      2. 2015: answered affirmatively to P2105 or P3005.
- `violencia_fisica_5_fuera_pareja`
      1. 2019: answered affirmatively to M3P1_5.
      2. 2015: answered affirmatively to P4804.
- `violencia_fisica_6_pareja`
      1. 2019: answered affirmatively to M1P4_0_6 or M2P4_0_6.
      2. 2015: answered affirmatively to P2106 or P3006.
- `violencia_fisica_6_fuera_pareja`
      1. 2019: answered affirmatively to M3P1_6.
      2. 2015: answered affirmatively to P4805.


## Source
Data extracted from the <a href="https://www.cis.es/" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Macroencuesta de Violencia contra la Mujer 2015 (study 3027) and 2019 (study 3235).
