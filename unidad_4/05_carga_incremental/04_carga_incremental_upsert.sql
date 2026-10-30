-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 05_carga_incremental / 04_carga_incremental_upsert.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Paso 5 - Carga incremental (UPSERT) al Data Mart y prueba de idempotencia
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- ------------------------------------------------------------------------------
-- 1. DDL DEL DATA MART (Esquema Estrella)
-- ------------------------------------------------------------------------------

-- Tabla dimensional de estados
CREATE TABLE IF NOT EXISTS dim_estado (
    estado_canonico VARCHAR(10) NOT NULL PRIMARY KEY COMMENT 'Clave oficial del estado (ej. NL, CDMX, NE)',
    nombre_oficial  VARCHAR(100) NOT NULL COMMENT 'Nombre completo oficial'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla dimensional de clientes
CREATE TABLE IF NOT EXISTS dim_cliente (
    id_cliente          VARCHAR(50) NOT NULL PRIMARY KEY COMMENT 'Clave natural única del cliente',
    nombre              VARCHAR(150) NOT NULL COMMENT 'Nombre del cliente',
    email               VARCHAR(150) NOT NULL COMMENT 'Correo electrónico verificado',
    estado_canonico     VARCHAR(10) NOT NULL COMMENT 'Clave canónica del estado de residencia',
    fecha_registro      DATE NULL COMMENT 'Fecha de registro estandarizada',
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_cliente_estado FOREIGN KEY (estado_canonico) REFERENCES dim_estado (estado_canonico)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de hechos de órdenes de compra
CREATE TABLE IF NOT EXISTS fact_ordenes (
    id_pedido           VARCHAR(50) NOT NULL PRIMARY KEY COMMENT 'Clave primaria natural del pedido',
    id_cliente          VARCHAR(50) NOT NULL COMMENT 'Clave foránea al cliente',
    estado_canonico     VARCHAR(10) NOT NULL COMMENT 'Clave foránea al estado de destino',
    fecha_pedido        DATE NOT NULL COMMENT 'Fecha de la transacción',
    importe             DECIMAL(12,2) NOT NULL COMMENT 'Monto financiero neto de la orden',
    estado_pedido       VARCHAR(50) NOT NULL COMMENT 'Estatus de la transacción',
    fecha_carga         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_fact_cliente FOREIGN KEY (id_cliente) REFERENCES dim_cliente (id_cliente),
    CONSTRAINT fk_fact_estado  FOREIGN KEY (estado_canonico) REFERENCES dim_estado (estado_canonico)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. CARGA INCREMENTAL (UPSERT): dim_estado
-- Inserta o actualiza entidades oficiales más la entidad comodín 'NE' (No Especificado)
-- ------------------------------------------------------------------------------
INSERT INTO dim_estado (estado_canonico, nombre_oficial)
SELECT estado_canonico, nombre_oficial FROM catalogo_estados
UNION ALL
SELECT 'NE', 'No Especificado'
ON DUPLICATE KEY UPDATE 
    nombre_oficial = VALUES(nombre_oficial);

-- ------------------------------------------------------------------------------
-- 3. CARGA INCREMENTAL (UPSERT): dim_cliente
-- Si el id_cliente ya existe, actualiza atributos sin duplicar filas.
-- ------------------------------------------------------------------------------
INSERT INTO dim_cliente (id_cliente, nombre, email, estado_canonico, fecha_registro)
SELECT 
    id_cliente,
    nombre,
    email,
    estado_canonico,
    fecha_registro
FROM stg_clientes
ON DUPLICATE KEY UPDATE 
    nombre = VALUES(nombre),
    email = VALUES(email),
    estado_canonico = VALUES(estado_canonico),
    fecha_registro = VALUES(fecha_registro);

-- ------------------------------------------------------------------------------
-- 4. CARGA INCREMENTAL (UPSERT): fact_ordenes (Paso 1 de la prueba)
-- ------------------------------------------------------------------------------
INSERT INTO fact_ordenes (id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido)
SELECT 
    id_pedido,
    id_cliente,
    estado_canonico,
    fecha_pedido,
    importe,
    estado_pedido
FROM stg_pedidos_limpios
ON DUPLICATE KEY UPDATE 
    id_cliente = VALUES(id_cliente),
    estado_canonico = VALUES(estado_canonico),
    fecha_pedido = VALUES(fecha_pedido),
    importe = VALUES(importe),
    estado_pedido = VALUES(estado_pedido);

-- Guardar conteo tras la primera corrida
SET @conteo_fact_corrida_1 := (SELECT COUNT(*) FROM fact_ordenes);
SET @monto_fact_corrida_1  := (SELECT SUM(importe) FROM fact_ordenes);

-- ------------------------------------------------------------------------------
-- 5. DEMOSTRACIÓN DE IDEMPOTENCIA (Re-ejecución sin filas nuevas en origen)
-- Se vuelve a ejecutar exactamente el mismo bloque de carga UPSERT.
-- ------------------------------------------------------------------------------
INSERT INTO fact_ordenes (id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido)
SELECT 
    id_pedido,
    id_cliente,
    estado_canonico,
    fecha_pedido,
    importe,
    estado_pedido
FROM stg_pedidos_limpios
ON DUPLICATE KEY UPDATE 
    id_cliente = VALUES(id_cliente),
    estado_canonico = VALUES(estado_canonico),
    fecha_pedido = VALUES(fecha_pedido),
    importe = VALUES(importe),
    estado_pedido = VALUES(estado_pedido);

SET @conteo_fact_corrida_2 := (SELECT COUNT(*) FROM fact_ordenes);
SET @monto_fact_corrida_2  := (SELECT SUM(importe) FROM fact_ordenes);

-- ------------------------------------------------------------------------------
-- 6. REPORTE DE VALIDACIÓN DE IDEMPOTENCIA
-- ------------------------------------------------------------------------------
SELECT 
    'Prueba de Idempotencia' AS prueba,
    @conteo_fact_corrida_1 AS filas_primera_ejecucion,
    @conteo_fact_corrida_2 AS filas_segunda_ejecucion,
    IF(@conteo_fact_corrida_1 = @conteo_fact_corrida_2, 'IDEMPOTENTE (EXITO)', 'ERROR (DUPLICACION DETECTADA)') AS resultado_volumen,
    @monto_fact_corrida_1 AS importe_primera_ejecucion,
    @monto_fact_corrida_2 AS importe_segunda_ejecucion,
    IF(@monto_fact_corrida_1 = @monto_fact_corrida_2, 'INTEGRO (SIN DESVIO)', 'ERROR (DESVIO DETECTADO)') AS resultado_financiero;
