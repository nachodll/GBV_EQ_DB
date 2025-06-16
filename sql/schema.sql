CREATE SCHEMA "geo";

CREATE SCHEMA "violencia";

CREATE TABLE "geo"."comunidades_autonomas" (
  "id" serial PRIMARY KEY,
  "nombre" varchar UNIQUE NOT NULL,
  "codigo_ine" varchar(2) UNIQUE
);

CREATE TABLE "geo"."provincias" (
  "id" serial PRIMARY KEY,
  "nombre" varchar UNIQUE NOT NULL,
  "comunidad_id" int,
  "codigo_ine" varchar(2) UNIQUE
);

CREATE TABLE "violencia"."feminicidios_pareja" (
  "id" serial PRIMARY KEY,
  "num_feminicidios" int,
  "huerfanos_menores" int,
  "provincia_id" int,
  "año" int,
  "mes" int,
  "vm_grupo_edad" varchar,
  "ag_grupo_edad" varchar
);

CREATE TABLE "violencia"."feminicidios_no_pareja" (
  "id" serial PRIMARY KEY,
  "num_feminicidios" int,
  "tipo_feminicidio" varchar,
  "comunidad_autonoma_id" int,
  "año" int
);

CREATE TABLE "violencia"."servicio_016" (
  "id" serial PRIMARY KEY,
  "provincia_id" int,
  "año" int,
  "mes" int,
  "idioma" varchar,
  "tipo_violencia" varchar,
  "total_consultas" int
);

ALTER TABLE "geo"."provincias" ADD FOREIGN KEY ("comunidad_id") REFERENCES "geo"."comunidades_autonomas" ("id");

ALTER TABLE "violencia"."feminicidios_pareja" ADD FOREIGN KEY ("provincia_id") REFERENCES "geo"."provincias" ("id");

ALTER TABLE "violencia"."feminicidios_no_pareja" ADD FOREIGN KEY ("comunidad_autonoma_id") REFERENCES "geo"."comunidades_autonomas" ("id");

ALTER TABLE "violencia"."servicio_016" ADD FOREIGN KEY ("provincia_id") REFERENCES "geo"."provincias" ("id");
