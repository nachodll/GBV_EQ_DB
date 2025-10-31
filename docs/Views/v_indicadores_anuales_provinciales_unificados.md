# analisis.v_indicadores_anuales_provinciales_unificados

The `analisis.v_indicadores_anuales_provinciales_unificados` view consolidates the main annual indicators that are available at province level. Every year contributes 52 rows (one per province), and any indicator without data for a province-year combination remains `NULL` in the unified output. This makes it possible to join the view safely with other yearly provincial datasets without losing the geographic universe.

Each row contains the `(anio, provincia_id, provincia)` key alongside the indicators summarised in the following table.

> **⚠️ Warning**
> The indicators in this view are already aggregated at the province level. Some upstream datasets include national records without territorial identifiers; as a result, summing the provincial totals will **not** always reproduce the national total published by the data source. Consult the documentation of each source table before aggregating beyond the provincial scope.

> **📝 Note** 
> This page summarises the unified output. Detailed metadata (definitions, caveats, unit descriptions…) for every indicator live in the documentation of the corresponding source tables listed below.


## Source views

The unified view draws from the following intermediate views defined in `sql/views.sql`. All of them align their outputs on the same `(anio, provincia_id)` keys before being joined together.

### Indicators included

| Indicator | Table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `poblacion_provincia` | [`demografia.poblacion_municipios`](../Tables/demografia/poblacion_municipios.md) | `analisis.v_poblacion_provincial` | Sum of municipal population for men and women | 1996-2024 |
| `matrimonios_heterosexuales` | [`demografia.matrimonios_heterosexuales`](../Tables/demografia/matrimonios_heterosexuales.md) | `analisis.v_matrimonios_heterosexuales_anual` | Sum of marriages where `estado_civil_anterior = 'Total'` | 1975-2023 |
| `matrimonios_homosexuales_hombres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `analisis.v_matrimonios_homosexuales_anual` | Sum of marriages between men | 2005-2023 |
| `matrimonios_homosexuales_mujeres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `analisis.v_matrimonios_homosexuales_anual` | Sum of marriages between women | 2005-2023 |
| `feminicidios_pareja_expareja` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `analisis.v_feminicidios_pareja_expareja_anual` | Sum of reported femicides (zeros are backfilled when no records exist) | 2003-2024 |
| `huerfanos_menores` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `analisis.v_feminicidios_pareja_expareja_anual` | Sum of orphaned minors (available from 2013 onwards; earlier years remain `NULL`) | 2013-2024 |
| `menores_victimas_mortales` | [`violencia_genero.menores_victimas_mortales`](../Tables/violencia_genero/menores_victimas_mortales.md) | `analisis.v_menores_victimas_mortales_anual` | Sum of victims (zeros are backfilled when no records exist) | 2013-2024 |
| `servicio_016_contactos` | [`violencia_genero.servicio_016`](../Tables/violencia_genero/servicio_016.md) | `analisis.v_servicio_016_anual` | Sum of calls, WhatsApp, emails and chats (zeros are backfilled when no records exist) | 2008-2024 |
| `atenpro_usuarias_activas` | [`violencia_genero.usuarias_atenpro`](../Tables/violencia_genero/usuarias_atenpro.md) | `analisis.v_atenpro_usuarias_activas_anual` | December measurement (end-of-year active users; missing years remain `NULL`) | 2005-2024 |
| `dispositivos_electronicos_seguimiento_activos` | [`violencia_genero.dispositivos_electronicos_seguimiento`](../Tables/violencia_genero/dispositivos_electronicos_seguimiento.md) | `analisis.v_dispositivos_electronicos_seguimiento_anual` | December measurement (end-of-year active devices; missing years remain `NULL`) | 2009-2024 |
| `denuncias_vg_pareja` | [`violencia_genero.denuncias_vg_pareja`](../Tables/violencia_genero/denuncias_vg_pareja.md) | `analisis.v_denuncias_vg_pareja_anual` | Sum of complaints (zeros are backfilled when no records exist) | 2009-2024 |
| `prestaciones_maternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `analisis.v_prestaciones_maternidad_paternidad_anual` | Sum of maternity benefits (`percibidas_madre` + `percibidas_padre` when `tipo = 'Maternidad'`) | 2002-2019 |
| `prestaciones_paternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `analisis.v_prestaciones_maternidad_paternidad_anual` | Sum of paternity benefits (`percibidas_padre` when `tipo = 'Paternidad'`; `NULL` before 2007) | 2007-2019 |
| `tasa_actividad` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Average of the four quarterly totals for the year | 2002-2024 |
| `tasa_empleo` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Average of the four quarterly totals for the year | 2002-2024 |
| `tasa_paro` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Average of the four quarterly totals for the year | 2002-2024 |
| `tasa_bruta_divorcialidad` | [`demografia.tasa_bruta_divorcialidad_provincias`](../Tables/demografia/tasa_bruta_divorcialidad_provincias.md) | `analisis.v_tasa_bruta_divorcialidad_provincial_anual` | Annual divorce rate published for each province | 2005-2023 |
| `promedio_ideologia_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Average reported ideology (0–10) among men | 1979-2024 |
| `porcentaje_ideologia_1_4_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of male respondents with ideology 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of male respondents with ideology 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of male respondents with ideology 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Men naming gender issues as a personal problem | 1979-2024 |
| `porcentaje_problema_espania_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Men naming gender issues as a top issue in Spain | 1979-2024 |
| `promedio_ideologia_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Average reported ideology (0–10) among women | 1979-2024 |
| `porcentaje_ideologia_1_4_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of female respondents with ideology 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of female respondents with ideology 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Share of female respondents with ideology 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Women naming gender issues as a personal problem | 1979-2024 |
| `porcentaje_problema_espania_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_provincias_anual` | Women naming gender issues as a top issue in Spain | 1979-2024 |
