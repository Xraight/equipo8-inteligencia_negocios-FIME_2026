-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 04_consultas_sql / 04_diferencias_sintaxis_motores.sql
-- OBJETIVO: Comparativa Técnica de Sintaxis entre PostgreSQL 16 y MySQL 8
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CUADRO COMPARATIVO DE SINTAXIS
-- ------------------------------------------------------------------------------
-- 1. Agrupación Estricta:
--    - MySQL 8: sql_mode = 'ONLY_FULL_GROUP_BY' produce ERROR 1055.
--    - PostgreSQL 16: SQLSTATE 42803 produce "column must appear in the GROUP BY clause".
--
-- 2. Manejo de Fechas y Partes Temporales:
--    - MySQL 8: YEAR(fecha), QUARTER(fecha), MONTH(fecha).
--    - PostgreSQL 16: EXTRACT(YEAR FROM fecha), EXTRACT(QUARTER FROM fecha).
--
-- 3. Funciones de Ventana y CTEs:
--    - Ambos motores soportan WITH (Common Table Expressions) y DENSE_RANK() OVER (...).
--
-- 4. Creación de Stored Procedures:
--    - MySQL 8: DELIMITER // CREATE PROCEDURE sp_name(IN p_param INT) ... END //
--    - PostgreSQL 16: CREATE OR REPLACE FUNCTION sp_name(p_param INT) RETURNS TABLE(...) LANGUAGE plpgsql AS $$ ... $$;
-- ------------------------------------------------------------------------------

-- EJEMPLO EQUIVALENTE EN POSTGRESQL 16:
SELECT 
    'PostgreSQL 16' AS motor,
    s.zona AS region,
    COUNT(*) AS total_ventas,
    ROUND(SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado), 2) AS rentabilidad_neta
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
WHERE t.anio = 2026 AND t.trimestre = 2
GROUP BY s.zona
ORDER BY rentabilidad_neta DESC;

-- VERSIÓN EQUIVALENTE EN MYSQL 8 (Comentada para portabilidad en psql):
/*
-- Configuración previa obligatoria en MySQL 8:
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';

SELECT 
    'MySQL 8' AS motor,
    s.zona AS region,
    COUNT(*) AS total_ventas,
    ROUND(SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado), 2) AS rentabilidad_neta
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
WHERE t.anio = 2026 AND t.trimestre = 2
GROUP BY s.zona
ORDER BY rentabilidad_neta DESC;
*/
