# Script: transformar_cis.py

Este script transforma los barómetros del CIS para convertirlos en un CSV normalizado listo para cargar en la base de datos.

## Funciones principales
- Cargar archivos `.xls` de los barómetros
- Seleccionar solo las variables relacionadas con violencia de género
- Renombrar columnas y estandarizar valores
- Exportar a `datasets/procesados/cis/barometros_limpio.csv`

## Uso
```bash
python scripts/etl/transformar_cis.py