CREATE TABLE
  "comunidades_autonomas" (
    "comunidad_autonoma_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL
  );

CREATE TABLE
  "provincias" (
    "provincia_id" int PRIMARY KEY,
    "nombre" varchar UNIQUE NOT NULL,
    "comunidad_autonoma_id" int
  );

CREATE TABLE
  "feminicidios_pareja_expareja" (
    "feminicidios_pareja_expareja_id" serial PRIMARY KEY,
    "num_feminicidios" int,
    "num_huerfanos_menores" int,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "victima_grupo_edad" varchar,
    "agresor_grupo_edad" varchar
  );

CREATE TABLE
  "feminicidios_fuera_pareja_expareja" (
    "feminicidios_fuera_pareja_expareja_id" serial PRIMARY KEY,
    "num_feminicidios" int,
    "tipo_feminicidio" varchar,
    "comunidad_autonoma_id" int,
    "año" int
  );

CREATE TABLE
  "menores_victimas_mortales" (
    "menores_victimas_mortales_id" serial PRIMARY KEY,
    "relacion_victima_agresor" varchar,
    "es_victima_vicaria" boolean,
    "num_menores_victimas_mortales" int,
    "provincia_id" int,
    "año" int,
    "mes" int
  );

CREATE TABLE
  "servicio_016" (
    "servicio_016_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "persona_consulta" varchar,
    "tipo_violencia" varchar,
    "total_consultas" int,
    "num_llamadas" int,
    "num_whatsapps" int,
    "num_emails" int,
    "num_chats" int
  );

CREATE TABLE
  "usuarias_atenpro" (
    "usuarias_atenpro_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "num_altas" int,
    "num_bajas" int,
    "num_usuaria_activas" int
  );

CREATE TABLE
  "dispositivos_electronicos_seguimiento" (
    "dispositivos_electronicos_seguimiento_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "num_instalaciones_acumuladas" int,
    "num_desinstalaciones_acumuladas" int,
    "num_dispositivos_activos" int
  );

CREATE TABLE
  "ayudas_articulo_27" (
    "ayudas_articulo_27_id" serial PRIMARY KEY,
    "comunidad_autonoma_id" int,
    "año" int,
    "num_ayudas_concedidas" int
  );

CREATE TABLE
  "viogen" (
    "viogen_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "nivel_riesgo" varchar,
    "num_casos" int,
    "num_casos_proteccion_policial" int
  );

CREATE TABLE
  "autorizaciones_residencia_trabajo_mevvg" (
    "autorizaciones_residencia_trabajo_mevvg_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "mes" int,
    "num_autorizaciones_concedidas" int
  );

CREATE TABLE
  "denuncias_vg_pareja" (
    "denuncias_vd_pareja_id" serial PRIMARY KEY,
    "origen_denuncia" varchar,
    "año" int,
    "trimestre" int,
    "provincia_id" int,
    "num_denuncias_vg" int
  );

CREATE TABLE
  "ordenes_proteccion" (
    "ordenes_proteccion_id" serial PRIMARY KEY,
    "estado_denuncia" varchar,
    "instancia" varchar,
    "año" int,
    "provincia_id" int,
    "num_ordenes_proteccion" int
  );

CREATE TABLE
  "renta_activa_insercion" (
    "renta_activa_insercion_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "num_perceptoras" int
  );

CREATE TABLE
  "contratos_bonificados_sustitucion" (
    "contratos_bonificados_sustitucion_id" serial PRIMARY KEY,
    "num_contratos_bonificados" int,
    "num_contratos_sustitucion" int,
    "año" int,
    "mes" int,
    "provincia_id" int,
    "colectivo" varchar,
    "tipo_contrato" varchar
  );

CREATE TABLE
  "ayudas_cambio_residencia" (
    "ayudas_cambio_residencia_id" serial PRIMARY KEY,
    "provincia_id" int,
    "año" int,
    "num_ayudas_cambio_residencia" int
  );

ALTER TABLE "provincias" ADD FOREIGN KEY ("comunidad_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "feminicidios_pareja_expareja" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "feminicidios_fuera_pareja_expareja" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "menores_victimas_mortales" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "servicio_016" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "usuarias_atenpro" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "dispositivos_electronicos_seguimiento" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ayudas_articulo_27" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "comunidades_autonomas" ("comunidad_autonoma_id");

ALTER TABLE "viogen" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "autorizaciones_residencia_trabajo_mevvg" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "denuncias_vg_pareja" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ordenes_proteccion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "renta_activa_insercion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "contratos_bonificados_sustitucion" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");

ALTER TABLE "ayudas_cambio_residencia" ADD FOREIGN KEY ("provincia_id") REFERENCES "provincias" ("provincia_id");