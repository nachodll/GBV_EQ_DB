# Gender Based Violence in Equal Times (GBVEQ)

The project aims to generate a central and unified database of gender-based violence data, integrating explanatory factors, as well as socioeconomic, cultural, and political variables that influence its prevalence.

## Source code

The source code of the project can be found at the <a href="https://github.com/nachodll/GBV_EQ_DB" target="_blank">public Github Repository</a>. This repository contains the following:

- **ETL scripts** for data processing
- **SQL schema** for the database
- **Scrapers** used to collect data
- **Documentation** source code (generates this static page)

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
            <tr style="background-color: #f8ccccff;">
            <td>Encuesta Europea 2023</td>
            <td>2024</td>
            <td>Nacional</td>
            <td>Eurostat</td>
            </tr>
            <tr style="background-color: #f8ccccff;">
            <td>Macroencuesta 2019</td>
            <td>2019</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr style="background-color: #f8ccccff;">
            <td>Macroencuesta 2015</td>
            <td>2015</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr style="background-color: #f8ccccff;">
            <td>Macroencuesta 2011</td>
            <td>2011</td>
            <td>Provincias</td>
            <td>CIS</td>
            </tr>
            <tr style="background-color: #f8ccccff;">
            <td>Denuncias Violencia de Género</td>
            <td>2007-2024</td>
            <td>Comunidades</td>
            <td>Instituto de las Mujeres</td>
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
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/demografia/poblacion_grupo_edad/">problacion_grupo_edad</a></td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Matrimonios entre personas de diferente sexo</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Matrimonios entre personas de diferente sexo por Estado Civil Anterior</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Matrimonios entre hombres</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Matrimonios entre mujeres</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Tasa de divoricialidad por sexo y edad</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Proporción de divorcios según grupo de duración de matrimonio</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Nulidades, separaciones y divorcios</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Hogares monoparentales</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Tasa Bruta Natalidad</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Empleo del Tiempo 2009</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Empleo del Tiempo 2002</td>
            <td></td>
            <td></td>
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
            <td></td>
            <td></td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_indicadores/">eige_indicadores</a></td>
            <td></td>
            <td></td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_interseccionalidades/">eige_interseccionalidades</a></td>
            <td></td>
            <td></td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_violencia/">eige_violencia</a></td>
            <td></td>
            <td></td>
            <td>EIGE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Ganancia por Hora Trabajo</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Ganancia por Hora Trabajo</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Mujeres en cargos autonómicos</td>
            <td></td>
            <td></td>
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
        <tr style="background-color: #f8ccccff;">
            <td>Legislación VDG</td>
            <td></td>
            <td></td>
            <td>BOE</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Organismos de igualdad</td>
            <td></td>
            <td></td>
            <td>Instituto de las Mujeres</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Recursos autonómicos en VG</td>
            <td></td>
            <td></td>
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
        <tr style="background-color: #f8ccccff;">
            <td>Excendencias y Permisos Maternidad/Paternidad</td>
            <td></td>
            <td></td>
            <td>Seguridad Social</td>
        </tr>
        <tr>
            <td><a href="./Tables/educacion_juventud/matriculados_educacion_no_universitaria/">matriculados_educacion_no_universitaria</a></td>
            <td></td>
            <td></td>
            <td>Ministerio Educacion</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Matriculados Universidad</td>
            <td></td>
            <td></td>
            <td>Ministerio de Ciencia, Educación y Universidades</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Egresados Universidad</td>
            <td></td>
            <td></td>
            <td>Ministerio de Ciencia, Educación y Universidades</td>
        </tr>
    </tbody>
</table>

### 6. migiracion

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
            <td></td>
            <td></td>
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
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/uso_internet_personas/">uso_internet_personas</a></td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/uso_internet_ninios/">uso_internet_ninios</a></td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
        </tr>
        <tr>
            <td><a href="./Tables/tecnologia_y_medios/usuarios_redes_sociales/">usuarios_redes_sociales</a></td>
            <td>2014-2024</td>
            <td>Cities</td>
            <td>Social Media Family</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Pornografia - Google trends</td>
            <td></td>
            <td></td>
            <td>Google Trends</td>
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
        <tr style="background-color: #f8ccccff;">
            <td>Barómetros Generales</td>
            <td></td>
            <td></td>
            <td>CIS</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Barómetro: Percepciones sobre la igualdad entre hombres y mujeres</td>
            <td></td>
            <td></td>
            <td>CIS</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Barómetro: la violencia sexual contra las mujeres</td>
            <td></td>
            <td></td>
            <td>CIS</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Barómetro: percepción social de la violencia sexual</td>
            <td></td>
            <td></td>
            <td>CIS</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Barómetro: Percepción social de la violencia de género por la adolescencia y la juventud</td>
            <td></td>
            <td></td>
            <td>CIS</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Barómetro: percepción social de la violencia de género</td>
            <td></td>
            <td></td>
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
        <tr style="background-color: #f8ccccff;">
            <td>Tasas de Actividad, Paro y Empleo</td>
            <td></td>
            <td></td>
            <td>INE</td>
        </tr>
    </tbody>
</table>

### 10. salud
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
        <tr style="background-color: #f8ccccff;">
            <td>Interrupciones Voluntarias del Embarazo</td>
            <td></td>
            <td></td>
            <td>Ministerio Sanidad</td>
        </tr>
    </tbody>
</table>

### 11. politica
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
        <tr style="background-color: #f8ccccff;">
            <td>Composición histórica congreso de los diputados</td>
            <td></td>
            <td></td>
            <td>Ministerio Interior</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Presidentes de España</td>
            <td></td>
            <td></td>
            <td>Moncloa</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Presidentes autonómicos</td>
            <td></td>
            <td></td>
            <td>Senado</td>
        </tr>
        <tr style="background-color: #f8ccccff;">
            <td>Composición histórica parlamentos autonómicos</td>
            <td></td>
            <td></td>
            <td>Gobiernos Autonómicos</td>
        </tr>
    </tbody>
</table>