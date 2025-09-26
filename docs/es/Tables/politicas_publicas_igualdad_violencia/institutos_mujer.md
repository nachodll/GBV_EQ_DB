# politicas_publicas_igualdad_violencia.institutos_mujer

Directorio de institutos de la mujer de las comunidades autónomas españolas. Las comunidades autónomas no listadas no disponen de instituto de la mujer autonómico.

- **Periodo temporal**: 1983-2025
- **Desagregación regional**: comunidades autónomas

## Columnas

| Nombre | Tipo de dato | Es Nullable | Descripción |
| --- | --- | --- | --- |
| institutos_mujer_id | serial | NO | clave primaria |
| comunidad_autonoma_id | int | NO | referencia a geo.comunidades_autonomas |
| nombre | text | NO | denominación oficial del organismo |
| anio_fundacion | int | SÍ | año de fundación |
| enlace | text | SÍ | página web o referencia oficial |

## Definición de la tabla

```sql
CREATE TABLE
  politicas_publicas_igualdad_violencia.institutos_mujer (
    institutos_mujer_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    anio_fundacion int CHECK (
      anio_fundacion BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    enlace text
  );
```

## Transformaciones notables

- Compilación manual de los datos del directorio del Instituto de las Mujeres, estandarizando denominaciones y códigos autonómicos.

## Fuente

Datos recopilados del <a href="https://www.inmujeres.gob.es/servRecursos/OrganismosIgualdad/AmbitoEstatal/AmbitoEstatal.htm" target="_blank">Instituto de las Mujeres</a>.

