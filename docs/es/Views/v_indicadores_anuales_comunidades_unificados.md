# analisis.v_indicadores_anuales_comunidades_unificados

La vista `analisis.v_indicadores_anuales_comunidades_unificados` reúne los principales indicadores anuales disponibles para las comunidades autónomas españolas. Cada fila representa una combinación `(anio, comunidad_autonoma_id, comunidad_autonoma)`, lo que facilita cruzar indicadores territoriales sin perder cobertura autonómica.

> **⚠️ Aviso**
> Las métricas listadas ya están agregadas a nivel autonómico. Varias fuentes publican también registros sin detalle territorial (por ejemplo, totales estatales). Por ello, sumar las comunidades **no** siempre coincide con los totales nacionales oficiales. Revisa la documentación original antes de agregar los indicadores por encima del ámbito autonómico.

>**📝 Nota**     
>Esta página describe la estructura de la vista unificada. Las definiciones, notas metodológicas y advertencias de cada indicador se encuentran en la documentación de las tablas origen enlazadas a continuación.

## Vistas y agregaciones origen

La mayoría de medidas provienen de los indicadores provinciales anuales y se agregan (mediante sumas u otros cálculos) hasta la comunidad autónoma. Otras se nutren de conjuntos de datos ya publicados a nivel autonómico. La siguiente tabla resume el contenido agrupado por temática.

### Demografía

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `poblacion_comunidad` | [`demografia.poblacion_municipios`](../Tables/demografia/poblacion_municipios.md) | `analisis.v_poblacion_provincial` | Suma de población provincial (mujeres y hombres) | 1996-2024 |
| `matrimonios_heterosexuales` | [`demografia.matrimonios_heterosexuales`](../Tables/demografia/matrimonios_heterosexuales.md) | `matrimonios_het_ccaa` | Suma de totales provinciales anuales | 1975-2023 |
| `matrimonios_homosexuales_hombres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `matrimonios_hom_ccaa` | Suma de matrimonios provinciales entre hombres | 2005-2023 |
| `matrimonios_homosexuales_mujeres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `matrimonios_hom_ccaa` | Suma de matrimonios provinciales entre mujeres | 2005-2023 |
| `tasa_bruta_divorcialidad` | [`demografia.tasa_bruta_divorcialidad_comunidades`](../Tables/demografia/tasa_bruta_divorcialidad_comunidades.md) | `analisis.v_tasa_bruta_divorcialidad_comunidades_anual` | Tasa anual publicada para cada comunidad | 2005-2023 |

### Educación

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `matriculados_universidad` | [`educacion_juventud.matriculados_universidad`](../Tables/educacion_juventud/matriculados_universidad.md) | `analisis.v_matriculados_universidad_comunidades_anual` | Suma de matrículas (sexo, nivel, tipo y rama = Total) | 1985-2024 |

### Violencia de género y protección

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `feminicidios_pareja_expareja` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `feminicidios_ccaa` | Suma de totales provinciales anuales | 2003-2024 |
| `huerfanos_menores` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `feminicidios_ccaa` | Suma de menores huérfanos provinciales | 2013-2024 |
| `feminicidios_fuera_pareja_expareja` | [`violencia_genero.feminicidios_fuera_pareja_expareja`](../Tables/violencia_genero/feminicidios_fuera_pareja_expareja.md) | `analisis.v_feminicidios_fuera_pareja_expareja_comunidades_anual` | Suma de totales autonómicos (faltas de datos rellenadas con 0) | 2022-2024 |
| `menores_victimas_mortales` | [`violencia_genero.menores_victimas_mortales`](../Tables/violencia_genero/menores_victimas_mortales.md) | `menores_victimas_ccaa` | Suma de totales provinciales (0 cuando no hay registro) | 2013-2024 |
| `servicio_016_contactos` | [`violencia_genero.servicio_016`](../Tables/violencia_genero/servicio_016.md) | `servicio_016_ccaa` | Suma de contactos provinciales (llamadas, WhatsApp, email, chat) | 2008-2024 |
| `atenpro_usuarias_activas` | [`violencia_genero.usuarias_atenpro`](../Tables/violencia_genero/usuarias_atenpro.md) | `atenpro_ccaa` | Suma de mediciones de diciembre provinciales (foto fin de año) | 2005-2024 |
| `dispositivos_electronicos_seguimiento_activos` | [`violencia_genero.dispositivos_electronicos_seguimiento`](../Tables/violencia_genero/dispositivos_electronicos_seguimiento.md) | `dispositivos_ccaa` | Suma de mediciones de diciembre provinciales (foto fin de año) | 2009-2024 |
| `denuncias_vg_pareja` | [`violencia_genero.denuncias_vg_pareja`](../Tables/violencia_genero/denuncias_vg_pareja.md) | `denuncias_ccaa` | Suma de totales provinciales (0 cuando no hay registro) | 2009-2024 |
| `denuncias_vg_presentadas` | [`violencia_genero.denuncias_vg_presentadas`](../Tables/violencia_genero/denuncias_vg_presentadas.md) | `analisis.v_denuncias_vg_presentadas_comunidades_anual` | Totales autonómicos del Consejo General del Poder Judicial | 2007-2024 |

### Prestaciones sociales

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `prestaciones_maternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `prestaciones_ccaa` | Suma de prestaciones provinciales (`percibidas_madre` + `percibidas_padre`) | 2002-2019 |
| `prestaciones_paternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `prestaciones_ccaa` | Suma de prestaciones provinciales (`percibidas_padre`; `NULL` antes de 2007) | 2007-2019 |

### Mercado laboral e ingresos

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `tasa_paro` | [`economia_laboral.tasa_paro_comunidades`](../Tables/economia_laboral/tasa_paro_comunidades.md) | `analisis.v_tasa_paro_comunidades_anual` | Promedio de los cuatro valores trimestrales | 2002-2024 |
| `ganancia_por_hora_trabajo` | [`igualdad_formal.ganancia_por_hora_trabajo`](../Tables/igualdad_formal/ganancia_por_hora_trabajo.md) | `analisis.v_ganancia_por_hora_trabajo_comunidades_anual` | Ganancia media por hora (sexo total, todos los sectores) | 2004-2023 |
| `porcentaje_mujeres_cargos_autonomicos` | [`igualdad_formal.mujeres_cargos_autonomicos`](../Tables/igualdad_formal/mujeres_cargos_autonomicos.md) | `analisis.v_mujeres_cargos_autonomicos_anual` | Porcentaje de mujeres en cargos autonómicos | 1996-2024 |

### Inclusión digital

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `porcentaje_acceso_internet_viviendas` | [`tecnologia_y_medios.acceso_internet_viviendas`](../Tables/tecnologia_y_medios/acceso_internet_viviendas.md) | `analisis.v_acceso_internet_viviendas_comunidades_anual` | Porcentaje de hogares con acceso a internet | 2006-2024 |
| `porcentaje_uso_internet_diario_personas` | [`tecnologia_y_medios.uso_internet_personas`](../Tables/tecnologia_y_medios/uso_internet_personas.md) | `analisis.v_acceso_internet_personas_comunidades_anual` | Porcentaje de personas que usan internet a diario | 2006-2024 |
| `porcentaje_ninios_con_telefono_movil` | [`tecnologia_y_medios.uso_internet_ninios`](../Tables/tecnologia_y_medios/uso_internet_ninios.md) | `analisis.v_uso_internet_ninios_comunidades_anual` | Porcentaje de menores con teléfono móvil | 2006-2024 |

### Inclusión social

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `porcentaje_arope` | [`economia_laboral.riesgo_pobreza_exclusion`](../Tables/economia_laboral/riesgo_pobreza_exclusion.md) | `analisis.v_riesgo_pobreza_exclusion_social_comunidades_anual` | Indicador AROPE publicado por comunidad | 2008-2024 |

### Seguridad y justicia

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `tasa_homicidios` | [`seguridad_criminalidad.tasas_homicidios_criminalidad`](../Tables/seguridad_criminalidad/tasas_homicidios_criminalidad.md) | `analisis.v_tasas_homicidios_criminalidad_comunidades_anual` | Tasa autonómica de homicidios | 2010-2023 |
| `tasa_criminalidad` | [`seguridad_criminalidad.tasas_homicidios_criminalidad`](../Tables/seguridad_criminalidad/tasas_homicidios_criminalidad.md) | `analisis.v_tasas_homicidios_criminalidad_comunidades_anual` | Tasa autonómica de criminalidad (por 100,000 habitantes) | 2010-2023 |

### Salud

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `tasa_ive` | [`salud.ive_ccaa`](../Tables/salud/ive_ccaa.md) | `analisis.v_ive_comunidades_anual` | Tasa de interrupción voluntaria del embarazo | 2014-2023 |

### Contexto institucional

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `fecha_primera_ley_violencia` | [`politicas_publicas_igualdad_violencia.legislacion`](../Tables/politicas_publicas_igualdad_violencia/legislacion.md) | `analisis.v_legislacion_primera_ley_autonomica` | Fecha de aprobacion de la primera ley autonómica especifica en violencia de genero, repetida cada año  | 1975-2024 |
| `fecha_primera_ley_igualdad` | [`politicas_publicas_igualdad_violencia.legislacion`](../Tables/politicas_publicas_igualdad_violencia/legislacion.md) | `analisis.v_legislacion_primera_ley_autonomica` | Fecha de aprobacion de la primera ley autonómica especifica en igualdad de genero , repetida cada año | 1975-2024 |
| `existe_instituto_mujer` | [`politicas_publicas_igualdad_violencia.institutos_mujer`](../Tables/politicas_publicas_igualdad_violencia/institutos_mujer.md) | `analisis.v_instituto_mujer_autonomico` | Indicador booleano de existencia de instituto de la mujer para dicho año-ccaa | 1975-2024 |
| `presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Presidente con más días en el cargo ese año | 1977-2024 |
| `partido_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Partido del presidente principal | 1977-2024 |
| `fecha_nombramiento_presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Fecha de nombramiento del presidente principal | 1977-2024 |
| `fecha_fin_presidente_principal` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Fecha de salida del gobierno del presidente | 1977-2024 |
| `cambio_presidente_durante_anio` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Indicador de cambios de presidencia dentro del año | 1977-2024 |
| `presidentes_completo` | [`politica.presidentes_autonomicos`](../Tables/politica/presidentes_autonomicos.md) | `analisis.v_presidentes_autonomicos_anual` | Lista concatenada de todos los presidentes del año | 1977-2024 |

### Percepción social

| Indicador | Tabla origen | Vista intermedia | Lógica de agregación | Periodo |
| --- | --- | --- | --- | --- |
| `promedio_ideologia_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Ideología media declarada (0–10) entre hombres | 1979-2024 |
| `porcentaje_ideologia_1_4_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de hombres con ideología 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de hombres con ideología 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de hombres con ideología 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Hombres que señalan la violencia/igualdad de género como problema personal | 1979-2024 |
| `porcentaje_problema_espania_genero_hombres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Hombres que señalan la violencia/igualdad de género como problema en España | 1979-2024 |
| `promedio_ideologia_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Ideología media declarada (0–10) entre mujeres | 1979-2024 |
| `porcentaje_ideologia_1_4_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de mujeres con ideología 1–4 | 1979-2024 |
| `porcentaje_ideologia_5_6_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de mujeres con ideología 5–6 | 1979-2024 |
| `porcentaje_ideologia_7_10_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Porcentaje de mujeres con ideología 7–10 | 1979-2024 |
| `porcentaje_problema_personal_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Mujeres que señalan la violencia/igualdad de género como problema personal | 1979-2024 |
| `porcentaje_problema_espania_genero_mujeres` | [`percepcion_social.barometros_generales`](../Tables/percepcion_social/barometros_generales.md) | `analisis.v_barometros_generales_comunidades_anual` | Mujeres que señalan la violencia/igualdad de género como problema en España | 1979-2024 |
