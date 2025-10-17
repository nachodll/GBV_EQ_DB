# educacion_juventud.excedencias_cuidado_hijos_familiares

Número de solicitudes de excedencia sin remuneración para el cuidado de hijas/os o familiares, desagregadas por sexo y motivo de la excedencia.

- **Periodo temporal**: 2007-2023, anual
- **Desagregación regional**: provincias

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| excedencias_cuidado_hijos_familiares_id | serial | NO | clave primaria |
| anio | int | NO | año |
| sexo | enums.sexo_enum | NO | sexo (`Hombre`, `Mujer`, `Total`) |
| motivo | text | NO | motivo de la excedencia (`Cuidado de hijos`, `Cuidado de familiares`) |
| provincia_id | int | NO | referencia a geo.provincias |
| excedencias | int | SÍ | número de excedencias concedidas |

## Definición de la tabla

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

## Transformaciones notables

- Se consolidaron hojas de cálculo anuales con estructuras variables en una tabla única de formato largo.
- Se eliminaron filas agregadas por comunidad autónoma y se homogeneizaron los nombres de provincia antes de normalizarlos.
- Se normalizaron las categorías de sexo y motivos mediante diccionarios comunes y se transformaron valores ausentes o marcadores en nulos.

## Fuente

Anuarios Estadísticos del Ministerio de Trabajo y Economía Social (<a href="https://www.mites.gob.es/es/estadisticas/anuarios/index.htm" target="_blank" rel="noopener">MITES</a>).
