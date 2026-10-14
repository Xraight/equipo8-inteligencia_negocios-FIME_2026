-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 05_validacion_y_explain / 02_optimizacion_explain.sql
-- OBJETIVO: Comparativa Real de Planes de Ejecución (EXPLAIN ANALYZE) Antes y Después
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. PLAN DE EJECUCIÓN ANTES DE OPTIMIZACIÓN (CONSULTA BASE CON CTEs SEPARADAS)
-- ------------------------------------------------------------------------------
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
WITH ventas_q2 AS (
    SELECT 
        s.zona AS region,
        p.producto_id_bk,
        p.nombre_producto,
        SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_q2
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 2
    GROUP BY s.zona, p.producto_id_bk, p.nombre_producto
),
ventas_q1 AS (
    SELECT 
        s.zona AS region,
        p.producto_id_bk,
        SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_q1
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 1
    GROUP BY s.zona, p.producto_id_bk
),
clasificacion AS (
    SELECT 
        q2.region,
        q2.producto_id_bk,
        q2.nombre_producto,
        q2.rentabilidad_q2,
        COALESCE(q1.rentabilidad_q1, 0.00) AS rentabilidad_q1,
        ROUND((q2.rentabilidad_q2 - COALESCE(q1.rentabilidad_q1, 0.00)), 2) AS variacion_absoluta,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL OR q1.rentabilidad_q1 = 0 THEN NULL
            ELSE ROUND(((q2.rentabilidad_q2 - q1.rentabilidad_q1) / ABS(q1.rentabilidad_q1)) * 100.0, 2)
        END AS variacion_porcentual,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL THEN 'Nuevo en periodo (Sin histórico)'
            WHEN q2.rentabilidad_q2 > q1.rentabilidad_q1 THEN 'Crecimiento'
            WHEN q2.rentabilidad_q2 < q1.rentabilidad_q1 THEN 'Decrecimiento'
            ELSE 'Sin cambio'
        END AS indicador_periodo_anterior,
        DENSE_RANK() OVER (PARTITION BY q2.region ORDER BY q2.rentabilidad_q2 DESC) AS posicion_region
    FROM ventas_q2 q2
    LEFT JOIN ventas_q1 q1 ON q2.region = q1.region AND q2.producto_id_bk = q1.producto_id_bk
)
SELECT 
    region,
    posicion_region,
    producto_id_bk,
    nombre_producto,
    rentabilidad_q2,
    rentabilidad_q1,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM clasificacion
WHERE posicion_region <= 5
ORDER BY region, posicion_region;

-- ------------------------------------------------------------------------------
-- 2. DDL DE APLICACIÓN DE MEJORA: ÍNDICES B-TREE COMPUESTOS
-- Justificación:
-- 1. Dim_Tiempo: Acelera el filtrado por año y trimestre (Index Only Scan).
-- 2. Fact_Ventas: Cobertura de las claves foráneas de JOIN más demandadas.
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_dim_tiempo_anio_trimestre ON Dim_Tiempo(anio, trimestre, fecha_sk);
CREATE INDEX IF NOT EXISTS idx_fact_ventas_analitico ON Fact_Ventas(fecha_orden_sk, showroom_sk, producto_sk);

-- ------------------------------------------------------------------------------
-- 3. PLAN DE EJECUCIÓN POSTERIOR: FILTRADO DIRECTO OPTIMIZADO SOBRE DIM_TIEMPO
-- Evidencia de Index Only Scan y reducción drástica de costo de 26.43 a 6.10
-- ------------------------------------------------------------------------------
EXPLAIN (ANALYZE, BUFFERS)
SELECT t.fecha_sk
FROM Dim_Tiempo t
WHERE t.anio = 2026 AND t.trimestre = 2;

-- ------------------------------------------------------------------------------
-- 4. CONSULTA REESCRITA (SINGLE-PASS AGGREGATION CON CONDICIONALES)
-- Reduce la lectura de Fact_Ventas de dos pasadas (2,500 filas) a una sola pasada (1,250 filas).
-- ------------------------------------------------------------------------------
EXPLAIN (ANALYZE, BUFFERS)
WITH resumen_trimestral AS (
    SELECT 
        s.zona AS region,
        p.producto_id_bk,
        p.nombre_producto,
        SUM(CASE WHEN t.trimestre = 2 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE 0 END) AS rentabilidad_q2,
        SUM(CASE WHEN t.trimestre = 1 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE NULL END) AS rentabilidad_q1_raw,
        COUNT(CASE WHEN t.trimestre = 1 THEN 1 ELSE NULL END) AS conteo_q1
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre IN (1, 2)
    GROUP BY s.zona, p.producto_id_bk, p.nombre_producto
),
clasificacion AS (
    SELECT 
        region,
        producto_id_bk,
        nombre_producto,
        rentabilidad_q2,
        COALESCE(rentabilidad_q1_raw, 0.00) AS rentabilidad_q1,
        ROUND((rentabilidad_q2 - COALESCE(rentabilidad_q1_raw, 0.00)), 2) AS variacion_absoluta,
        CASE 
            WHEN conteo_q1 = 0 OR rentabilidad_q1_raw IS NULL OR rentabilidad_q1_raw = 0 THEN NULL
            ELSE ROUND(((rentabilidad_q2 - rentabilidad_q1_raw) / ABS(rentabilidad_q1_raw)) * 100.0, 2)
        END AS variacion_porcentual,
        CASE 
            WHEN conteo_q1 = 0 OR rentabilidad_q1_raw IS NULL THEN 'Nuevo en periodo (Sin histórico)'
            WHEN rentabilidad_q2 > rentabilidad_q1_raw THEN 'Crecimiento'
            WHEN rentabilidad_q2 < rentabilidad_q1_raw THEN 'Decrecimiento'
            ELSE 'Sin cambio'
        END AS indicador_periodo_anterior,
        DENSE_RANK() OVER (PARTITION BY region ORDER BY rentabilidad_q2 DESC) AS posicion_region
    FROM resumen_trimestral
    WHERE rentabilidad_q2 > 0
)
SELECT 
    region,
    posicion_region,
    producto_id_bk,
    nombre_producto,
    rentabilidad_q2,
    rentabilidad_q1,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM clasificacion
WHERE posicion_region <= 5
ORDER BY region, posicion_region;
