# tecnologia_y_medios.usuarios_redes_sociales

**Data loading script:** `pipelines/extract_transform/tecnologia_y_medios/004_et_usuarios_redes_sociales.py`

## Columns

| Name | Data Type | Is Nullable | Description |
| --- | --- | --- | --- |
| usuarios_redes_sociales_id | serial | NO | PRIMARY KEY |
| anio | int | NO | CHECK ( anio BETWEEN 1900 AND EXTRACT( YEAR FROM CURRENT_DATE ) ) |
| ciudad | text | NO | CHECK (ciudad ~ '^[A-Za-zÀ-ÿ\s]+$') |
| red_social | text | NO | CHECK ( red_social IN ( 'Facebook', 'Instagram', 'Twitter', 'TikTok', 'LinkedIn', 'YouTube' ) ) |
| usuarios | int | NO | CHECK (usuarios >= 0) |

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
