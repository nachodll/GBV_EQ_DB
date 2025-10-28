# tecnologia_y_medios.acceso_internet_viviendas

Percentages of spanish households according to type of internet access.

- **Time period**: 2006-2024, anually
- **Regional breakdown**: comunidades autónomas

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| acceso_internet_viviendas_id | serial | NO | primary key |
| anio | int | NO | year |
| comunidad_autonoma_id | int | NO | references geo.comunidades_autonomas |
| tipo_equipamiento | text | NO | type of equipment |
| porcentaje | numeric | NO | percentage |

## Table definition

```sql
CREATE TABLE
  tecnologia_y_medios.acceso_internet_viviendas (
    acceso_internet_viviendas_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_equipamiento text NOT NULL CHECK (
      tipo_equipamiento IN (
        'Viviendas con algún tipo de ordenador',
        'Viviendas que disponen de acceso a Internet',
        'Viviendas con conexión de Banda Ancha  (ADSL, Red de cable, etc.)',
        'Viviendas con teléfono fijo',
        'Viviendas con teléfono móvil'
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );
```

## Notable transformations
No notable transformations were performed over this dataset. 

## Source
Data extracted from <a href="https://www.ine.es/jaxi/Tabla.htm?tpx=70470&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>. 
Consulted on 9 June 2025.
