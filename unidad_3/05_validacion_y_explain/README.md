# 05 - Validación, Depuración (Error 1055) y Optimización (EXPLAIN)

## 🎯 Objetivo General
Documentar la resolución práctica de los retos técnicos de **depuración de errores de agregación (Reto 2)** y **optimización de rendimiento de consultas OLAP (Reto 3)** mediante planes de ejecución reales generados por el motor de base de datos.

---

## 📦 Contenido del Directorio

| Archivo | Tipo | Descripción |
|---|---|---|
| [`01_depuracion_error_1055.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/01_depuracion_error_1055.sql) | SQL Depuración | Script ejecutable que captura controladamente el error de agrupación incompleta (`ONLY_FULL_GROUP_BY` / SQLSTATE 42803) y ejecuta la versión corregida conforme al grano. |
| [`reporte_depuracion_1055.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/reporte_depuracion_1055.md) | Documento Técnico | Reporte con los mensajes textuales de error en MySQL 8 y PostgreSQL 16, análisis de la causa raíz en el estándar SQL y justificación de la nueva agrupación. |
| [`02_optimizacion_explain.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/02_optimizacion_explain.sql) | SQL Benchmarking | Scripts de `EXPLAIN (ANALYZE, BUFFERS)`, creación de índices B-Tree compuestos y consulta reescrita a una sola pasada (Single-Pass). |
| [`reporte_optimizacion_explain.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/reporte_optimizacion_explain.md) | Documento Técnico | Comparativa detallada del plan de ejecución antes vs. después, demostrando una reducción del 76.9% en costo de escaneo y 50% en lectura de filas de hechos. |
