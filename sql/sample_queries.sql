-- Get all denuncias
SELECT
  *
FROM
  denuncias_vg_pareja;

-- Join denuncias_vg_pareja with provincias to get province names 
SELECT
  d.num_denuncias,
  p.nombre AS provincia,
  d.año
FROM
  denuncias_vg_pareja d
  JOIN provincias p ON d.provincia_id = p.provincia_id;

-- Total ordenes de proteccion incoadas and total consultas 016 by province and year
SELECT
  p.nombre AS provincia,
  o.año,
  SUM(o.num_ordenes_proteccion) AS total_ordenes_proteccion,
  SUM(s.total_consultas) AS total_consultas
FROM
  ordenes_proteccion o
  JOIN servicio_016 s ON o.provincia_id = s.provincia_id
  AND o.año = s.año
  JOIN provincias p ON o.provincia_id = p.provincia_id
GROUP BY
  p.nombre,
  o.año
ORDER BY
  p.nombre DESC,
  o.año DESC;

-- Top 5 months with the highest number of feminicides by province
SELECT
  p.nombre AS provincia,
  f.año,
  SUM(f.num_feminicidios) AS total_feminicidios
FROM
  feminicidios_pareja_expareja f
  JOIN provincias p ON f.provincia_id = p.provincia_id
GROUP BY
  p.nombre,
  f.año
ORDER BY
  total_feminicidios DESC,
  f.año DESC
LIMIT
  5;

-- Monthly trend of active users in the ATENPRO service for Madrid
SELECT
  p.nombre AS provincia,
  a.año,
  a.mes,
  a.num_usuarias_activas
FROM
  usuarias_atenpro a
  JOIN provincias p ON a.provincia_id = p.provincia_id
WHERE
  p.nombre = 'Madrid'
ORDER BY
  a.año DESC,
  a.mes DESC;

-- Total ayudas granted per autonomous community by year
SELECT
  c.nombre AS comunidad_autonoma,
  a.año,
  SUM(a.num_ayudas_concedidas) AS total_ayudas
FROM
  ayudas_articulo_27 a
  JOIN comunidades_autonomas c ON a.comunidad_autonoma_id = c.comunidad_autonoma_id
GROUP BY
  c.nombre,
  a.año
ORDER BY
  a.año DESC,
  total_ayudas DESC;

-- Trend of electronic monitoring devices installed, by province
SELECT
  p.nombre AS provincia,
  d.año,
  d.mes,
  d.num_instalaciones_acumuladas
FROM
  dispositivos_electronicos_seguimiento d
  JOIN provincias p ON d.provincia_id = p.provincia_id
ORDER BY
  d.año DESC,
  d.mes DESC,
  provincia;