-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 06_vistas_analiticas_kpi.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Crear vistas SQL analíticas pre-agregadas para alimentar tableros de control,
-- reporting ejecutivo y facilitar la extracción hacia Excel y Power Pivot.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. `vw_kpi_resumen_mensual`: Tendencia histórica de ventas netas, utilidad y margen.
-- 2. `vw_kpi_desempeno_categorias`: Desglose por línea de producto y devoluciones
--    (diseñado estrictamente compatible con ONLY_FULL_GROUP_BY).
-- 3. `vw_kpi_omnicanalidad`: Análisis comparativo Tienda vs Web vs App.
-- 4. `vw_kpi_sucursales`: Rentabilidad y ventas por metro cuadrado de exhibición.
-- 5. `vw_kpi_instalaciones_sla`: Nivel de servicio, días de retraso y satisfacción.
-- 6. `vw_kpi_inventario_critico`: Alertas de desabasto y quiebres de stock.
-- ==============================================================================

USE `ce_bi`;

-- ------------------------------------------------------------------------------
-- 1. Vista: Resumen Mensual de Ventas, Margen y Ticket Promedio
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_resumen_mensual`;
CREATE VIEW `vw_kpi_resumen_mensual` AS
SELECT
  t.`anio`,
  t.`mes`,
  t.`mes_nombre`,
  t.`mes_anio`,
  COUNT(DISTINCT f.`venta_id`) AS `transacciones`,
  SUM(f.`cantidad`) AS `unidades_vendidas`,
  SUM(f.`monto_bruto`) AS `venta_bruta`,
  SUM(f.`monto_descuento`) AS `descuentos_otorgados`,
  SUM(f.`monto_neto`) AS `venta_neta`,
  SUM(f.`costo_total`) AS `costo_ventas_cogs`,
  SUM(f.`utilidad_bruta`) AS `utilidad_bruta`,
  ROUND((SUM(f.`utilidad_bruta`) / NULLIF(SUM(f.`monto_neto`), 0)) * 100, 2) AS `margen_bruto_pct`,
  ROUND(SUM(f.`monto_neto`) / NULLIF(COUNT(DISTINCT f.`venta_id`), 0), 2) AS `ticket_promedio`
FROM `fact_ventas_detalle` f
INNER JOIN `dim_tiempo` t ON f.`tiempo_id` = t.`tiempo_id`
GROUP BY t.`anio`, t.`mes`, t.`mes_nombre`, t.`mes_anio`
ORDER BY t.`anio`, t.`mes`;

-- ------------------------------------------------------------------------------
-- 2. Vista: Desempeño por Categoría de Muebles y Decoración (Subconsultas aisladas)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_desempeno_categorias`;
CREATE VIEW `vw_kpi_desempeno_categorias` AS
SELECT
  v.`categoria`,
  v.`skus_activos`,
  v.`unidades_vendidas`,
  v.`venta_bruta`,
  v.`venta_neta`,
  v.`costo_total`,
  v.`utilidad_bruta`,
  ROUND((v.`utilidad_bruta` / NULLIF(v.`venta_neta`, 0)) * 100, 2) AS `margen_pct`,
  COALESCE(d.`unidades_devueltas`, 0) AS `unidades_devueltas`,
  COALESCE(d.`monto_devuelto`, 0.00) AS `monto_devuelto`,
  ROUND((COALESCE(d.`monto_devuelto`, 0.00) / NULLIF(v.`venta_bruta`, 0)) * 100, 2) AS `tasa_devolucion_pct`
FROM (
  SELECT
    p.`categoria`,
    COUNT(DISTINCT p.`producto_key`) AS `skus_activos`,
    SUM(f.`cantidad`) AS `unidades_vendidas`,
    SUM(f.`monto_bruto`) AS `venta_bruta`,
    SUM(f.`monto_neto`) AS `venta_neta`,
    SUM(f.`costo_total`) AS `costo_total`,
    SUM(f.`utilidad_bruta`) AS `utilidad_bruta`
  FROM `dim_producto` p
  INNER JOIN `fact_ventas_detalle` f ON p.`producto_key` = f.`producto_key`
  GROUP BY p.`categoria`
) v
LEFT JOIN (
  SELECT
    p.`categoria`,
    SUM(dev.`cantidad_devuelta`) AS `unidades_devueltas`,
    SUM(dev.`importe_devuelto`) AS `monto_devuelto`
  FROM `dim_producto` p
  INNER JOIN `fact_devoluciones` dev ON p.`producto_key` = dev.`producto_key`
  GROUP BY p.`categoria`
) d ON v.`categoria` = d.`categoria`
ORDER BY v.`venta_neta` DESC;

-- ------------------------------------------------------------------------------
-- 3. Vista: Desempeño Omnicanal (Tienda vs Web vs App)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_omnicanalidad`;
CREATE VIEW `vw_kpi_omnicanalidad` AS
SELECT
  c.`canal_nombre` AS `canal`,
  COUNT(DISTINCT f.`venta_id`) AS `transacciones`,
  SUM(f.`cantidad`) AS `unidades_vendidas`,
  SUM(f.`monto_neto`) AS `venta_neta`,
  ROUND(SUM(f.`monto_neto`) / NULLIF(COUNT(DISTINCT f.`venta_id`), 0), 2) AS `ticket_promedio`,
  SUM(f.`utilidad_bruta`) AS `utilidad_bruta`,
  ROUND((SUM(f.`utilidad_bruta`) / NULLIF(SUM(f.`monto_neto`), 0)) * 100, 2) AS `margen_pct`
FROM `dim_canal` c
INNER JOIN `fact_ventas_detalle` f ON c.`canal_id` = f.`canal_id`
GROUP BY c.`canal_nombre`
ORDER BY `venta_neta` DESC;

-- ------------------------------------------------------------------------------
-- 4. Vista: Productividad y Rentabilidad por Sucursal Física
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_sucursales`;
CREATE VIEW `vw_kpi_sucursales` AS
SELECT
  s.`sucursal_id`,
  s.`sucursal`,
  s.`ciudad`,
  s.`estado`,
  s.`m2`,
  s.`categoria_tamano`,
  COUNT(DISTINCT f.`venta_id`) AS `transacciones`,
  SUM(f.`monto_neto`) AS `venta_neta`,
  ROUND(SUM(f.`monto_neto`) / NULLIF(s.`m2`, 0), 2) AS `venta_por_m2`,
  SUM(f.`utilidad_bruta`) AS `utilidad_bruta`,
  ROUND((SUM(f.`utilidad_bruta`) / NULLIF(SUM(f.`monto_neto`), 0)) * 100, 2) AS `margen_pct`
FROM `dim_sucursal` s
INNER JOIN `fact_ventas_detalle` f ON s.`sucursal_key` = f.`sucursal_key`
GROUP BY s.`sucursal_id`, s.`sucursal`, s.`ciudad`, s.`estado`, s.`m2`, s.`categoria_tamano`
ORDER BY `venta_neta` DESC;

-- ------------------------------------------------------------------------------
-- 5. Vista: Nivel de Servicio Logístico (SLA Instalaciones)
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_instalaciones_sla`;
CREATE VIEW `vw_kpi_instalaciones_sla` AS
SELECT
  s.`sucursal`,
  COUNT(*) AS `total_servicios`,
  SUM(i.`cumplio_sla`) AS `servicios_a_tiempo`,
  SUM(1 - i.`cumplio_sla`) AS `servicios_con_retraso`,
  ROUND((SUM(i.`cumplio_sla`) / COUNT(*)) * 100, 2) AS `cumplimiento_sla_pct`,
  ROUND(AVG(i.`dias_reales`), 2) AS `dias_reales_promedio`,
  ROUND(AVG(i.`dias_desviacion`), 2) AS `dias_retraso_promedio`,
  ROUND(AVG(i.`satisfaccion`), 2) AS `satisfaccion_promedio`
FROM `fact_instalaciones` i
INNER JOIN `dim_sucursal` s ON i.`sucursal_key` = s.`sucursal_key`
GROUP BY s.`sucursal`
ORDER BY `cumplimiento_sla_pct` ASC;

-- ------------------------------------------------------------------------------
-- 6. Vista: Diagnóstico de Inventario y Riesgo de Rotura
-- ------------------------------------------------------------------------------
DROP VIEW IF EXISTS `vw_kpi_inventario_critico`;
CREATE VIEW `vw_kpi_inventario_critico` AS
SELECT
  s.`sucursal`,
  p.`producto_id`,
  p.`producto`,
  p.`categoria`,
  inv.`stock_actual`,
  inv.`punto_reorden`,
  inv.`deficit_unidades`,
  inv.`valor_inventario_costo`,
  inv.`estatus_stock`
FROM `fact_inventario_snapshot` inv
INNER JOIN `dim_sucursal` s ON inv.`sucursal_key` = s.`sucursal_key`
INNER JOIN `dim_producto` p ON inv.`producto_key` = p.`producto_key`
WHERE inv.`estatus_stock` IN ('Rotura Stock', 'Alerta Reorden')
ORDER BY inv.`deficit_unidades` DESC, inv.`stock_actual` ASC;

SELECT 'Vistas analíticas actualizadas y 100% compatibles con ONLY_FULL_GROUP_BY.' AS resultado;
