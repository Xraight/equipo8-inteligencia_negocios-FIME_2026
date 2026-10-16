-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 04_consultas_sql / 01_consulta_inicial_ia.sql
-- OBJETIVO: Versión inicial propuesta por la IA (Entregable 5 - Versión Inicial)
-- NOTA METODOLÓGICA: Esta es la primera iteración generada por el LLM antes de
--                    la revisión y correcciones aplicadas por el Equipo 8.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- LIMITACIONES IDENTIFICADAS EN ESTA VERSIÓN:
-- 1. Agrupación por variante (p.producto_sk) en lugar de producto maestro (producto_id_bk).
-- 2. Omisión del flete prorrateado (monto_envio_prorrateado) en la rentabilidad neta.
-- 3. Uso de RANK() en vez de DENSE_RANK(), permitiendo huecos numéricos ordinales.
-- 4. No contempla la clave de negocio requerida (producto_id_bk).
-- ------------------------------------------------------------------------------

WITH ventas_q2 AS (
    SELECT 
        s.zona AS region,
        p.producto_sk,
        p.nombre_producto,
        SUM(f.monto_venta_neta - f.monto_costo_total) AS rentabilidad_q2
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 2
    GROUP BY s.zona, p.producto_sk, p.nombre_producto
),
ventas_q1 AS (
    SELECT 
        s.zona AS region,
        p.producto_sk,
        SUM(f.monto_venta_neta - f.monto_costo_total) AS rentabilidad_q1
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 1
    GROUP BY s.zona, p.producto_sk
),
consolidado AS (
    SELECT 
        q2.region,
        q2.producto_sk,
        q2.nombre_producto,
        q2.rentabilidad_q2,
        COALESCE(q1.rentabilidad_q1, 0) AS rentabilidad_q1,
        (q2.rentabilidad_q2 - COALESCE(q1.rentabilidad_q1, 0)) AS variacion_absoluta,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL OR q1.rentabilidad_q1 = 0 THEN NULL
            ELSE ROUND(((q2.rentabilidad_q2 - q1.rentabilidad_q1) / q1.rentabilidad_q1) * 100, 2)
        END AS variacion_porcentual,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL THEN 'Sin datos previos'
            WHEN q2.rentabilidad_q2 > q1.rentabilidad_q1 THEN 'Crecimiento'
            ELSE 'Decrecimiento'
        END AS indicador_periodo_anterior,
        RANK() OVER (PARTITION BY q2.region ORDER BY q2.rentabilidad_q2 DESC) AS posicion_region
    FROM ventas_q2 q2
    LEFT JOIN ventas_q1 q1 ON q2.region = q1.region AND q2.producto_sk = q1.producto_sk
)
SELECT 
    region,
    posicion_region,
    producto_sk AS id_producto,
    nombre_producto,
    rentabilidad_q2,
    rentabilidad_q1,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM consolidado 
WHERE posicion_region <= 5
ORDER BY region, posicion_region;
