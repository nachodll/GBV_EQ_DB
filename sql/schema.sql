CREATE SCHEMA metadata;

CREATE SCHEMA geo;

CREATE SCHEMA demografia;

CREATE SCHEMA migracion;

CREATE SCHEMA violencia_genero;

CREATE SCHEMA igualdad_formal;

CREATE SCHEMA enums;

------------------------------------------------------------------------------------
-- enums
------------------------------------------------------------------------------------
CREATE TYPE enums."tipo_feminicidio_enum" AS ENUM('Familiar', 'Sexual', 'Social', 'Vicario');

CREATE TYPE enums."persona_consulta_enum" AS ENUM(
  'Usuaria',
  'Familiares/Allegados',
  'Otras personas'
);

CREATE TYPE enums."tipo_violencia_enum" AS ENUM(
  'Pareja/Expareja',
  'Familiar',
  'Sexual',
  'Otras violencias'
);

CREATE TYPE enums."nivel_riesgo_viogen_enum" AS ENUM(
  'No apreciado',
  'Bajo',
  'Medio',
  'Alto',
  'Extremo'
);

CREATE TYPE enums."sexo_enum" AS ENUM('Hombre', 'Mujer');

CREATE TYPE enums."origen_denuncia_enum" AS ENUM(
  'Presentada directamente por víctima',
  'Presentada directamente por familiares',
  'Atestados policiales - con denuncia víctima',
  'Atestados policiales - con denuncia familiar',
  'Atestados policiales - por intervención directa policial',
  'Parte de lesiones',
  'Servicios asistencia - Terceros en general'
);

CREATE TYPE enums."estado_orden_proteccion_enum" AS ENUM(
  'Incoadas',
  'Adoptadas',
  'Denegadas',
  'Inadmitidas',
  'Pendientes'
);

CREATE TYPE enums."instancia_orden_proteccion_enum" AS ENUM(
  'A instancia de la víctima',
  'A instancia de otras personas',
  'A instancia del Minist. Fiscal',
  'De oficio',
  'A instancia de la Administración'
);

CREATE TYPE enums."colectivo_contratos_bonificados_sustitucion_enum" AS ENUM(
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

CREATE TYPE enums."tipo_contrato_enum" AS ENUM('Indefinido', 'Temporal');

CREATE TYPE enums."tipo_documentacino_enum" AS ENUM(
  'Certificado de registro',
  'Autorización',
  'TIE-Acuerdo de Retirada'
);

CREATE TYPE enums."tipo_regimen_enum" AS ENUM(
  'Régimen General',
  'Régimen de libre circulación UE'
);

------------------------------------------------------------------------------------
-- metadata
------------------------------------------------------------------------------------
CREATE TABLE
  metadata."fuentes" (
    "fuente_id" serial PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

CREATE TABLE
  metadata."fuentes_tablas" (
    "fuentes_tablas_id" serial PRIMARY KEY,
    "fuente_id" int NOT NULL REFERENCES metadata."fuentes" ("fuente_id"),
    "nombre" varchar NOT NULL,
    "fecha_actualizacion" date NOT NULL CHECK (
      fecha_actualizacion >= DATE '1900-01-01'
      AND fecha_actualizacion <= CURRENT_DATE
    ),
    "descripcion" text,
    "url" varchar NOT NULL
  );

------------------------------------------------------------------------------------
-- geo
------------------------------------------------------------------------------------
CREATE TABLE
  geo."comunidades_autonomas" (
    "comunidad_autonoma_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

CREATE TABLE
  geo."provincias" (
    "provincia_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL,
    "comunidad_autonoma_id" int NOT NULL REFERENCES geo."comunidades_autonomas" ("comunidad_autonoma_id")
  );

CREATE TABLE
  geo."municipios" (
    "municipio_id" int PRIMARY KEY,
    "nombre" varchar NOT NULL,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id")
  );

CREATE TABLE
  geo."paises" (
    "pais_id" serial PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

------------------------------------------------------------------------------------
-- migracion
------------------------------------------------------------------------------------
CREATE TABLE
  migracion."personas_autorizacion_residencia" (
    "personas_autorizacion_residencia_id" serial PRIMARY KEY,
    "provincia_id" int REFERENCES geo."provincias" ("provincia_id"),
    "nacionalidad" int REFERENCES geo."paises" ("pais_id"),
    "sexo" enums.sexo_enum NOT NULL,
    "es_nacido_espania" boolean,
    "grupo_edad" varchar CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    "fecha" date NOT NULL CHECK (
      fecha >= DATE '1900-01-01'
      AND fecha <= CURRENT_DATE
    ),
    "personas_autorizacion_residencia" int NOT NULL CHECK (personas_autorizacion_residencia >= 0),
    "tipo_documentacion" enums.tipo_documentacino_enum,
    "regimen" enums.tipo_regimen_enum NOT NULL
  );

------------------------------------------------------------------------------------
-- demografia
------------------------------------------------------------------------------------
CREATE TABLE
  demografia."poblacion_municipios" (
    "poblacion_municipios_id" serial PRIMARY KEY,
    "municipio_id" int NOT NULL REFERENCES geo."municipios" ("municipio_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "sexo" enums.sexo_enum NOT NULL,
    "poblacion" int NOT NULL CHECK (poblacion >= 0)
  );

CREATE TABLE
  demografia."poblacion_grupo_edad" (
    "poblacion_grupo_edad_id" serial PRIMARY KEY,
    "nacionalidad" int REFERENCES geo."paises" ("pais_id"),
    "sexo" enums.sexo_enum NOT NULL,
    "grupo_edad" varchar NOT NULL CHECK (
      grupo_edad ~ '^\d+-\d+$'
      OR grupo_edad ~ '^<\d+$'
      OR grupo_edad ~ '^>\d+$'
    ),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "poblacion" int NOT NULL CHECK (poblacion >= 0)
  );

------------------------------------------------------------------------------------
-- violencia_genero
------------------------------------------------------------------------------------
CREATE TABLE
  violencia_genero."feminicidios_pareja_expareja" (
    "feminicidios_pareja_expareja_id" serial PRIMARY KEY,
    "feminicidios" int NOT NULL CHECK (feminicidios >= 0),
    "huerfanos_menores" int NOT NULL CHECK (huerfanos_menores >= 0),
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "victima_grupo_edad" varchar CHECK (
      victima_grupo_edad ~ '^\d+-\d+$'
      OR victima_grupo_edad ~ '^<\d+$'
      OR victima_grupo_edad ~ '^>\d+$'
    ),
    "agresor_grupo_edad" varchar CHECK (
      agresor_grupo_edad ~ '^\d+-\d+$'
      OR agresor_grupo_edad ~ '^<\d+$'
      OR agresor_grupo_edad ~ '^>\d+$'
    )
  );

CREATE TABLE
  violencia_genero."feminicidios_fuera_pareja_expareja" (
    "feminicidios_fuera_pareja_expareja_id" serial PRIMARY KEY,
    "feminicidios" int NOT NULL CHECK (feminicidios >= 0),
    "tipo_feminicidio" enums.tipo_feminicidio_enum NOT NULL,
    "comunidad_autonoma_id" int NOT NULL REFERENCES geo."comunidades_autonomas" ("comunidad_autonoma_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    )
  );

CREATE TABLE
  violencia_genero."menores_victimas_mortales" (
    "menores_victimas_mortales_id" serial PRIMARY KEY,
    "es_hijo_agresor" boolean NOT NULL,
    "es_victima_vicaria" boolean NOT NULL,
    "menores_victimas_mortales" int NOT NULL CHECK (menores_victimas_mortales >= 0),
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12)
  );

CREATE TABLE
  violencia_genero."servicio_016" (
    "servicio_016_id" serial PRIMARY KEY,
    "provincia_id" int REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "persona_consulta" enums.persona_consulta_enum,
    "tipo_violencia" enums.tipo_violencia_enum,
    "llamadas" int NOT NULL CHECK (llamadas >= 0),
    "whatsapps" int NOT NULL CHECK (whatsapps >= 0),
    "emails" int NOT NULL CHECK (emails >= 0),
    "chats" int NOT NULL CHECK (chats >= 0)
  );

CREATE TABLE
  violencia_genero."usuarias_atenpro" (
    "usuarias_atenpro_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "altas" int NOT NULL CHECK (altas >= 0),
    "bajas" int NOT NULL CHECK (bajas >= 0),
    "usuarias_activas" int NOT NULL CHECK (usuarias_activas >= 0)
  );

CREATE TABLE
  violencia_genero."dispositivos_electronicos_seguimiento" (
    "dispositivos_electronicos_seguimiento_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "instalaciones_acumuladas" int NOT NULL CHECK (instalaciones_acumuladas >= 0),
    "desinstalaciones_acumuladas" int NOT NULL CHECK (desinstalaciones_acumuladas >= 0),
    "dispositivos_activos" int NOT NULL CHECK (dispositivos_activos >= 0)
  );

CREATE TABLE
  violencia_genero."ayudas_articulo_27" (
    "ayudas_articulo_27_id" serial PRIMARY KEY,
    "comunidad_autonoma_id" int REFERENCES geo."comunidades_autonomas" ("comunidad_autonoma_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "ayudas_concedidas" int NOT NULL CHECK (ayudas_concedidas >= 0)
  );

CREATE TABLE
  violencia_genero."viogen" (
    "viogen_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "nivel_riesgo" enums.nivel_riesgo_viogen_enum NOT NULL,
    "casos" int NOT NULL CHECK (casos >= 0),
    "casos_proteccion_policial" int NOT NULL CHECK (casos_proteccion_policial >= 0)
  );

CREATE TABLE
  violencia_genero."autorizaciones_residencia_trabajo_vvg" (
    "autorizaciones_residencia_trabajo_vvg_id" serial PRIMARY KEY,
    "provincia_id" int REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "autorizaciones_concedidas" int NOT NULL CHECK (autorizaciones_concedidas >= 0)
  );

CREATE TABLE
  violencia_genero."denuncias_vg_pareja" (
    "denuncias_vg_pareja_id" serial PRIMARY KEY,
    "origen_denuncia" enums.origen_denuncia_enum NOT NULL,
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "denuncias" int NOT NULL CHECK (denuncias >= 0)
  );

CREATE TABLE
  violencia_genero."ordenes_proteccion" (
    "ordenes_proteccion_id" serial PRIMARY KEY,
    "estado_proceso" enums.estado_orden_proteccion_enum NOT NULL,
    "instancia" enums.instancia_orden_proteccion_enum NOT NULL,
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "ordenes_proteccion" int NOT NULL CHECK (ordenes_proteccion >= 0)
  );

CREATE TABLE
  violencia_genero."renta_activa_insercion" (
    "renta_activa_insercion_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "perceptoras" int NOT NULL CHECK (perceptoras >= 0)
  );

CREATE TABLE
  violencia_genero."contratos_bonificados_sustitucion" (
    "contratos_bonificados_sustitucion_id" serial PRIMARY KEY NOT NULL,
    "contratos_bonificados" int NOT NULL CHECK (contratos_bonificados >= 0),
    "contratos_sustitucion" int NOT NULL CHECK (contratos_sustitucion >= 0),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "provincia_id" int REFERENCES geo."provincias" ("provincia_id"),
    "colectivo" enums.colectivo_contratos_bonificados_sustitucion_enum NOT NULL,
    "tipo_contrato" enums.tipo_contrato_enum NOT NULL
  );

CREATE TABLE
  violencia_genero."ayudas_cambio_residencia" (
    "ayudas_cambio_residencia_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES geo."provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "ayudas_cambio_residencia" int NOT NULL CHECK (ayudas_cambio_residencia >= 0)
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
  igualdad_formal."eige_dominios" (
    eige_dominio_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo."paises" ("pais_id"),
    dominio_subdominio enums."eige_dominio_subdominio_enum" NOT NULL,
    valor numeric NOT NULL CHECK (valor >= 0)
  );

CREATE TABLE
  igualdad_formal."eige_indicadores" (
    eige_indicador_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo."paises" ("pais_id"),
    indicador text NOT NULL,
    valor int NOT NULL CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL
  );

CREATE TYPE enums."eige_interseccionalidades_enum" AS ENUM(
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
  igualdad_formal."eige_interseccionalidades" (
    eige_interseccionalidad_id serial PRIMARY KEY,
    anio int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    pais_id int NOT NULL REFERENCES geo."paises" ("pais_id"),
    indicador text NOT NULL,
    valor int CHECK (valor >= 0),
    sexo enums.sexo_enum NOT NULL,
    interseccionalidad enums."eige_interseccionalidades_enum" NOT NULL
  );