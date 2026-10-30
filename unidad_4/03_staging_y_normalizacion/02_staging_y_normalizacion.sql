-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 03_staging_y_normalizacion / 02_staging_y_normalizacion.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Pasos 2 y 3 - Creación de zona Staging, normalización y homologación
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- Limpieza de tablas staging previas
DROP TABLE IF EXISTS stg_pedidos;
DROP TABLE IF EXISTS stg_clientes;

-- ------------------------------------------------------------------------------
-- 1. TABLA STAGING: stg_clientes
-- DESCRIPCIÓN: Datos normalizados de clientes con deduplicación por id_cliente,
--              homologación estatal canónica y tipado estricto de fechas (DATE).
-- ------------------------------------------------------------------------------
CREATE TABLE stg_clientes (
    id_cliente          VARCHAR(50) NOT NULL PRIMARY KEY COMMENT 'Clave primaria natural del cliente',
    nombre              VARCHAR(150) NOT NULL COMMENT 'Nombre completo normalizado',
    email               VARCHAR(150) NOT NULL COMMENT 'Correo electrónico verificado',
    estado_original     VARCHAR(100) NULL COMMENT 'Estado tal como ingresó en raw',
    estado_canonico     VARCHAR(10) NOT NULL COMMENT 'Clave oficial homologada o NE (No Especificado)',
    fecha_registro      DATE NULL COMMENT 'Fecha de registro estandarizada en formato DATE',
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Auditoría de carga'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. POBLACIÓN Y TRANSFORMACIÓN: stg_clientes
-- Regla de deduplicación: Se utiliza ROW_NUMBER() seleccionando la fila más reciente
--                         (mayor fila_id) para clientes con id repetido.
-- Regla de estado: Homologación contra catalogo_estados; si no hay coincidencia, se asigna 'NE'.
-- Regla de fecha: Soporte para formato ISO ('%Y-%m-%d') y latino ('%d/%m/%Y').
-- ------------------------------------------------------------------------------
INSERT INTO stg_clientes (id_cliente, nombre, email, estado_original, estado_canonico, fecha_registro)
WITH deduplicado_clientes AS (
    SELECT 
        fila_id,
        TRIM(id_cliente) AS id_cliente,
        TRIM(nombre) AS nombre,
        TRIM(email) AS email,
        TRIM(estado) AS estado_raw,
        TRIM(fecha_registro) AS fecha_raw,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(id_cliente) 
            ORDER BY fila_id DESC
        ) AS rn
    FROM raw_clientes
    WHERE id_cliente IS NOT NULL AND TRIM(id_cliente) != ''
)
SELECT 
    d.id_cliente,
    d.nombre,
    d.email,
    d.estado_raw AS estado_original,
    COALESCE(ce.estado_canonico, 'NE') AS estado_canonico,
    CASE 
        WHEN d.fecha_raw REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 
            THEN STR_TO_DATE(d.fecha_raw, '%Y-%m-%d')
        WHEN d.fecha_raw REGEXP '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$' 
            THEN STR_TO_DATE(d.fecha_raw, '%d/%m/%Y')
        ELSE NULL
    END AS fecha_registro
FROM deduplicado_clientes d
LEFT JOIN catalogo_estados ce 
    ON d.estado_raw = ce.estado_canonico 
    OR d.estado_raw = ce.nombre_oficial
    OR FIND_IN_SET(d.estado_raw, REPLACE(ce.alias, ', ', ',')) > 0
WHERE d.rn = 1;

-- ------------------------------------------------------------------------------
-- 3. TABLA STAGING: stg_pedidos
-- DESCRIPCIÓN: Zona de preparación tipada de transacciones. Conserva valores 
--              originales crudos para auditoría y almacena campos parseados.
-- ------------------------------------------------------------------------------
CREATE TABLE stg_pedidos (
    fila_id                 INT NOT NULL PRIMARY KEY COMMENT 'Referencia a la fila original en raw_pedidos',
    id_pedido               VARCHAR(50) NOT NULL COMMENT 'Identificador de la orden',
    id_cliente              VARCHAR(50) NOT NULL COMMENT 'Identificador del cliente comprador',
    fecha_pedido_raw        VARCHAR(50) NULL COMMENT 'Texto original de fecha',
    fecha_pedido_norm       DATE NULL COMMENT 'Fecha convertida a tipo nativo DATE',
    importe_raw             VARCHAR(50) NULL COMMENT 'Texto original de importe',
    importe_norm            DECIMAL(12,2) NULL COMMENT 'Importe convertido a tipo numérico con 2 decimales',
    estado_pedido           VARCHAR(50) NOT NULL COMMENT 'Estatus operativo de la orden',
    estado_envio_raw        VARCHAR(100) NULL COMMENT 'Estado de destino crudo',
    estado_envio_canonico   VARCHAR(10) NULL COMMENT 'Clave oficial del estado o NULL si no existe',
    fecha_procesamiento     TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Marca temporal de transformación'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 4. POBLACIÓN Y NORMALIZACIÓN: stg_pedidos
-- Realiza el parsing controlado de fechas y montos sin descartar aún ningún registro.
-- ------------------------------------------------------------------------------
INSERT INTO stg_pedidos (
    fila_id, 
    id_pedido, 
    id_cliente, 
    fecha_pedido_raw, 
    fecha_pedido_norm, 
    importe_raw, 
    importe_norm, 
    estado_pedido, 
    estado_envio_raw, 
    estado_envio_canonico
)
SELECT 
    p.fila_id,
    TRIM(p.id_pedido) AS id_pedido,
    TRIM(p.id_cliente) AS id_cliente,
    p.fecha_pedido AS fecha_pedido_raw,
    CASE 
        WHEN TRIM(p.fecha_pedido) REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 
            THEN STR_TO_DATE(TRIM(p.fecha_pedido), '%Y-%m-%d')
        WHEN TRIM(p.fecha_pedido) REGEXP '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$' 
            THEN STR_TO_DATE(TRIM(p.fecha_pedido), '%d/%m/%Y')
        ELSE NULL
    END AS fecha_pedido_norm,
    p.importe AS importe_raw,
    CASE 
        WHEN TRIM(p.importe) REGEXP '^-?[0-9]+(\\.[0-9]+)?$'
            THEN CAST(TRIM(p.importe) AS DECIMAL(12,2))
        ELSE NULL
    END AS importe_norm,
    TRIM(p.estado_pedido) AS estado_pedido,
    TRIM(p.estado_envio) AS estado_envio_raw,
    ce.estado_canonico AS estado_envio_canonico
FROM raw_pedidos p
LEFT JOIN catalogo_estados ce 
    ON TRIM(p.estado_envio) = ce.estado_canonico 
    OR TRIM(p.estado_envio) = ce.nombre_oficial
    OR FIND_IN_SET(TRIM(p.estado_envio), REPLACE(ce.alias, ', ', ',')) > 0;

-- ------------------------------------------------------------------------------
-- 5. Consultas de verificación de staging y normalización
-- ------------------------------------------------------------------------------
SELECT 'stg_clientes' AS tabla, COUNT(*) AS total_filas_normalizadas FROM stg_clientes;
SELECT 'stg_pedidos'  AS tabla, COUNT(*) AS total_filas_preparadas FROM stg_pedidos;

-- Muestra de homologación estatal:
SELECT id_cliente, nombre, estado_original, estado_canonico, fecha_registro 
FROM stg_clientes 
LIMIT 10;
