-- 1. Get all denuncias
SELECT
  *
FROM
  violencia_genero.denuncias_vg_pareja;

-- 2. Join denuncias_vg_pareja with provincias to get province names 
SELECT
  d.denuncias,
  p.nombre AS provincia,
  d.anio
FROM
  violencia_genero.denuncias_vg_pareja d
  JOIN geo.provincias p ON d.provincia_id = p.provincia_id;

-- 3. Total ordenes de proteccion incoadas and total consultas 016 by province and year
SELECT
  p.nombre AS provincia,
  o.anio,
  SUM(o.ordenes_proteccion) AS total_ordenes_proteccion,
  SUM(s.llamadas) AS llamadas
FROM
  violencia_genero.ordenes_proteccion o
  JOIN violencia_genero.servicio_016 s ON o.provincia_id = s.provincia_id
  AND o.anio = s.anio
  JOIN geo.provincias p ON o.provincia_id = p.provincia_id
GROUP BY
  p.nombre,
  o.anio
ORDER BY
  p.nombre DESC,
  o.anio DESC;

-- 4. Top 5 months with the highest number of feminicides by province
SELECT
  p.nombre AS provincia,
  f.anio,
  SUM(f.feminicidios) AS total_feminicidios
FROM
  violencia_genero.feminicidios_pareja_expareja f
  JOIN geo.provincias p ON f.provincia_id = p.provincia_id
GROUP BY
  p.nombre,
  f.anio
ORDER BY
  total_feminicidios DESC,
  f.anio DESC
LIMIT
  5;

-- 5. Monthly trend of active users in the ATENPRO service for Madrid
SELECT
  p.nombre AS provincia,
  a.anio,
  a.mes,
  a.usuarias_activas
FROM
  violencia_genero.usuarias_atenpro a
  JOIN geo.provincias p ON a.provincia_id = p.provincia_id
WHERE
  p.nombre = 'Madrid'
ORDER BY
  a.anio DESC,
  a.mes DESC;

-- 6. Total ayudas granted per autonomous community by year
SELECT
  c.nombre AS comunidad_autonoma,
  a.anio,
  SUM(a.ayudas_concedidas) AS total_ayudas
FROM
  violencia_genero.ayudas_articulo_27 a
  JOIN geo.comunidades_autonomas c ON a.comunidad_autonoma_id = c.comunidad_autonoma_id
GROUP BY
  c.nombre,
  a.anio
ORDER BY
  a.anio DESC,
  total_ayudas DESC;

-- 7. Trend of electronic monitoring devices installed, by province
SELECT
  p.nombre AS provincia,
  d.anio,
  d.mes,
  d.instalaciones_acumuladas
FROM
  violencia_genero.dispositivos_electronicos_seguimiento d
  JOIN geo.provincias p ON d.provincia_id = p.provincia_id
ORDER BY
  d.anio DESC,
  d.mes DESC,
  provincia;

-- Get all tables and all schemas in the database
SELECT
  table_schema,
  table_name
FROM
  information_schema.tables
WHERE
  table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY
  table_schema,
  table_name;

SELECT
  serv.anio,
  prov.nombre,
  SUM(
    serv.llamadas + serv.whatsapps + serv.emails + serv.chats
  ) AS total_consultas
FROM
  violencia_genero.servicio_016 serv
  JOIN geo.provincias prov ON serv.provincia_id = prov.provincia_id
GROUP BY
  serv.anio,
  prov.nombre
ORDER BY
  serv.anio DESC;