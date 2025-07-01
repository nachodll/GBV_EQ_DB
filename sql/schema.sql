CREATE TYPE "tipo_feminicidio_enum" AS ENUM ('Familiar', 'Sexual', 'Social', 'Vicario');

CREATE TYPE "persona_consulta_enum" AS ENUM (
  'Usuaria',
  'Familiares/Allegados',
  'Otras personas',
  'No consta'
);

CREATE TYPE "tipo_violencia_enum" AS ENUM (
  'Pareja/Expareja',
  'No desagregada',
  'Familiar',
  'Sexual',
  'Otras violencias'
);

CREATE TYPE "nivel_riesgo_viogen_enum" AS ENUM (
  'No apreciado',
  'Bajo',
  'Medio',
  'Alto',
  'Extremo'
);

CREATE TYPE "origen_denuncia_enum" AS ENUM (
  'Presentada directamente por víctima',
  'Presentada directamente por familiares',
  'Atestados policiales - con denuncia víctima',
  'Atestados policiales - con denuncia familiar',
  'Atestados policiales - por intervención directa policial',
  'Parte de lesiones',
  'Servicios asistencia - Terceros en general'
);

CREATE TYPE "estado_orden_proteccion_enum" AS ENUM (
  'Incoadas',
  'Adoptadas',
  'Denegadas',
  'Inadmitidas',
  'Pendientes'
);

CREATE TYPE "instancia_orden_proteccion_enum" AS ENUM (
  'A instancia de la víctima',
  'A instancia de otras personas',
  'A instancia del Minist. Fiscal',
  'De oficio',
  'A instancia de la Administración'
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
    "comunidad_autonoma_id" int NOT NULL
  );

CREATE TABLE
  "feminicidios_pareja_expareja" (
    "feminicidios_pareja_expareja_id" serial PRIMARY KEY,
    "num_feminicidios" int NOT NULL CHECK (num_feminicidios >= 0),
    "num_huerfanos_menores" int NOT NULL CHECK (num_huerfanos_menores >= 0),
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "victima_grupo_edad" varchar,
    "agresor_grupo_edad" varchar
  );

CREATE TABLE
  "feminicidios_fuera_pareja_expareja" (
    "feminicidios_fuera_pareja_expareja_id" serial PRIMARY KEY,
    "num_feminicidios" int NOT NULL CHECK (num_feminicidios >= 0),
    "tipo_feminicidio" tipo_feminicidio_enum NOT NULL,
    "comunidad_autonoma_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
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
    "num_menores_victimas_mortales" int NOT NULL CHECK (num_menores_victimas_mortales >= 0),
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
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
    "provincia_id" int,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "persona_consulta" persona_consulta_enum,
    "tipo_violencia" tipo_violencia_enum NOT NULL,
    "total_consultas" int NOT NULL CHECK (total_consultas >= 0),
    "num_llamadas" int NOT NULL CHECK (num_llamadas >= 0),
    "num_whatsapps" int NOT NULL CHECK (num_whatsapps >= 0),
    "num_emails" int NOT NULL CHECK (num_emails >= 0),
    "num_chats" int NOT NULL CHECK (num_chats >= 0)
  );

CREATE TABLE
  "usuarias_atenpro" (
    "usuarias_atenpro_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "num_altas" int NOT NULL CHECK (num_altas >= 0),
    "num_bajas" int NOT NULL CHECK (num_bajas >= 0),
    "num_usuarias_activas" int NOT NULL CHECK (num_usuarias_activas >= 0)
  );

CREATE TABLE
  "dispositivos_electronicos_seguimiento" (
    "dispositivos_electronicos_seguimiento_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "num_instalaciones_acumuladas" int NOT NULL CHECK (num_instalaciones_acumuladas >= 0),
    "num_desinstalaciones_acumuladas" int NOT NULL CHECK (num_desinstalaciones_acumuladas >= 0),
    "num_dispositivos_activos" int NOT NULL CHECK (num_dispositivos_activos >= 0)
  );

CREATE TABLE
  "ayudas_articulo_27" (
    "ayudas_articulo_27_id" serial PRIMARY KEY,
    "comunidad_autonoma_id" int,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "num_ayudas_concedidas" int NOT NULL CHECK (num_ayudas_concedidas >= 0)
  );

CREATE TABLE
  "viogen" (
    "viogen_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "nivel_riesgo" nivel_riesgo_viogen_enum NOT NULL,
    "num_casos" int NOT NULL CHECK (num_casos >= 0),
    "num_casos_proteccion_policial" int NOT NULL CHECK (num_casos_proteccion_policial >= 0)
  );

CREATE TABLE
  "autorizaciones_residencia_trabajo_vvg" (
    "autorizaciones_residencia_trabajo_vvg_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "num_autorizaciones_concedidas" int NOT NULL CHECK (num_autorizaciones_concedidas >= 0)
  );

CREATE TABLE
  "denuncias_vg_pareja" (
    "denuncias_vg_pareja_id" serial PRIMARY KEY,
    "origen_denuncia" origen_denuncia_enum NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL,
    "num_denuncias" int NOT NULL CHECK (num_denuncias >= 0)
  );

CREATE TABLE
  "ordenes_proteccion" (
    "ordenes_proteccion_id" serial PRIMARY KEY,
    "estado_proceso" estado_orden_proteccion_enum NOT NULL,
    "instancia" instancia_orden_proteccion_enum NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "trimestre" int NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    "provincia_id" int NOT NULL,
    "num_ordenes_proteccion" int NOT NULL CHECK (num_ordenes_proteccion >= 0)
  );

CREATE TABLE
  "renta_activa_insercion" (
    "renta_activa_insercion_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "num_perceptoras" int NOT NULL CHECK (num_perceptoras >= 0)
  );

CREATE TABLE
  "contratos_bonificados_sustitucion" (
    "contratos_bonificados_sustitucion_id" serial PRIMARY KEY NOT NULL,
    "num_contratos_bonificados" int NOT NULL CHECK (num_contratos_bonificados >= 0),
    "num_contratos_sustitucion" int NOT NULL CHECK (num_contratos_sustitucion >= 0),
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "mes" int NOT NULL CHECK (mes BETWEEN 1 AND 12),
    "provincia_id" int NOT NULL,
    "colectivo" varchar NOT NULL,
    "tipo_contrato" varchar NOT NULL
  );

CREATE TABLE
  "ayudas_cambio_residencia" (
    "ayudas_cambio_residencia_id" serial PRIMARY KEY,
    "provincia_id" int NOT NULL,
    "año" int NOT NULL CHECK (
      año BETWEEN 1900 AND EXTRACT(
        YEAR
        FROM
          CURRENT_DATE
      )
    ),
    "num_ayudas_cambio_residencia" int NOT NULL CHECK (num_ayudas_cambio_residencia >= 0)
  );

ALTER TABLE "provincias" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "feminicidios_pareja_expareja" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "feminicidios_fuera_pareja_expareja" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "menores_victimas_mortales" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "servicio_016" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "usuarias_atenpro" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "dispositivos_electronicos_seguimiento" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ayudas_articulo_27" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "viogen" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "autorizaciones_residencia_trabajo_vvg" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "denuncias_vg_pareja" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ordenes_proteccion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "renta_activa_insercion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "contratos_bonificados_sustitucion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ayudas_cambio_residencia" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");