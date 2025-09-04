# tecnologia_y_medios.usuarios_redes_sociales

Number of active users in different social networks among the top spanish cities.

- **Time period**: 2014-2022, anually
- **Regional breakdown**: top bigger cities
  
Below is a list of the years in which each of the social networks was analyzed.

- Facebook: 2014-2022
- Twitter: 2014-2022
- Instagram: 2016-2022

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| usuarios_redes_sociales_id | serial | NO | primary key |
| anio | int | NO | year |
| ciudad | text | NO | city |
| red_social | text | NO | social network |
| usuarios | int | NO | number of users |

## Table definition

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
    ciudad text NOT NULL CHECK (ciudad ~ '^[A-Za-zÀ-ÿ\s]+$'),
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

## Notable transformations
Tables were extracted from each year's pdf report and merged together. 

## Source
Data extracted from <a href="hhttps://thesocialmediafamily.com/" target="_blank">Social Media Family</a> reports. 