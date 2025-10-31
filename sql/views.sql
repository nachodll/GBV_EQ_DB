DROP SCHEMA IF EXISTS analisis CASCADE;

CREATE SCHEMA IF NOT EXISTS analisis;

----------------------------s--------------------------------------------------------
-- v_indicadores_anuales_provinciales_unificados
------------------------------------------------------------------------------------
-- 0. Base geography view
CREATE OR REPLACE VIEW
    analisis.v_provincias AS
SELECT
    p.provincia_id,
    p.nombre AS provincia
FROM
    geo.provincias p;

-- 1. Population view by province
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

-- 2. feminicidios_pareja_expareja, yearly aggregated totals by province with zeros for missing data within 2003-2024
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

-- 3. menores_victimas_mortales, yearly aggregated totals by province with zeros for missing data within 2013-2024
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

-- 4. servicio_016, yearly aggregated totals by province with zeros for missing data within 2008-2024
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

-- 5. usuarias_atenpro, yearly total (last month is used) by province with nulls for missing data within 2005-2024
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

-- 6. denuncias_vg_pareja, yearly aggregated total by province with zeros for missing data within 2003-2024
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

-- 7. matrimonios_heterosexuales, yearly aggregated totals by province with zeros for missing data within 1975-2023
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

-- 8. matrimonios_homosexuales, yearly aggregated totals by province with nulls for missing data within 2005-2023
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

-- 9. prestaciones_maternidad_paternidad, yearly aggregated totals by province with nulls for missing data within 2002-2019
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

-- 10. tasa_actividad_paro_empleo_provincias, yearly average of 4 quarters by province with nulls for missing data within 2002-2024
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

-- 11. tasa_bruta_divorcialidad_comunidades, yearly totals by province with nulls for missing data within 2005-2023
CREATE OR REPLACE VIEW
    analisis.v_tasa_bruta_divorcialidad_provincial_anual AS
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
            tasa_bruta_divorcialidad
        FROM
            demografia.tasa_bruta_divorcialidad_provincias
    )
SELECT
    ac.anio,
    ac.provincia_id,
    ad.tasa_bruta_divorcialidad
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.provincia_id = ad.provincia_id
ORDER BY
    ac.anio,
    ac.provincia_id;

-- 12. barometros_generales_provincias, yearly average score for selected variables by provincia within 1979-2024
CREATE OR REPLACE VIEW
    analisis.v_barometros_generales_provincias_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(1979, 2024) AS anio
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
    -- Define the list of gender violence related problems
    gender_violence_problems AS (
        SELECT
            unnest(
                ARRAY[
                    'La violencia contra la mujer',
                    'La violencia de género',
                    'Las desigualdades, incluida la de género, las diferencias de clases, la pobreza',
                    'Los problemas relacionados con la mujer. La violencia de género',
                    'Problemas laborales y familiares de la mujer',
                    'Problemas relacionados con la mujer',
                    'Violencia contra la mujer',
                    'Los problemas laborales y familiares de las mujeres',
                    'Los problemas relacionados con la mujer'
                ]
            ) AS problema_text
    ),
    actual_data AS (
        SELECT
            EXTRACT(
                YEAR
                FROM
                    bg.fecha
            ) AS anio,
            bg.provincia_id,
            -- Average ideology by gender
            ROUND(
                AVG(
                    CASE
                        WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                    END
                )::NUMERIC,
                2
            ) AS promedio_ideologia_hombres,
            ROUND(
                AVG(
                    CASE
                        WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                    END
                )::NUMERIC,
                2
            ) AS promedio_ideologia_mujeres,
            -- Ideology 1-4 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 1
                        AND bg.ideologia <= 4 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_1_4_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 1
                        AND bg.ideologia <= 4 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_1_4_mujeres,
            -- Ideology 5-6 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 5
                        AND bg.ideologia <= 6 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_5_6_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 5
                        AND bg.ideologia <= 6 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_5_6_mujeres,
            -- Ideology 7-10 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 7
                        AND bg.ideologia <= 10 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_7_10_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 7
                        AND bg.ideologia <= 10 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_7_10_mujeres,
            -- Personal violence problem percentage by gender (using expanded list)
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND (
                            bg.problema_personal_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre'
                            AND (
                                bg.problema_personal_1 IS NOT NULL
                                OR bg.problema_personal_2 IS NOT NULL
                                OR bg.problema_personal_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_personal_genero_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND (
                            bg.problema_personal_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer'
                            AND (
                                bg.problema_personal_1 IS NOT NULL
                                OR bg.problema_personal_2 IS NOT NULL
                                OR bg.problema_personal_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_personal_genero_mujeres,
            -- Spain violence problem percentage by gender (using expanded list)
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND (
                            bg.problema_espania_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre'
                            AND (
                                bg.problema_espania_1 IS NOT NULL
                                OR bg.problema_espania_2 IS NOT NULL
                                OR bg.problema_espania_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_espania_genero_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND (
                            bg.problema_espania_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer'
                            AND (
                                bg.problema_espania_1 IS NOT NULL
                                OR bg.problema_espania_2 IS NOT NULL
                                OR bg.problema_espania_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_espania_genero_mujeres
        FROM
            percepcion_social.barometros_generales bg,
            gender_violence_problems
        WHERE
            bg.sexo IN ('Hombre', 'Mujer')
            AND bg.provincia_id IS NOT NULL
        GROUP BY
            EXTRACT(
                YEAR
                FROM
                    bg.fecha
            ),
            bg.provincia_id
    )
SELECT
    ac.anio,
    ac.provincia_id,
    -- Men indicators
    ad.promedio_ideologia_hombres,
    ad.porcentaje_ideologia_1_4_hombres,
    ad.porcentaje_ideologia_5_6_hombres,
    ad.porcentaje_ideologia_7_10_hombres,
    ad.porcentaje_problema_personal_genero_hombres,
    ad.porcentaje_problema_espania_genero_hombres,
    -- Women indicators
    ad.promedio_ideologia_mujeres,
    ad.porcentaje_ideologia_1_4_mujeres,
    ad.porcentaje_ideologia_5_6_mujeres,
    ad.porcentaje_ideologia_7_10_mujeres,
    ad.porcentaje_problema_personal_genero_mujeres,
    ad.porcentaje_problema_espania_genero_mujeres
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
        UNION
        SELECT
            anio,
            provincia_id
        FROM
            analisis.v_tasa_bruta_divorcialidad_provincial_anual
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
    div.tasa_bruta_divorcialidad,
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
    LEFT JOIN analisis.v_tasa_bruta_divorcialidad_provincial_anual div ON div.anio = k.anio
    AND div.provincia_id = k.provincia_id
ORDER BY
    k.anio,
    p.provincia_id;

------------------------------------------------------------------------------------
-- v_indicadores_anuales_comunidades_unificados
------------------------------------------------------------------------------------
-- 1. tasa_paro_comunidades, yearly average of 4 quarters by comunidad autónoma with nulls for missing data within 2002-2024
CREATE OR REPLACE VIEW
    analisis.v_tasa_paro_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2002, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            ROUND(AVG(tasa_paro)::NUMERIC, 2) AS tasa_paro
        FROM
            economia_laboral.tasa_paro_comunidades
        WHERE
            sexo = 'Total'
        GROUP BY
            anio,
            comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.tasa_paro
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 2. tasa_bruta_divorcialidad_comunidades, yearly totals by comunidad autónoma with nulls for missing data within 2005-2023
CREATE OR REPLACE VIEW
    analisis.v_tasa_bruta_divorcialidad_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2005, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            tasa_bruta_divorcialidad
        FROM
            demografia.tasa_bruta_divorcialidad_comunidades
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.tasa_bruta_divorcialidad
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

--3. feminicidios_fuera_pareja_expareja, yearly aggregated totals by comunidad autónoma with zeros for missing data within 2022-2024
CREATE OR REPLACE VIEW
    analisis.v_feminicidios_fuera_pareja_expareja_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2022, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            SUM(feminicidios) AS feminicidios_fuera_pareja_expareja
        FROM
            violencia_genero.feminicidios_fuera_pareja_expareja
        GROUP BY
            anio,
            comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    COALESCE(ad.feminicidios_fuera_pareja_expareja, 0) AS feminicidios_fuera_pareja_expareja
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

--4. denuncias_vg_presentadas, yearly totals by comunidad autónoma with nulls for missing data within 2007-2024
CREATE OR REPLACE VIEW
    analisis.v_denuncias_vg_presentadas_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2007, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            denuncias_presentadas AS denuncias_vg_presentadas
        FROM
            violencia_genero.denuncias_vg_presentadas
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.denuncias_vg_presentadas
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 5. ganancia_por_hora_trabajo, yearly average by comunidad autónoma with nulls for missing data within 2004-2023
CREATE OR REPLACE VIEW
    analisis.v_ganancia_por_hora_trabajo_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2004, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            ganancia_por_hora_trabajo
        FROM
            igualdad_formal.ganancia_por_hora_trabajo
        WHERE
            sexo = 'Total'
            AND sector_actividad = 'Todos los sectores'
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.ganancia_por_hora_trabajo
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 6. mujeres_cargos_autonomicos, yearly percentage by comunidad autónoma with nulls for missing data within 1996-2024
CREATE OR REPLACE VIEW
    analisis.v_mujeres_cargos_autonomicos_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(1996, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            ROUND(
                (
                    SUM(
                        CASE
                            WHEN sexo = 'Mujer' THEN numero_cargos
                            ELSE 0
                        END
                    )::NUMERIC / NULLIF(
                        SUM(
                            CASE
                                WHEN sexo = 'Total' THEN numero_cargos
                                ELSE 0
                            END
                        ),
                        0
                    ) * 100
                ),
                2
            ) AS porcentaje_mujeres_cargos_autonomicos
        FROM
            igualdad_formal.mujeres_cargos_autonomicos
        WHERE
            sexo IN ('Mujer', 'Total')
        GROUP BY
            anio,
            comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.porcentaje_mujeres_cargos_autonomicos
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 7. matriculados_universidad, yearly totals by comunidad autónoma with nulls for missing data within 1985-2024
CREATE OR REPLACE VIEW
    analisis.v_matriculados_universidad_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(1985, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            CAST(SPLIT_PART(curso, '-', 1) AS INTEGER) AS anio,
            comunidad_autonoma_id,
            SUM(matriculados) AS matriculados_universidad
        FROM
            educacion_juventud.matriculados_universidad
        WHERE
            nivel_academico = 'Total'
            AND tipo_universidad = 'Total'
            AND sexo = 'Total'
            AND modalidad_universidad = 'Total'
            AND rama_conocimiento = 'Total'
        GROUP BY
            anio,
            comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.matriculados_universidad
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 8. acceso_internet_viviendas, yearly percentage by comunidad autónoma with nulls for missing data within 2006-2024
CREATE OR REPLACE VIEW
    analisis.v_acceso_internet_viviendas_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2006, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            porcentaje AS porcentaje_acceso_internet_viviendas
        FROM
            tecnologia_y_medios.acceso_internet_viviendas
        WHERE
            tipo_equipamiento = 'Viviendas que disponen de acceso a Internet'
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.porcentaje_acceso_internet_viviendas
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 9. acceso_internet_personas, yearly percentage of daily access by comunidad autónoma with nulls for missing data within 2006-2024
CREATE OR REPLACE VIEW
    analisis.v_acceso_internet_personas_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2006, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            porcentaje AS porcentaje_uso_internet_diario_personas
        FROM
            tecnologia_y_medios.uso_internet_personas
        WHERE
            tipo_uso = 'Personas que han utilizado Internet diariamente (al menos 5 días a la semana)'
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.porcentaje_uso_internet_diario_personas
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 10. uso_internet_ninios, yearly percentage of children with phones by comunidad autónoma with nulls for missing data within 2006-2024
CREATE OR REPLACE VIEW
    analisis.v_uso_internet_ninios_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2006, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            porcentaje AS porcentaje_ninios_con_telefono_movil
        FROM
            tecnologia_y_medios.uso_internet_ninios
        WHERE
            tipo_uso = 'Niños que disponen de teléfono móvil'
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.porcentaje_ninios_con_telefono_movil
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 11. riesgo_pobreza_exclusion_social, yearly percentage by comunidad autónoma of AROPE indicator with nulls for missing data within 2008-2024
CREATE OR REPLACE VIEW
    analisis.v_riesgo_pobreza_exclusion_social_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2008, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            porcentaje AS porcentaje_arope
        FROM
            economia_laboral.riesgo_pobreza_exclusion
        WHERE
            indicador = 'Tasa de riesgo de pobreza o exclusión social (indicador AROPE)'
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.porcentaje_arope
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 12. tasas_homicidios_criminalidad, yearly rates by comunidad autónoma with nulls for missing data within 2010-2023
CREATE OR REPLACE VIEW
    analisis.v_tasas_homicidios_criminalidad_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2010, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            SUM(
                CASE
                    WHEN tipo_tasa = 'Tasa de homicidios' THEN total
                END
            ) AS tasa_homicidios,
            SUM(
                CASE
                    WHEN tipo_tasa = 'Tasa de criminalidad' THEN total
                END
            ) AS tasa_criminalidad
        FROM
            seguridad_criminalidad.tasas_homicidios_criminalidad
        GROUP BY
            anio,
            comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.tasa_homicidios,
    ad.tasa_criminalidad
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 13. ive_ccaa, yearly totals by comunidad autónoma with nulls for missing data within 2014-2023
CREATE OR REPLACE VIEW
    analisis.v_ive_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(2014, 2023) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    actual_data AS (
        SELECT
            anio,
            comunidad_autonoma_id,
            tasa AS tasa_ive
        FROM
            salud.ive_ccaa
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    ad.tasa_ive
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 14. legislacion, approval date of first autonomic law on gender equality/violence by comunidad autónoma, repeated for every year 1975-2024
CREATE OR REPLACE VIEW
    analisis.v_legislacion_primera_ley_autonomica AS
WITH
    year_range AS (
        SELECT
            generate_series(1975, 2024) AS anio
    ),
    primera_ley_por_ccaa AS (
        SELECT
            l.comunidad_autonoma_id,
            MIN(
                CASE
                    WHEN l.tematica = 'Violencia de género' THEN l.fecha_aprobacion
                END
            ) AS fecha_primera_ley_violencia,
            MIN(
                CASE
                    WHEN l.tematica = 'Igualdad' THEN l.fecha_aprobacion
                END
            ) AS fecha_primera_ley_igualdad
        FROM
            politicas_publicas_igualdad_violencia.legislacion l
        WHERE
            l.tematica IN ('Violencia de género', 'Igualdad')
        GROUP BY
            l.comunidad_autonoma_id
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    pl.fecha_primera_ley_violencia,
    pl.fecha_primera_ley_igualdad
FROM
    all_combinations ac
    LEFT JOIN primera_ley_por_ccaa pl ON pl.comunidad_autonoma_id = ac.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 15. instituo_mujer, existence of autonomic institute for women for every year 1975-2024
CREATE OR REPLACE VIEW
    analisis.v_instituto_mujer_autonomico AS
WITH
    year_range AS (
        SELECT
            generate_series(1975, 2024) AS anio
    ),
    institutos_por_ccaa AS (
        SELECT
            im.comunidad_autonoma_id,
            MIN(im.anio_fundacion) AS anio_creacion_instituto
        FROM
            politicas_publicas_igualdad_violencia.institutos_mujer im
        GROUP BY
            im.comunidad_autonoma_id
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    CASE
        WHEN im.anio_creacion_instituto IS NOT NULL
        AND ac.anio >= im.anio_creacion_instituto THEN TRUE
        ELSE FALSE
    END AS existe_instituto_mujer
FROM
    all_combinations ac
    LEFT JOIN institutos_por_ccaa im ON im.comunidad_autonoma_id = ac.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

-- 16. barometros_generales, yearly average score for selected variables by comunidad autónoma and sex within 1979-2024
CREATE OR REPLACE VIEW
    analisis.v_barometros_generales_comunidades_anual AS
WITH
    year_range AS (
        SELECT
            generate_series(1979, 2024) AS anio
    ),
    all_combinations AS (
        SELECT
            yr.anio,
            ca.comunidad_autonoma_id
        FROM
            year_range yr
            CROSS JOIN geo.comunidades_autonomas ca
        WHERE
            ca.comunidad_autonoma_id != 0
    ),
    -- Define the list of gender violence related problems
    gender_violence_problems AS (
        SELECT
            unnest(
                ARRAY[
                    'La violencia contra la mujer',
                    'La violencia de género',
                    'Las desigualdades, incluida la de género, las diferencias de clases, la pobreza',
                    'Los problemas relacionados con la mujer. La violencia de género',
                    'Problemas laborales y familiares de la mujer',
                    'Problemas relacionados con la mujer',
                    'Violencia contra la mujer',
                    'Los problemas laborales y familiares de las mujeres',
                    'Los problemas relacionados con la mujer'
                ]
            ) AS problema_text
    ),
    actual_data AS (
        SELECT
            EXTRACT(
                YEAR
                FROM
                    bg.fecha
            ) AS anio,
            bg.comunidad_autonoma_id,
            -- Average ideology by gender
            ROUND(
                AVG(
                    CASE
                        WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                    END
                )::NUMERIC,
                2
            ) AS promedio_ideologia_hombres,
            ROUND(
                AVG(
                    CASE
                        WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                    END
                )::NUMERIC,
                2
            ) AS promedio_ideologia_mujeres,
            -- Ideology 1-4 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 1
                        AND bg.ideologia <= 4 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_1_4_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 1
                        AND bg.ideologia <= 4 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_1_4_mujeres,
            -- Ideology 5-6 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 5
                        AND bg.ideologia <= 6 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_5_6_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 5
                        AND bg.ideologia <= 6 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_5_6_mujeres,
            -- Ideology 7-10 percentage by gender
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND bg.ideologia >= 7
                        AND bg.ideologia <= 10 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_7_10_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND bg.ideologia >= 7
                        AND bg.ideologia <= 10 THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer' THEN bg.ideologia
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_ideologia_7_10_mujeres,
            -- Personal violence problem percentage by gender (using expanded list)
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND (
                            bg.problema_personal_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre'
                            AND (
                                bg.problema_personal_1 IS NOT NULL
                                OR bg.problema_personal_2 IS NOT NULL
                                OR bg.problema_personal_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_personal_genero_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND (
                            bg.problema_personal_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_personal_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer'
                            AND (
                                bg.problema_personal_1 IS NOT NULL
                                OR bg.problema_personal_2 IS NOT NULL
                                OR bg.problema_personal_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_personal_genero_mujeres,
            -- Spain violence problem percentage by gender (using expanded list)
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Hombre'
                        AND (
                            bg.problema_espania_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Hombre'
                            AND (
                                bg.problema_espania_1 IS NOT NULL
                                OR bg.problema_espania_2 IS NOT NULL
                                OR bg.problema_espania_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_espania_genero_hombres,
            ROUND(
                SUM(
                    CASE
                        WHEN bg.sexo = 'Mujer'
                        AND (
                            bg.problema_espania_1 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_2 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                            OR bg.problema_espania_3 IN (
                                SELECT
                                    problema_text
                                FROM
                                    gender_violence_problems
                            )
                        ) THEN 1
                        ELSE 0
                    END
                )::NUMERIC / NULLIF(
                    COUNT(
                        CASE
                            WHEN bg.sexo = 'Mujer'
                            AND (
                                bg.problema_espania_1 IS NOT NULL
                                OR bg.problema_espania_2 IS NOT NULL
                                OR bg.problema_espania_3 IS NOT NULL
                            ) THEN 1
                        END
                    ),
                    0
                ) * 100,
                2
            ) AS porcentaje_problema_espania_genero_mujeres
        FROM
            percepcion_social.barometros_generales bg,
            gender_violence_problems -- Cross join to make the CTE available
        WHERE
            bg.sexo IN ('Hombre', 'Mujer')
        GROUP BY
            EXTRACT(
                YEAR
                FROM
                    bg.fecha
            ),
            bg.comunidad_autonoma_id
    )
SELECT
    ac.anio,
    ac.comunidad_autonoma_id,
    -- Men indicators
    ad.promedio_ideologia_hombres,
    ad.porcentaje_ideologia_1_4_hombres,
    ad.porcentaje_ideologia_5_6_hombres,
    ad.porcentaje_ideologia_7_10_hombres,
    ad.porcentaje_problema_personal_genero_hombres,
    ad.porcentaje_problema_espania_genero_hombres,
    -- Women indicators
    ad.promedio_ideologia_mujeres,
    ad.porcentaje_ideologia_1_4_mujeres,
    ad.porcentaje_ideologia_5_6_mujeres,
    ad.porcentaje_ideologia_7_10_mujeres,
    ad.porcentaje_problema_personal_genero_mujeres,
    ad.porcentaje_problema_espania_genero_mujeres
FROM
    all_combinations ac
    LEFT JOIN actual_data ad ON ac.anio = ad.anio
    AND ac.comunidad_autonoma_id = ad.comunidad_autonoma_id
ORDER BY
    ac.anio,
    ac.comunidad_autonoma_id;

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
        UNION
        SELECT
            anio,
            comunidad_autonoma_id
        FROM
            analisis.v_tasa_paro_comunidades_anual
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
    prest.prestaciones_paternidad,
    -- Labor market indicators
    tasa.tasa_paro
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
    LEFT JOIN analisis.v_tasa_paro_comunidades_anual tasa ON tasa.anio = k.anio
    AND tasa.comunidad_autonoma_id = k.comunidad_autonoma_id
ORDER BY
    k.anio,
    ca.comunidad_autonoma_id;