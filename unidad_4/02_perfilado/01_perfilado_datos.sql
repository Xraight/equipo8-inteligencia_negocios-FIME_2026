-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 02_perfilado / 01_perfilado_datos.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Paso 1 - Perfilado de datos y generación de tabla de observaciones
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- 1. Creación de la tabla de observaciones de perfilado
DROP TABLE IF EXISTS observaciones_perfilado;

CREATE TABLE observaciones_perfilado (
    id_observacion     INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la observación',
    tabla_origen       VARCHAR(50) NOT NULL COMMENT 'Tabla cruda analizada',
    regla_o_metrica    VARCHAR(100) NOT NULL COMMENT 'Tipo de comprobación o anomalía evaluada',
    registros_afectados INT NOT NULL COMMENT 'Cantidad de registros que presentan el hallazgo',
    severidad          ENUM('INFO', 'BAJA', 'MEDIA', 'ALTA') NOT NULL COMMENT 'Nivel de severidad técnica',
    detalle_hallazgo   TEXT NOT NULL COMMENT 'Descripción técnica y ejemplos de los valores anómalos',
    fecha_analisis     TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Momento exacto del perfilado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. Conteo general de registros por tabla
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_clientes', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', 
       CONCAT('Total de registros crudos ingresados desde clientes.csv: ', COUNT(*))
FROM raw_clientes;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_pedidos', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', 
       CONCAT('Total de transacciones crudas ingresadas desde pedidos.sql: ', COUNT(*))
FROM raw_pedidos;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'catalogo_estados', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', 
       CONCAT('Total de entidades federativas canónicas registradas: ', COUNT(*))
FROM catalogo_estados;

-- ------------------------------------------------------------------------------
-- 3. Búsqueda de id_cliente duplicados en raw_clientes
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_clientes', 
    'DUPLICADOS_ID_CLIENTE', 
    COUNT(*), 
    'ALTA',
    CONCAT('Se detectaron clientes con clave natural duplicada. Claves afectadas: ', 
           GROUP_CONCAT(DISTINCT id_cliente SEPARATOR ', '))
FROM (
    SELECT id_cliente
    FROM raw_clientes
    WHERE id_cliente IS NOT NULL
    GROUP BY id_cliente
    HAVING COUNT(*) > 1
) dup;

-- ------------------------------------------------------------------------------
-- 4. Búsqueda de id_pedido duplicados en raw_pedidos
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_pedidos', 
    'DUPLICADOS_ID_PEDIDO', 
    SUM(cnt - 1), 
    'ALTA',
    CONCAT('Transacciones con id_pedido duplicado que violan la unicidad transaccional: ', 
           GROUP_CONCAT(CONCAT(id_pedido, ' (', cnt, ' repeticiones)') SEPARATOR '; '))
FROM (
    SELECT id_pedido, COUNT(*) AS cnt
    FROM raw_pedidos
    WHERE id_pedido IS NOT NULL
    GROUP BY id_pedido
    HAVING COUNT(*) > 1
) dup;

-- ------------------------------------------------------------------------------
-- 5. Búsqueda de estados no estandarizados o vacíos
-- ------------------------------------------------------------------------------
-- En clientes:
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_clientes', 
    'ESTADOS_NO_ESTANDARIZADOS_O_VACIOS', 
    COUNT(*), 
    'MEDIA',
    CONCAT('Clientes cuyos estados no coinciden con la clave canónica exacta (incluye alias o vacíos): ',
           GROUP_CONCAT(DISTINCT COALESCE(NULLIF(estado, ''), '[VACIO]') SEPARATOR ', '))
FROM raw_clientes c
LEFT JOIN catalogo_estados ce ON c.estado = ce.estado_canonico
WHERE ce.estado_canonico IS NULL;

-- En pedidos (estado de envío):
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_pedidos', 
    'ESTADOS_ENVIO_NO_CANONICOS', 
    COUNT(*), 
    'MEDIA',
    CONCAT('Pedidos cuyo estado de envío no coincide con la clave canónica exacta: ',
           GROUP_CONCAT(DISTINCT COALESCE(NULLIF(estado_envio, ''), '[VACIO]') SEPARATOR ', '))
FROM raw_pedidos p
LEFT JOIN catalogo_estados ce ON p.estado_envio = ce.estado_canonico
WHERE ce.estado_canonico IS NULL;

-- ------------------------------------------------------------------------------
-- 6. Búsqueda de fechas vacías o heterogéneas (ISO vs DD/MM/AAAA vs inválidas)
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_clientes', 
    'FECHAS_CLIENTE_NO_ISO_O_VACIAS', 
    COUNT(*), 
    'MEDIA',
    CONCAT('Registros de clientes con fecha vacía o en formato no ISO (DD/MM/AAAA): ',
           GROUP_CONCAT(CONCAT(id_cliente, ' (', COALESCE(NULLIF(fecha_registro, ''), '[VACIO]'), ')') SEPARATOR ', '))
FROM raw_clientes
WHERE fecha_registro IS NULL 
   OR fecha_registro = '' 
   OR fecha_registro NOT REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$';

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_pedidos', 
    'FECHAS_PEDIDO_INVALIDAS_O_NO_ISO', 
    COUNT(*), 
    'ALTA',
    CONCAT('Pedidos con fecha vacía, corrupta o formato alternativo (DD/MM/AAAA): ',
           GROUP_CONCAT(CONCAT(id_pedido, ' (', COALESCE(NULLIF(fecha_pedido, ''), '[VACIO]'), ')') SEPARATOR ', '))
FROM raw_pedidos
WHERE fecha_pedido IS NULL 
   OR fecha_pedido = '' 
   OR fecha_pedido NOT REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$';

-- ------------------------------------------------------------------------------
-- 7. Búsqueda de montos no positivos (menores o iguales a cero, o nulos)
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_pedidos', 
    'MONTOS_NO_POSITIVOS', 
    COUNT(*), 
    'ALTA',
    CONCAT('Pedidos con importe <= 0 o no numérico: ',
           GROUP_CONCAT(CONCAT(id_pedido, ' (monto: ', COALESCE(importe, 'NULL'), ')') SEPARATOR ', '))
FROM raw_pedidos
WHERE CAST(importe AS DECIMAL(12,2)) <= 0 
   OR importe IS NULL;

-- ------------------------------------------------------------------------------
-- 8. Búsqueda de clientes huérfanos (pedidos apuntando a clientes inexistentes)
-- ------------------------------------------------------------------------------
INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 
    'raw_pedidos', 
    'CLIENTES_HUERFANOS', 
    COUNT(*), 
    'ALTA',
    CONCAT('Pedidos referenciando id_cliente inexistente en raw_clientes: ',
           GROUP_CONCAT(CONCAT(p.id_pedido, ' -> ', p.id_cliente) SEPARATOR ', '))
FROM raw_pedidos p
LEFT JOIN raw_clientes c ON p.id_cliente = c.id_cliente
WHERE c.id_cliente IS NULL;

-- ------------------------------------------------------------------------------
-- 9. Consulta de salida de resultados de perfilado
-- ------------------------------------------------------------------------------
SELECT 
    id_observacion,
    tabla_origen,
    regla_o_metrica,
    registros_afectados,
    severidad,
    detalle_hallazgo
FROM observaciones_perfilado
ORDER BY id_observacion ASC;
