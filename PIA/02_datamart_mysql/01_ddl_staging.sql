-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 01_ddl_staging.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Definir la capa de persistencia intermedia (Staging Area) para la ingesta
-- directa y sin alteraciones destructivas de los 11 archivos CSV del ecosistema RAW.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Crear las 11 tablas temporales/staging con prefijo `stg_ce_`.
-- 2. Implementar tipos de datos tolerantes para capturar cadenas, nulos y formatos.
-- 3. Incorporar metadatos de carga (`fecha_ingesta` y `archivo_origen`) para auditoría.
-- ==============================================================================

USE `ce_bi`;

-- ------------------------------------------------------------------------------
-- 1. Staging Productos (ERP)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_productos`;
CREATE TABLE `stg_ce_productos` (
  `producto_id` VARCHAR(50),
  `sku` VARCHAR(50),
  `producto` VARCHAR(255),
  `categoria` VARCHAR(100),
  `marca` VARCHAR(100),
  `costo` VARCHAR(50),
  `precio_lista` VARCHAR(50),
  `activo` VARCHAR(20),
  `requiere_instalacion` VARCHAR(20),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Capa Staging: Productos ERP';

-- ------------------------------------------------------------------------------
-- 2. Staging Proveedores (ERP)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_proveedores`;
CREATE TABLE `stg_ce_proveedores` (
  `proveedor_id` VARCHAR(50),
  `proveedor` VARCHAR(255),
  `ciudad` VARCHAR(100),
  `lead_time_dias` VARCHAR(50),
  `rating` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Capa Staging: Proveedores ERP';

-- ------------------------------------------------------------------------------
-- 3. Staging Clientes (CRM)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_clientes`;
CREATE TABLE `stg_ce_clientes` (
  `cliente_id` VARCHAR(50),
  `nombre` VARCHAR(255),
  `sexo` VARCHAR(20),
  `fecha_alta` VARCHAR(50),
  `ciudad` VARCHAR(100),
  `segmento` VARCHAR(50),
  `email` VARCHAR(255),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Capa Staging: Clientes CRM';

-- ------------------------------------------------------------------------------
-- 4. Staging Sucursales (Operación)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_sucursales`;
CREATE TABLE `stg_ce_sucursales` (
  `sucursal_id` VARCHAR(50),
  `sucursal` VARCHAR(255),
  `ciudad` VARCHAR(100),
  `estado` VARCHAR(100),
  `m2` VARCHAR(50),
  `fecha_apertura` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Capa Staging: Sucursales de Operación';

-- ------------------------------------------------------------------------------
-- 5. Staging Promociones (Marketing)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_promociones`;
CREATE TABLE `stg_ce_promociones` (
  `promocion_id` VARCHAR(50),
  `nombre` VARCHAR(255),
  `fecha_inicio` VARCHAR(50),
  `descuento_pct` VARCHAR(50),
  `fecha_fin` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB COMMENT='Capa Staging: Promociones Marketing';

-- ------------------------------------------------------------------------------
-- 6. Staging Ventas Cabecera (POS)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_ventas`;
CREATE TABLE `stg_ce_ventas` (
  `venta_id` VARCHAR(50),
  `fecha` VARCHAR(50),
  `hora` VARCHAR(50),
  `sucursal_id` VARCHAR(50),
  `cliente_id` VARCHAR(50),
  `canal` VARCHAR(50),
  `metodo_pago` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_v_venta_id` (`venta_id`),
  INDEX `idx_stg_v_fecha` (`fecha`)
) ENGINE=InnoDB COMMENT='Capa Staging: Ventas Cabecera POS';

-- ------------------------------------------------------------------------------
-- 7. Staging Detalle de Ventas (POS)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_detalle_ventas`;
CREATE TABLE `stg_ce_detalle_ventas` (
  `venta_id` VARCHAR(50),
  `linea` VARCHAR(50),
  `producto_id` VARCHAR(50),
  `cantidad` VARCHAR(50),
  `precio_unitario` VARCHAR(50),
  `descuento_pct` VARCHAR(50),
  `importe` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_dv_venta_linea` (`venta_id`, `linea`),
  INDEX `idx_stg_dv_producto` (`producto_id`)
) ENGINE=InnoDB COMMENT='Capa Staging: Detalle de Líneas de Ventas POS';

-- ------------------------------------------------------------------------------
-- 8. Staging Devoluciones (POS)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_devoluciones`;
CREATE TABLE `stg_ce_devoluciones` (
  `devolucion_id` VARCHAR(50),
  `venta_id` VARCHAR(50),
  `producto_id` VARCHAR(50),
  `cantidad_devuelta` VARCHAR(50),
  `importe_devuelto` VARCHAR(50),
  `motivo` VARCHAR(100),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_dev_venta_prod` (`venta_id`, `producto_id`)
) ENGINE=InnoDB COMMENT='Capa Staging: Devoluciones POS';

-- ------------------------------------------------------------------------------
-- 9. Staging Existencias (Inventario)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_existencias`;
CREATE TABLE `stg_ce_existencias` (
  `sucursal_id` VARCHAR(50),
  `producto_id` VARCHAR(50),
  `existencia` VARCHAR(50),
  `punto_reorden` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_ex_suc_prod` (`sucursal_id`, `producto_id`)
) ENGINE=InnoDB COMMENT='Capa Staging: Existencias de Inventario';

-- ------------------------------------------------------------------------------
-- 10. Staging Órdenes de Compra (Compras)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_ordenes_compra`;
CREATE TABLE `stg_ce_ordenes_compra` (
  `orden_id` VARCHAR(50),
  `fecha_orden` VARCHAR(50),
  `proveedor_id` VARCHAR(50),
  `sucursal_id` VARCHAR(50),
  `producto_id` VARCHAR(50),
  `cantidad` VARCHAR(50),
  `estatus` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_oc_orden` (`orden_id`)
) ENGINE=InnoDB COMMENT='Capa Staging: Órdenes de Compra';

-- ------------------------------------------------------------------------------
-- 11. Staging Instalaciones (Específico Mueblería)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `stg_ce_instalaciones`;
CREATE TABLE `stg_ce_instalaciones` (
  `instalacion_id` VARCHAR(50),
  `venta_id` VARCHAR(50),
  `dias_programados` VARCHAR(50),
  `dias_reales` VARCHAR(50),
  `satisfaccion` VARCHAR(50),
  `fecha_ingesta` DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_stg_inst_venta` (`venta_id`)
) ENGINE=InnoDB COMMENT='Capa Staging: Servicios de Instalación';

SELECT 'Tablas de Staging (11 tablas stg_ce_*) creadas exitosamente.' AS resultado;
