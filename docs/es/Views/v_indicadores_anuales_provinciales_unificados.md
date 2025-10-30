# analisis.v_indicadores_anuales_provinciales_unificados

La vista `analisis.v_indicadores_anuales_provinciales_unificados` reúne los principales indicadores anuales disponibles a nivel provincial. Cada año aporta 52 filas (una por provincia) y cualquier indicador sin datos para una combinación provincia-año permanece en `NULL` dentro del resultado. Así se pueden cruzar otras tablas anuales provinciales sin perder cobertura geográfica.

## Vistas origen

La vista unificada combina las vistas intermedias definidas en `sql/views.sql`. Todas alinean sus resultados sobre las mismas claves `(anio, provincia_id)` antes de unirse.

### Indicadores incluidos

| Indicador | Tabla | Vista intermedia | Lógica de agregación | Periodo temporal |
| --- | --- | --- | --- | --- |
| `poblacion_provincia` | [`demografia.poblacion_municipios`](../Tables/demografia/poblacion_municipios.md) | `analisis.v_poblacion_provincial` | Suma de la población municipal de mujeres y hombres | 1996-2024 |
| `matrimonios_heterosexuales` | [`demografia.matrimonios_heterosexuales`](../Tables/demografia/matrimonios_heterosexuales.md) | `analisis.v_matrimonios_heterosexuales_anual` | Suma de matrimonios con `estado_civil_anterior = 'Total'` | 1975-2023 |
| `matrimonios_homosexuales_hombres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `analisis.v_matrimonios_homosexuales_anual` | Suma de matrimonios entre hombres | 2005-2023 |
| `matrimonios_homosexuales_mujeres` | [`demografia.matrimonios_homosexuales`](../Tables/demografia/matrimonios_homosexuales.md) | `analisis.v_matrimonios_homosexuales_anual` | Suma de matrimonios entre mujeres | 2005-2023 |
| `feminicidios_pareja_expareja` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `analisis.v_feminicidios_pareja_expareja_anual` | Suma de casos registrados (se rellenan ceros cuando no hay registros) | 2003-2024 |
| `huerfanos_menores` | [`violencia_genero.feminicidios_pareja_expareja`](../Tables/violencia_genero/feminicidios_pareja_expareja.md) | `analisis.v_feminicidios_pareja_expareja_anual` | Suma de menores huérfanos (disponible desde 2013; años previos quedan en `NULL`) | 2013-2024 |
| `menores_victimas_mortales` | [`violencia_genero.menores_victimas_mortales`](../Tables/violencia_genero/menores_victimas_mortales.md) | `analisis.v_menores_victimas_mortales_anual` | Suma de víctimas (se rellenan ceros cuando no hay registros) | 2013-2024 |
| `servicio_016_contactos` | [`violencia_genero.servicio_016`](../Tables/violencia_genero/servicio_016.md) | `analisis.v_servicio_016_anual` | Suma de llamadas, WhatsApp, emails y chats (se rellenan ceros cuando no hay registros) | 2008-2024 |
| `atenpro_usuarias_activas` | [`violencia_genero.usuarias_atenpro`](../Tables/violencia_genero/usuarias_atenpro.md) | `analisis.v_atenpro_usuarias_activas_anual` | Medición de diciembre (valor de final de año; los años sin dato quedan en `NULL`) | 2005-2024 |
| `dispositivos_electronicos_seguimiento_activos` | [`violencia_genero.dispositivos_electronicos_seguimiento`](../Tables/violencia_genero/dispositivos_electronicos_seguimiento.md) | `analisis.v_dispositivos_electronicos_seguimiento_anual` | Medición de diciembre (valor de final de año; los años sin dato quedan en `NULL`) | 2009-2024 |
| `denuncias_vg_pareja` | [`violencia_genero.denuncias_vg_pareja`](../Tables/violencia_genero/denuncias_vg_pareja.md) | `analisis.v_denuncias_vg_pareja_anual` | Suma de denuncias (se rellenan ceros cuando no hay registros) | 2009-2024 |
| `prestaciones_maternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `analisis.v_prestaciones_maternidad_paternidad_anual` | Suma de prestaciones de maternidad (`percibidas_madre` + `percibidas_padre` cuando `tipo = 'Maternidad'`) | 2002-2019 |
| `prestaciones_paternidad` | [`educacion_juventud.prestaciones_maternidad_paternidad`](../Tables/educacion_juventud/prestaciones_maternidad_paternidad.md) | `analisis.v_prestaciones_maternidad_paternidad_anual` | Suma de prestaciones de paternidad (`percibidas_padre` cuando `tipo = 'Paternidad'`; `NULL` antes de 2007) | 2007-2019 |
| `tasa_actividad` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Promedio de los cuatro totales trimestrales del año | 2002-2024 |
| `tasa_empleo` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Promedio de los cuatro totales trimestrales del año | 2002-2024 |
| `tasa_paro` | [`economia_laboral.tasa_actividad_paro_empleo_provincias`](../Tables/economia_laboral/tasa_actividad_paro_empleo_provincias.md) | `analisis.v_tasa_actividad_paro_empleo_anual` | Promedio de los cuatro totales trimestrales del año | 2002-2024 |
