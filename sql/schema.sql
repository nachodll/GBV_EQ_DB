CREATE SCHEMA metadata;

CREATE SCHEMA geo;

CREATE SCHEMA demografia;

CREATE SCHEMA migracion;

CREATE SCHEMA violencia_genero;

CREATE SCHEMA igualdad_formal;

CREATE SCHEMA educacion_juventud;

CREATE SCHEMA enums;

CREATE SCHEMA tecnologia_y_medios;

CREATE SCHEMA salud;

CREATE SCHEMA politica;

CREATE SCHEMA politicas_publicas_igualdad_violencia;

CREATE SCHEMA percepcion_social;

------------------------------------------------------------------------------------
-- enums
------------------------------------------------------------------------------------
CREATE TYPE enums.tipo_feminicidio_enum AS ENUM('Familiar', 'Sexual', 'Social', 'Vicario');

CREATE TYPE enums.persona_consulta_enum AS ENUM(
  'Usuaria',
  'Familiares/Allegados',
  'Otras personas'
);

CREATE TYPE enums.tipo_violencia_enum AS ENUM(
  'Pareja/Expareja',
  'Familiar',
  'Sexual',
  'Otras violencias'
);

CREATE TYPE enums.nivel_riesgo_viogen_enum AS ENUM(
  'No apreciado',
  'Bajo',
  'Medio',
  'Alto',
  'Extremo'
);

CREATE TYPE enums.sexo_enum AS ENUM('Hombre', 'Mujer', 'Total');

CREATE TYPE enums.origen_denuncia_enum AS ENUM(
  'Presentada directamente por víctima',
  'Presentada directamente por familiares',
  'Atestados policiales - con denuncia víctima',
  'Atestados policiales - con denuncia familiar',
  'Atestados policiales - por intervención directa policial',
  'Parte de lesiones',
  'Servicios asistencia - Terceros en general'
);

CREATE TYPE enums.estado_orden_proteccion_enum AS ENUM(
  'Incoadas',
  'Adoptadas',
  'Denegadas',
  'Inadmitidas',
  'Pendientes'
);

CREATE TYPE enums.instancia_orden_proteccion_enum AS ENUM(
  'A instancia de la víctima',
  'A instancia de otras personas',
  'A instancia del Minist. Fiscal',
  'De oficio',
  'A instancia de la Administración'
);

CREATE TYPE enums.colectivo_contratos_bonificados_sustitucion_enum AS ENUM(
  'Contratos de sustitución por vg',
  'Transformación en indefinidos de contratos de vvg',
  'Trata y mujeres en contexto de prostitución',
  'Violencia de genero',
  'Violencia domestica',
  'Contrato de sustitución por violencia sexual',
  'Transformación en indefinidos de contratos de vdomestica',
  'Violencia sexual',
  'Cargas familiares de vdomestica'
);

CREATE TYPE enums.tipo_contrato_enum AS ENUM('Indefinido', 'Temporal');

CREATE TYPE enums.tipo_documentacino_enum AS ENUM(
  'Certificado de registro',
  'Autorización',
  'TIE-Acuerdo de Retirada'
);

CREATE TYPE enums.tipo_regimen_enum AS ENUM(
  'Régimen General',
  'Régimen de libre circulación UE'
);

------------------------------------------------------------------------------------
-- metadata
------------------------------------------------------------------------------------
CREATE TABLE
  metadata.fuentes (
    fuente_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );

CREATE TABLE
  metadata.fuentes_tablas (
    fuentes_tablas_id serial PRIMARY KEY,
    fuente_id int NOT NULL REFERENCES metadata.fuentes (fuente_id),
    nombre varchar NOT NULL,
    fecha_actualizacion date NOT NULL CHECK (
      fecha_actualizacion >= DATE '1900-01-01'
      AND fecha_actualizacion <= CURRENT_DATE
    ),
    descripcion text,
    url varchar NOT NULL
  );

------------------------------------------------------------------------------------
-- geo
------------------------------------------------------------------------------------
CREATE TABLE
  geo.comunidades_autonomas (
    comunidad_autonoma_id int PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );

CREATE TABLE
  geo.provincias (
    provincia_id int PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id)
  );

CREATE TABLE
  geo.municipios (
    municipio_id int PRIMARY KEY,
    nombre varchar NOT NULL,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id)
  );

CREATE TABLE
  geo.paises (
    pais_id serial PRIMARY KEY,
    nombre varchar UNIQUE NOT NULL
  );

------------------------------------------------------------------------------------
-- migracion
------------------------------------------------------------------------------------
CREATE TABLE
  migracion.residentes_extranjeros (
    residentes_extranjeros_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum,
    es_nacido_espania boolean,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    fecha date NOT NULL CHECK (
      fecha >= DATE '1900-01-01'
      AND fecha <= CURRENT_DATE
    ),
    residentes_extranjeros int NOT NULL CHECK (residentes_extranjeros >= 0),
    tipo_documentacion enums.tipo_documentacino_enum,
    regimen enums.tipo_regimen_enum
  );

------------------------------------------------------------------------------------
-- demografia
------------------------------------------------------------------------------------
CREATE TABLE
  demografia.poblacion_municipios (
    poblacion_municipios_id serial PRIMARY KEY,
    municipio_id int NOT NULL REFERENCES geo.municipios (municipio_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );

CREATE TABLE
  demografia.poblacion_grupo_edad (
    poblacion_grupo_edad_id serial PRIMARY KEY,
    nacionalidad int REFERENCES geo.paises (pais_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    poblacion int NOT NULL CHECK (poblacion >= 0)
  );

CREATE TABLE
  demografia.matrimonios_heterosexuales (
    matrimonios_heterosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    edad varchar NOT NULL CHECK (
      edad ~ '^\d+$'
      OR edad ~ '^<\d+$'
      OR edad ~ '^>\d+$'
    ),
    estado_civil_anterior varchar CHECK (
      estado_civil_anterior IN (
        'Total',
        'Solteros/Solteras',
        'Viudos/Viudas',
        'Divorciados/Divorciadas'
      )
      OR estado_civil_anterior IS NULL
    ),
    matrimonios int NOT NULL CHECK (matrimonios >= 0),
    es_residente_espania boolean NOT NULL
  );

CREATE TABLE
  demografia.matrimonios_homosexuales (
    matrimonios_homosexuales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    conyuge_1_grupo_edad varchar NOT NULL CHECK (
      conyuge_1_grupo_edad ~ '^\d+-\d+$'
      OR conyuge_1_grupo_edad ~ '^<\d+$'
      OR conyuge_1_grupo_edad ~ '^>\d+$'
    ),
    conyuge_2_grupo_edad varchar NOT NULL CHECK (
      conyuge_2_grupo_edad ~ '^\d+-\d+$'
      OR conyuge_2_grupo_edad ~ '^<\d+$'
      OR conyuge_2_grupo_edad ~ '^>\d+$'
    ),
    matrimonios_hombres int NOT NULL CHECK (matrimonios_hombres >= 0),
    matrimonios_mujeres int NOT NULL CHECK (matrimonios_mujeres >= 0),
    es_residente_espania boolean NOT NULL
  );

CREATE TABLE
  demografia.tasa_divorcialidad (
    tasa_divorcialidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    tasa_divorcialidad float NOT NULL CHECK (
      tasa_divorcialidad >= 0
      AND tasa_divorcialidad <= 1000
    )
  );

CREATE TABLE
  demografia.divorcios_segun_duracion_matrimonio (
    divorcios_segun_duracion_matrimonio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    duracion_matrimonio varchar NOT NULL CHECK (
      duracion_matrimonio IN (
        'Menos de 1 año',
        'De 1 año',
        'De 1 a 2 años',
        'De 2 a 4 años',
        'De 3 a 5 años',
        'De 5 a 9 años',
        'De 6 a 10 años',
        'De 10 a 14 años',
        'De 11 a 15 años',
        'De 15 a 19 años',
        'De 16 a 19 años',
        'De 20 a 29 años',
        '20 y más años',
        '30 y más años'
      )
    ),
    porcentaje_divorcios float CHECK (
      porcentaje_divorcios >= 0
      AND porcentaje_divorcios <= 100
    )
  );

CREATE TABLE
  demografia.nulidades_separaciones_divorcios (
    nulidades_separaciones_divorcios_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tipo_disolucion varchar NOT NULL CHECK (
      tipo_disolucion IN ('Nulidades', 'Separaciones', 'Divorcios')
    ),
    disoluciones_matrimoniales int NOT NULL CHECK (disoluciones_matrimoniales >= 0)
  );

CREATE TABLE
  demografia.hogares_monoparentales (
    hogares_monoparentales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    grupo_edad varchar CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    estado_civil varchar CHECK (
      estado_civil IN (
        'Soltero/a',
        'Casado/a',
        'Viudo/a',
        'Separado/a',
        'Divorciado/a'
      )
      OR estado_civil IS NULL
    ),
    hogares_monoparentales float NOT NULL CHECK (hogares_monoparentales >= 0)
  );

CREATE TABLE
  demografia.tasa_bruta_natalidad (
    tasa_bruta_natalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    tasa_bruta_natalidad float NOT NULL CHECK (tasa_bruta_natalidad >= 0)
  );

CREATE TABLE
  demografia.uso_tiempo (
    uso_tiempo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    actividad varchar NOT NULL CHECK (
      actividad IN (
        '0 Cuidados personales',
        '1 Trabajo remunerado',
        '2 Estudios',
        '3 Hogar y familia',
        '4 Trabajo voluntario y reuniones',
        '5 Vida social y diversión',
        '6 Deportes y actividades al aire libre',
        '7 Aficiones e informática',
        '8 Medios de comunicación',
        '9 Trayectos y empleo del tiempo no especificado'
      )
    ),
    horas int NOT NULL CHECK (
      horas >= 0
      AND horas <= 24
    ),
    minutos int NOT NULL CHECK (
      minutos >= 0
      AND minutos < 60
    )
  );

------------------------------------------------------------------------------------
-- violencia_genero
------------------------------------------------------------------------------------
CREATE TABLE
  violencia_genero.feminicidios_pareja_expareja (
    feminicidios_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    huerfanos_menores int CHECK (huerfanos_menores >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    victima_grupo_edad varchar CHECK (
      victima_grupo_edad ~ '^\d+-\d+$'
      OR victima_grupo_edad ~ '^<\d+$'
      OR victima_grupo_edad ~ '^>\d+$'
    ),
    agresor_grupo_edad varchar CHECK (
      agresor_grupo_edad ~ '^\d+-\d+$'
      OR agresor_grupo_edad ~ '^<\d+$'
      OR agresor_grupo_edad ~ '^>\d+$'
    )
  );

CREATE TABLE
  violencia_genero.feminicidios_fuera_pareja_expareja (
    feminicidios_fuera_pareja_expareja_id serial PRIMARY KEY,
    feminicidios int NOT NULL CHECK (feminicidios >= 0),
    tipo_feminicidio enums.tipo_feminicidio_enum NOT NULL,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    )
  );

CREATE TABLE
  violencia_genero.menores_victimas_mortales (
    menores_victimas_mortales_id serial PRIMARY KEY,
    es_hijo_agresor boolean NOT NULL,
    es_victima_vicaria boolean NOT NULL,
    menores_victimas_mortales int NOT NULL CHECK (menores_victimas_mortales >= 0),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12)
  );

CREATE TABLE
  violencia_genero.servicio_016 (
    servicio_016_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    persona_consulta enums.persona_consulta_enum,
    tipo_violencia enums.tipo_violencia_enum,
    llamadas int NOT NULL CHECK (llamadas >= 0),
    whatsapps int NOT NULL CHECK (whatsapps >= 0),
    emails int NOT NULL CHECK (emails >= 0),
    chats int NOT NULL CHECK (chats >= 0)
  );

CREATE TABLE
  violencia_genero.usuarias_atenpro (
    usuarias_atenpro_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    altas int NOT NULL CHECK (altas >= 0),
    bajas int NOT NULL CHECK (bajas >= 0),
    usuarias_activas int NOT NULL CHECK (usuarias_activas >= 0)
  );

CREATE TABLE
  violencia_genero.dispositivos_electronicos_seguimiento (
    dispositivos_electronicos_seguimiento_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    instalaciones_acumuladas int NOT NULL CHECK (instalaciones_acumuladas >= 0),
    desinstalaciones_acumuladas int NOT NULL CHECK (desinstalaciones_acumuladas >= 0),
    dispositivos_activos int NOT NULL CHECK (dispositivos_activos >= 0)
  );

CREATE TABLE
  violencia_genero.ayudas_articulo_27 (
    ayudas_articulo_27_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_concedidas int NOT NULL CHECK (ayudas_concedidas >= 0)
  );

CREATE TABLE
  violencia_genero.viogen (
    viogen_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    nivel_riesgo enums.nivel_riesgo_viogen_enum NOT NULL,
    casos int NOT NULL CHECK (casos >= 0),
    casos_proteccion_policial int NOT NULL CHECK (casos_proteccion_policial >= 0)
  );

CREATE TABLE
  violencia_genero.autorizaciones_residencia_trabajo_vvg (
    autorizaciones_residencia_trabajo_vvg_id serial PRIMARY KEY,
    provincia_id int REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    autorizaciones_concedidas int NOT NULL CHECK (autorizaciones_concedidas >= 0)
  );

CREATE TABLE
  violencia_genero.denuncias_vg_pareja (
    denuncias_vg_pareja_id serial PRIMARY KEY,
    origen_denuncia enums.origen_denuncia_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    denuncias int NOT NULL CHECK (denuncias >= 0)
  );

CREATE TABLE
  violencia_genero.ordenes_proteccion (
    ordenes_proteccion_id serial PRIMARY KEY,
    estado_proceso enums.estado_orden_proteccion_enum NOT NULL,
    instancia enums.instancia_orden_proteccion_enum NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    trimestre int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    ordenes_proteccion int NOT NULL CHECK (ordenes_proteccion >= 0)
  );

CREATE TABLE
  violencia_genero.renta_activa_insercion (
    renta_activa_insercion_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    perceptoras int NOT NULL CHECK (perceptoras >= 0)
  );

CREATE TABLE
  violencia_genero.contratos_bonificados_sustitucion (
    contratos_bonificados_sustitucion_id serial PRIMARY KEY NOT NULL,
    contratos_bonificados int NOT NULL CHECK (contratos_bonificados >= 0),
    contratos_sustitucion int NOT NULL CHECK (contratos_sustitucion >= 0),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    colectivo enums.colectivo_contratos_bonificados_sustitucion_enum NOT NULL,
    tipo_contrato enums.tipo_contrato_enum NOT NULL
  );

CREATE TABLE
  violencia_genero.ayudas_cambio_residencia (
    ayudas_cambio_residencia_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ayudas_cambio_residencia int NOT NULL CHECK (ayudas_cambio_residencia >= 0)
  );

CREATE TABLE
  violencia_genero.denuncias_vg_presentadas (
    denuncias_vg_presentadas_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    denuncias_presentadas int NOT NULL CHECK (denuncias_presentadas >= 0)
  );

CREATE TABLE
  violencia_genero.infracciones_penales_inputadas_vg (
    infracciones_penales_inputadas_vg_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_infraccion text NOT NULL CHECK (
      tipo_infraccion IN (
        'Delitos',
        'Homicidio y sus formas',
        'Lesiones',
        'Detenciones ilegales y secuestro',
        'Amenazas',
        'Coacciones',
        'Torturas e integridad moral',
        'Agresiones sexuales',
        'Abusos sexuales',
        'Abusos y agresiones sexuales a menores de 16 años',
        'Allanamiento de morada',
        'Injurias',
        'Daños',
        'Quebrantamiento de condena',
        'Otros delitos sin especificar',
        'Faltas',
        'Faltas contra las personas',
        'Otras faltas sin especificar'
      )
    ),
    infracciones_penales_inputadas int NOT NULL CHECK (infracciones_penales_inputadas >= 0)
  );

CREATE TABLE
  violencia_genero.encuesta_europea_2022 (
    encuesta_europea_2022_id serial PRIMARY KEY,
    variables_json jsonb NOT NULL
  );

CREATE TABLE
  violencia_genero.macroencuesta_2019 (
    macroencuesta_2019_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );

CREATE TABLE
  violencia_genero.macroencuesta_2015 (
    macroencuesta_2015_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );

CREATE TABLE
  violencia_genero.macroencuesta_2011 (
    macroencuesta_2011_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );

CREATE TABLE
  violencia_genero.fusion_encuestas (
    fusion_encuestas_id serial PRIMARY KEY,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    codigo_estudio int NOT NULL,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    violencia_sexual_1_pareja boolean NOT NULL,
    violencia_sexual_1_fuera_pareja boolean NOT NULL,
    violencia_sexual_2_pareja boolean NOT NULL,
    violencia_sexual_3_pareja boolean NOT NULL,
    violencia_fisica_1_pareja boolean NOT NULL,
    violencia_fisica_2_pareja boolean NOT NULL,
    violencia_fisica_2_fuera_pareja boolean NOT NULL,
    violencia_fisica_3_pareja boolean NOT NULL,
    violencia_fisica_4_pareja boolean NOT NULL,
    violencia_fisica_5_pareja boolean NOT NULL,
    violencia_fisica_5_fuera_pareja boolean NOT NULL,
    violencia_fisica_6_pareja boolean NOT NULL,
    violencia_fisica_6_fuera_pareja boolean NOT NULL
  );

------------------------------------------------------------------------------------
-- igualdad_formal
------------------------------------------------------------------------------------
CREATE TYPE enums.eige_dominio_subdominio_enum AS ENUM(
  'Access to health structures (Subdomain score)',
  'Attainment and participation (Subdomain score)',
  'Care activities (Subdomain score)',
  'Economic power (Subdomain score)',
  'Economic situation (Subdomain score)',
  'Financial resources (Subdomain score)',
  'Health (Domain score)',
  'Health status (Subdomain score)',
  'Healthy behaviour (Subdomain score)',
  'Knowledge (Domain score)',
  'Money (Domain score)',
  'Overall Gender Equality Index',
  'Participation in work (Subdomain score)',
  'Political power (Subdomain score)',
  'Power (Domain score)',
  'Segregation (Subdomain score)',
  'Segregation and quality of work (Subdomain score)',
  'Social activities (Subdomain score)',
  'Social power (Subdomain score)',
  'Time (Domain score)',
  'Work (Domain score)'
);

CREATE TABLE
  igualdad_formal.eige_dominios (
    eige_dominio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    dominio_subdominio enums.eige_dominio_subdominio_enum NOT NULL,
    valor numeric NOT NULL CHECK (valor >= 0)
  );

CREATE TABLE
  igualdad_formal.eige_indicadores (
    eige_indicador_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int NOT NULL CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL
  );

CREATE TYPE enums.eige_interseccionalidades_enum AS ENUM(
  'Couple with children',
  'Couple without children',
  'With disability',
  'High educated',
  'Low educated',
  'Medium educated',
  'EU-born',
  'Foreign born',
  'Lone parent',
  'Native born',
  'Non-EU-born',
  'Without disability',
  'Single',
  '15/16/18-24',
  '25-34',
  '25-49',
  '35-44',
  '45-64',
  '50-64',
  '65-74',
  '65+',
  '75+'
);

CREATE TABLE
  igualdad_formal.eige_interseccionalidades (
    eige_interseccionalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL,
    interseccionalidad enums.eige_interseccionalidades_enum NOT NULL
  );

CREATE TABLE
  igualdad_formal.eige_violencia (
    eige_violencia_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo.paises (pais_id),
    indicador text NOT NULL,
    valor int NOT NULL CHECK (valor >= 0)
  );

CREATE TABLE
  igualdad_formal.ganancia_por_hora_trabajo (
    ganancia_por_hora_trabajo_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    sector_actividad text NOT NULL CHECK (
      sector_actividad IN (
        'Todos los sectores',
        'Industria',
        'Construcción',
        'Servicios'
      )
    ),
    ganancia_por_hora_trabajo float NOT NULL CHECK (ganancia_por_hora_trabajo >= 0)
  );

CREATE TABLE
  igualdad_formal.mujeres_cargos_autonomicos (
    mujeres_cargos_autonomicos_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    sexo enums.sexo_enum NOT NULL,
    numero_cargos int NOT NULL CHECK (numero_cargos >= 0)
  );

------------------------------------------------------------------------------------
-- educacion_juventud
------------------------------------------------------------------------------------
CREATE TYPE enums.titularidad_centro_ensenanza_enum AS ENUM(
  'Público',
  'Privado',
  'Privado concertado',
  'Privado no concertado'
);

CREATE TABLE
  educacion_juventud.matriculados_educacion_no_universitaria (
    matriculados_educacion_no_universitaria_id serial PRIMARY KEY,
    titularidad enums.titularidad_centro_ensenanza_enum NOT NULL,
    curso varchar NOT NULL CHECK (
      curso ~ '^\d{4}-\d{2}$'
      AND (
        substring(curso, 1, 4)::int BETWEEN 1900 AND EXTRACT(
          YEAR
          FROM
            CURRENT_DATE
        )
      )
      AND (
        substring(curso, 6, 2)::int = (substring(curso, 3, 2)::int + 1) % 100
      )
    ),
    sexo enums.sexo_enum,
    provincia_id int NOT NULL REFERENCES geo.provincias (provincia_id),
    ensenianza varchar NOT NULL,
    matriculados int NOT NULL CHECK (matriculados >= 0)
  );

CREATE TABLE
  educacion_juventud.matriculados_universidad (
    matriculados_universidad_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nivel_academico text NOT NULL CHECK (
      nivel_academico IN (
        'Total',
        'Grado',
        '1º y 2º ciclo',
        'Máster',
        'Doctorado'
      )
    ),
    tipo_universidad text CHECK (
      tipo_universidad IN ('Total', 'Pública', 'Privada')
    ),
    modalidad_universidad text CHECK (
      modalidad_universidad IN (
        'Total',
        'Presencial',
        'No Presencial',
        'Especial'
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    rama_conocimiento text NOT NULL CHECK (
      rama_conocimiento IN (
        'Total',
        'Ciencias Sociales y Jurídicas',
        'Ingeniería y Arquitectura',
        'Artes y Humanidades',
        'Ciencias de la Salud',
        'Ciencias'
      )
    ),
    curso varchar NOT NULL CHECK (
      curso ~ '^\d{4}-\d{2}$'
      AND (
        substring(curso, 1, 4)::int BETWEEN 1900 AND EXTRACT(
          YEAR
          FROM
            CURRENT_DATE
        )
      )
      AND (
        substring(curso, 6, 2)::int = (substring(curso, 3, 2)::int + 1) % 100
      )
    ),
    matriculados int NOT NULL CHECK (matriculados >= 0)
  );

CREATE TABLE
  educacion_juventud.egresados_universidad (
    egresados_universidad_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nivel_academico text NOT NULL CHECK (
      nivel_academico IN (
        'Total',
        'Grado',
        '1º y 2º ciclo',
        'Máster',
        'Doctorado'
      )
    ),
    tipo_universidad text CHECK (
      tipo_universidad IN ('Total', 'Pública', 'Privada')
    ),
    modalidad_universidad text CHECK (
      modalidad_universidad IN (
        'Total',
        'Presencial',
        'No Presencial',
        'Especial'
      )
    ),
    sexo enums.sexo_enum NOT NULL,
    rama_conocimiento text NOT NULL CHECK (
      rama_conocimiento IN (
        'Total',
        'Ciencias Sociales y Jurídicas',
        'Ingeniería y Arquitectura',
        'Artes y Humanidades',
        'Ciencias de la Salud',
        'Ciencias'
      )
    ),
    curso varchar NOT NULL CHECK (
      curso ~ '^\d{4}-\d{2}$'
      AND (
        substring(curso, 1, 4)::int BETWEEN 1900 AND EXTRACT(
          YEAR
          FROM
            CURRENT_DATE
        )
      )
      AND (
        substring(curso, 6, 2)::int = (substring(curso, 3, 2)::int + 1) % 100
      )
    ),
    egresados int NOT NULL CHECK (egresados >= 0)
  );

------------------------------------------------------------------------------------
-- tecnologia_y_medios
------------------------------------------------------------------------------------
CREATE TABLE
  tecnologia_y_medios.acceso_internet_viviendas (
    acceso_internet_viviendas_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_equipamiento text NOT NULL CHECK (
      tipo_equipamiento IN (
        'Viviendas con algún tipo de ordenador',
        'Viviendas que disponen de acceso a Internet',
        'Viviendas con conexión de Banda Ancha  (ADSL, Red de cable, etc.)',
        'Viviendas con teléfono fijo',
        'Viviendas con teléfono móvil'
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    )
  );

CREATE TABLE
  tecnologia_y_medios.uso_internet_personas (
    uso_internet_personas_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_uso text NOT NULL CHECK (
      tipo_uso IN (
        'Personas que han utilizado Internet en los últimos 3 meses',
        'Personas que han utilizado Internet diariamente (al menos 5 días a la semana)',
        'Personas que han comprado a través de Internet en los últimos 3 meses',
        'Personas que usan el teléfono móvil'
      )
    )
  );

CREATE TABLE
  tecnologia_y_medios.uso_internet_ninios (
    uso_internet_ninios_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    porcentaje numeric NOT NULL CHECK (
      porcentaje >= 0
      AND porcentaje <= 100
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tipo_uso text NOT NULL CHECK (
      tipo_uso IN (
        'Niños usuarios de Internet en los últimos 3 meses',
        'Niños que disponen de teléfono móvil',
        'Niños usuarios de ordenador en los últimos 3 meses'
      )
    )
  );

CREATE TABLE
  tecnologia_y_medios.usuarios_redes_sociales (
    usuarios_redes_sociales_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    ciudad text NOT NULL CHECK (ciudad ~ '^[A-Za-zÀ-ÿ\s]+$'),
    red_social text NOT NULL CHECK (
      red_social IN (
        'Facebook',
        'Instagram',
        'Twitter',
        'TikTok',
        'LinkedIn',
        'YouTube'
      )
    ),
    usuarios int NOT NULL CHECK (usuarios >= 0)
  );

------------------------------------------------------------------------------------
-- salud
------------------------------------------------------------------------------------
CREATE TABLE
  salud.ive_total (
    ive_total_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    centros_notificadores int NOT NULL CHECK (centros_notificadores >= 0),
    ives int NOT NULL CHECK (ives >= 0),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );

CREATE TABLE
  salud.ive_grupo_edad (
    ive_grupo_edad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    grupo_edad varchar NOT NULL CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );

CREATE TABLE
  salud.ive_ccaa (
    ive_ccaa_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    tasa float NOT NULL CHECK (
      tasa >= 0
      AND tasa <= 1000
    )
  );

------------------------------------------------------------------------------------
-- politica
------------------------------------------------------------------------------------
CREATE TABLE
  politica.elecciones_congreso (
    elecciones_congreso_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    mes int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );

CREATE TABLE
  politica.presidentes_espania (
    presidentes_espania_id serial PRIMARY KEY,
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    cese date CHECK (
      cese <= CURRENT_DATE
      AND cese >= nombramiento
    ),
    partidos_gobierno text NOT NULL,
    tipo_mayoria text NOT NULL CHECK (
      tipo_mayoria IN ('Absoluta', 'Simple', 'Minoría', 'En funciones')
    )
  );

CREATE TABLE
  politica.presidentes_autonomicos (
    presidentes_autonomicos_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    legislatura varchar NOT NULL CHECK (
      legislatura ~ '^(?=[MDCLXVI])M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    ),
    presidente varchar NOT NULL,
    nombramiento date NOT NULL CHECK (nombramiento <= CURRENT_DATE),
    partido text NOT NULL
  );

CREATE TABLE
  politica.elecciones_parlamentos_autonomicos (
    elecciones_parlamentos_autonomicos_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    candidatura varchar NOT NULL,
    votos int NOT NULL CHECK (votos >= 0),
    representantes int NOT NULL CHECK (representantes >= 0)
  );

------------------------------------------------------------------------------------
-- politicas_publicas_igualdad_violencia
------------------------------------------------------------------------------------
CREATE TABLE
  politicas_publicas_igualdad_violencia.legislacion (
    legislacion_id serial PRIMARY KEY,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    fecha_aprobacion date NOT NULL CHECK (fecha_aprobacion <= CURRENT_DATE),
    enlace_boe text NOT NULL,
    tematica text NOT NULL CHECK (tematica IN ('Violencia de género', 'Igualdad')),
    vigente boolean NOT NULL,
    fecha_derogacion date CHECK (
      fecha_derogacion <= CURRENT_DATE
      AND fecha_derogacion >= fecha_aprobacion
    )
  );

CREATE TABLE
  politicas_publicas_igualdad_violencia.institutos_mujer (
    institutos_mujer_id serial PRIMARY KEY,
    comunidad_autonoma_id int NOT NULL REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    nombre text NOT NULL,
    anio_fundacion int CHECK (
      anio_fundacion BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    enlace text
  );

------------------------------------------------------------------------------------
-- percepcion_social
------------------------------------------------------------------------------------
CREATE TABLE
  percepcion_social.barometros_generales (
    barometros_generales_id serial PRIMARY KEY,
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    cuestionario int,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    edad int CHECK (edad BETWEEN 1 AND 150),
    sexo enums.sexo_enum,
    ideologia int CHECK (ideologia BETWEEN 1 AND 10),
    religiosidad varchar CHECK (
      religiosidad IN (
        'Ateo/a',
        'Agnóstico/a',
        'Indiferente, no creyente',
        'Católico/a',
        'Católico/a practicante',
        'Católico/a no practicante',
        'Creyente de otra religión'
      )
      OR religiosidad IS NULL
    ),
    problema_personal_1 text,
    problema_personal_2 text,
    problema_personal_3 text,
    problema_espania_1 text,
    problema_espania_2 text,
    problema_espania_3 text
  );

CREATE TABLE
  percepcion_social.encuesta_igualdad_2023 (
    encuesta_igualdad_2023_id serial PRIMARY KEY,
    codigo_estudio varchar(4) NOT NULL CHECK (codigo_estudio ~ '^\d{4}$'),
    fecha date NOT NULL CHECK (fecha <= CURRENT_DATE),
    cuestionario int NOT NULL,
    comunidad_autonoma_id int REFERENCES geo.comunidades_autonomas (comunidad_autonoma_id),
    provincia_id int REFERENCES geo.provincias (provincia_id),
    variables_json jsonb NOT NULL
  );

------------------------------------------------------------------------------------
-- Grant permissions to readonly user over all schemas
------------------------------------------------------------------------------------
DO $$
DECLARE
    schema_rec RECORD;
BEGIN
    FOR schema_rec IN
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
    LOOP
        EXECUTE format('GRANT USAGE ON SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %I TO gbv_db_user_readonly;', schema_rec.schema_name);
        EXECUTE format('ALTER DEFAULT PRIVILEGES IN SCHEMA %I GRANT SELECT ON TABLES TO gbv_db_user_readonly;', schema_rec.schema_name);
    END LOOP;
END
$$;