# analisis.v_indicadores_anuales_comunidades_unificados

The `analisis.v_indicadores_anuales_comunidades_unificados` view brings together the main annual indicators that can be observed at the level of Spain's autonomous communities. Each row represents a `(anio, comunidad_autonoma_id, comunidad_autonoma)` combination, providing a one-stop table to join territorial indicators without losing the community universe.

> **⚠️ Warning**
> The metrics listed below are already aggregated by autonomous community. Several source datasets also publish records without territorial detail (for example, national totals). Summing across communities may therefore **not** match the official national totals. Always review the original table documentation before rolling up these indicators beyond the community level.

> **📝 Note** 
> This page describes the shape of the unified view. Definitions, methodological notes, and caveats for every indicator are documented in the respective source table pages linked below.

## Source views and aggregations

Most measures come from the provincial annual indicators and are summed (or otherwise aggregated) to the community level. Others originate from datasets that are already reported by community. The table below summarises the content grouped by theme.

### Demographics

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `poblacion_comunidad` | [`demografia.poblacion_municipios`](../Tables/demografia/poblacion_municipios.md) | `analisis.v_poblacion_provincial` | Sum of provincial population (men and women) | 1996-2024 |
| `matrimonios_heterosexuales` | [`demografia.matrimonios_heterosexuales`](../Tables/demografia/matrimonios_heterosexuales.md) | `matrimonios_het_ccaa` | Sum of provincial annual totals | 1975-2023 |
| `matrimonios_homosexuales_hombres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `matrimonios_hom_ccaa` | Sum of provincial marriages between men | 2005-2023 |
| `matrimonios_homosexuales_mujeres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `matrimonios_hom_ccaa` | Sum of provincial marriages between women | 2005-2023 |
| `tasa_bruta_divorcialidad` | [`demografia.tasa_bruta_divorcialidad_comunidades`](../Tables/demografia/tasa_bruta_divorcialidad_comunidades.md) | `analisis.v_tasa_bruta_divorcialidad_comunidades_anual` | Published annual divorce rate by community | 2005-2023 |

### Education

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `matriculados_universidad` | [`educacion_juventud.matriculados_universidad`](../Tables/educacion_juventud/matriculados_universidad.md) | `analisis.v_matriculados_universidad_comunidades_anual` | Sum of enrolments (total sex, level, university type and field) | 1985-2024 |

### Gender-based violence and protection

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `feminicidios_pareja_expareja` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `feminicidios_ccaa` | Sum of provincial annual totals | 2003-2024 |
| `huerfanos_menores` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `feminicidios_ccaa` | Sum of provincial orphaned minors | 2013-2024 |
| `feminicidios_fuera_pareja_expareja` | [`violencia_genero.feminicidios_fuera_pareja_expareja`](../Tables/violencia_genero/feminicidios_fuera_pareja_expareja.md) | `analisis.v_feminicidios_fuera_pareja_expareja_comunidades_anual` | Sum of community-level annual totals (missing data filled with 0) | 2022-2024 |
| `menores_victimas_mortales` | [`violencia_genero.menores_victimas_mortales`](../Tables/violencia_genero/menores_victimas_mortales.md) | `menores_victimas_ccaa` | Sum of provincial annual totals (0 when no record) | 2013-2024 |
| `servicio_016_contactos` | [`violencia_genero.servicio_016`](../Tables/violencia_genero/servicio_016.md) | `servicio_016_ccaa` | Sum of provincial contacts (calls, WhatsApp, email, chat) | 2008-2024 |
| `atenpro_usuarias_activas` | [`violencia_genero.usuarias_atenpro`](../Tables/violencia_genero/usuarias_atenpro.md) | `atenpro_ccaa` | Sum of provincial December measurements (end-of-year snapshot) | 2005-2024 |
| `dispositivos_electronicos_seguimiento_activos` | [`violencia_genero.dispositivos_electronicos_seguimiento`](../Tables/violencia_genero/dispositivos_electronicos_seguimiento.md) | `dispositivos_ccaa` | Sum of provincial December measurements (end-of-year snapshot) | 2009-2024 |
| `denuncias_vg_pareja` | [`violencia_genero.denuncias_vg_pareja`](../Tables/violencia_genero/denuncias_vg_pareja.md) | `denuncias_ccaa` | Sum of provincial annual totals (0 when no record) | 2009-2024 |
| `denuncias_vg_presentadas` | [`violencia_genero.denuncias_vg_presentadas`](../Tables/violencia_genero/denuncias_vg_presentadas.md) | `analisis.v_denuncias_vg_presentadas_comunidades_anual` | Community totals reported by Consejo General del Poder Judicial | 2007-2024 |

### Social benefits

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `prestaciones_maternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `prestaciones_ccaa` | Sum of provincial maternity benefits (`percibidas_madre` + `percibidas_padre`) | 2002-2019 |
| `prestaciones_paternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `prestaciones_ccaa` | Sum of provincial paternity benefits (`percibidas_padre`; `NULL` before 2007) | 2007-2019 |

### Labour market and income

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `tasa_paro` | [`economia_laboral.tasa_paro_comunidades`](../Tables/economia_laboral/tasa_paro_comunidades.md) | `analisis.v_tasa_paro_comunidades_anual` | Average of the four quarterly values | 2002-2024 |
| `ganancia_por_hora_trabajo` | [`igualdad_formal.ganancia_por_hora_trabajo`](../Tables/igualdad_formal/ganancia_por_hora_trabajo.md) | `analisis.v_ganancia_por_hora_trabajo_comunidades_anual` | Average hourly earnings (total sex, all sectors) | 2004-2023 |
| `porcentaje_mujeres_cargos_autonomicos` | [`igualdad_formal.mujeres_cargos_autonomicos`](../Tables/igualdad_formal/mujeres_cargos_autonomicos.md) | `analisis.v_mujeres_cargos_autonomicos_anual` | Share of women among regional government seats | 1996-2024 |

### Digital inclusion

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `porcentaje_acceso_internet_viviendas` | [`tecnologia_y_medios.acceso_internet_viviendas`](../Tables/tecnologia_y_medios/acceso_internet_viviendas.md) | `analisis.v_acceso_internet_viviendas_comunidades_anual` | Percentage of households with internet access | 2006-2024 |
| `porcentaje_uso_internet_diario_personas` | [`tecnologia_y_medios.uso_internet_personas`](../Tables/tecnologia_y_medios/uso_internet_personas.md) | `analisis.v_acceso_internet_personas_comunidades_anual` | Percentage of people using the internet daily | 2006-2024 |
| `porcentaje_ninios_con_telefono_movil` | [`tecnologia_y_medios.uso_internet_ninios`](../Tables/tecnologia_y_medios/uso_internet_ninios.md) | `analisis.v_uso_internet_ninios_comunidades_anual` | Percentage of children owning a mobile phone | 2006-2024 |

### Social inclusion

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `porcentaje_arope` | [`economia_laboral.riesgo_pobreza_exclusion`](../Tables/economia_laboral/riesgo_pobreza_exclusion.md) | `analisis.v_riesgo_pobreza_exclusion_social_comunidades_anual` | AROPE indicator reported by community | 2008-2024 |

### Safety and justice

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `tasa_homicidios` | [`seguridad_criminalidad.tasas_homicidios_criminalidad`](../Tables/seguridad_criminalidad/tasas_homicidios_criminalidad.md) | `analisis.v_tasas_homicidios_criminalidad_comunidades_anual` | Community-level homicide rate | 2010-2023 |
| `tasa_criminalidad` | [`seguridad_criminalidad.tasas_homicidios_criminalidad`](../Tables/seguridad_criminalidad/tasas_homicidios_criminalidad.md) | `analisis.v_tasas_homicidios_criminalidad_comunidades_anual` | Community-level crime rate (per 100,000 inhabitants) | 2010-2023 |

### Health

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `tasa_ive` | [`salud.ive_ccaa`](../Tables/salud/ive_ccaa.md) | `analisis.v_ive_comunidades_anual` | Voluntary interruption of pregnancy rate | 2014-2023 |

### Policy context

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `fecha_primera_ley_violencia` | [`politicas_publicas_igualdad_violencia.legislacion`](../Tables/politicas_publicas_igualdad_violencia/legislacion.md) | `analisis.v_legislacion_primera_ley_autonomica` | Date of approval of the first specific regional law on gender violence, repeated annually | 1975-2024 |
| `fecha_primera_ley_igualdad` | [`politicas_publicas_igualdad_violencia.legislacion`](../Tables/politicas_publicas_igualdad_violencia/legislacion.md) | `analisis.v_legislacion_primera_ley_autonomica` | Date of approval of the first specific regional law on gender equality, repeated annually | 1975-2024 |
| `existe_instituto_mujer` | [`politicas_publicas_igualdad_violencia.institutos_mujer`](../Tables/politicas_publicas_igualdad_violencia/institutos_mujer.md) | `analisis.v_instituto_mujer_autonomico` | Boolean flag indicating whether a women's institute existed that year-comunidad | 1975-2024 |
| `presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Main president (most days in office) during the year | 1977-2024 |
| `partido_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Party of the main president | 1977-2024 |
| `fecha_nombramiento_presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Appointment date of the main president | 1977-2024 |
| `fecha_fin_presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | President's departure date from government | 1977-2024 |
| `cambio_presidente_durante_anio` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Flag indicating multiple presidents within the year | 1977-2024 |
| `presidentes_completo` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Concatenated list of all presidents in the year | 1977-2024 |

### Public perception

| Indicator | Source table | Intermediate view | Aggregation logic | Time period |
| --- | --- | --- | --- | --- |
| `promedio_ideologia_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Average reported ideology (0–10) among men | 1979-2024 |
| `porcentaje_ideologia_1_4_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of male respondents with ideology 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of male respondents with ideology 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of male respondents with ideology 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Men naming gender issues as a personal problem | 1979-2024 |
| `porcentaje_problema_espania_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Men naming gender issues as a top issue in Spain | 1979-2024 |
| `promedio_ideologia_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Average reported ideology (0–10) among women | 1979-2024 |
| `porcentaje_ideologia_1_4_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of female respondents with ideology 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of female respondents with ideology 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Share of female respondents with ideology 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Women naming gender issues as a personal problem | 1979-2024 |
| `porcentaje_problema_espania_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Women naming gender issues as a top issue in Spain | 1979-2024 |
