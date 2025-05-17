# Fuente: Barómetros del CIS

- **Organismo:** Centro de Investigaciones Sociológicas
- **Enlace:** https://www.cis.es/
- **Cobertura:** Estatal, desde 2000 hasta la actualidad
- **Periodicidad:** Mensual
- **Formato original:** XLS y CSV
- **Tema relevante:** Opinión pública sobre la violencia de género

## Variables extraídas
- `vg_importancia`: importancia de la violencia de género como problema social
- `vg_conocimiento_leyes`: conocimiento de leyes específicas
- `vg_satisfaccion_medidas`: percepción de efectividad de las medidas gubernamentales

## Procesamiento
- Script: `scripts/etl/transformar_cis.py`
- Output: `datasets/procesados/cis/barometros_limpio.csv`