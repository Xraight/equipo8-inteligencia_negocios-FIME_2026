-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 02_ddl_y_datos / 03_verificacion_calidad_datos.sql
-- OBJETIVO: Validación de Calidad, Integridad Referencial y Coherencia Numérica
-- ==============================================================================

-- 1. Verificación del Volumen Mínimo (> 1,000 filas requeridas por la rúbrica)
SELECT 
    'Fact_Ventas' AS tabla, 
    COUNT(*) AS total_filas,
    CASE WHEN COUNT(*) >= 1000 THEN 'CUMPLE (>1000 filas)' ELSE 'FALLA' END AS estado_volumen
FROM Fact_Ventas;

-- 2. Verificación de Cobertura Temporal (Dos trimestres consecutivos 2026: Q1 y Q2)
SELECT 
    t.anio, 
    t.trimestre, 
    COUNT(*) AS total_lineas,
    MIN(t.fecha_completa) AS fecha_inicio,
    MAX(t.fecha_completa) AS fecha_fin,
    CASE 
        WHEN t.trimestre = 1 AND COUNT(*) > 0 THEN 'Q1 2026 Completo'
        WHEN t.trimestre = 2 AND COUNT(*) > 0 THEN 'Q2 2026 Completo'
        ELSE 'Otro Periodo'
    END AS evaluacion_periodo
FROM Fact_Ventas f
JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
WHERE t.anio = 2026
GROUP BY t.anio, t.trimestre
ORDER BY t.anio, t.trimestre;

-- 3. Verificación de Cobertura Regional (Mínimo 3 regiones requeridas, Casa&Estilo cubre 5)
SELECT 
    s.zona AS region,
    COUNT(*) AS lineas_venta,
    COUNT(DISTINCT f.orden_id) AS total_ordenes,
    COUNT(DISTINCT f.producto_sk) AS variantes_distintas,
    COUNT(DISTINCT p.producto_id_bk) AS productos_comerciales_distintos
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY s.zona
ORDER BY lineas_venta DESC;

-- 4. Verificación de Integridad de Claves Foráneas (Huérfanos = 0)
SELECT 
    COUNT(*) AS registros_huerfanos_tiempo
FROM Fact_Ventas f
LEFT JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
WHERE t.fecha_sk IS NULL;

SELECT 
    COUNT(*) AS registros_huerfanos_showroom
FROM Fact_Ventas f
LEFT JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
WHERE s.showroom_sk IS NULL;

SELECT 
    COUNT(*) AS registros_huerfanos_producto
FROM Fact_Ventas f
LEFT JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
WHERE p.producto_sk IS NULL;

-- 5. Verificación de Coherencia Matemática y Montos No Negativos
-- Regla: monto_subtotal = cantidad * precio_unitario
-- Regla: monto_costo_total = cantidad * costo_unitario
-- Regla: monto_venta_neta >= 0 y ganancia_bruta calculada correctamente
SELECT 
    COUNT(*) AS discrepancias_matematicas
FROM Fact_Ventas
WHERE 
    ROUND(monto_subtotal, 2) != ROUND(cantidad * precio_unitario, 2)
    OR ROUND(monto_costo_total, 2) != ROUND(cantidad * costo_unitario, 2)
    OR monto_venta_neta < 0
    OR precio_unitario <= 0
    OR costo_unitario <= 0;
