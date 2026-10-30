-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 07_indicadores / 06_indicadores_negocio.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Paso 7 - Indicadores analíticos de ventas netas y pedidos entregados
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- ==============================================================================
-- NOTA METODOLÓGICA Y SUPUESTO ANALÍTICO DE NEGOCIO:
-- Para los fines didácticos de este laboratorio, la métrica "Ventas Netas" se define
-- estrictamente como la suma monetaria de los pedidos en estatus 'Entregado'.
-- No se consideran deducciones por impuestos (IVA), costos de flete, descuentos 
-- comerciales ni notas de crédito por devoluciones. En un entorno contable real, 
-- las ventas netas requerirían deducir dichos rubros de los ingresos brutos.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CONSULTA 1: Indicadores Diarios por Estado Canónico y Fecha
-- ------------------------------------------------------------------------------
SELECT 
    f.fecha_pedido,
    e.estado_canonico,
    e.nombre_oficial AS estado_destino,
    COUNT(CASE WHEN f.estado_pedido = 'Entregado' THEN f.id_pedido END) AS pedidos_entregados,
    COALESCE(SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 0.00) AS ventas_netas,
    ROUND(AVG(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 2) AS ticket_promedio_entregado
FROM fact_ordenes f
JOIN dim_estado e ON f.estado_canonico = e.estado_canonico
GROUP BY 
    f.fecha_pedido, 
    e.estado_canonico, 
    e.nombre_oficial
HAVING pedidos_entregados > 0
ORDER BY 
    f.fecha_pedido ASC, 
    ventas_netas DESC;

-- ------------------------------------------------------------------------------
-- CONSULTA 2: Consolidado Estratégico por Entidad Federativa (Data Mart Summary)
-- ------------------------------------------------------------------------------
SELECT 
    e.estado_canonico,
    e.nombre_oficial AS estado,
    COUNT(CASE WHEN f.estado_pedido = 'Entregado' THEN f.id_pedido END) AS total_pedidos_entregados,
    COALESCE(SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 0.00) AS total_ventas_netas,
    ROUND(
        100.0 * COALESCE(SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 0.00) / 
        (SELECT SUM(importe) FROM fact_ordenes WHERE estado_pedido = 'Entregado'), 
        2
    ) AS porcentaje_participacion,
    ROUND(AVG(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 2) AS ticket_promedio
FROM dim_estado e
LEFT JOIN fact_ordenes f ON e.estado_canonico = f.estado_canonico
GROUP BY 
    e.estado_canonico, 
    e.nombre_oficial
HAVING total_pedidos_entregados > 0
ORDER BY 
    total_ventas_netas DESC;
