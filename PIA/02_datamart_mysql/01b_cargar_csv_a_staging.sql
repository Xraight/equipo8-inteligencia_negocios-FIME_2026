-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 01b_cargar_csv_a_staging.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Ingestar masiva y ultrarrápida de los 11 archivos CSV del ecosistema RAW
-- hacia las tablas staging de `ce_bi` mediante `LOAD DATA INFILE`.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Limpiar previamente las 11 tablas staging (TRUNCATE).
-- 2. Cargar cada CSV saltando la cabecera (IGNORE 1 LINES) y preservando los datos.
-- 3. Emitir el conteo de filas cargadas para verificación inmediata.
-- ==============================================================================

USE `ce_bi`;

-- 1. Productos ERP
TRUNCATE TABLE `stg_ce_productos`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/ERP/productos.csv'
INTO TABLE `stg_ce_productos`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`producto_id`, `sku`, `producto`, `categoria`, `marca`, `costo`, `precio_lista`, `activo`, `requiere_instalacion`);

-- 2. Proveedores ERP
TRUNCATE TABLE `stg_ce_proveedores`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/ERP/proveedores.csv'
INTO TABLE `stg_ce_proveedores`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`proveedor_id`, `proveedor`, `ciudad`, `lead_time_dias`, `rating`);

-- 3. Clientes CRM
TRUNCATE TABLE `stg_ce_clientes`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/CRM/clientes.csv'
INTO TABLE `stg_ce_clientes`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`cliente_id`, `nombre`, `sexo`, `fecha_alta`, `ciudad`, `segmento`, `email`);

-- 4. Sucursales Operación
TRUNCATE TABLE `stg_ce_sucursales`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/OPERACION/sucursales.csv'
INTO TABLE `stg_ce_sucursales`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`sucursal_id`, `sucursal`, `ciudad`, `estado`, `m2`, `fecha_apertura`);

-- 5. Promociones Marketing
TRUNCATE TABLE `stg_ce_promociones`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/MARKETING/promociones.csv'
INTO TABLE `stg_ce_promociones`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`promocion_id`, `nombre`, `fecha_inicio`, `descuento_pct`, `fecha_fin`);

-- 6. Ventas Cabecera POS
TRUNCATE TABLE `stg_ce_ventas`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/POS/ventas.csv'
INTO TABLE `stg_ce_ventas`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`venta_id`, `fecha`, `hora`, `sucursal_id`, `cliente_id`, `canal`, `metodo_pago`);

-- 7. Detalle de Ventas POS
TRUNCATE TABLE `stg_ce_detalle_ventas`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/POS/detalle_ventas.csv'
INTO TABLE `stg_ce_detalle_ventas`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`venta_id`, `linea`, `producto_id`, `cantidad`, `precio_unitario`, `descuento_pct`, `importe`);

-- 8. Devoluciones POS
TRUNCATE TABLE `stg_ce_devoluciones`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/POS/devoluciones.csv'
INTO TABLE `stg_ce_devoluciones`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`devolucion_id`, `venta_id`, `producto_id`, `cantidad_devuelta`, `importe_devuelto`, `motivo`);

-- 9. Existencias Inventario
TRUNCATE TABLE `stg_ce_existencias`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/INVENTARIO/existencias.csv'
INTO TABLE `stg_ce_existencias`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`sucursal_id`, `producto_id`, `existencia`, `punto_reorden`);

-- 10. Órdenes de Compra
TRUNCATE TABLE `stg_ce_ordenes_compra`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/COMPRAS/ordenes_compra.csv'
INTO TABLE `stg_ce_ordenes_compra`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`orden_id`, `fecha_orden`, `proveedor_id`, `sucursal_id`, `producto_id`, `cantidad`, `estatus`);

-- 11. Instalaciones
TRUNCATE TABLE `stg_ce_instalaciones`;
LOAD DATA INFILE '/var/lib/mysql-files/raw/ESPECIFICO/instalaciones.csv'
INTO TABLE `stg_ce_instalaciones`
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(`instalacion_id`, `venta_id`, `dias_programados`, `dias_reales`, `satisfaccion`);

-- Resumen de filas en Staging
SELECT
  (SELECT COUNT(*) FROM `stg_ce_productos`) AS `stg_productos`,
  (SELECT COUNT(*) FROM `stg_ce_proveedores`) AS `stg_proveedores`,
  (SELECT COUNT(*) FROM `stg_ce_clientes`) AS `stg_clientes`,
  (SELECT COUNT(*) FROM `stg_ce_sucursales`) AS `stg_sucursales`,
  (SELECT COUNT(*) FROM `stg_ce_promociones`) AS `stg_promociones`,
  (SELECT COUNT(*) FROM `stg_ce_ventas`) AS `stg_ventas`,
  (SELECT COUNT(*) FROM `stg_ce_detalle_ventas`) AS `stg_detalle_ventas`,
  (SELECT COUNT(*) FROM `stg_ce_devoluciones`) AS `stg_devoluciones`,
  (SELECT COUNT(*) FROM `stg_ce_existencias`) AS `stg_existencias`,
  (SELECT COUNT(*) FROM `stg_ce_ordenes_compra`) AS `stg_ordenes_compra`,
  (SELECT COUNT(*) FROM `stg_ce_instalaciones`) AS `stg_instalaciones`;
