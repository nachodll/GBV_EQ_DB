# Violencia de Género en Tiempos de Igualdad (GBVEQ)

El proyecto tiene como objetivo generar una base de datos central y unificada sobre violencia de género, integrando factores explicativos, así como variables socioeconómicas, culturales y políticas que influyen en su prevalencia.

## Código fuente

El código fuente del proyecto se encuentra en el <a href="https://github.com/nachodll/GBV_EQ_DB" target="_blank">repositorio público de Github</a>. Este repositorio contiene:

- **Scripts ETL** para el procesamiento de datos.
- **Esquema SQL** de la base de datos.
- **Scrapers** utilizados para recopilar datos.
- **Código de la documentación** que genera esta página estática.

## Base de datos

La base de datos de este proyecto no es de acceso público por el momento (actualmente en desarrollo).

- Todos los conjuntos de datos (crudos y limpios) se encuentran en el <a href="https://github.com/nachodll/GBV_EQ_DB_data" target="_blank">repositorio privado de Github</a>. Contactar con Leire Rincón para obtener acceso.
- La base de datos PostgreSQL está desplegada en un servidor físico en las instalaciones de la UAB y el acceso también es privado. Más información sobre cómo acceder en el siguiente <a href="https://uab-my.sharepoint.com/my?id=%2Fpersonal%2F1781576%5Fuab%5Fcat%2FDocuments%2FDatos%2DGBV%5FET%2FSteps%20to%20connect%20to%20UAB%20db%2023ec1ff81eb480e597e8ec2f25861331%2Ehtml&parent=%2Fpersonal%2F1781576%5Fuab%5Fcat%2FDocuments%2FDatos%2DGBV%5FET" target="_blank">documento interno</a>.

## Contacto

- Leire Rincón: leire.rincon@uab.cat
- Ignacio Dorado: nachodoradollamas@gmail.com

## Indicadores

Las tablas se distribuyen en diferentes esquemas según el ámbito al que pertenecen los datos. El esquema principal, que contiene las variables objetivo, es *violencia_genero*. Los esquemas restantes contienen indicadores socioeconómicos, culturales o políticos independientes. A continuación se muestra una tabla resumen para cada esquema.

### 1. violencia_genero
<table>
    <thead>
        <tr>
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <td>España</td>
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
        </tr>
    </tbody>
</table>

### 2. demografia
<table>
    <thead>
        <tr>
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <td>España</td>
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
            <td>2012-2024</td>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_dominios/">eige_dominios</a></td>
            <td>2013-2024</td>
            <td>España</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_indicadores/">eige_indicadores</a></td>
            <td>2013-2025</td>
            <td>España</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_interseccionalidades/">eige_interseccionalidades</a></td>
            <td>2017-2024</td>
            <td>España</td>
            <td>EIGE</td>
        </tr>
        <tr>
            <td><a href="./Tables/igualdad_formal/eige_violencia/">eige_violencia</a></td>
            <td>2013, 2024</td>
            <td>España</td>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <td>1999-2023</td>
            <td>Provincias</td>
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

### 6. migracion

<table>
    <thead>
        <tr>
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="./Tables/salud/ive_total/">ive_total</a></td>
            <td>2014-2023</td>
            <td>España</td>
            <td>Ministerio Sanidad</td>
        </tr>
        <tr>
            <td><a href="./Tables/salud/ive_grupo_edad/">ive_grupo_edad</a></td>
            <td>2014-2023</td>
            <td>España</td>
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

### 11. politica
<table>
    <thead>
        <tr>
            <th>Tabla</th>
            <th>Periodo temporal</th>
            <th>Desagregación regional</th>
            <th>Fuente</th>
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
