-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 04_validacion_y_rechazos / 03_validacion_y_rechazos.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Paso 4 - Validación de reglas de negocio, aislamiento de rechazos y pedidos limpios
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- Limpieza de tablas de rechazo y staging limpio
DROP TABLE IF EXISTS pedidos_rechazados;
DROP TABLE IF EXISTS stg_pedidos_limpios;

-- ------------------------------------------------------------------------------
-- 1. TABLA: pedidos_rechazados (Quarantine / Error Mart)
-- DESCRIPCIÓN: Almacena cada transacción rechazada junto con su motivo específico,
--              valores originales y detalles técnicos del error para auditoría.
-- ------------------------------------------------------------------------------
CREATE TABLE pedidos_rechazados (
    id_rechazo          INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador secuencial del rechazo',
    fila_id             INT NOT NULL COMMENT 'Fila de origen en raw_pedidos',
    id_pedido           VARCHAR(50) NOT NULL COMMENT 'Identificador de la orden',
    id_cliente          VARCHAR(50) NOT NULL COMMENT 'Identificador del cliente',
    fecha_pedido_raw    VARCHAR(50) NULL COMMENT 'Fecha original cruda',
    importe_raw         VARCHAR(50) NULL COMMENT 'Importe original crudo',
    estado_pedido       VARCHAR(50) NOT NULL COMMENT 'Estatus de la orden',
    estado_envio_raw    VARCHAR(100) NULL COMMENT 'Destino crudo reportado',
    motivo_rechazo      VARCHAR(50) NOT NULL COMMENT 'Código de la regla de calidad violada',
    detalle_error       TEXT NOT NULL COMMENT 'Explicación del fallo de calidad',
    fecha_evaluacion    TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Momento en que fue rechazado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. TABLA: stg_pedidos_limpios
-- DESCRIPCIÓN: Zona de paso que contiene únicamente transacciones validadas,
--              deduplicadas, tipadas y listas para su carga al Data Mart.
-- ------------------------------------------------------------------------------
CREATE TABLE stg_pedidos_limpios (
    id_pedido           VARCHAR(50) NOT NULL PRIMARY KEY COMMENT 'Clave primaria natural única de la orden',
    id_cliente          VARCHAR(50) NOT NULL COMMENT 'Clave natural del cliente verificado',
    fecha_pedido        DATE NOT NULL COMMENT 'Fecha de compra validada',
    importe             DECIMAL(12,2) NOT NULL COMMENT 'Monto financiero positivo validado',
    estado_pedido       VARCHAR(50) NOT NULL COMMENT 'Estatus de la orden',
    estado_canonico     VARCHAR(10) NOT NULL COMMENT 'Clave estatal de destino homologada',
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Auditoría de inserción'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 3. AISLAMIENTO DE RECHAZOS EN pedidos_rechazados
-- Se evalúan jerárquicamente las 5 causales de descalificación de calidad:
-- 1. Duplicidad por id_pedido (instancias secundarias).
-- 2. Cliente inexistente en la dimensión clientes normalizada.
-- 3. Fecha vacía o no convertible a DATE.
-- 4. Importe menor o igual a cero, o nulo.
-- 5. Estado de destino no reconocido en catalogo_estados.
-- ------------------------------------------------------------------------------
INSERT INTO pedidos_rechazados (
    fila_id,
    id_pedido,
    id_cliente,
    fecha_pedido_raw,
    importe_raw,
    estado_pedido,
    estado_envio_raw,
    motivo_rechazo,
    detalle_error
)
WITH evaluacion_pedidos AS (
    SELECT 
        p.*,
        ROW_NUMBER() OVER (
            PARTITION BY p.id_pedido 
            ORDER BY p.fila_id ASC
        ) AS orden_aparicion,
        c.id_cliente AS cliente_existe
    FROM stg_pedidos p
    LEFT JOIN stg_clientes c ON p.id_cliente = c.id_cliente
)
-- Caso 1: Duplicados por id_pedido
SELECT 
    fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw,
    'ID_PEDIDO_DUPLICADO' AS motivo_rechazo,
    CONCAT('Transacción duplicada detectada. Ya existe un registro previo para el id_pedido: ', id_pedido) AS detalle_error
FROM evaluacion_pedidos
WHERE orden_aparicion > 1

UNION ALL

-- Caso 2: Cliente inexistente (solo evaluado en la primera aparición)
SELECT 
    fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw,
    'CLIENTE_INEXISTENTE' AS motivo_rechazo,
    CONCAT('El cliente ', id_cliente, ' no existe en la base de clientes registrada.') AS detalle_error
FROM evaluacion_pedidos
WHERE orden_aparicion = 1 
  AND cliente_existe IS NULL

UNION ALL

-- Caso 3: Fecha inválida o vacía
SELECT 
    fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw,
    'FECHA_INVALIDA' AS motivo_rechazo,
    CONCAT('Fecha nula, vacía o con formato no reconocido: ', COALESCE(NULLIF(fecha_pedido_raw, ''), '[VACIO]')) AS detalle_error
FROM evaluacion_pedidos
WHERE orden_aparicion = 1 
  AND cliente_existe IS NOT NULL
  AND fecha_pedido_norm IS NULL

UNION ALL

-- Caso 4: Importe no positivo (<= 0 o no numérico)
SELECT 
    fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw,
    'IMPORTE_NO_POSITIVO' AS motivo_rechazo,
    CONCAT('Importe inválido en transacción. Monto reportado: ', COALESCE(importe_raw, 'NULL')) AS detalle_error
FROM evaluacion_pedidos
WHERE orden_aparicion = 1 
  AND cliente_existe IS NOT NULL
  AND fecha_pedido_norm IS NOT NULL
  AND (importe_norm IS NULL OR importe_norm <= 0)

UNION ALL

-- Caso 5: Estado de envío no reconocido en el catálogo oficial
SELECT 
    fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw,
    'ESTADO_NO_RECONOCIDO' AS motivo_rechazo,
    CONCAT('El estado de destino reportado (', estado_envio_raw, ') no tiene equivalencia en catalogo_estados.') AS detalle_error
FROM evaluacion_pedidos
WHERE orden_aparicion = 1 
  AND cliente_existe IS NOT NULL
  AND fecha_pedido_norm IS NOT NULL
  AND (importe_norm IS NOT NULL AND importe_norm > 0)
  AND estado_envio_canonico IS NULL;

-- ------------------------------------------------------------------------------
-- 4. INSERCIÓN DE PEDIDOS ACEPTADOS EN stg_pedidos_limpios
-- Solo ingresan aquellas transacciones que no presentan ninguna causal de rechazo.
-- ------------------------------------------------------------------------------
INSERT INTO stg_pedidos_limpios (
    id_pedido, 
    id_cliente, 
    fecha_pedido, 
    importe, 
    estado_pedido, 
    estado_canonico
)
SELECT 
    p.id_pedido,
    p.id_cliente,
    p.fecha_pedido_norm,
    p.importe_norm,
    p.estado_pedido,
    p.estado_envio_canonico
FROM stg_pedidos p
WHERE p.fila_id NOT IN (SELECT fila_id FROM pedidos_rechazados);

-- ------------------------------------------------------------------------------
-- 5. Consultas de control y resumen de rechazos
-- ------------------------------------------------------------------------------
-- Resumen agrupado por motivo de rechazo:
SELECT 
    motivo_rechazo,
    COUNT(*) AS total_rechazados,
    GROUP_CONCAT(id_pedido SEPARATOR ', ') AS pedidos_afectados
FROM pedidos_rechazados
GROUP BY motivo_rechazo
ORDER BY total_rechazados DESC;

-- Detalle individual de todos los registros en cuarentena:
SELECT 
    id_rechazo,
    fila_id,
    id_pedido,
    id_cliente,
    fecha_pedido_raw,
    importe_raw,
    motivo_rechazo,
    detalle_error
FROM pedidos_rechazados
ORDER BY id_rechazo ASC;

-- Total de pedidos limpios aptos para el Data Mart:
SELECT COUNT(*) AS total_pedidos_limpios FROM stg_pedidos_limpios;
