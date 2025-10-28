# violencia_genero.fusion_encuestas

Indicadores binarios derivados de las encuestas de 2015 y 2019 de la "Macroencuesta de Violencia contra la Mujer" realizadas por el Centro de Investigaciones Sociológicas (CIS). Cada fila representa a una persona encuestada y resume si declaró distintos tipos de violencia sexual o física, junto con la metainformación de la encuesta y el identificador de provincia.

- **Periodo temporal**: 2015, 2019
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| fusion_encuestas_id | serial | NO | clave primaria |
| provincia_id | int | NO | referencia a geo.provincias |
| codigo_estudio | int | NO | código de estudio del CIS que identifica la encuesta |
| anio | int | NO | año registrado para el trabajo de campo |
| mes | int | NO | mes del trabajo de campo (valor numérico) |
| violencia_sexual_1_pareja | boolean | NO | alguna pareja alguna vez le ha obligado a mantener relaciones sexuales cuando no quería |
| violencia_sexual_1_fuera_pareja | boolean | NO | alguna persona (no pareja) alguna vez le ha obligado a mantener relaciones sexuales cuando no quería |
| violencia_sexual_2_pareja | boolean | NO | alguna pareja alguna vez le ha hecho mantener relaciones sexuales cuando era incapaz de rechazarlas debido a que estaba bajo la influencia del alcohol o las drogas |
| violencia_sexual_3_pareja | boolean | NO | alguna pareja alguna vez le ha obligado a realizar alguna otra práctica de tipo sexual que no se le haya mencionado ya |
| violencia_fisica_1_pareja | boolean | NO | alguna pareja alguna vez le ha abofeteado o tirado algo que pudiese hacerle daño |
| violencia_fisica_2_pareja | boolean | NO | alguna pareja alguna vez le ha empujado, agarrado o tirado del pelo |
| violencia_fisica_2_fuera_pareja | boolean | NO | alguna persona (no pareja) alguna vez le ha empujado, agarrado o tirado del pelo |
| violencia_fisica_3_pareja | boolean | NO | alguna pareja alguna vez le ha golpeado con su puño o con alguna otra cosa que pudiese hacerle daño |
| violencia_fisica_4_pareja | boolean | NO | alguna pareja alguna vez le ha dado patadas, arrastrado o pegado una paliza |
| violencia_fisica_5_pareja | boolean | NO | alguna pareja alguna vez le ha intentado asfixiar o quemar a propósito |
| violencia_fisica_5_fuera_pareja | boolean | NO | alguna persona (no pareja) alguna vez le ha intentado asfixiar o quemar a propósito |
| violencia_fisica_6_pareja | boolean | NO | alguna pareja alguna vez le ha amenazado con usar o ha usado una pistola, cuchillo u otra arma o substancia peligrosa contra ella |
| violencia_fisica_6_fuera_pareja | boolean | NO | alguna persona (no pareja) alguna vez le ha amenazado con usar o ha usado una pistola, cuchillo u otra arma o substancia peligrosa contra ella |

## Definición de la tabla

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

## Transformaciones notables

- Los ficheros SAV de 2015 (estudio 3027) y 2019 (estudio 3235) se leen con `pyreadstat`, seleccionando el identificador de provincia y las preguntas relativas a violencia física y sexual.
- Se añaden manualmente las columnas de metadatos (`codigo_estudio`, `anio`, `mes`) para registrar el número de estudio del CIS y la fecha de trabajo de campo de cada estudio; el estudio de 2015 corresponde al trabajo de campo realizado en septiembre de 2014.
- `violencia_sexual_1_pareja`
      1. 2019: se respondió 'Sí' en M1P5_0_4 o M2P5_0_4.
      2. 2015: se respondió 'Sí' en P2201 o P3101.
- `violencia_sexual_1_fuera_pareja`
      1. 2019: se respondió 'Sí' en M3P2_4.
      2. 2015: se respondió 'Sí' en P52.
- `violencia_sexual_2_pareja`
      1. 2019: se respondió 'Sí' en M1P5_0_2 o M2P5_0_2.
      2. 2015: se respondió 'Sí' en P2202 o P3102.
- `violencia_sexual_3_pareja`
      1. 2019: se respondió 'Sí' en M1P5_0_8 o M2P5_0_8.
      2. 2015: se respondió 'Sí' en P2203 o P3103.
- `violencia_fisica_1_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_1 o M2P4_0_1.
      2. 2015: se respondió 'Sí' en P2101 o P3001.
- `violencia_fisica_2_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_2 o M2P4_0_2.
      2. 2015: se respondió 'Sí' en P2102 o P3002.
- `violencia_fisica_2_fuera_pareja`
      1. 2019: se respondió 'Sí' en M3P1_2.
      2. 2015: se respondió 'Sí' en P4803.
- `violencia_fisica_3_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_3 o M2P4_0_3.
      2. 2015: se respondió 'Sí' en P2103 o P3003.
- `violencia_fisica_4_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_4 o M2P4_0_4.
      2. 2015: se respondió 'Sí' en P2104 o P3004.
- `violencia_fisica_5_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_5 o M2P4_0_5.
      2. 2015: se respondió 'Sí' en P2105 o P3005.
- `violencia_fisica_5_fuera_pareja`
      1. 2019: se respondió 'Sí' en M3P1_5.
      2. 2015: se respondió 'Sí' en P4804.
- `violencia_fisica_6_pareja`
      1. 2019: se respondió 'Sí' en M1P4_0_6 o M2P4_0_6.
      2. 2015: se respondió 'Sí' en P2106 o P3006.
- `violencia_fisica_6_fuera_pareja`
      1. 2019: se respondió 'Sí' en M3P1_6.
      2. 2015: se respondió 'Sí' en P4805.

## Fuente
Datos extraídos del <a href="https://www.cis.es/" target="_blank">Centro de Investigaciones Sociológicas (CIS)</a>. Macroencuesta de Violencia contra la Mujer 2015 (estudio 3027) y 2019 (estudio 3235).
Consultado el 17 de junio de 2025.
