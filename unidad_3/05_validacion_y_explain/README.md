# 05 - Validación y EXPLAIN (Optimización y Performance)

## 🎯 Objetivo General
Analizar, documentar y validar el rendimiento de las consultas analíticas del Data Mart mediante planes de ejecución de PostgreSQL (`EXPLAIN` y `EXPLAIN ANALYZE`).

## 📌 Función Específica
- Evaluar el costo computacional (`Total Cost`, `Execution Time`, `Planning Time`) de las consultas analíticas más demandantes.
- Identificar cuellos de botella como escaneos secuenciales masivos (`Seq Scan`) en tablas grandes.
- Proponer e implementar estrategias de indexación (índices B-Tree, índices compuestos, índices parciales) y comparar el antes vs. después del plan de ejecución.
- Validar la consistencia y precisión de los resultados arrojados por las consultas frente a los datos esperados.

## 📦 Estructura Sugerida
- `reporte_explain_analisis.md`: Comparativa de planes de ejecución antes y después de optimizaciones.
- `01_explain_consultas_base.sql`: Salidas de `EXPLAIN ANALYZE` sobre consultas sin indexar.
- `02_indices_optimizacion.sql`: Scripts DDL de índices creados para mejorar los tiempos de respuesta.
- `03_explain_consultas_optimizadas.sql`: Salidas de `EXPLAIN ANALYZE` posteriores a la optimización.
