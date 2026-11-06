-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 02_ddl_datamart.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Definir la estructura física del Data Mart Dimensional en Esquema Estrella
-- (Constelación Analítica) para Casa&Estilo en la base de datos `ce_bi`.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Crear las dimensiones conformes (`dim_tiempo`, `dim_producto`, `dim_cliente`,
--    `dim_sucursal`, `dim_canal`, `dim_metodo_pago`).
-- 2. Crear las tablas de hechos atómicas y especializadas (`fact_ventas_detalle`,
--    `fact_devoluciones`, `fact_instalaciones`, `fact_inventario_snapshot`).
-- 3. Crear claves foráneas e índices B-Tree para optimización de consultas OLAP.
-- ==============================================================================

USE `ce_bi`;

-- Desactivar temporalmente revisión de claves foráneas para recreación limpia
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------------------------
-- 1. Dimensión Conforme: Tiempo / Calendario
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_tiempo`;
CREATE TABLE `dim_tiempo` (
  `tiempo_id` INT PRIMARY KEY COMMENT 'Clave primaria entera formato YYYYMMDD (ej. 20260517)',
  `fecha` DATE NOT NULL UNIQUE COMMENT 'Fecha calendario real',
  `anio` SMALLINT NOT NULL COMMENT 'Año calendario (2024, 2025, 2026)',
  `trimestre` TINYINT NOT NULL COMMENT 'Trimestre (1 a 4)',
  `trimestre_nombre` VARCHAR(10) NOT NULL COMMENT 'Etiqueta Q1, Q2, Q3, Q4',
  `mes` TINYINT NOT NULL COMMENT 'Mes del año (1 a 12)',
  `mes_nombre` VARCHAR(15) NOT NULL COMMENT 'Nombre del mes en español',
  `mes_anio` VARCHAR(10) NOT NULL COMMENT 'Periodo cronológico YYYY-MM',
  `semana_anio` TINYINT NOT NULL COMMENT 'Número de semana (1 a 53)',
  `dia_mes` TINYINT NOT NULL COMMENT 'Día del mes (1 a 31)',
  `dia_semana` TINYINT NOT NULL COMMENT 'Día de la semana (1=Lunes a 7=Domingo)',
  `dia_semana_nombre` VARCHAR(12) NOT NULL COMMENT 'Nombre del día (Lunes, Martes...)',
  `es_fin_semana` TINYINT NOT NULL COMMENT '1 si es fin de semana, 0 entre semana',
  INDEX `idx_tiempo_anio_mes` (`anio`, `mes`),
  INDEX `idx_tiempo_trimestre` (`anio`, `trimestre`)
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Tiempo y Calendario';

-- ------------------------------------------------------------------------------
-- 2. Dimensión Conforme: Producto
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_producto`;
CREATE TABLE `dim_producto` (
  `producto_key` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Clave sustituta artificial',
  `producto_id` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Clave natural de negocio transaccional (CE-P00001)',
  `sku` VARCHAR(30) NOT NULL COMMENT 'Código SKU de almacén',
  `producto` VARCHAR(150) NOT NULL COMMENT 'Denominación comercial del artículo',
  `categoria` VARCHAR(50) NOT NULL COMMENT 'Categoría de mobiliario o decoración',
  `marca` VARCHAR(50) NOT NULL COMMENT 'Marca comercial',
  `costo` DECIMAL(12,2) NOT NULL COMMENT 'Costo de compra al proveedor',
  `precio_lista` DECIMAL(12,2) NOT NULL COMMENT 'Precio base al público sin descuento',
  `margen_teorico_pct` DECIMAL(6,2) NOT NULL COMMENT 'Margen teórico de catálogo ((precio-costo)/precio)*100',
  `activo` CHAR(2) NOT NULL COMMENT 'Disponibilidad operativa (SI / NO)',
  `requiere_instalacion` CHAR(2) NOT NULL COMMENT 'Requiere servicio técnico de armado (SI / NO)',
  INDEX `idx_prod_categoria` (`categoria`),
  INDEX `idx_prod_marca` (`marca`),
  INDEX `idx_prod_activo` (`activo`)
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Productos de Mobiliario y Decoración';

-- ------------------------------------------------------------------------------
-- 3. Dimensión Conforme: Cliente
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_cliente`;
CREATE TABLE `dim_cliente` (
  `cliente_key` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Clave sustituta artificial',
  `cliente_id` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Clave natural transaccional en CRM (CE-C000001)',
  `nombre` VARCHAR(150) NOT NULL COMMENT 'Nombre completo del cliente',
  `sexo` VARCHAR(25) NOT NULL COMMENT 'Género normalizado (Masculino, Femenino, No Especificado)',
  `fecha_alta` DATE NOT NULL COMMENT 'Fecha de registro en el CRM',
  `ciudad` VARCHAR(80) NOT NULL COMMENT 'Ciudad de residencia (imputada si ausente)',
  `segmento` VARCHAR(30) NOT NULL COMMENT 'Segmento de valor (Premium, Frecuente, Nuevo, Inactivo)',
  `email` VARCHAR(150) NOT NULL COMMENT 'Correo electrónico verificado/imputado',
  INDEX `idx_cli_segmento` (`segmento`),
  INDEX `idx_cli_ciudad` (`ciudad`),
  INDEX `idx_cli_sexo` (`sexo`)
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Clientes CRM';

-- ------------------------------------------------------------------------------
-- 4. Dimensión Conforme: Sucursal
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_sucursal`;
CREATE TABLE `dim_sucursal` (
  `sucursal_key` INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Clave sustituta artificial',
  `sucursal_id` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Clave natural transaccional (CE-S001..S016)',
  `sucursal` VARCHAR(100) NOT NULL COMMENT 'Nombre comercial de la sucursal física',
  `ciudad` VARCHAR(80) NOT NULL COMMENT 'Ciudad de localización',
  `estado` VARCHAR(80) NOT NULL COMMENT 'Estado de la República',
  `m2` INT NOT NULL COMMENT 'Superficie comercial en metros cuadrados',
  `categoria_tamano` VARCHAR(35) NOT NULL COMMENT 'Segmentación: Pequeña, Mediana, Grande',
  `fecha_apertura` DATE NOT NULL COMMENT 'Fecha de inauguración comercial',
  INDEX `idx_suc_estado` (`estado`),
  INDEX `idx_suc_ciudad` (`ciudad`),
  INDEX `idx_suc_tamano` (`categoria_tamano`)
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Sucursales de Operación';

-- ------------------------------------------------------------------------------
-- 5. Dimensión Conforme: Canal Comercial
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_canal`;
CREATE TABLE `dim_canal` (
  `canal_id` TINYINT PRIMARY KEY COMMENT 'Identificador de canal (1=Tienda, 2=Web, 3=App)',
  `canal_nombre` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Nombre comercial del canal de venta'
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Canales de Venta';

-- ------------------------------------------------------------------------------
-- 6. Dimensión Conforme: Método de Pago
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `dim_metodo_pago`;
CREATE TABLE `dim_metodo_pago` (
  `metodo_pago_id` TINYINT PRIMARY KEY COMMENT 'Identificador (1=Tarjeta, 2=Efectivo, 3=Transferencia, 4=Wallet)',
  `metodo_nombre` VARCHAR(30) NOT NULL UNIQUE COMMENT 'Denominación del método de pago'
) ENGINE=InnoDB COMMENT='Dimensión Conforme de Medios de Pago';

-- ------------------------------------------------------------------------------
-- 7. Hecho Central: Detalle de Ventas
-- Granularidad atómica: 1 fila por renglón de ticket vendido (331,758 filas)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `fact_ventas_detalle`;
CREATE TABLE `fact_ventas_detalle` (
  `venta_id` VARCHAR(30) NOT NULL COMMENT 'Folio único de ticket transaccional',
  `linea` INT NOT NULL COMMENT 'Renglón dentro del ticket',
  `tiempo_id` INT NOT NULL COMMENT 'Clave de fecha en dim_tiempo',
  `producto_key` INT NOT NULL COMMENT 'Clave sustituta en dim_producto',
  `cliente_key` INT NOT NULL COMMENT 'Clave sustituta en dim_cliente',
  `sucursal_key` INT NOT NULL COMMENT 'Clave sustituta en dim_sucursal',
  `canal_id` TINYINT NOT NULL COMMENT 'Clave de canal en dim_canal',
  `metodo_pago_id` TINYINT NOT NULL COMMENT 'Clave de método de pago en dim_metodo_pago',
  `hora_venta` TIME NOT NULL COMMENT 'Hora de la transacción',
  `cantidad` INT NOT NULL COMMENT 'Unidades físicas vendidas',
  `precio_unitario` DECIMAL(12,2) NOT NULL COMMENT 'Precio unitario cobrado al cliente',
  `descuento_pct` DECIMAL(5,2) NOT NULL COMMENT 'Porcentaje de descuento comercial aplicado',
  `monto_bruto` DECIMAL(14,2) NOT NULL COMMENT 'Subtotal antes de descuento: cantidad * precio_unitario',
  `monto_descuento` DECIMAL(14,2) NOT NULL COMMENT 'Monto en dinero descontado: monto_bruto * (descuento_pct/100)',
  `monto_neto` DECIMAL(14,2) NOT NULL COMMENT 'Ingreso efectivo percibido: monto_bruto - monto_descuento',
  `costo_unitario` DECIMAL(12,2) NOT NULL COMMENT 'Costo de adquisición del producto',
  `costo_total` DECIMAL(14,2) NOT NULL COMMENT 'Costo total de la mercancía vendida (COGS): cantidad * costo_unitario',
  `utilidad_bruta` DECIMAL(14,2) NOT NULL COMMENT 'Beneficio comercial bruto: monto_neto - costo_total',
  `margen_pct` DECIMAL(6,2) NOT NULL COMMENT 'Margen bruto porcentual real: (utilidad_bruta / monto_neto) * 100',
  `es_devuelto` TINYINT NOT NULL DEFAULT 0 COMMENT '1 si el producto fue devuelto, 0 en caso contrario',
  PRIMARY KEY (`venta_id`, `linea`),
  CONSTRAINT `fk_fvd_tiempo` FOREIGN KEY (`tiempo_id`) REFERENCES `dim_tiempo` (`tiempo_id`),
  CONSTRAINT `fk_fvd_producto` FOREIGN KEY (`producto_key`) REFERENCES `dim_producto` (`producto_key`),
  CONSTRAINT `fk_fvd_cliente` FOREIGN KEY (`cliente_key`) REFERENCES `dim_cliente` (`cliente_key`),
  CONSTRAINT `fk_fvd_sucursal` FOREIGN KEY (`sucursal_key`) REFERENCES `dim_sucursal` (`sucursal_key`),
  CONSTRAINT `fk_fvd_canal` FOREIGN KEY (`canal_id`) REFERENCES `dim_canal` (`canal_id`),
  CONSTRAINT `fk_fvd_metodo` FOREIGN KEY (`metodo_pago_id`) REFERENCES `dim_metodo_pago` (`metodo_pago_id`),
  INDEX `idx_fvd_tiempo` (`tiempo_id`),
  INDEX `idx_fvd_producto` (`producto_key`),
  INDEX `idx_fvd_cliente` (`cliente_key`),
  INDEX `idx_fvd_sucursal` (`sucursal_key`),
  INDEX `idx_fvd_canal` (`canal_id`),
  INDEX `idx_fvd_devuelto` (`es_devuelto`)
) ENGINE=InnoDB COMMENT='Tabla de Hechos Central: Ventas Detalle Transaccional';

-- ------------------------------------------------------------------------------
-- 8. Hecho Satélite: Devoluciones
-- Granularidad: 1 fila por evento de reembolso (9,952 filas)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `fact_devoluciones`;
CREATE TABLE `fact_devoluciones` (
  `devolucion_id` VARCHAR(30) PRIMARY KEY COMMENT 'Folio único de devolución transaccional',
  `venta_id` VARCHAR(30) NOT NULL COMMENT 'Venta de origen asociada',
  `tiempo_id` INT NOT NULL COMMENT 'Fecha de la venta original',
  `producto_key` INT NOT NULL COMMENT 'Producto devuelto',
  `sucursal_key` INT NOT NULL COMMENT 'Sucursal donde se efectuó la venta',
  `cliente_key` INT NOT NULL COMMENT 'Cliente que solicitó el reembolso',
  `cantidad_devuelta` INT NOT NULL COMMENT 'Unidades físicas devueltas',
  `importe_devuelto` DECIMAL(14,2) NOT NULL COMMENT 'Monto total reembolsado',
  `motivo` VARCHAR(100) NOT NULL COMMENT 'Causa de devolución: Defecto, Daño, etc.',
  CONSTRAINT `fk_fdev_tiempo` FOREIGN KEY (`tiempo_id`) REFERENCES `dim_tiempo` (`tiempo_id`),
  CONSTRAINT `fk_fdev_producto` FOREIGN KEY (`producto_key`) REFERENCES `dim_producto` (`producto_key`),
  CONSTRAINT `fk_fdev_sucursal` FOREIGN KEY (`sucursal_key`) REFERENCES `dim_sucursal` (`sucursal_key`),
  CONSTRAINT `fk_fdev_cliente` FOREIGN KEY (`cliente_key`) REFERENCES `dim_cliente` (`cliente_key`),
  INDEX `idx_fdev_motivo` (`motivo`),
  INDEX `idx_fdev_producto` (`producto_key`),
  INDEX `idx_fdev_tiempo` (`tiempo_id`)
) ENGINE=InnoDB COMMENT='Tabla de Hechos Satélite: Devoluciones y Costo de No Calidad';

-- ------------------------------------------------------------------------------
-- 9. Hecho Satélite: Instalaciones y Servicios Técnicos
-- Granularidad: 1 fila por servicio de armado/instalación programado (6,500 filas)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `fact_instalaciones`;
CREATE TABLE `fact_instalaciones` (
  `instalacion_id` VARCHAR(30) PRIMARY KEY COMMENT 'Folio único del servicio técnico',
  `venta_id` VARCHAR(30) NOT NULL COMMENT 'Venta asociada al servicio',
  `tiempo_id` INT NOT NULL COMMENT 'Fecha de la venta',
  `cliente_key` INT NOT NULL COMMENT 'Cliente atendido',
  `sucursal_key` INT NOT NULL COMMENT 'Sucursal despachadora',
  `dias_programados` INT NOT NULL COMMENT 'Plazo pactado de entrega y armado',
  `dias_reales` INT NOT NULL COMMENT 'Días efectivos en completar el servicio',
  `dias_desviacion` INT NOT NULL COMMENT 'Días reales - Días programados (retraso > 0)',
  `cumplio_sla` TINYINT NOT NULL COMMENT '1 si dias_reales <= dias_programados, 0 si hay retraso',
  `satisfaccion` INT NOT NULL COMMENT 'Calificación del cliente (escala 1 a 5)',
  CONSTRAINT `fk_finst_tiempo` FOREIGN KEY (`tiempo_id`) REFERENCES `dim_tiempo` (`tiempo_id`),
  CONSTRAINT `fk_finst_cliente` FOREIGN KEY (`cliente_key`) REFERENCES `dim_cliente` (`cliente_key`),
  CONSTRAINT `fk_finst_sucursal` FOREIGN KEY (`sucursal_key`) REFERENCES `dim_sucursal` (`sucursal_key`),
  INDEX `idx_finst_cumplio_sla` (`cumplio_sla`),
  INDEX `idx_finst_satisfaccion` (`satisfaccion`),
  INDEX `idx_finst_sucursal` (`sucursal_key`)
) ENGINE=InnoDB COMMENT='Tabla de Hechos Satélite: Desempeño Logístico de Instalaciones';

-- ------------------------------------------------------------------------------
-- 10. Hecho Satélite: Foto de Inventarios (Snapshot de Existencias)
-- Granularidad: 1 fila por combinación sucursal y producto (21,440 filas)
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `fact_inventario_snapshot`;
CREATE TABLE `fact_inventario_snapshot` (
  `sucursal_key` INT NOT NULL COMMENT 'Clave de sucursal',
  `producto_key` INT NOT NULL COMMENT 'Clave de producto',
  `stock_actual` INT NOT NULL COMMENT 'Unidades en piso y almacén',
  `punto_reorden` INT NOT NULL COMMENT 'Umbral mínimo de seguridad',
  `deficit_unidades` INT NOT NULL COMMENT 'Unidades faltantes frente al punto de reorden',
  `valor_inventario_costo` DECIMAL(14,2) NOT NULL COMMENT 'Capital invertido en inventario (stock * costo)',
  `estatus_stock` VARCHAR(30) NOT NULL COMMENT 'Optimo, Alerta Reorden, Rotura Stock',
  PRIMARY KEY (`sucursal_key`, `producto_key`),
  CONSTRAINT `fk_finv_sucursal` FOREIGN KEY (`sucursal_key`) REFERENCES `dim_sucursal` (`sucursal_key`),
  CONSTRAINT `fk_finv_producto` FOREIGN KEY (`producto_key`) REFERENCES `dim_producto` (`producto_key`),
  INDEX `idx_finv_estatus` (`estatus_stock`)
) ENGINE=InnoDB COMMENT='Tabla de Hechos: Snapshot de Existencias e Inventario';

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'Tablas del Data Mart Dimensional creadas exitosamente con claves e índices B-Tree.' AS resultado;
