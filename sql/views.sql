CREATE SCHEMA IF NOT EXISTS analysis;

-- Base geography view
CREATE OR REPLACE VIEW
    analysis.v_provincias AS
SELECT
    p.provincia_id,
    p.nombre AS provincia
FROM
    geo.provincias p;

-- Population view by province
CREATE OR REPLACE VIEW
    analysis.v_poblacion_provincial AS
SELECT
    pm.anio,
    m.provincia_id,
    SUM(pm.poblacion)::bigint AS poblacion_provincia
FROM
    demografia.poblacion_municipios pm
    JOIN geo.municipios m ON m.municipio_id = pm.municipio_id
WHERE
    pm.sexo IN ('Hombre', 'Mujer')
GROUP BY
    pm.anio,
    m.provincia_id;

-- feminicidios_pareja_expareja, yearly aggregated totals by province with zeros for missing data within 2003-2024
CREATE OR REPLACE VIEW
    analysis.v_feminicidios_pareja_expareja_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2003, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(feminicidios) AS feminicidios_pareja_expareja,
            SUM(COALESCE(huerfanos_menores, 0)) AS huerfanos_menores
        FROM
            violencia_genero.feminicidios_pareja_expareja
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    COALESCE(ad.feminicidios_pareja_expareja, 0) AS feminicidios_pareja_expareja,
    CASE
        WHEN ac.anio < 2013 THEN NULL -- Data not available before 2013
        ELSE COALESCE(ad.huerfanos_menores, 0)
    END AS huerfanos_menores
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- menores_victimas_mortales, yearly aggregated totals by province with zeros for missing data within 2013-2024
CREATE OR REPLACE VIEW
    analysis.v_menores_victimas_mortales_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2013, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(menores_victimas_mortales) AS menores_victimas_mortales
        FROM
            violencia_genero.menores_victimas_mortales
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    COALESCE(ad.menores_victimas_mortales, 0) AS menores_victimas_mortales
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- servicio_016, yearly aggregated totals by province with zeros for missing data within 2008-2024
CREATE OR REPLACE VIEW
    analysis.v_servicio_016_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2008, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(llamadas + whatsapps + emails + chats) AS servicio_016_contactos
        FROM
            violencia_genero.servicio_016
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    COALESCE(ad.servicio_016_contactos, 0) AS servicio_016_contactos
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- usuarias_atenpro, yearly total (last month is used) by province with nulls for missing data within 2005-2024
CREATE OR REPLACE VIEW
    analysis.v_atenpro_usuarias_activas_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2005, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            usuarias_activas
        FROM
            violencia_genero.usuarias_atenpro
        WHERE
            mes = 12
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.usuarias_activas AS atenpro_usuarias_activas
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- dispositivos_electronicos_seguimiento, yearly total (last month is used) by province with nulls for missing data within 2009-2024
CREATE OR REPLACE VIEW
    analysis.v_dispositivos_electronicos_seguimiento_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2009, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            dispositivos_activos
        FROM
            violencia_genero.dispositivos_electronicos_seguimiento
        WHERE
            mes = 12
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.dispositivos_activos AS dispositivos_electronicos_seguimiento_activos
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- denuncias_vg_pareja, yearly aggregated total by province with zeros for missing data within 2003-2024
CREATE OR REPLACE VIEW
    analysis.v_denuncias_vg_pareja_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2009, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(denuncias) AS denuncias_vg_pareja
        FROM
            violencia_genero.denuncias_vg_pareja
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    COALESCE(ad.denuncias_vg_pareja, 0) AS denuncias_vg_pareja
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- mattrimonios_heterosexuales, yearly aggregated totals by province with zeros for missing data within 1975-2023
CREATE OR REPLACE VIEW
    analysis.v_matrimonios_heterosexuales_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(1975, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(matrimonios) AS matrimonios_heterosexuales
        FROM
            demografia.matrimonios_heterosexuales
        WHERE
            estado_civil_anterior = 'Total'
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    COALESCE(ad.matrimonios_heterosexuales, 0) AS matrimonios_heterosexuales
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- mattrimonios_homosexuales, yearly aggregated totals by province with nulls for missing data within 2005-2023
CREATE OR REPLACE VIEW
    analysis.v_matrimonios_homosexuales_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2005, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(matrimonios_hombres) AS matrimonios_hombres,
            SUM(matrimonios_mujeres) AS matrimonios_mujeres
        FROM
            demografia.matrimonios_homosexuales
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.matrimonios_hombres AS matrimonios_homosexuales_hombres,
    ad.matrimonios_mujeres AS matrimonios_homosexuales_mujeres
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- prestaciones_maternidad_paternidad, yearly aggregated totals by province with nulls for missing data within 2002-2019
CREATE OR REPLACE VIEW
    analysis.v_prestaciones_maternidad_paternidad_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2002, 2019) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            SUM(
                CASE
                    WHEN tipo = 'Maternidad' THEN COALESCE(percibidas_madre, 0) + COALESCE(percibidas_padre, 0)
                    ELSE 0
                END
            ) AS prestaciones_maternidad,
            SUM(
                CASE
                    WHEN tipo = 'Paternidad' THEN COALESCE(percibidas_padre, 0) -- not transferred to mother
                    ELSE 0
                END
            ) AS prestaciones_paternidad
        FROM
            educacion_juventud.prestaciones_maternidad_paternidad
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.prestaciones_maternidad AS prestaciones_maternidad,
    CASE
        WHEN ac.anio < 2007 THEN NULL -- Paternidad data not available before 2007
        ELSE ad.prestaciones_paternidad
    END AS prestaciones_paternidad
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- tasa_actividad_paro_empleo, yearly average of 4 quarters by province with nulls for missing data within 2002-2024
-- do not count provincia_id = 0, take only sexo='Total', aggregate by tasa=Tasa de actividad, Tasa de empleo, Tasa de paro
CREATE OR REPLACE VIEW
    analysis.v_tasa_actividad_paro_empleo_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2002, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            p.provincia_id
        FROM
            year_range yr
            CROSS JOIN geo.provincias p
        WHERE
            p.provincia_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            provincia_id,
            ROUND(
                AVG(
                    CASE
                        WHEN tasa = 'Tasa de actividad' THEN total
                    END
                )::NUMERIC,
                2
            ) AS tasa_actividad,
            ROUND(
                AVG(
                    CASE
                        WHEN tasa = 'Tasa de empleo' THEN total
                    END
                )::NUMERIC,
                2
            ) AS tasa_empleo,
            ROUND(
                AVG(
                    CASE
                        WHEN tasa = 'Tasa de paro' THEN total
                    END
                )::NUMERIC,
                2
            ) AS tasa_paro
        FROM
            economia_laboral.tasa_actividad_paro_empleo
        WHERE
            sexo = 'Total'
        GROUP BY
            anio,
            provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.tasa_actividad,
    ad.tasa_empleo,
    ad.tasa_paro
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- Unified view combining all provincial annual indicators
CREATE OR REPLACE VIEW
    analysis.v_indicadores_anuales_provinciales_unificados AS
WITH
    -- Get all unique year-province combinations from all views
    all_keys AS (
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_feminicidios_pareja_expareja_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_menores_victimas_mortales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_servicio_016_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_atenpro_usuarias_activas_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_dispositivos_electronicos_seguimiento_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_denuncias_vg_pareja_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_matrimonios_heterosexuales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_matrimonios_homosexuales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_prestaciones_maternidad_paternidad_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_tasa_actividad_paro_empleo_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analysis.v_poblacion_provincial
    )
SELECT
    k.anio,
    k.provincia_id,
    p.provincia,
    -- Demographics
    pop.poblacion_provincia,
    mat_het.matrimonios_heterosexuales,
    mat_hom.matrimonios_homosexuales_hombres,
    mat_hom.matrimonios_homosexuales_mujeres,
    -- Gender-based violence indicators
    fem.feminicidios_pareja_expareja,
    fem.huerfanos_menores,
    men.menores_victimas_mortales,
    s016.servicio_016_contactos,
    aten.atenpro_usuarias_activas,
    disp.dispositivos_electronicos_seguimiento_activos,
    den.denuncias_vg_pareja,
    -- Social benefits
    prest.prestaciones_maternidad,
    prest.prestaciones_paternidad,
    -- Labor market indicators
    epa.tasa_actividad,
    epa.tasa_empleo,
    epa.tasa_paro
FROM
    all_keys k
    JOIN analysis.v_provincias p ON p.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_poblacion_provincial pop ON pop.anio = k.anio
    AND pop.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_feminicidios_pareja_expareja_anual fem ON fem.anio = k.anio
    AND fem.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_menores_victimas_mortales_anual men ON men.anio = k.anio
    AND men.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_servicio_016_anual s016 ON s016.anio = k.anio
    AND s016.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_atenpro_usuarias_activas_anual aten ON aten.anio = k.anio
    AND aten.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_dispositivos_electronicos_seguimiento_anual disp ON disp.anio = k.anio
    AND disp.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_denuncias_vg_pareja_anual den ON den.anio = k.anio
    AND den.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_matrimonios_heterosexuales_anual mat_het ON mat_het.anio = k.anio
    AND mat_het.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_matrimonios_homosexuales_anual mat_hom ON mat_hom.anio = k.anio
    AND mat_hom.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_prestaciones_maternidad_paternidad_anual prest ON prest.anio = k.anio
    AND prest.provincia_id = k.provincia_id
    LEFT JOIN analysis.v_tasa_actividad_paro_empleo_anual epa ON epa.anio = k.anio
    AND epa.provincia_id = k.provincia_id
ORDER BY
    k.anio,
    p.provincia_id;