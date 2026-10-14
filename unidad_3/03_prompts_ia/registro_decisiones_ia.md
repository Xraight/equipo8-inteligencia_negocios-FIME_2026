# 📑 Registro de Decisiones y Evaluación de Respuestas de Inteligencia Artificial

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
### 🎯 Propósito: Trazabilidad metodológica entre las propuestas de la IA, el juicio crítico del equipo y la evidencia técnica utilizada.

---

## 📊 Matriz de Decisiones Técnicas

| # | Componente / Reto | Propuesta Inicial de la IA | Decisión del Equipo | Evidencia Técnica Utilizada | Impacto en el Proyecto |
|---|---|---|---|---|---|
| **1** | **Fórmula de Rentabilidad (Reto 1)** | Calculó `monto_venta_neta - monto_costo_total`. | **Rechazar y Corregir:** Restar `monto_envio_prorrateado` para obtener la rentabilidad neta real. | Documento de especificación de la práctica (Página 2): *"Casa&Estilo: Rentabilidad considerando entrega o instalación"*. | Se evita sobreestimar la rentabilidad de productos de gran volumen que generan fletes elevados. |
| **2** | **Nivel de Agrupación (Reto 1)** | Agrupó por `p.producto_sk` (variante de producto). | **Rechazar y Corregir:** Agrupar por `p.producto_id_bk` y `p.nombre_producto`. | Consulta preliminar en BD arrojó el mismo producto dos veces en el Top 5 (Sofá Oslo gris y Sofá Oslo beige). | Cumplimiento del requerimiento de 5 productos distintos consolidados por región. |
| **3** | **Función de Ventana (Reto 1)** | Sugirió `RANK() OVER (...)`. | **Modificar a `DENSE_RANK()`:** Evita saltos en la numeración ordinal ante posibles empates de margen. | Buenas prácticas OLAP y pruebas de escritorio en SQL. | Garantiza una secuencia ordinal continua ($1, 2, 3, 4, 5$). |
| **4** | **Tratamiento de División por Cero (Reto 1)** | Usó división simple `(q2 - q1) / q1 * 100` retornando NULL solo si q1 es 0. | **Aceptar con Ajuste:** Evaluar con `CASE WHEN q1 IS NULL OR q1 = 0 THEN NULL` y agregar un indicador cualitativo textual. | Prueba de ejecución sobre periodos sin ventas arrojó error `division by zero` en PostgreSQL. | Estabilidad numérica total sin fallos en runtime. |
| **5** | **Diagnóstico de Error 1055 (Reto 2)** | Explicó la violación del estándar ANSI SQL por columnas no agrupadas ni agregadas en `GROUP BY`. | **Aceptar Íntegramente:** Incorporar la explicación teórica y corregir agregando las columnas proyectadas al `GROUP BY`. | Mensaje de error real capturado en terminal: `ERROR: column p.nombre_producto must appear in the GROUP BY clause` (PostgreSQL 42803) y MySQL 1055. | Comprensión rigurosa del estándar `ONLY_FULL_GROUP_BY`. |
| **6** | **Estrategia de Índices (Reto 3)** | Sugirió crear índices individuales en cada FK de la tabla de hechos. | **Modificar a Índices Compuestos:** Crear `idx_dim_tiempo_anio_trimestre` en `Dim_Tiempo` y `idx_fact_ventas_analitico` en `Fact_Ventas`. | `EXPLAIN (ANALYZE, BUFFERS)`: El índice compuesto redujo el costo de escaneo de 26.43 a 6.10 y habilitó `Index Only Scan` con 0 heap fetches. | Rendimiento óptimo en consultas de reporting recurrente. |
| **7** | **Reescritura de Consulta (Reto 3)** | Propuso reescribir las dos CTEs a una agregación unificada con `CASE WHEN` condicional (Single-Pass). | **Aceptar y Documentar Ambas:** Conservar la consulta estructurada en CTEs para legibilidad pedagógica y la consulta optimizada de una pasada para alto rendimiento. | Comparativa de planes `EXPLAIN`: Se redujo la lectura de filas de 2,500 a 1,250 y se eliminó un Hash Join intermedio en memoria. | Doble evidencia de optimización por código y por indexación. |
| **8** | **Diseño del Stored Procedure (Reto 4)** | Propuso una función PL/pgSQL que recibe año y trimestre y calcula automáticamente el trimestre previo. | **Aceptar e Implementar:** Implementar como `FUNCTION ... RETURNS TABLE` en PostgreSQL para permitir `SELECT * FROM`, agregando wrapper `PROCEDURE` y sintaxis MySQL. | Ejecución exitosa con `SELECT * FROM sp_reporte_rentabilidad_top5(2026, 2)` retornando las 25 filas requeridas. | Automatización completa ejecutable desde cualquier cliente SQL o herramienta de BI. |
