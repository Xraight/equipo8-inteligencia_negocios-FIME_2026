-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 07_auditoria_balance_masa.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Ejecutar auditorías de calidad, consistencia relacional y balance de masa
-- certificando que el Data Mart no presenta pérdidas de transacciones ni descuadres.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Validar conteos entre Staging y Data Mart (Balance de Masa).
-- 2. Validar que no existen claves foráneas huérfanas o nulas en hechos.
-- 3. Validar la precisión matemática de la ecuación contable:
--    Monto Neto = Monto Bruto - Monto Descuento
--    Utilidad Bruta = Monto Neto - Costo Total
-- 4. Emitir el reporte oficial de certificación del Data Mart.
-- ==============================================================================

USE `ce_bi`;

-- ------------------------------------------------------------------------------
-- 1. Reporte de Balance de Masa Oficial
-- ------------------------------------------------------------------------------
SELECT
  `concepto` AS 'Entidad Auditada',
  `conteo_origen_raw` AS 'Volumen RAW',
  `conteo_staging` AS 'Volumen Staging',
  `conteo_datamart` AS 'Volumen Data Mart',
  `discrepancia` AS 'Discrepancia',
  CONCAT(`porcentaje_integridad`, '%') AS 'Integridad (%)',
  `estatus_validacion` AS 'Estatus Oficial'
FROM `etl_balance_masa`;

-- ------------------------------------------------------------------------------
-- 2. Verificación de Integridad Referencial (Huérfanos en fact_ventas_detalle)
-- ------------------------------------------------------------------------------
SELECT
  SUM(CASE WHEN `tiempo_id` IS NULL THEN 1 ELSE 0 END) AS 'Huerfanos Tiempo',
  SUM(CASE WHEN `producto_key` IS NULL OR `producto_key` = 0 THEN 1 ELSE 0 END) AS 'Huerfanos Producto',
  SUM(CASE WHEN `cliente_key` IS NULL OR `cliente_key` = 0 THEN 1 ELSE 0 END) AS 'Huerfanos Cliente',
  SUM(CASE WHEN `sucursal_key` IS NULL OR `sucursal_key` = 0 THEN 1 ELSE 0 END) AS 'Huerfanos Sucursal',
  SUM(CASE WHEN `canal_id` IS NULL OR `canal_id` = 0 THEN 1 ELSE 0 END) AS 'Huerfanos Canal',
  SUM(CASE WHEN `metodo_pago_id` IS NULL OR `metodo_pago_id` = 0 THEN 1 ELSE 0 END) AS 'Huerfanos Metodo Pago'
FROM `fact_ventas_detalle`;

-- ------------------------------------------------------------------------------
-- 3. Verificación de Ecuación Contable y Cero Discrepancias
-- ------------------------------------------------------------------------------
SELECT
  COUNT(*) AS 'Total Registros Auditados',
  SUM(CASE WHEN ABS(`monto_neto` - (`monto_bruto` - `monto_descuento`)) > 0.01 THEN 1 ELSE 0 END) AS 'Inconsistencias Venta Neta',
  SUM(CASE WHEN ABS(`utilidad_bruta` - (`monto_neto` - `costo_total`)) > 0.01 THEN 1 ELSE 0 END) AS 'Inconsistencias Utilidad Bruta',
  SUM(CASE WHEN `monto_neto` < 0 THEN 1 ELSE 0 END) AS 'Montos Negativos',
  SUM(CASE WHEN `cantidad` <= 0 THEN 1 ELSE 0 END) AS 'Cantidades No Positivas'
FROM `fact_ventas_detalle`;

-- ------------------------------------------------------------------------------
-- 4. Totales Financieros de Control (Cifras Oficiales de Certificación)
-- ------------------------------------------------------------------------------
SELECT
  COUNT(DISTINCT `venta_id`) AS 'Tickets Únicos',
  COUNT(*) AS 'Líneas Totales Vendidas',
  SUM(`cantidad`) AS 'Unidades Físicas',
  CONCAT('$', FORMAT(SUM(`monto_bruto`), 2)) AS 'Venta Bruta Global',
  CONCAT('$', FORMAT(SUM(`monto_descuento`), 2)) AS 'Descuentos Totales',
  CONCAT('$', FORMAT(SUM(`monto_neto`), 2)) AS 'Venta Neta Global',
  CONCAT('$', FORMAT(SUM(`costo_total`), 2)) AS 'COGS Global',
  CONCAT('$', FORMAT(SUM(`utilidad_bruta`), 2)) AS 'Utilidad Bruta Global',
  CONCAT(ROUND((SUM(`utilidad_bruta`) / SUM(`monto_neto`)) * 100, 2), '%') AS 'Margen Bruto Pct',
  CONCAT('$', FORMAT(SUM(`monto_neto`) / COUNT(DISTINCT `venta_id`), 2)) AS 'Ticket Promedio Global'
FROM `fact_ventas_detalle`;
