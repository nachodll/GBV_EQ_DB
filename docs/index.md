# Gender Based Violence in Equal Times (GBVEQ)

The project aims to generate a central and unified database of gender-based violence data, integrating explanatory factors, as well as socioeconomic, cultural, and political variables that influence its prevalence.

## Source code

The source code of the project can be found at the <a href="https://github.com/nachodll/GBV_EQ_DB" target="_blank">public Github Repository</a>. This repository contains the following:

- **ETL scripts** for data processing.
- **SQL schema** for the database.
- **Scrapers** used to collect data.
- **Documentation source code** to generate this static page.

## Database

This project's database is not publicly accessible for the moment (currently under development).

- All datasets (raw and clean) can be found at the <a href="https://github.com/nachodll/GBV_EQ_DB_data" target="_blank">private Github Repository</a>. Contact Leire Rincón for access.
- The PostgreSQL database is deployed at a physical server at UAB facilities and access is also private. More on how to access in the following <a href="https://uab-my.sharepoint.com/my?id=%2Fpersonal%2F1781576%5Fuab%5Fcat%2FDocuments%2FDatos%2DGBV%5FET%2FSteps%20to%20connect%20to%20UAB%20db%2023ec1ff81eb480e597e8ec2f25861331%2Ehtml&parent=%2Fpersonal%2F1781576%5Fuab%5Fcat%2FDocuments%2FDatos%2DGBV%5FET" target="_blank">internal document</a>.

## Contact

- Leire Rincón: leire.rincon@uab.cat
- Ignacio Dorado: nachodoradollamas@gmail.com

## Indicators

Tables are distributed in different schemas according to the field to which their data belongs. The main schema, which contains the target variables, is *violencia_genero*. The remaining schemas contain independent socioeconomic, cultural, or political indicators. Following, a summary table for each schema is displayed. 

### 1. violencia_genero

<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/violencia_genero/feminicidios_pareja_expareja/">feminicidios_pareja_expareja</a></td>
            <td>2003-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
        <tr>
            <td><a href="./Tables/violencia_genero/feminicidios_fuera_pareja_expareja/">feminicidios_fuera_pareja_expareja</a></td>
            <td>2022-2025</td>
            <td>Comunidades</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/menores_victimas_mortales/">menores_victimas_mortales</a></td>
            <td>2013-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/servicio_016/">servicio_016</a></td>
            <td>2007-2025 </td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/usuarias_atenpro/">usuarias_atenpro</a></td>
            <td>2005-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/dispositivos_electronicos_seguimiento/">dispositivos_electronicos_seguimiento</a></td>
            <td>2009-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/ayudas_articulo_27/">ayudas_articulo_27</a></td>
            <td>2007-2025</td>
            <td>Comunidades</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/viogen/">viogen</a></td>
            <td>2013-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/autorizaciones_residencia_trabajo_vvg/">autorizaciones_residencia_trabajo_vvg</a></td>
            <td>2006-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/denuncias_vg_pareja/">denuncias_vg_pareja</a></td>
            <td>2009-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/denuncias_vg_presentadas/">denuncias_vg_presentadas</a></td>
            <td>2007-2024</td>
            <td>Comunidades</td>
            <td>Instituto de las Mujeres</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/infracciones_penales_inputadas_vg/">infracciones_penales_inputadas_vg</a></td>
            <td>2011-2024</td>
            <td>Comunidades</td>
            <td>INE</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/ordenes_proteccion/">ordenes_proteccion</a></td>
            <td>2009-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/renta_activa_insercion/">renta_activa_insercion</a></td>
            <td>2006-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/contratos_bonificados_sustitucion/">contratos_bonificados_sustitucion</a></td>
            <td>2003-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/ayudas_cambio_residencia/">ayudas_cambio_residencia</a></td>
            <td>2005-2025</td>
            <td>Provincias</td>
            <td>DGVG</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/encuesta_europea_2022/">encuesta_europea_2022</a></td>
            <td>2022</td>
            <td>Spain</td>
            <td>Eurostat</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/macroencuesta_2019/">macroencuesta_2019</a></td>
            <td>2019</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/macroencuesta_2015/">macroencuesta_2015</a></td>
            <td>2015</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/macroencuesta_2011/">macroencuesta_2011</a></td>
            <td>2011</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr>
            <td><a href="./Tables/violencia_genero/fusion_encuestas/">fusion_encuestas</a></td>
            <td>2015, 2019</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
        </tr>
    </tbody>
</table>

### 2. demografia
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/demografia/poblacion_municipios/">poblacion_municipios</a></td>
            <td>1996-2024</td>
            <td>Municipios</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/poblacion_grupo_edad/">problacion_grupo_edad</a></td>
            <td>1998-2022</td>
            <td>Spain</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/matrimonios_heterosexuales/">matrimonios_heterosexuales</a></td>
            <td>1975-2023</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/matrimonios_homosexuales/">matrimonios_homosexuales</a></td>
            <td>2005-2023</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/tasa_divorcialidad/">tasa_divorcialidad</a></td>
            <td>2005-2023</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/divorcios_segun_duracion_matrimonio/">divorcios_segun_duracion_matrimonio</a></td>
            <td>2005-2023</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/nulidades_separaciones_divorcios/">nulidades_separaciones_divorcios</a></td>
            <td>2013-2024</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/hogares_monoparentales/">hogares_monoparentales</a></td>
            <td>2014-2020</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/tasa_bruta_natalidad/">tasa_bruta_natalidad</a></td>
            <td>1975-2023</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/uso_tiempo/">uso_tiempo</a></td>
            <td>2002-2003, 2009-2010</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
    </tbody>
</table>
</table>

### 3. igualdad_formal
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_dominios/">eige_dominios</a></td>
            <td>2013-2024</td>
            <td>Spain</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_indicadores/">eige_indicadores</a></td>
            <td>2013-2025</td>
            <td>Spain</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_interseccionalidades/">eige_interseccionalidades</a></td>
            <td>2017-2024</td>
            <td>Spain</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_violencia/">eige_violencia</a></td>
            <td>2013, 2024</td>
            <td>Spain</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/ganancia_por_hora_trabajo/">ganancia_por_hora_trabajo</a></td>
            <td>2004-2023</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/mujeres_cargos_autonomicos/">mujeres_cargos_autonomicos</a></td>
            <td>1996-2024</td>
            <td>Comunidades</td>
            <td>Instituto de las Mujeres</td>
        </tr>
    </tbody>
</table>

### 4. politicas_publicas_igualdad_violencia
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/politicas_publicas_igualdad_violencia/legislacion/">legislacion</a></td>
            <td>2001-2025</td>
            <td>Comunidades</td>
            <td>Self-produced (BOE)</td>
        </tr>
        <tr>
            <td><a href="./Tables/politicas_publicas_igualdad_violencia/institutos_mujer/">institutos_mujer</a></td>
            <td>1983-2025</td>
            <td>Comunidades</td>
            <td>Instituto de las Mujeres</td>
        </tr>
        <tr>
            <td><a href="./Tables/politicas_publicas_igualdad_violencia/centros_acogida_emergencia/">centros_acogida_emergencia</a></td>
            <td>2017, 2020, 2022</td>
            <td>Provincias</td>
            <td>DGVG</td>
        </tr>
    </tbody>
</table>

### 5. educacion_juventud

<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/educacion_juventud/excedencias_cuidado_hijos_familiares/">excedencias_cuidado_hijos_familiares</a></td>
            <td>2007-2023</td>
            <td>Provincias</td>
            <td>Ministerio de Trabajo y Economía Social</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/prestaciones_nacimiento_y_cuidado_menor/">prestaciones_nacimiento_y_cuidado_menor</a></td>
            <td>2019-2023</td>
            <td>Provincias</td>
            <td>Ministerio de Trabajo y Economía Social</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/prestaciones_maternidad_paternidad/">prestaciones_maternidad_paternidad</a></td>
            <td>2002-2019</td>
            <td>Provincias</td>
            <td>Ministerio de Trabajo y Economía Social</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/matriculados_educacion_no_universitaria/">matriculados_educacion_no_universitaria</a></td>
            <td>1999-2023</td>
            <td>Provincias</td>
            <td>Ministerio Educacion</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/matriculados_universidad/">matriculados_universidad</a></td>
            <td>1985-2024</td>
            <td>Comunidades</td>
            <td>Ministerio de Ciencia Innovacion y Universidades</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/egresados_universidad/">egresados_universidad</a></td>
            <td>1985-2024</td>
            <td>Comunidades</td>
            <td>Ministerio de Ciencia Innovacion y Universidades</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/nivel_formacion/">nivel_formacion</a></td>
            <td>2004-2023</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
    </tbody>
</table>

### 6. migracion

<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/migracion/residentes_extranjeros/">residentes_extranjeros</a></td>
            <td>1996-2024</td>
            <td>Provincias</td>
            <td>OPI</td>
        </tr>
    </tbody>
</table>

### 7. tecnologia_y_medios
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/acceso_internet_viviendas/">acceso_internet_viviendas</a></td>
            <td>2006-2024</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/uso_internet_personas/">uso_internet_personas</a></td>
            <td>2006-2024</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/uso_internet_ninios/">uso_internet_ninios</a></td>
            <td>2006-2024</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/usuarios_redes_sociales/">usuarios_redes_sociales</a></td>
            <td>2014-2024</td>
            <td>Cities</td>
            <td>Social Media Family</td>
        </tr>
    </tbody>
</table>

### 8. percepcion_social
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/percepcion_social/barometros_generales/">barometros_generales</a></td>
            <td>1979-2025</td>
            <td>Comunidades, Provincias</td>
            <td>CIS</td>
        </tr>
        <tr>
            <td><a href="./Tables/percepcion_social/encuesta_igualdad_2023/">encuesta_igualdad_2023</a></td>
            <td>2023</td>
            <td>Provincias</td>
            <td>CIS</td>
        </tr>
        <tr>
            <td><a href="./Tables/percepcion_social/encuesta_violencia_sexual_2023/">encuesta_violencia_sexual_2023</a></td>
            <td>2023</td>
            <td>Provincias</td>
            <td>CIS</td>
        </tr>
        <tr>
            <td><a href="./Tables/percepcion_social/encuesta_violencia_sexual_2017/">encuesta_violencia_sexual_2017</a></td>
            <td>2017</td>
            <td>Provincias</td>
            <td>CIS</td>
        </tr>
        <tr>
            <td><a href="./Tables/percepcion_social/encuesta_violencia_genero_juventud_2013/">encuesta_violencia_genero_juventud_2013</a></td>
            <td>2013</td>
            <td>Provincias</td>
            <td>CIS</td>
        </tr>
        <tr>
            <td><a href="./Tables/percepcion_social/encuesta_violencia_genero_2012/">encuesta_violencia_genero_2012</a></td>
            <td>2012</td>
            <td>Provincias</td>
            <td>CIS</td>
        </tr>
    </tbody>
</table>

### 9. economia_laboral
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/economia_laboral/tasa_actividad_paro_empleo/">tasa_actividad_paro_empleo</a></td>
            <td>2002-2025</td>
            <td>Provincias</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/economia_laboral/riesgo_pobreza_exclusion/">riesgo_pobreza_exclusion</a></td>
            <td>2008-2024</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
    </tbody>
</table>

### 10. seguridad_criminalidad
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/seguridad_criminalidad/tasas_homicidios_criminalidad/">tasas_homicidios_criminalidad</a></td>
            <td>2010-2023</td>
            <td>Comunidades</td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/seguridad_criminalidad/delitos_sexuales/">delitos_sexuales</a></td>
            <td>2017-2024</td>
            <td>Spain</td>
            <td>INE</td>
        </tr>
    </tbody>
</table>

### 11. salud
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/salud/ive_total/">ive_total</a></td>
            <td>2014-2023</td>
            <td>Spain</td>
            <td>Ministerio Sanidad</td>
        </tr>
        <tr>
            <td><a href="./Tables/salud/ive_grupo_edad/">ive_grupo_edad</a></td>
            <td>2014-2023</td>
            <td>Spain</td>
            <td>Ministerio Sanidad</td>
        </tr>
        <tr>
            <td><a href="./Tables/salud/ive_ccaa/">ive_ccaa</a></td>
            <td>2014-2023</td>
            <td>Comunidades</td>
            <td>Ministerio Sanidad</td>
        </tr>
    </tbody>
</table>

### 12. politica
<table>
    <thead>
        <tr>
            <th>Table</th>
            <th>Time Period</th>
            <th>Regional Breakdown</th>
            <th>Source</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/politica/elecciones_congreso/">elecciones_congreso</a></td>
            <td>1977-2023</td>
            <td>Spain</td>
            <td>Ministerio del Interior</td>
        </tr>
        <tr>
            <td><a href="./Tables/politica/elecciones_parlamentos_autonomicos/">elecciones_parlamentos_autonomicos</a></td>
            <td>1980-2025</td>
            <td>Comunidades</td>
            <td>Junta Electoral Central</td>
        </tr>
        <tr>
            <td><a href="./Tables/politica/presidentes_espania/">presidentes_espania</a></td>
            <td>1979-2023</td>
            <td>Spain</td>
            <td>La Moncloa</td>
        </tr>
        <tr>
            <td><a href="./Tables/politica/presidentes_autonomicos/">presidentes_autonomicos</a></td>
            <td>1980-2025</td>
            <td>Comunidades</td>
            <td>Senado de España</td>
        </tr>
    </tbody>
</table>
