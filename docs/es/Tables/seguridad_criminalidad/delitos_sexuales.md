# seguridad_criminalidad.delitos_sexuales

Recuento de delitos contra la libertad e indemnidad sexual registrados por el Ministerio del Interior y publicados por el INE, desglosados por clasificación del Código Penal y sexo.

- **Periodo temporal**: 2017-2024, anual
- **Desagregación regional**: España (total nacional)

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| delitos_sexuales_id | serial | NO | primary key |
| sexo | enums.sexo_enum | NO | sexo del total registrado (Hombre, Mujer, Total) |
| anio | int | NO | año |
| nivel_2 | text | NO | categoría de nivel 2 del Código Penal (siempre "8 Contra la libertad e indemnidad sexuales") |
| nivel_3 | text | YES | categoría de nivel 3 del Código Penal |
| nivel_4 | text | YES | categoría de nivel 4 del Código Penal |
| delitos | int | NO | número de delitos registrados |

## Definición de la tabla

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

## Transformaciones notables
- Se descartaron registros sin número de delitos.

## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxiT3/Tabla.htm?t=28750" target="_blank">Instituto Nacional de Estadística (INE)</a>.
