-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 06_stored_procedure / 01_sp_reporte_rentabilidad_top5.sql
-- OBJETIVO: Automatización del Reporte Analítico en Stored Procedure / Función (Reto 4)
-- EQUIPO 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
-- MOTOR: PostgreSQL 16 (PL/pgSQL) con Notas de Portabilidad para MySQL 8
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. FUNCIÓN / PROCEDIMIENTO ALMACENADO PRINCIPAL (POSTGRESQL 16)
-- Nombre: sp_reporte_rentabilidad_top5
-- Parámetros:
--   - p_anio INT: Año a evaluar (ej. 2026)
--   - p_trimestre INT: Trimestre de análisis (1 a 4)
-- Comportamiento Dinámico:
--   - Determina automáticamente el periodo previo para comparación:
--       * Si p_trimestre > 1 -> Compara contra (p_anio, p_trimestre - 1)
--       * Si p_trimestre = 1 -> Compara contra (p_anio - 1, 4)
--   - Maneja casos de productos nuevos sin ventas en el trimestre anterior.
--   - Evita divisiones entre cero retornando NULL en variacion_porcentual.
-- ------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION sp_reporte_rentabilidad_top5(
    p_anio INT,
    p_trimestre INT
)
RETURNS TABLE (
    region VARCHAR(100),
    posicion_region BIGINT,
    producto_id_bk INT,
    nombre_producto VARCHAR(150),
    rentabilidad_actual NUMERIC(14,2),
    rentabilidad_anterior NUMERIC(14,2),
    variacion_absoluta NUMERIC(14,2),
    variacion_porcentual NUMERIC(7,2),
    indicador_periodo_anterior VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_anio_ant INT;
    v_trimestre_ant INT;
BEGIN
    -- Validación de parámetros de entrada
    IF p_trimestre NOT BETWEEN 1 AND 4 THEN
        RAISE EXCEPTION 'El parámetro p_trimestre debe estar comprendido entre 1 y 4. Valor recibido: %', p_trimestre;
    END IF;

    -- Cálculo dinámico del periodo comparativo anterior
    IF p_trimestre = 1 THEN
        v_anio_ant := p_anio - 1;
        v_trimestre_ant := 4;
    ELSE
        v_anio_ant := p_anio;
        v_trimestre_ant := p_trimestre - 1;
    END IF;

    RETURN QUERY
    WITH ventas_actual AS (
        -- Sumariza la rentabilidad neta (restando flete) del periodo actual
        SELECT 
            s.zona AS reg,
            p.producto_id_bk AS prod_bk,
            p.nombre_producto AS prod_nombre,
            SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rent_act
        FROM Fact_Ventas f
        JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        WHERE t.anio = p_anio AND t.trimestre = p_trimestre
        GROUP BY s.zona, p.producto_id_bk, p.nombre_producto
    ),
    ventas_anterior AS (
        -- Sumariza la rentabilidad neta del periodo anterior calculado
        SELECT 
            s.zona AS reg,
            p.producto_id_bk AS prod_bk,
            SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rent_ant
        FROM Fact_Ventas f
        JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        WHERE t.anio = v_anio_ant AND t.trimestre = v_trimestre_ant
        GROUP BY s.zona, p.producto_id_bk
    ),
    clasificacion AS (
        -- Une ambos periodos, calcula métricas diferenciales y aplica función de ventana
        SELECT 
            act.reg::VARCHAR(100) AS region,
            DENSE_RANK() OVER (
                PARTITION BY act.reg 
                ORDER BY act.rent_act DESC
            )::BIGINT AS pos,
            act.prod_bk AS p_bk,
            act.prod_nombre::VARCHAR(150) AS p_nom,
            ROUND(act.rent_act, 2) AS r_act,
            ROUND(COALESCE(ant.rent_ant, 0.00), 2) AS r_ant,
            ROUND((act.rent_act - COALESCE(ant.rent_ant, 0.00)), 2) AS var_abs,
            CASE 
                WHEN ant.rent_ant IS NULL OR ant.rent_ant = 0 THEN NULL
                ELSE ROUND(((act.rent_act - ant.rent_ant) / ABS(ant.rent_ant)) * 100.0, 2)
            END AS var_pct,
            CASE 
                WHEN ant.rent_ant IS NULL THEN 'Nuevo en periodo (Sin histórico)'::VARCHAR(50)
                WHEN act.rent_act > ant.rent_ant THEN 'Crecimiento'::VARCHAR(50)
                WHEN act.rent_act < ant.rent_ant THEN 'Decrecimiento'::VARCHAR(50)
                ELSE 'Sin cambio'::VARCHAR(50)
            END AS ind_estatus
        FROM ventas_actual act
        LEFT JOIN ventas_anterior ant 
            ON act.reg = ant.reg 
            AND act.prod_bk = ant.prod_bk
    )
    SELECT 
        c.region,
        c.pos,
        c.p_bk,
        c.p_nom,
        c.r_act,
        c.r_ant,
        c.var_abs,
        c.var_pct,
        c.ind_estatus
    FROM clasificacion c
    WHERE c.pos <= 5
    ORDER BY c.region ASC, c.pos ASC;
END;
$$;

-- ------------------------------------------------------------------------------
-- 2. PROCEDIMIENTO PROCEDURAL AUXILIAR (COMPATIBLE CON 'CALL')
-- ------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE pr_ejecutar_reporte_rentabilidad(
    IN p_anio INT, 
    IN p_trimestre INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_filas INT;
BEGIN
    SELECT COUNT(*) INTO v_total_filas FROM sp_reporte_rentabilidad_top5(p_anio, p_trimestre);
    RAISE NOTICE 'Procedimiento ejecutado para Año %, Trimestre %. Filas generadas: %', p_anio, p_trimestre, v_total_filas;
END;
$$;

-- ------------------------------------------------------------------------------
-- 3. SINTAXIS EQUIVALENTE PARA MYSQL 8 (DOCUMENTADA PARA PORTABILIDAD)
-- ------------------------------------------------------------------------------
/*
DELIMITER //

DROP PROCEDURE IF EXISTS sp_reporte_rentabilidad_top5_mysql //
CREATE PROCEDURE sp_reporte_rentabilidad_top5_mysql(
    IN p_anio INT,
    IN p_trimestre INT
)
BEGIN
    DECLARE v_anio_ant INT;
    DECLARE v_trimestre_ant INT;

    IF p_trimestre = 1 THEN
        SET v_anio_ant = p_anio - 1;
        SET v_trimestre_ant = 4;
    ELSE
        SET v_anio_ant = p_anio;
        SET v_trimestre_ant = p_trimestre - 1;
    END IF;

    WITH ventas_actual AS (
        SELECT 
            s.zona AS region,
            p.producto_id_bk,
            p.nombre_producto,
            SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rent_act
        FROM Fact_Ventas f
        JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        WHERE t.anio = p_anio AND t.trimestre = p_trimestre
        GROUP BY s.zona, p.producto_id_bk, p.nombre_producto
    ),
    ventas_anterior AS (
        SELECT 
            s.zona AS region,
            p.producto_id_bk,
            SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rent_ant
        FROM Fact_Ventas f
        JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
        JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
        JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
        WHERE t.anio = v_anio_ant AND t.trimestre = v_trimestre_ant
        GROUP BY s.zona, p.producto_id_bk
    ),
    clasificacion AS (
        SELECT 
            act.region,
            DENSE_RANK() OVER (PARTITION BY act.region ORDER BY act.rent_act DESC) AS pos,
            act.producto_id_bk,
            act.nombre_producto,
            ROUND(act.rent_act, 2) AS rentabilidad_actual,
            ROUND(COALESCE(ant.rent_ant, 0.00), 2) AS rentabilidad_anterior,
            ROUND((act.rent_act - COALESCE(ant.rent_ant, 0.00)), 2) AS variacion_absoluta,
            CASE 
                WHEN ant.rent_ant IS NULL OR ant.rent_ant = 0 THEN NULL
                ELSE ROUND(((act.rent_act - ant.rent_ant) / ABS(ant.rent_ant)) * 100.0, 2)
            END AS variacion_porcentual,
            CASE 
                WHEN ant.rent_ant IS NULL THEN 'Nuevo en periodo (Sin histórico)'
                WHEN act.rent_act > ant.rent_ant THEN 'Crecimiento'
                WHEN act.rent_act < ant.rent_ant THEN 'Decrecimiento'
                ELSE 'Sin cambio'
            END AS indicador_periodo_anterior
        FROM ventas_actual act
        LEFT JOIN ventas_anterior ant 
            ON act.region = ant.region 
            AND act.producto_id_bk = ant.producto_id_bk
    )
    SELECT * 
    FROM clasificacion 
    WHERE pos <= 5
    ORDER BY region, pos;
END //

DELIMITER ;
*/
