-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 05_validacion_y_explain / 01_depuracion_error_1055.sql
-- OBJETIVO: Demostración y Depuración de Error de Agrupación Incompleta 1055 / 42803
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. CONSULTA QUE PROVOCA EL ERROR DE AGRUPACIÓN INCOMPLETA (RETO 2)
-- La consulta proyecta 'nombre_producto' y 'categoria' pero solo agrupa por 's.zona'.
-- En MySQL 8 con sql_mode=ONLY_FULL_GROUP_BY produce:
--   ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause...
-- En PostgreSQL 16 produce:
--   ERROR: column "p.nombre_producto" must appear in the GROUP BY clause or be used in an aggregate function (SQLSTATE 42803).
-- ------------------------------------------------------------------------------

-- Demostración capturada de forma controlada en PostgreSQL:
DO $$
BEGIN
    EXECUTE '
        SELECT 
            s.zona AS region,
            p.nombre_producto,
            p.categoria,
            SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_total
        FROM Fact_Ventas f
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        GROUP BY s.zona';
EXCEPTION
    WHEN SQLSTATE '42803' THEN
        RAISE NOTICE '----------------------------------------------------------------------';
        RAISE NOTICE '[DEMOSTRACIÓN RETO 2] ERROR CAPTURADO EXITOSAMENTE:';
        RAISE NOTICE 'Mensaje: %', SQLERRM;
        RAISE NOTICE 'Código de Estado: SQLSTATE 42803 (Equivalente exacto a MySQL Error 1055)';
        RAISE NOTICE 'Causa: Agrupación incompleta de columnas proyectadas en el SELECT.';
        RAISE NOTICE '----------------------------------------------------------------------';
END $$;

-- ------------------------------------------------------------------------------
-- 2. CONSULTA CORREGIDA Y VALIDADA
-- Se incorporan todas las columnas no agregadas en la cláusula GROUP BY,
-- garantizando la correspondencia estricta con el grano del negocio.
-- ------------------------------------------------------------------------------
SELECT 
    s.zona AS region,
    p.producto_id_bk,
    p.nombre_producto,
    p.categoria,
    COUNT(*) AS total_transacciones,
    SUM(f.cantidad) AS volumen_unidades,
    ROUND(SUM(f.monto_venta_neta), 2) AS venta_neta_total,
    ROUND(SUM(f.monto_costo_total), 2) AS costo_mercancia_total,
    ROUND(SUM(f.monto_envio_prorrateado), 2) AS costo_entrega_total,
    ROUND(SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado), 2) AS rentabilidad_neta_total
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY 
    s.zona, 
    p.producto_id_bk, 
    p.nombre_producto, 
    p.categoria
ORDER BY 
    region ASC, 
    rentabilidad_neta_total DESC;
