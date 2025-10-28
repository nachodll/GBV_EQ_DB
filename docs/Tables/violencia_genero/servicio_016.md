# violencia_genero.servicio_016

Total monthly inquiries made by different means to the 016 service per province.

- **Time period**: 2007-2025, monthly
- **Regional breakdown**: provincias

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| servicio_016_id | serial | NO | primary key |
| provincia_id | int | YES | references geo.provincias |
| anio | int | NO | year |
| mes | int | NO | month |
| persona_consulta | enums.persona_consulta_enum | YES | person who made the query |
| tipo_violencia | enums.tipo_violencia_enum | YES | 'Pareja/Expareja', 'Familiar' or 'Sexual' |
| llamadas | int | NO | number of inquiries via phone |
| whatsapps | int | NO | number of inquiries via whatsapp |
| emails | int | NO | number of inquiries via email |
| chats | int | NO | number of inquiries via chat |

## Table definition

```sql
CREATE TABLE
  violencia_genero.servicio_016 (
    servicio_016_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    persona_consulta enums.persona_consulta_enum,
    tipo_violencia enums.tipo_violencia_enum,
    llamadas int NOT NULL CHECK (llamadas >= 0),
    whatsapps int NOT NULL CHECK (whatsapps >= 0),
    emails int NOT NULL CHECK (emails >= 0),
    chats int NOT NULL CHECK (chats >= 0)
  );
```

## Notable transformations
No notable transformations were performed over this dataset. Source data provider only allows 5 analysis variable to be selected at time. More analysis variables are available at the original source. 

## Source
Data extracted from <a href="https://estadisticasviolenciagenero.igualdad.gob.es/" target="_blank">Portal Estadísdico de la Delegación del Gobierno contra la Violencia de Género (DGVG)</a>. Table: "040 Servicio 016".
Consulted on 11 June 2025.
