# tecnologia_y_medios.usuarios_redes_sociales

Número de usuarios activos en diferentes redes sociales para las principales ciudades españolas.

- **Periodo temporal**: 2014-2022, anual
- **Desagregación regional**: principales ciudades

A continuación se muestra la lista de los años en los que se analizó cada una de las redes sociales.

- Facebook: 2014-2022
- Twitter: 2014-2022
- Instagram: 2016-2022

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| usuarios_redes_sociales_id | serial | NO | primary key |
| anio | int | NO | año |
| ciudad | text | NO | ciudad |
| red_social | text | NO | red social |
| usuarios | int | NO | número de usuarios |

## Definición de la tabla

```sql
CREATE TABLE
  tecnologia_y_medios.usuarios_redes_sociales (
    usuarios_redes_sociales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ciudad text NOT NULL CHECK (ciudad ~ '^[A-Za-zÀ-ÿ\\s]+$'),
    red_social text NOT NULL CHECK (
      red_social IN (
        'Facebook',
        'Instagram',
        'Twitter',
        'TikTok',
        'LinkedIn',
        'YouTube'
      )
    ),
    usuarios int NOT NULL CHECK (usuarios >= 0)
  );
```

## Transformaciones notables
Las diferentes tablas fueron extraídas de los informes anuale en PDF  y combinadas en un solo conjunto de datos.

## Fuente
Datos extraídos de los informes de <a href="hhttps://thesocialmediafamily.com/" target="_blank">Social Media Family</a>.
Consultado el 17 de junio de 2025.
