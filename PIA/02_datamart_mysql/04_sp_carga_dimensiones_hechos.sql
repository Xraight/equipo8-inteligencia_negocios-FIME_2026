-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 04_sp_carga_dimensiones_hechos.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Implementar los procedimientos almacenados para la carga atómica, mapeo
-- de claves sustitutas y cálculo de métricas en Dimensiones y Tablas de Hechos.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Cargar dimensiones fijas (`dim_canal`, `dim_metodo_pago`).
-- 2. Cargar dimensiones maestras (`dim_producto`, `dim_cliente`, `dim_sucursal`)
--    con registros comodín (-1) para garantizar integridad referencial.
-- 3. Cargar la tabla de hechos central `fact_ventas_detalle` aplicando la fórmula
--    saneada de importes netos y márgenes.
-- 4. Cargar hechos satélites: `fact_devoluciones`, `fact_instalaciones`,
--    `fact_inventario_snapshot`.
-- ==============================================================================

USE `ce_bi`;

DELIMITER //

-- ------------------------------------------------------------------------------
-- 1. Carga de Dimensiones Conformes
-- ------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_etl_cargar_dimensiones`//
CREATE PROCEDURE `sp_etl_cargar_dimensiones`()
BEGIN
  DECLARE v_inicio DATETIME;
  DECLARE v_fin DATETIME;
  DECLARE v_prods BIGINT DEFAULT 0;
  DECLARE v_clis BIGINT DEFAULT 0;
  DECLARE v_sucs BIGINT DEFAULT 0;

  SET v_inicio = NOW();

  -- Carga Canales
  INSERT INTO `dim_canal` (`canal_id`, `canal_nombre`)
  VALUES (1, 'Tienda'), (2, 'Web'), (3, 'App')
  ON DUPLICATE KEY UPDATE `canal_nombre` = VALUES(`canal_nombre`);

  -- Carga Métodos de Pago
  INSERT INTO `dim_metodo_pago` (`metodo_pago_id`, `metodo_nombre`)
  VALUES (1, 'Tarjeta'), (2, 'Efectivo'), (3, 'Transferencia'), (4, 'Wallet')
  ON DUPLICATE KEY UPDATE `metodo_nombre` = VALUES(`metodo_nombre`);

  -- Carga Dimensión Producto (con comodín)
  INSERT INTO `dim_producto` (
    `producto_key`, `producto_id`, `sku`, `producto`, `categoria`,
    `marca`, `costo`, `precio_lista`, `margen_teorico_pct`, `activo`, `requiere_instalacion`
  ) VALUES (
    1, 'NO-ID', 'SKU-000', 'Producto No Identificado', 'Sin Categoría',
    'Genérica', 0.00, 0.00, 0.00, 'NO', 'NO'
  ) ON DUPLICATE KEY UPDATE `producto` = VALUES(`producto`);

  INSERT INTO `dim_producto` (
    `producto_id`, `sku`, `producto`, `categoria`, `marca`,
    `costo`, `precio_lista`, `margen_teorico_pct`, `activo`, `requiere_instalacion`
  )
  SELECT
    p.`producto_id`,
    p.`sku`,
    p.`producto`,
    p.`categoria`,
    p.`marca`,
    CAST(p.`costo` AS DECIMAL(12,2)),
    CAST(p.`precio_lista` AS DECIMAL(12,2)),
    ROUND(((CAST(p.`precio_lista` AS DECIMAL(12,2)) - CAST(p.`costo` AS DECIMAL(12,2))) / CAST(p.`precio_lista` AS DECIMAL(12,2))) * 100, 2),
    p.`activo`,
    p.`requiere_instalacion`
  FROM `stg_ce_productos` p
  ON DUPLICATE KEY UPDATE
    `producto` = VALUES(`producto`),
    `categoria` = VALUES(`categoria`),
    `marca` = VALUES(`marca`),
    `costo` = VALUES(`costo`),
    `precio_lista` = VALUES(`precio_lista`);

  SELECT COUNT(*) INTO v_prods FROM `dim_producto`;

  -- Carga Dimensión Cliente (con comodín)
  INSERT INTO `dim_cliente` (
    `cliente_key`, `cliente_id`, `nombre`, `sexo`, `fecha_alta`,
    `ciudad`, `segmento`, `email`
  ) VALUES (
    1, 'NO-ID', 'Cliente Mostrador / No Identificado', 'No Especificado', '2024-01-01',
    'No Especificada', 'General', 'sin_correo@ejemplo.com'
  ) ON DUPLICATE KEY UPDATE `nombre` = VALUES(`nombre`);

  INSERT INTO `dim_cliente` (
    `cliente_id`, `nombre`, `sexo`, `fecha_alta`, `ciudad`, `segmento`, `email`
  )
  SELECT
    c.`cliente_id`,
    c.`nombre`,
    c.`sexo`,
    STR_TO_DATE(c.`fecha_alta`, '%Y-%m-%d'),
    c.`ciudad`,
    c.`segmento`,
    c.`email`
  FROM `stg_ce_clientes` c
  ON DUPLICATE KEY UPDATE
    `nombre` = VALUES(`nombre`),
    `sexo` = VALUES(`sexo`),
    `ciudad` = VALUES(`ciudad`),
    `segmento` = VALUES(`segmento`),
    `email` = VALUES(`email`);

  SELECT COUNT(*) INTO v_clis FROM `dim_cliente`;

  -- Carga Dimensión Sucursal (con comodín)
  INSERT INTO `dim_sucursal` (
    `sucursal_key`, `sucursal_id`, `sucursal`, `ciudad`, `estado`,
    `m2`, `categoria_tamano`, `fecha_apertura`
  ) VALUES (
    1, 'NO-ID', 'Sucursal Central / No Identificada', 'Monterrey', 'Nuevo León',
    1000, 'Mediana (1200-1600 m2)', '2020-01-01'
  ) ON DUPLICATE KEY UPDATE `sucursal` = VALUES(`sucursal`);

  INSERT INTO `dim_sucursal` (
    `sucursal_id`, `sucursal`, `ciudad`, `estado`, `m2`,
    `categoria_tamano`, `fecha_apertura`
  )
  SELECT
    s.`sucursal_id`,
    s.`sucursal`,
    s.`ciudad`,
    s.`estado`,
    CAST(s.`m2` AS SIGNED),
    CASE
      WHEN CAST(s.`m2` AS SIGNED) < 1200 THEN 'Pequeña (<1200 m2)'
      WHEN CAST(s.`m2` AS SIGNED) <= 1600 THEN 'Mediana (1200-1600 m2)'
      ELSE 'Grande (>1600 m2)'
    END,
    STR_TO_DATE(s.`fecha_apertura`, '%Y-%m-%d')
  FROM `stg_ce_sucursales` s
  ON DUPLICATE KEY UPDATE
    `sucursal` = VALUES(`sucursal`),
    `ciudad` = VALUES(`ciudad`),
    `m2` = VALUES(`m2`),
    `categoria_tamano` = VALUES(`categoria_tamano`);

  SELECT COUNT(*) INTO v_sucs FROM `dim_sucursal`;

  SET v_fin = NOW();

  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'sp_etl_cargar_dimensiones', v_inicio, v_fin,
    TIMESTAMPDIFF(MICROSECOND, v_inicio, v_fin) / 1000000.0,
    v_prods + v_clis + v_sucs, v_prods + v_clis + v_sucs, 0, 'EXITOSO',
    CONCAT('Dimensiones cargadas: Prods=', v_prods, ', Clis=', v_clis, ', Sucs=', v_sucs)
  );
END //

-- ------------------------------------------------------------------------------
-- 2. Carga del Hecho Principal: fact_ventas_detalle
-- ------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_etl_cargar_fact_ventas`//
CREATE PROCEDURE `sp_etl_cargar_fact_ventas`()
BEGIN
  DECLARE v_inicio DATETIME;
  DECLARE v_fin DATETIME;
  DECLARE v_leidas BIGINT DEFAULT 0;
  DECLARE v_cargadas BIGINT DEFAULT 0;

  SET v_inicio = NOW();

  SELECT COUNT(*) INTO v_leidas FROM `stg_ce_detalle_ventas`;

  -- Limpiar tabla de hechos antes de recarga completa
  TRUNCATE TABLE `fact_ventas_detalle`;

  INSERT INTO `fact_ventas_detalle` (
    `venta_id`, `linea`, `tiempo_id`, `producto_key`, `cliente_key`,
    `sucursal_key`, `canal_id`, `metodo_pago_id`, `hora_venta`,
    `cantidad`, `precio_unitario`, `descuento_pct`,
    `monto_bruto`, `monto_descuento`, `monto_neto`,
    `costo_unitario`, `costo_total`, `utilidad_bruta`, `margen_pct`, `es_devuelto`
  )
  SELECT
    dv.`venta_id`,
    CAST(dv.`linea` AS SIGNED) AS `linea`,
    (YEAR(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 10000 +
     MONTH(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 100 +
     DAY(STR_TO_DATE(v.`fecha`, '%Y-%m-%d'))) AS `tiempo_id`,
    COALESCE(dp.`producto_key`, 1) AS `producto_key`,
    COALESCE(dc.`cliente_key`, 1)  AS `cliente_key`,
    COALESCE(ds.`sucursal_key`, 1) AS `sucursal_key`,
    CASE LOWER(TRIM(v.`canal`))
      WHEN 'tienda' THEN 1
      WHEN 'web'    THEN 2
      WHEN 'app'    THEN 3
      ELSE 1
    END AS `canal_id`,
    CASE LOWER(TRIM(v.`metodo_pago`))
      WHEN 'tarjeta'       THEN 1
      WHEN 'efectivo'      THEN 2
      WHEN 'transferencia' THEN 3
      WHEN 'wallet'        THEN 4
      ELSE 1
    END AS `metodo_pago_id`,
    CAST(v.`hora` AS TIME) AS `hora_venta`,
    CAST(dv.`cantidad` AS SIGNED) AS `cantidad`,
    CAST(dv.`precio_unitario` AS DECIMAL(12,2)) AS `precio_unitario`,
    CAST(dv.`descuento_pct` AS DECIMAL(5,2)) AS `descuento_pct`,
    -- Subtotal bruto
    ROUND(CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2)), 2) AS `monto_bruto`,
    -- Descuento concedido en pesos
    ROUND((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) * (CAST(dv.`descuento_pct` AS DECIMAL(5,2)) / 100.0), 2) AS `monto_descuento`,
    -- Venta neta real
    ROUND((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) -
          ((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) * (CAST(dv.`descuento_pct` AS DECIMAL(5,2)) / 100.0)), 2) AS `monto_neto`,
    -- Costo unitario según catálogo maestro
    dp.`costo` AS `costo_unitario`,
    -- Costo de la mercancía vendida (COGS)
    ROUND(CAST(dv.`cantidad` AS SIGNED) * dp.`costo`, 2) AS `costo_total`,
    -- Utilidad Bruta Real
    ROUND(((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) -
           ((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) * (CAST(dv.`descuento_pct` AS DECIMAL(5,2)) / 100.0))) -
          (CAST(dv.`cantidad` AS SIGNED) * dp.`costo`), 2) AS `utilidad_bruta`,
    -- Margen porcentual
    ROUND(((((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) -
            ((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) * (CAST(dv.`descuento_pct` AS DECIMAL(5,2)) / 100.0))) -
           (CAST(dv.`cantidad` AS SIGNED) * dp.`costo`)) /
           NULLIF(((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) -
                   ((CAST(dv.`cantidad` AS SIGNED) * CAST(dv.`precio_unitario` AS DECIMAL(12,2))) * (CAST(dv.`descuento_pct` AS DECIMAL(5,2)) / 100.0))), 0)) * 100, 2) AS `margen_pct`,
    -- Bandera de devolución
    IF(dev.`venta_id` IS NOT NULL, 1, 0) AS `es_devuelto`
  FROM `stg_ce_detalle_ventas` dv
  INNER JOIN `stg_ce_ventas` v ON dv.`venta_id` = v.`venta_id`
  LEFT JOIN `dim_producto` dp ON dv.`producto_id` = dp.`producto_id`
  LEFT JOIN `dim_cliente` dc ON v.`cliente_id` = dc.`cliente_id`
  LEFT JOIN `dim_sucursal` ds ON v.`sucursal_id` = ds.`sucursal_id`
  LEFT JOIN (
    SELECT DISTINCT `venta_id`, `producto_id` FROM `stg_ce_devoluciones`
  ) dev ON dv.`venta_id` = dev.`venta_id` AND dv.`producto_id` = dev.`producto_id`;

  SELECT COUNT(*) INTO v_cargadas FROM `fact_ventas_detalle`;

  SET v_fin = NOW();

  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'sp_etl_cargar_fact_ventas', v_inicio, v_fin,
    TIMESTAMPDIFF(MICROSECOND, v_inicio, v_fin) / 1000000.0,
    v_leidas, v_cargadas, (v_leidas - v_cargadas), 'EXITOSO',
    'Carga atómica de fact_ventas_detalle con desglose de montos brutos, descuentos, netos y COGS'
  );
END //

-- ------------------------------------------------------------------------------
-- 3. Carga de Hechos Satélites
-- ------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_etl_cargar_hechos_satelites`//
CREATE PROCEDURE `sp_etl_cargar_hechos_satelites`()
BEGIN
  DECLARE v_inicio DATETIME;
  DECLARE v_fin DATETIME;
  DECLARE v_devs BIGINT DEFAULT 0;
  DECLARE v_inst BIGINT DEFAULT 0;
  DECLARE v_inv BIGINT DEFAULT 0;

  SET v_inicio = NOW();

  -- 3.1. Carga fact_devoluciones
  TRUNCATE TABLE `fact_devoluciones`;
  INSERT INTO `fact_devoluciones` (
    `devolucion_id`, `venta_id`, `tiempo_id`, `producto_key`,
    `sucursal_key`, `cliente_key`, `cantidad_devuelta`, `importe_devuelto`, `motivo`
  )
  SELECT
    d.`devolucion_id`,
    d.`venta_id`,
    (YEAR(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 10000 +
     MONTH(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 100 +
     DAY(STR_TO_DATE(v.`fecha`, '%Y-%m-%d'))) AS `tiempo_id`,
    COALESCE(dp.`producto_key`, 1) AS `producto_key`,
    COALESCE(ds.`sucursal_key`, 1) AS `sucursal_key`,
    COALESCE(dc.`cliente_key`, 1)  AS `cliente_key`,
    CAST(d.`cantidad_devuelta` AS SIGNED),
    CAST(d.`importe_devuelto` AS DECIMAL(14,2)),
    TRIM(d.`motivo`)
  FROM `stg_ce_devoluciones` d
  INNER JOIN `stg_ce_ventas` v ON d.`venta_id` = v.`venta_id`
  LEFT JOIN `dim_producto` dp ON d.`producto_id` = dp.`producto_id`
  LEFT JOIN `dim_sucursal` ds ON v.`sucursal_id` = ds.`sucursal_id`
  LEFT JOIN `dim_cliente` dc ON v.`cliente_id` = dc.`cliente_id`;

  SELECT COUNT(*) INTO v_devs FROM `fact_devoluciones`;

  -- 3.2. Carga fact_instalaciones
  TRUNCATE TABLE `fact_instalaciones`;
  INSERT INTO `fact_instalaciones` (
    `instalacion_id`, `venta_id`, `tiempo_id`, `cliente_key`,
    `sucursal_key`, `dias_programados`, `dias_reales`,
    `dias_desviacion`, `cumplio_sla`, `satisfaccion`
  )
  SELECT
    i.`instalacion_id`,
    i.`venta_id`,
    (YEAR(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 10000 +
     MONTH(STR_TO_DATE(v.`fecha`, '%Y-%m-%d')) * 100 +
     DAY(STR_TO_DATE(v.`fecha`, '%Y-%m-%d'))) AS `tiempo_id`,
    COALESCE(dc.`cliente_key`, 1)  AS `cliente_key`,
    COALESCE(ds.`sucursal_key`, 1) AS `sucursal_key`,
    CAST(i.`dias_programados` AS SIGNED),
    CAST(i.`dias_reales` AS SIGNED),
    (CAST(i.`dias_reales` AS SIGNED) - CAST(i.`dias_programados` AS SIGNED)),
    IF(CAST(i.`dias_reales` AS SIGNED) <= CAST(i.`dias_programados` AS SIGNED), 1, 0),
    CAST(i.`satisfaccion` AS SIGNED)
  FROM `stg_ce_instalaciones` i
  INNER JOIN `stg_ce_ventas` v ON i.`venta_id` = v.`venta_id`
  LEFT JOIN `dim_cliente` dc ON v.`cliente_id` = dc.`cliente_id`
  LEFT JOIN `dim_sucursal` ds ON v.`sucursal_id` = ds.`sucursal_id`;

  SELECT COUNT(*) INTO v_inst FROM `fact_instalaciones`;

  -- 3.3. Carga fact_inventario_snapshot
  TRUNCATE TABLE `fact_inventario_snapshot`;
  INSERT INTO `fact_inventario_snapshot` (
    `sucursal_key`, `producto_key`, `stock_actual`, `punto_reorden`,
    `deficit_unidades`, `valor_inventario_costo`, `estatus_stock`
  )
  SELECT
    COALESCE(ds.`sucursal_key`, 1) AS `sucursal_key`,
    COALESCE(dp.`producto_key`, 1) AS `producto_key`,
    CAST(e.`existencia` AS SIGNED) AS `stock_actual`,
    CAST(e.`punto_reorden` AS SIGNED) AS `punto_reorden`,
    GREATEST(0, CAST(e.`punto_reorden` AS SIGNED) - CAST(e.`existencia` AS SIGNED)) AS `deficit_unidades`,
    ROUND(CAST(e.`existencia` AS SIGNED) * dp.`costo`, 2) AS `valor_inventario_costo`,
    CASE
      WHEN CAST(e.`existencia` AS SIGNED) = 0 THEN 'Rotura Stock'
      WHEN CAST(e.`existencia` AS SIGNED) <= CAST(e.`punto_reorden` AS SIGNED) THEN 'Alerta Reorden'
      ELSE 'Optimo'
    END AS `estatus_stock`
  FROM `stg_ce_existencias` e
  INNER JOIN `dim_sucursal` ds ON e.`sucursal_id` = ds.`sucursal_id`
  INNER JOIN `dim_producto` dp ON e.`producto_id` = dp.`producto_id`;

  SELECT COUNT(*) INTO v_inv FROM `fact_inventario_snapshot`;

  SET v_fin = NOW();

  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'sp_etl_cargar_hechos_satelites', v_inicio, v_fin,
    TIMESTAMPDIFF(MICROSECOND, v_inicio, v_fin) / 1000000.0,
    v_devs + v_inst + v_inv, v_devs + v_inst + v_inv, 0, 'EXITOSO',
    CONCAT('Hechos satélites cargados: Devs=', v_devs, ', Inst=', v_inst, ', Inv=', v_inv)
  );
END //

DELIMITER ;

SELECT 'Procedimientos de carga dimensional y hechos creados exitosamente.' AS resultado;
