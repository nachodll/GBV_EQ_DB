CREATE TYPE "tipo_feminicidio_enum" AS ENUM('Familiar', 'Sexual', 'Social', 'Vicario');

CREATE TYPE "persona_consulta_enum" AS ENUM(
  'Usuaria',
  'Familiares/Allegados',
  'Otras personas'
);

CREATE TYPE "tipo_violencia_enum" AS ENUM(
  'Pareja/Expareja',
  'Familiar',
  'Sexual',
  'Otras violencias'
);

CREATE TYPE "nivel_riesgo_viogen_enum" AS ENUM(
  'No apreciado',
  'Bajo',
  'Medio',
  'Alto',
  'Extremo'
);

CREATE TYPE "sexo_enum" AS ENUM('Hombre', 'Mujer');

CREATE TYPE "nacionalidad_enum" AS ENUM('Española', 'Extranjera');

CREATE TYPE "origen_denuncia_enum" AS ENUM(
  'Presentada directamente por víctima',
  'Presentada directamente por familiares',
  'Atestados policiales - con denuncia víctima',
  'Atestados policiales - con denuncia familiar',
  'Atestados policiales - por intervención directa policial',
  'Parte de lesiones',
  'Servicios asistencia - Terceros en general'
);

CREATE TYPE "estado_orden_proteccion_enum" AS ENUM(
  'Incoadas',
  'Adoptadas',
  'Denegadas',
  'Inadmitidas',
  'Pendientes'
);

CREATE TYPE "instancia_orden_proteccion_enum" AS ENUM(
  'A instancia de la víctima',
  'A instancia de otras personas',
  'A instancia del Minist. Fiscal',
  'De oficio',
  'A instancia de la Administración'
);

CREATE TYPE "colectivo_contratos_bonificados_sustitucion_enum" AS ENUM(
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

CREATE TYPE "tipo_contrato_enum" AS ENUM('Indefinido', 'Temporal');

CREATE TABLE
  "fuentes" (
    "fuente_id" serial PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

CREATE TABLE
  "fuentes_tablas" (
    "fuentes_tablas_id" serial PRIMARY KEY,
    "fuente_id" int NOT NULL REFERENCES "fuentes" ("fuente_id"),
    "nombre" varchar NOT NULL,
    "fecha_actualizacion" date NOT NULL CHECK (
      fecha_actualizacion >= DATE '1900-01-01'
      AND fecha_actualizacion <= CURRENT_DATE
    ),
    "descripcion" text,
    "url" varchar NOT NULL
  );

CREATE TABLE
  "comunidades_autonomas" (
    "comunidad_autonoma_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

CREATE TABLE
  "provincias" (
    "provincia_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL,
    "comunidad_autonoma_id" int NOT NULL REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id")
  );

CREATE TABLE
  "municipios" (
    "municipio_id" int PRIMARY KEY,
    "nombre" varchar NOT NULL,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id")
  );

CREATE TABLE
  "autorizaciones_residencia" (
    "autorizaciones_residencia_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id")
  );

CREATE TABLE
  "poblacion_municipios" (
    "poblacion_municipios_id" serial PRIMARY KEY,
    "municipio_id" int NOT NULL REFERENCES "municipios" ("municipio_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "sexo" sexo_enum NOT NULL,
    "poblacion" int NOT NULL CHECK (poblacion >= 0)
  );

CREATE TABLE
  "poblacion_grupo_edad" (
    "poblacion_grupo_edad_id" serial PRIMARY KEY,
    "nacionalidad" nacionalidad_enum NOT NULL,
    "sexo" sexo_enum NOT NULL,
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

CREATE TABLE
  "feminicidios_pareja_expareja" (
    "feminicidios_pareja_expareja_id" serial PRIMARY KEY,
    "feminicidios" int NOT NULL CHECK (feminicidios >= 0),
    "huerfanos_menores" int NOT NULL CHECK (huerfanos_menores >= 0),
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
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
  "feminicidios_fuera_pareja_expareja" (
    "feminicidios_fuera_pareja_expareja_id" serial PRIMARY KEY,
    "feminicidios" int NOT NULL CHECK (feminicidios >= 0),
    "tipo_feminicidio" tipo_feminicidio_enum NOT NULL,
    "comunidad_autonoma_id" int NOT NULL REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    )
  );

CREATE TABLE
  "menores_victimas_mortales" (
    "menores_victimas_mortales_id" serial PRIMARY KEY,
    "es_hijo_agresor" boolean NOT NULL,
    "es_victima_vicaria" boolean NOT NULL,
    "menores_victimas_mortales" int NOT NULL CHECK (menores_victimas_mortales >= 0),
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
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
  "servicio_016" (
    "servicio_016_id" serial PRIMARY KEY,
    "provincia_id" int REFERENCES "provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "persona_consulta" persona_consulta_enum,
    "tipo_violencia" tipo_violencia_enum,
    "llamadas" int NOT NULL CHECK (llamadas >= 0),
    "whatsapps" int NOT NULL CHECK (whatsapps >= 0),
    "emails" int NOT NULL CHECK (emails >= 0),
    "chats" int NOT NULL CHECK (chats >= 0)
  );

CREATE TABLE
  "usuarias_atenpro" (
    "usuarias_atenpro_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
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
  "dispositivos_electronicos_seguimiento" (
    "dispositivos_electronicos_seguimiento_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
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
  "ayudas_articulo_27" (
    "ayudas_articulo_27_id" serial PRIMARY KEY,
    "comunidad_autonoma_id" int REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id"),
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
  "viogen" (
    "viogen_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "nivel_riesgo" nivel_riesgo_viogen_enum NOT NULL,
    "casos" int NOT NULL CHECK (casos >= 0),
    "casos_proteccion_policial" int NOT NULL CHECK (casos_proteccion_policial >= 0)
  );

CREATE TABLE
  "autorizaciones_residencia_trabajo_vvg" (
    "autorizaciones_residencia_trabajo_vvg_id" serial PRIMARY KEY,
    "provincia_id" int REFERENCES "provincias" ("provincia_id"),
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
  "denuncias_vg_pareja" (
    "denuncias_vg_pareja_id" serial PRIMARY KEY,
    "origen_denuncia" origen_denuncia_enum NOT NULL,
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
    "denuncias" int NOT NULL CHECK (denuncias >= 0)
  );

CREATE TABLE
  "ordenes_proteccion" (
    "ordenes_proteccion_id" serial PRIMARY KEY,
    "estado_proceso" estado_orden_proteccion_enum NOT NULL,
    "instancia" instancia_orden_proteccion_enum NOT NULL,
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
    "ordenes_proteccion" int NOT NULL CHECK (ordenes_proteccion >= 0)
  );

CREATE TABLE
  "renta_activa_insercion" (
    "renta_activa_insercion_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
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
  "contratos_bonificados_sustitucion" (
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
    "provincia_id" int REFERENCES "provincias" ("provincia_id"),
    "colectivo" colectivo_contratos_bonificados_sustitucion_enum NOT NULL,
    "tipo_contrato" tipo_contrato_enum NOT NULL
  );

CREATE TABLE
  "ayudas_cambio_residencia" (
    "ayudas_cambio_residencia_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL REFERENCES "provincias" ("provincia_id"),
    "anio" int NOT NULL CHECK (
      anio BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "ayudas_cambio_residencia" int NOT NULL CHECK (ayudas_cambio_residencia >= 0)
  );