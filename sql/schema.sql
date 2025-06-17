CREATE TABLE
  comunidades_autonomas (
    comunidades_autonomas_id INT PRIMARY KEY,
    nombre VARCHAR UNIQUE NOT NULL
  );

CREATE TABLE
  provincias (
    provincias_id INT PRIMARY KEY,
    nombre VARCHAR UNIQUE NOT NULL,
    comunidad_autonoma_id INT
  );

CREATE TABLE
  feminicidios_pareja (
    feminicidios_pareja_id SERIAL PRIMARY KEY,
    feminicidios INT,
    huerfanos_menores INT,
    provincia_id INT,
    año INT,
    mes INT,
    edad_grupo_victima VARCHAR,
    edad_grupo_agresor VARCHAR
  );

CREATE TABLE
  feminicidios_no_pareja (
    feminicidios_no_pareja_id SERIAL PRIMARY KEY,
    feminicidios INT,
    tipo_feminicidio VARCHAR,
    comunidad_autonoma_id INT,
    año INT
  );

CREATE TABLE
  servicio_016 (
    servicio_016_id SERIAL PRIMARY KEY,
    provincia_id INT,
    año INT,
    mes INT,
    idioma VARCHAR,
    tipo_violencia VARCHAR,
    total_consultas INT
  );

-- Foreign keys
ALTER TABLE provincias ADD FOREIGN KEY (comunidad_autonoma_id) REFERENCES comunidades_autonomas (comunidades_autonomas_id);

ALTER TABLE feminicidios_pareja ADD FOREIGN KEY (provincia_id) REFERENCES provincias (provincias_id);

ALTER TABLE feminicidios_no_pareja ADD FOREIGN KEY (comunidad_autonoma_id) REFERENCES comunidades_autonomas (comunidades_autonomas_id);

ALTER TABLE servicio_016 ADD FOREIGN KEY (provincia_id) REFERENCES provincias (provincias_id);