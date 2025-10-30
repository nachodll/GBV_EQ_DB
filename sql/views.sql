DROP SCHEMA IF EXISTS analisis CASCADE;

CREATE SCHEMA IF NOT EXISTS analisis;

------------------------------------------------------------------------------------
-- v_indicadores_anuales_provinciales_unificados
------------------------------------------------------------------------------------
-- Base geography view
CREATE OR REPLACE VIEW
    analisis.v_provincias AS
SELECT
    p.provincia_id,
    p.nombre AS provincia
FROM
    geo.provincias p;

-- Population view by province
CREATE OR REPLACE VIEW
    analisis.v_poblacion_provincial AS
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
    analisis.v_feminicidios_pareja_expareja_anual AS
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
    analisis.v_menores_victimas_mortales_anual AS
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
    analisis.v_servicio_016_anual AS
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
    analisis.v_atenpro_usuarias_activas_anual AS
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
    analisis.v_dispositivos_electronicos_seguimiento_anual AS
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
    analisis.v_denuncias_vg_pareja_anual AS
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
    analisis.v_matrimonios_heterosexuales_anual AS
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
    analisis.v_matrimonios_homosexuales_anual AS
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
    analisis.v_prestaciones_maternidad_paternidad_anual AS
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
    analisis.v_tasa_actividad_paro_empleo_anual AS
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
            economia_laboral.tasa_actividad_paro_empleo_provincias
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
    analisis.v_indicadores_anuales_provinciales_unificados AS
WITH
    -- Get all unique year-province combinations from all views
    all_keys AS (
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_feminicidios_pareja_expareja_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_menores_victimas_mortales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_servicio_016_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_atenpro_usuarias_activas_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_dispositivos_electronicos_seguimiento_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_denuncias_vg_pareja_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_matrimonios_heterosexuales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_matrimonios_homosexuales_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_prestaciones_maternidad_paternidad_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_tasa_actividad_paro_empleo_anual
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_poblacion_provincial
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
    JOIN analisis.v_provincias p ON p.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_poblacion_provincial pop ON pop.anio = k.anio
    AND pop.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_feminicidios_pareja_expareja_anual fem ON fem.anio = k.anio
    AND fem.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_menores_victimas_mortales_anual men ON men.anio = k.anio
    AND men.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_servicio_016_anual s016 ON s016.anio = k.anio
    AND s016.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_atenpro_usuarias_activas_anual aten ON aten.anio = k.anio
    AND aten.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_dispositivos_electronicos_seguimiento_anual disp ON disp.anio = k.anio
    AND disp.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_denuncias_vg_pareja_anual den ON den.anio = k.anio
    AND den.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_matrimonios_heterosexuales_anual mat_het ON mat_het.anio = k.anio
    AND mat_het.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_matrimonios_homosexuales_anual mat_hom ON mat_hom.anio = k.anio
    AND mat_hom.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_prestaciones_maternidad_paternidad_anual prest ON prest.anio = k.anio
    AND prest.provincia_id = k.provincia_id
    LEFT JOIN analisis.v_tasa_actividad_paro_empleo_anual epa ON epa.anio = k.anio
    AND epa.provincia_id = k.provincia_id
ORDER BY
    k.anio,
    p.provincia_id;

------------------------------------------------------------------------------------
-- v_indicadores_anuales_comunidades_unificados
------------------------------------------------------------------------------------
-- Unified view combining all comunidad autónoma annual indicators
CREATE OR REPLACE VIEW
    analisis.v_indicadores_anuales_comunidades_unificados AS
WITH
    -- Aggregate provincial data to comunidad autónoma level
    poblacion_ccaa AS (
        SELECT
            pop.anio,
            p.comunidad_autonoma_id,
            SUM(pop.poblacion_provincia) AS poblacion_comunidad
        FROM
            analisis.v_poblacion_provincial pop
            JOIN geo.provincias p ON p.provincia_id = pop.provincia_id
        GROUP BY
            pop.anio,
            p.comunidad_autonoma_id
    ),
    feminicidios_ccaa AS (
        SELECT
            fem.anio,
            p.comunidad_autonoma_id,
            SUM(fem.feminicidios_pareja_expareja) AS feminicidios_pareja_expareja,
            SUM(COALESCE(fem.huerfanos_menores, 0)) AS huerfanos_menores
        FROM
            analisis.v_feminicidios_pareja_expareja_anual fem
            JOIN geo.provincias p ON p.provincia_id = fem.provincia_id
        GROUP BY
            fem.anio,
            p.comunidad_autonoma_id
    ),
    menores_victimas_ccaa AS (
        SELECT
            men.anio,
            p.comunidad_autonoma_id,
            SUM(men.menores_victimas_mortales) AS menores_victimas_mortales
        FROM
            analisis.v_menores_victimas_mortales_anual men
            JOIN geo.provincias p ON p.provincia_id = men.provincia_id
        GROUP BY
            men.anio,
            p.comunidad_autonoma_id
    ),
    servicio_016_ccaa AS (
        SELECT
            s016.anio,
            p.comunidad_autonoma_id,
            SUM(s016.servicio_016_contactos) AS servicio_016_contactos
        FROM
            analisis.v_servicio_016_anual s016
            JOIN geo.provincias p ON p.provincia_id = s016.provincia_id
        GROUP BY
            s016.anio,
            p.comunidad_autonoma_id
    ),
    atenpro_ccaa AS (
        SELECT
            aten.anio,
            p.comunidad_autonoma_id,
            SUM(COALESCE(aten.atenpro_usuarias_activas, 0)) AS atenpro_usuarias_activas
        FROM
            analisis.v_atenpro_usuarias_activas_anual aten
            JOIN geo.provincias p ON p.provincia_id = aten.provincia_id
        GROUP BY
            aten.anio,
            p.comunidad_autonoma_id
    ),
    dispositivos_ccaa AS (
        SELECT
            disp.anio,
            p.comunidad_autonoma_id,
            SUM(
                COALESCE(
                    disp.dispositivos_electronicos_seguimiento_activos,
                    0
                )
            ) AS dispositivos_electronicos_seguimiento_activos
        FROM
            analisis.v_dispositivos_electronicos_seguimiento_anual disp
            JOIN geo.provincias p ON p.provincia_id = disp.provincia_id
        GROUP BY
            disp.anio,
            p.comunidad_autonoma_id
    ),
    denuncias_ccaa AS (
        SELECT
            den.anio,
            p.comunidad_autonoma_id,
            SUM(den.denuncias_vg_pareja) AS denuncias_vg_pareja
        FROM
            analisis.v_denuncias_vg_pareja_anual den
            JOIN geo.provincias p ON p.provincia_id = den.provincia_id
        GROUP BY
            den.anio,
            p.comunidad_autonoma_id
    ),
    matrimonios_het_ccaa AS (
        SELECT
            mat_het.anio,
            p.comunidad_autonoma_id,
            SUM(mat_het.matrimonios_heterosexuales) AS matrimonios_heterosexuales
        FROM
            analisis.v_matrimonios_heterosexuales_anual mat_het
            JOIN geo.provincias p ON p.provincia_id = mat_het.provincia_id
        GROUP BY
            mat_het.anio,
            p.comunidad_autonoma_id
    ),
    matrimonios_hom_ccaa AS (
        SELECT
            mat_hom.anio,
            p.comunidad_autonoma_id,
            SUM(
                COALESCE(mat_hom.matrimonios_homosexuales_hombres, 0)
            ) AS matrimonios_homosexuales_hombres,
            SUM(
                COALESCE(mat_hom.matrimonios_homosexuales_mujeres, 0)
            ) AS matrimonios_homosexuales_mujeres
        FROM
            analisis.v_matrimonios_homosexuales_anual mat_hom
            JOIN geo.provincias p ON p.provincia_id = mat_hom.provincia_id
        GROUP BY
            mat_hom.anio,
            p.comunidad_autonoma_id
    ),
    prestaciones_ccaa AS (
        SELECT
            prest.anio,
            p.comunidad_autonoma_id,
            SUM(COALESCE(prest.prestaciones_maternidad, 0)) AS prestaciones_maternidad,
            SUM(COALESCE(prest.prestaciones_paternidad, 0)) AS prestaciones_paternidad
        FROM
            analisis.v_prestaciones_maternidad_paternidad_anual prest
            JOIN geo.provincias p ON p.provincia_id = prest.provincia_id
        GROUP BY
            prest.anio,
            p.comunidad_autonoma_id
    ),
    -- Get all unique year-comunidad combinations
    all_keys AS (
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            poblacion_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            feminicidios_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            menores_victimas_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            servicio_016_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            atenpro_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            dispositivos_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            denuncias_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            matrimonios_het_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            matrimonios_hom_ccaa
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            prestaciones_ccaa
    )
SELECT
    k.anio,
    k.comunidad_autonoma_id,
    ca.nombre AS comunidad_autonoma,
    -- Demographics
    pop.poblacion_comunidad,
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
    prest.prestaciones_paternidad
FROM
    all_keys k
    JOIN geo.comunidades_autonomas ca ON ca.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN poblacion_ccaa pop ON pop.anio = k.anio
    AND pop.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN feminicidios_ccaa fem ON fem.anio = k.anio
    AND fem.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN menores_victimas_ccaa men ON men.anio = k.anio
    AND men.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN servicio_016_ccaa s016 ON s016.anio = k.anio
    AND s016.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN atenpro_ccaa aten ON aten.anio = k.anio
    AND aten.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN dispositivos_ccaa disp ON disp.anio = k.anio
    AND disp.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN denuncias_ccaa den ON den.anio = k.anio
    AND den.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN matrimonios_het_ccaa mat_het ON mat_het.anio = k.anio
    AND mat_het.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN matrimonios_hom_ccaa mat_hom ON mat_hom.anio = k.anio
    AND mat_hom.comunidad_autonoma_id = k.comunidad_autonoma_id
    LEFT JOIN prestaciones_ccaa prest ON prest.anio = k.anio
    AND prest.comunidad_autonoma_id = k.comunidad_autonoma_id
ORDER BY
    k.anio,
    ca.comunidad_autonoma_id;