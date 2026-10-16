-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 04_consultas_sql / 02_consulta_final_validada.sql
-- OBJETIVO: Consulta Analítica Compleja Validada (Entregable 5 - Versión Final)
-- EQUIPO 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
-- MOTOR: PostgreSQL 16 (Compatible con MySQL 8)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- DESCRIPCIÓN DE LA SOLUCIÓN:
-- 1. Resuelve el Reto de Negocio: Top 5 de productos más rentables por región en
--    el segundo trimestre de 2026 (Q2) comparado contra el primer trimestre (Q1).
-- 2. Considera el costo de entrega e instalación (monto_envio_prorrateado) como
--    parte de la rentabilidad neta de Casa&Estilo.
-- 3. Consolida el grano a nivel producto comercial (producto_id_bk, nombre_producto)
--    sumando todas las variantes físicas vendidas.
-- 4. Utiliza DENSE_RANK() particionado por región para clasificar estrictamente el Top 5.
-- 5. Maneja matemáticamente los periodos sin histórico para prevenir división entre cero.
-- ------------------------------------------------------------------------------

WITH ventas_q2_2026 AS (
    -- Etapa 1: Agregación de rentabilidad neta para el periodo de análisis (Q2 2026)
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
ventas_q1_2026 AS (
    -- Etapa 2: Agregación de rentabilidad neta para el periodo base comparativo (Q1 2026)
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
clasificacion_regional AS (
    -- Etapa 3: Integración de periodos, variaciones y asignación de posición con función de ventana
    SELECT 
        q2.region,
        q2.producto_id_bk,
        q2.nombre_producto,
        ROUND(q2.rentabilidad_q2, 2) AS rentabilidad_q2_2026,
        ROUND(COALESCE(q1.rentabilidad_q1, 0.00), 2) AS rentabilidad_q1_2026,
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
        DENSE_RANK() OVER (
            PARTITION BY q2.region 
            ORDER BY q2.rentabilidad_q2 DESC
        ) AS posicion_region
    FROM ventas_q2_2026 q2
    LEFT JOIN ventas_q1_2026 q1 
        ON q2.region = q1.region 
        AND q2.producto_id_bk = q1.producto_id_bk
)
-- Etapa 4: Proyección final filtrando estrictamente los cinco productos líderes por región
SELECT 
    region,
    posicion_region,
    producto_id_bk,
    nombre_producto,
    rentabilidad_q2_2026,
    rentabilidad_q1_2026,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM clasificacion_regional
WHERE posicion_region <= 5
ORDER BY 
    region ASC, 
    posicion_region ASC;
