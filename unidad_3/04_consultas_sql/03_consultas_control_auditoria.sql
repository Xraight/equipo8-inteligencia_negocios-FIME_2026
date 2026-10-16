-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 04_consultas_sql / 03_consultas_control_auditoria.sql
-- OBJETIVO: Consultas de Control, Auditoría Numérica y Validación de Grano
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. CONTROL DE REINICIO DE CLASIFICACIÓN Y MÁXIMO 5 PRODUCTOS POR REGIÓN
-- Verifica que cada región contenga como máximo 5 productos y ninguna supere el límite.
-- ------------------------------------------------------------------------------
WITH reporte_top5 AS (
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
    clasificacion AS (
        SELECT 
            region,
            producto_id_bk,
            nombre_producto,
            rentabilidad_q2,
            DENSE_RANK() OVER (PARTITION BY region ORDER BY rentabilidad_q2 DESC) AS posicion_region
        FROM ventas_q2
    )
    SELECT * FROM clasificacion WHERE posicion_region <= 5
)
SELECT 
    region,
    COUNT(*) AS total_productos_reportados,
    MIN(posicion_region) AS ranking_minimo,
    MAX(posicion_region) AS ranking_maximo,
    CASE 
        WHEN COUNT(*) <= 5 AND MAX(posicion_region) <= 5 THEN 'CORRECTO (<= 5 productos)'
        ELSE 'VIOLACIÓN DETECTADA'
    END AS evaluacion_control
FROM reporte_top5
GROUP BY region
ORDER BY region;

-- ------------------------------------------------------------------------------
-- 2. CONTROL DE PRESERVACIÓN DEL GRANO (SIN DUPLICACIÓN POR JOINs)
-- Compara el total acumulado de ventas netas y costos de la tabla de hechos directa
-- contra la suma de la consulta con JOINs a dimensiones.
-- Ambos totales deben coincidir exactamente al centavo.
-- ------------------------------------------------------------------------------
WITH total_hechos_directo AS (
    SELECT 
        SUM(monto_venta_neta) AS total_venta_neta_base,
        SUM(monto_costo_total) AS total_costo_base,
        SUM(monto_envio_prorrateado) AS total_envio_base,
        COUNT(*) AS total_filas_base
    FROM Fact_Ventas
),
total_hechos_con_joins AS (
    SELECT 
        SUM(f.monto_venta_neta) AS total_venta_neta_join,
        SUM(f.monto_costo_total) AS total_costo_join,
        SUM(f.monto_envio_prorrateado) AS total_envio_join,
        COUNT(*) AS total_filas_join
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    JOIN Dim_Cliente c ON f.cliente_sk = c.cliente_sk
    JOIN Dim_Asesor a ON f.asesor_sk = a.asesor_sk
    JOIN Dim_Canal cn ON f.canal_sk = cn.canal_sk
)
SELECT 
    d.total_filas_base,
    j.total_filas_join,
    d.total_venta_neta_base,
    j.total_venta_neta_join,
    ROUND((d.total_venta_neta_base - j.total_venta_neta_join), 2) AS diferencia_venta_neta,
    ROUND((d.total_costo_base - j.total_costo_join), 2) AS diferencia_costo,
    CASE 
        WHEN d.total_filas_base = j.total_filas_join 
         AND d.total_venta_neta_base = j.total_venta_neta_join THEN 'INTEGRIDAD PERFECTA (Sin producto cartesiano)'
        ELSE 'ERROR: Duplicación de importes detectada'
    END AS dictamen_grano
FROM total_hechos_directo d
CROSS JOIN total_hechos_con_joins j;

-- ------------------------------------------------------------------------------
-- 3. MUESTRA DE CONTROL MANUAL (CONTRASTE CON FILAS AISLADAS)
-- Valida un producto y región específicos (Región Norte, Producto 401: Sofá Seccional Oslo)
-- ------------------------------------------------------------------------------
SELECT 
    'Control Muestra Manual: Sofá Oslo en Norte Q2 2026' AS concepto,
    COUNT(*) AS total_transacciones,
    SUM(f.cantidad) AS unidades_vendidas,
    SUM(f.monto_venta_neta) AS suma_ventas_netas,
    SUM(f.monto_costo_total) AS suma_costos_totales,
    SUM(f.monto_envio_prorrateado) AS suma_envios_prorrateados,
    SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_calculada_manual
FROM Fact_Ventas f
JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
WHERE t.anio = 2026 AND t.trimestre = 2
  AND s.zona = 'Norte'
  AND p.producto_id_bk = 401;
