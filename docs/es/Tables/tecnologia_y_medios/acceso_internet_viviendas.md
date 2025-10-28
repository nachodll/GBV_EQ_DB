# tecnologia_y_medios.acceso_internet_viviendas

Porcentajes de hogares españoles según el tipo de acceso a Internet.

- **Periodo temporal**: 2006-2024, anual
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| acceso_internet_viviendas_id | serial | NO | primary key |
| anio | int | NO | año |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| tipo_equipamiento | text | NO | tipo de equipamiento |
| porcentaje | numeric | NO | porcentaje |

## Definición de la tabla

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

## Transformaciones notables
No se realizaron transformaciones notables sobre este conjunto de datos.

## Fuente
Datos extraídos del <a href="https://www.ine.es/jaxi/Tabla.htm?tpx=70470&L=0" target="_blank">Instituto Nacional de Estadística (INE)</a>.
Consultado el 9 de junio de 2025.
