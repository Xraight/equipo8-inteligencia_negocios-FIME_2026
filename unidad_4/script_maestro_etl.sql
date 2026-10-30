-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: SCRIPT MAESTRO INTEGRAL DE EJECUCIÓN CONTINUA
-- ARCHIVO: unidad_4/script_maestro_etl.sql
-- MOTOR: MySQL 8.0+
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- DESCRIPCIÓN: Script unificado, determinista e idempotente que ejecuta el pipeline
--              completo desde la ingesta cruda hasta los indicadores analíticos.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- FASE 0: CREACIÓN DE BASE DE DATOS Y ENTORNO LIMPIO
-- ------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS tienda_bi
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tienda_bi;

-- Limpieza preventiva de todas las tablas en orden de dependencias
DROP TABLE IF EXISTS fact_ordenes;
DROP TABLE IF EXISTS dim_cliente;
DROP TABLE IF EXISTS dim_estado;
DROP TABLE IF EXISTS etl_auditoria;
DROP TABLE IF EXISTS pedidos_rechazados;
DROP TABLE IF EXISTS stg_pedidos_limpios;
DROP TABLE IF EXISTS stg_pedidos;
DROP TABLE IF EXISTS stg_clientes;
DROP TABLE IF EXISTS observaciones_perfilado;
DROP TABLE IF EXISTS raw_pedidos;
DROP TABLE IF EXISTS raw_clientes;
DROP TABLE IF EXISTS catalogo_estados;

-- ------------------------------------------------------------------------------
-- FASE 1: CREACIÓN DE TABLAS CRUDAS Y CATÁLOGO
-- ------------------------------------------------------------------------------
CREATE TABLE catalogo_estados (
    estado_canonico VARCHAR(10) NOT NULL PRIMARY KEY,
    nombre_oficial  VARCHAR(100) NOT NULL,
    alias           TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE raw_clientes (
    fila_id         INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente      VARCHAR(50) NULL,
    nombre          VARCHAR(150) NULL,
    email           VARCHAR(150) NULL,
    estado          VARCHAR(100) NULL,
    fecha_registro  VARCHAR(50) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE raw_pedidos (
    fila_id         INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido       VARCHAR(50) NULL,
    id_cliente      VARCHAR(50) NULL,
    fecha_pedido    VARCHAR(50) NULL,
    importe         VARCHAR(50) NULL,
    estado_pedido   VARCHAR(50) NULL,
    estado_envio    VARCHAR(100) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- FASE 2: INGESTA DE DATOS DE ORIGEN
-- ------------------------------------------------------------------------------
-- 1. Catálogo oficial de estados
INSERT INTO catalogo_estados (estado_canonico, nombre_oficial, alias) VALUES
('NL', 'Nuevo León', 'NL,N.L.,Nuevo Leon,NUEVO LEON,NL.,Nuevo León'),
('CDMX', 'Ciudad de México', 'CDMX,C.D.M.X.,Ciudad de Mexico,DF,D.F.,Distrito Federal,D.F,CDMX.'),
('JAL', 'Jalisco', 'JAL,Jal.,Jalisco,JALISCO,Jal'),
('COAH', 'Coahuila', 'COAH,Coah.,Coahuila de Zaragoza,Coahuila,COAHUILA'),
('TAM', 'Tamaulipas', 'TAM,Tamps.,Tamaulipas,TAMPS,TAM'),
('PUE', 'Puebla', 'PUE,Pue.,Puebla,PUEBLA'),
('QRO', 'Querétaro', 'QRO,Qro.,Queretaro,Querétaro,QUERETARO'),
('YUC', 'Yucatán', 'YUC,Yuc.,Yucatan,Yucatán,YUCATAN'),
('VER', 'Veracruz', 'VER,Ver.,Veracruz,Veracruz de Ignacio de la Llave'),
('GTO', 'Guanajuato', 'GTO,Gto.,Guanajuato,GUANAJUATO');

-- 2. Clientes crudos (clientes.csv)
INSERT INTO raw_clientes (id_cliente, nombre, email, estado, fecha_registro) VALUES
('CLI-001', 'Carlos Mendoza', 'carlos.mendoza@email.com', 'Nuevo Leon', '2026-01-15'),
('CLI-002', 'Ana Sofia Garza', 'ana.garza@email.com', 'N.L.', '14/02/2026'),
('CLI-003', 'Roberto Martinez', 'roberto.mtz@email.com', 'CDMX', '2026-01-20'),
('CLI-004', 'Mariana Sanchez', 'mariana.snz@email.com', 'D.F.', '05/02/2026'),
('CLI-005', 'Eduardo Trevino', 'eduardo.trv@email.com', 'Jalisco', '2026-01-10'),
('CLI-005', 'Eduardo Trevino', 'eduardo.trv@email.com', 'JAL', '12/01/2026'),
('CLI-006', 'Lucia Hernandez', 'lucia.hdz@email.com', 'Jal.', '2026-02-01'),
('CLI-007', 'Fernando Castillo', 'fernando.c@email.com', 'Coahuila', '2026-01-25'),
('CLI-008', 'Valeria Ramos', 'valeria.ramos@email.com', 'COAH', '18/02/2026'),
('CLI-009', 'Jorge Morales', 'jorge.morales@email.com', 'TAMPS', '2026-01-30'),
('CLI-010', 'Patricia Flores', 'patricia.fl@email.com', 'Puebla', '2026-02-10'),
('CLI-011', 'Diego Villarreal', 'diego.v@email.com', 'PUE', '22/02/2026'),
('CLI-012', 'Daniela Ortiz', 'daniela.ortiz@email.com', 'Yucatan', '2026-02-15'),
('CLI-013', 'Alejandro Gomez', 'alejandro.g@email.com', 'YUC', '2026-02-18'),
('CLI-014', 'Gabriela Rios', 'gabriela.r@email.com', 'Queretaro', '2026-02-20'),
('CLI-015', 'Mauricio Benitez', 'mauricio.b@email.com', 'QRO', '25/02/2026'),
('CLI-016', 'Laura Cavazos', 'laura.c@email.com', 'Veracruz', '2026-02-28'),
('CLI-017', 'Esteban Luna', 'esteban.luna@email.com', 'GTO', '2026-03-01'),
('CLI-018', 'Karla Navarro', 'karla.navarro@email.com', '', '2026-03-02'),
('CLI-019', 'Hector Salinas', 'hector.salinas@email.com', 'DESCONOCIDO', '2026-03-05'),
('CLI-020', 'Beatriz Delgado', 'beatriz.delgado@email.com', 'NL', '');

-- 3. Pedidos crudos (pedidos.sql)
INSERT INTO raw_pedidos (id_pedido, id_cliente, fecha_pedido, importe, estado_pedido, estado_envio) VALUES
('PED-1001', 'CLI-001', '2026-03-01', '1250.00', 'Entregado', 'NL'),
('PED-1002', 'CLI-002', '02/03/2026', '840.50',  'Entregado', 'Nuevo Leon'),
('PED-1003', 'CLI-003', '2026-03-03', '2100.00', 'Entregado', 'CDMX'),
('PED-1004', 'CLI-004', '04/03/2026', '1450.00', 'Entregado', 'D.F.'),
('PED-1005', 'CLI-005', '2026-03-05', '3200.00', 'Entregado', 'JAL'),
('PED-1006', 'CLI-006', '2026-03-06', '750.00',  'Entregado', 'Jalisco'),
('PED-1007', 'CLI-007', '2026-03-07', '1890.00', 'Entregado', 'Coahuila'),
('PED-1008', 'CLI-008', '08/03/2026', '920.00',  'Entregado', 'COAH'),
('PED-1009', 'CLI-009', '2026-03-09', '1100.00', 'Entregado', 'TAMPS'),
('PED-1010', 'CLI-010', '2026-03-10', '2650.00', 'Entregado', 'Puebla'),
('PED-1011', 'CLI-011', '11/03/2026', '1350.00', 'Entregado', 'PUE'),
('PED-1012', 'CLI-012', '2026-03-12', '1780.00', 'Entregado', 'YUC'),
('PED-1013', 'CLI-013', '2026-03-13', '2900.00', 'Entregado', 'Yucatan'),
('PED-1014', 'CLI-014', '2026-03-14', '1560.00', 'Entregado', 'Queretaro'),
('PED-1015', 'CLI-015', '2026-03-15', '890.00',  'Entregado', 'QRO'),
('PED-1016', 'CLI-016', '2026-03-16', '3400.00', 'Entregado', 'Veracruz'),
('PED-1017', 'CLI-017', '2026-03-17', '1200.00', 'Entregado', 'GTO'),
('PED-1018', 'CLI-001', '2026-03-18', '950.00',  'En tránsito', 'NL'),
('PED-1019', 'CLI-003', '2026-03-19', '1800.00', 'Cancelado',   'CDMX'),
('PED-1020', 'CLI-005', '2026-03-20', '650.00',  'Pendiente',   'JAL'),
('PED-1021', 'CLI-002', '2026-03-21', '-350.00', 'Entregado',   'NL'),
('PED-1022', 'CLI-004', '2026-03-22', '0.00',    'Entregado',   'CDMX'),
('PED-1023', 'CLI-999', '2026-03-23', '1500.00', 'Entregado',   'NL'),
('PED-1024', 'CLI-007', '',           '1200.00', 'Entregado',   'COAH'),
('PED-1025', 'CLI-008', 'FECHA_ROTA', '980.00',  'Entregado',   'COAH'),
('PED-1026', 'CLI-009', '2026-03-25', '1400.00', 'Entregado',   'ESTADO_INEXISTENTE'),
('PED-1001', 'CLI-001', '2026-03-01', '1250.00', 'Entregado',   'NL'),
('PED-1010', 'CLI-010', '2026-03-10', '2650.00', 'Entregado',   'Puebla'),
('PED-1027', 'CLI-010', '2026-03-26', '2100.00', 'Entregado',   'PUE'),
('PED-1028', 'CLI-012', '27/03/2026', '1650.00', 'Entregado',   'YUC'),
('PED-1029', 'CLI-014', '2026-03-28', '1950.00', 'Entregado',   'QRO'),
('PED-1030', 'CLI-017', '2026-03-29', '880.00',  'Entregado',   'GTO');

-- ------------------------------------------------------------------------------
-- FASE 3: PERFILADO DE DATOS (PASO 1)
-- ------------------------------------------------------------------------------
CREATE TABLE observaciones_perfilado (
    id_observacion      INT AUTO_INCREMENT PRIMARY KEY,
    tabla_origen        VARCHAR(50) NOT NULL,
    regla_o_metrica     VARCHAR(100) NOT NULL,
    registros_afectados INT NOT NULL,
    severidad           ENUM('INFO', 'BAJA', 'MEDIA', 'ALTA') NOT NULL,
    detalle_hallazgo    TEXT NOT NULL,
    fecha_analisis      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_clientes', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', CONCAT('Total clientes: ', COUNT(*)) FROM raw_clientes;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_pedidos', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', CONCAT('Total pedidos: ', COUNT(*)) FROM raw_pedidos;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'catalogo_estados', 'VOLUMETRIA_TOTAL', COUNT(*), 'INFO', CONCAT('Total entidades canónicas: ', COUNT(*)) FROM catalogo_estados;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_clientes', 'DUPLICADOS_ID_CLIENTE', COUNT(*), 'ALTA',
       CONCAT('Clientes duplicados: ', GROUP_CONCAT(DISTINCT id_cliente SEPARATOR ', '))
FROM (SELECT id_cliente FROM raw_clientes GROUP BY id_cliente HAVING COUNT(*) > 1) d;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_pedidos', 'DUPLICADOS_ID_PEDIDO', SUM(cnt - 1), 'ALTA',
       CONCAT('Pedidos repetidos: ', GROUP_CONCAT(CONCAT(id_pedido, ' (', cnt, ')') SEPARATOR '; '))
FROM (SELECT id_pedido, COUNT(*) AS cnt FROM raw_pedidos GROUP BY id_pedido HAVING COUNT(*) > 1) d;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_pedidos', 'MONTOS_NO_POSITIVOS', COUNT(*), 'ALTA',
       CONCAT('Montos <= 0 detectados: ', GROUP_CONCAT(CONCAT(id_pedido, ' ($', importe, ')') SEPARATOR ', '))
FROM raw_pedidos WHERE CAST(importe AS DECIMAL(12,2)) <= 0 OR importe IS NULL;

INSERT INTO observaciones_perfilado (tabla_origen, regla_o_metrica, registros_afectados, severidad, detalle_hallazgo)
SELECT 'raw_pedidos', 'CLIENTES_HUERFANOS', COUNT(*), 'ALTA',
       CONCAT('Pedidos a clientes inexistentes: ', GROUP_CONCAT(CONCAT(p.id_pedido, ' -> ', p.id_cliente) SEPARATOR ', '))
FROM raw_pedidos p LEFT JOIN raw_clientes c ON p.id_cliente = c.id_cliente WHERE c.id_cliente IS NULL;

-- ------------------------------------------------------------------------------
-- FASE 4: STAGING Y NORMALIZACIÓN (PASOS 2 Y 3)
-- ------------------------------------------------------------------------------
CREATE TABLE stg_clientes (
    id_cliente          VARCHAR(50) NOT NULL PRIMARY KEY,
    nombre              VARCHAR(150) NOT NULL,
    email               VARCHAR(150) NOT NULL,
    estado_original     VARCHAR(100) NULL,
    estado_canonico     VARCHAR(10) NOT NULL,
    fecha_registro      DATE NULL,
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO stg_clientes (id_cliente, nombre, email, estado_original, estado_canonico, fecha_registro)
WITH dedup AS (
    SELECT 
        fila_id,
        TRIM(id_cliente) AS id_cliente,
        TRIM(nombre) AS nombre,
        TRIM(email) AS email,
        TRIM(estado) AS estado_raw,
        TRIM(fecha_registro) AS fecha_raw,
        ROW_NUMBER() OVER (PARTITION BY TRIM(id_cliente) ORDER BY fila_id DESC) AS rn
    FROM raw_clientes
    WHERE id_cliente IS NOT NULL AND TRIM(id_cliente) != ''
)
SELECT 
    d.id_cliente,
    d.nombre,
    d.email,
    d.estado_raw,
    COALESCE(ce.estado_canonico, 'NE') AS estado_canonico,
    CASE 
        WHEN d.fecha_raw REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN STR_TO_DATE(d.fecha_raw, '%Y-%m-%d')
        WHEN d.fecha_raw REGEXP '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$' THEN STR_TO_DATE(d.fecha_raw, '%d/%m/%Y')
        ELSE NULL
    END
FROM dedup d
LEFT JOIN catalogo_estados ce 
    ON d.estado_raw = ce.estado_canonico 
    OR d.estado_raw = ce.nombre_oficial
    OR FIND_IN_SET(d.estado_raw, REPLACE(ce.alias, ', ', ',')) > 0
WHERE d.rn = 1;

CREATE TABLE stg_pedidos (
    fila_id                 INT NOT NULL PRIMARY KEY,
    id_pedido               VARCHAR(50) NOT NULL,
    id_cliente              VARCHAR(50) NOT NULL,
    fecha_pedido_raw        VARCHAR(50) NULL,
    fecha_pedido_norm       DATE NULL,
    importe_raw             VARCHAR(50) NULL,
    importe_norm            DECIMAL(12,2) NULL,
    estado_pedido           VARCHAR(50) NOT NULL,
    estado_envio_raw        VARCHAR(100) NULL,
    estado_envio_canonico   VARCHAR(10) NULL,
    fecha_procesamiento     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO stg_pedidos (fila_id, id_pedido, id_cliente, fecha_pedido_raw, fecha_pedido_norm, importe_raw, importe_norm, estado_pedido, estado_envio_raw, estado_envio_canonico)
SELECT 
    p.fila_id,
    TRIM(p.id_pedido),
    TRIM(p.id_cliente),
    p.fecha_pedido,
    CASE 
        WHEN TRIM(p.fecha_pedido) REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN STR_TO_DATE(TRIM(p.fecha_pedido), '%Y-%m-%d')
        WHEN TRIM(p.fecha_pedido) REGEXP '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$' THEN STR_TO_DATE(TRIM(p.fecha_pedido), '%d/%m/%Y')
        ELSE NULL
    END,
    p.importe,
    CASE 
        WHEN TRIM(p.importe) REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN CAST(TRIM(p.importe) AS DECIMAL(12,2))
        ELSE NULL
    END,
    TRIM(p.estado_pedido),
    TRIM(p.estado_envio),
    ce.estado_canonico
FROM raw_pedidos p
LEFT JOIN catalogo_estados ce 
    ON TRIM(p.estado_envio) = ce.estado_canonico 
    OR TRIM(p.estado_envio) = ce.nombre_oficial
    OR FIND_IN_SET(TRIM(p.estado_envio), REPLACE(ce.alias, ', ', ',')) > 0;

-- ------------------------------------------------------------------------------
-- FASE 5: VALIDACIÓN Y RECHAZOS (PASO 4)
-- ------------------------------------------------------------------------------
CREATE TABLE pedidos_rechazados (
    id_rechazo          INT AUTO_INCREMENT PRIMARY KEY,
    fila_id             INT NOT NULL,
    id_pedido           VARCHAR(50) NOT NULL,
    id_cliente          VARCHAR(50) NOT NULL,
    fecha_pedido_raw    VARCHAR(50) NULL,
    importe_raw         VARCHAR(50) NULL,
    estado_pedido       VARCHAR(50) NOT NULL,
    estado_envio_raw    VARCHAR(100) NULL,
    motivo_rechazo      VARCHAR(50) NOT NULL,
    detalle_error       TEXT NOT NULL,
    fecha_evaluacion    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE stg_pedidos_limpios (
    id_pedido           VARCHAR(50) NOT NULL PRIMARY KEY,
    id_cliente          VARCHAR(50) NOT NULL,
    fecha_pedido        DATE NOT NULL,
    importe             DECIMAL(12,2) NOT NULL,
    estado_pedido       VARCHAR(50) NOT NULL,
    estado_canonico     VARCHAR(10) NOT NULL,
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO pedidos_rechazados (fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, motivo_rechazo, detalle_error)
WITH evaluacion AS (
    SELECT 
        p.*,
        ROW_NUMBER() OVER (PARTITION BY p.id_pedido ORDER BY p.fila_id ASC) AS orden_aparicion,
        c.id_cliente AS cliente_existe
    FROM stg_pedidos p
    LEFT JOIN stg_clientes c ON p.id_cliente = c.id_cliente
)
SELECT fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, 'ID_PEDIDO_DUPLICADO', CONCAT('Pedido repetido id: ', id_pedido)
FROM evaluacion WHERE orden_aparicion > 1
UNION ALL
SELECT fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, 'CLIENTE_INEXISTENTE', CONCAT('Cliente ', id_cliente, ' no existe en clientes.')
FROM evaluacion WHERE orden_aparicion = 1 AND cliente_existe IS NULL
UNION ALL
SELECT fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, 'FECHA_INVALIDA', CONCAT('Fecha invalida o vacia: ', COALESCE(NULLIF(fecha_pedido_raw, ''), '[VACIO]'))
FROM evaluacion WHERE orden_aparicion = 1 AND cliente_existe IS NOT NULL AND fecha_pedido_norm IS NULL
UNION ALL
SELECT fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, 'IMPORTE_NO_POSITIVO', CONCAT('Importe <= 0: ', COALESCE(importe_raw, 'NULL'))
FROM evaluacion WHERE orden_aparicion = 1 AND cliente_existe IS NOT NULL AND fecha_pedido_norm IS NOT NULL AND (importe_norm IS NULL OR importe_norm <= 0)
UNION ALL
SELECT fila_id, id_pedido, id_cliente, fecha_pedido_raw, importe_raw, estado_pedido, estado_envio_raw, 'ESTADO_NO_RECONOCIDO', CONCAT('Estado desconocido: ', estado_envio_raw)
FROM evaluacion WHERE orden_aparicion = 1 AND cliente_existe IS NOT NULL AND fecha_pedido_norm IS NOT NULL AND (importe_norm IS NOT NULL AND importe_norm > 0) AND estado_envio_canonico IS NULL;

INSERT INTO stg_pedidos_limpios (id_pedido, id_cliente, fecha_pedido, importe, estado_pedido, estado_canonico)
SELECT p.id_pedido, p.id_cliente, p.fecha_pedido_norm, p.importe_norm, p.estado_pedido, p.estado_envio_canonico
FROM stg_pedidos p
WHERE p.fila_id NOT IN (SELECT fila_id FROM pedidos_rechazados);

-- ------------------------------------------------------------------------------
-- FASE 6: CARGA INCREMENTAL AL DATA MART Y PRUEBA DE IDEMPOTENCIA (PASO 5)
-- ------------------------------------------------------------------------------
CREATE TABLE dim_estado (
    estado_canonico VARCHAR(10) NOT NULL PRIMARY KEY,
    nombre_oficial  VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE dim_cliente (
    id_cliente          VARCHAR(50) NOT NULL PRIMARY KEY,
    nombre              VARCHAR(150) NOT NULL,
    email               VARCHAR(150) NOT NULL,
    estado_canonico     VARCHAR(10) NOT NULL,
    fecha_registro      DATE NULL,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_c_estado FOREIGN KEY (estado_canonico) REFERENCES dim_estado (estado_canonico)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE fact_ordenes (
    id_pedido           VARCHAR(50) NOT NULL PRIMARY KEY,
    id_cliente          VARCHAR(50) NOT NULL,
    estado_canonico     VARCHAR(10) NOT NULL,
    fecha_pedido        DATE NOT NULL,
    importe             DECIMAL(12,2) NOT NULL,
    estado_pedido       VARCHAR(50) NOT NULL,
    fecha_carga         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_f_cliente FOREIGN KEY (id_cliente) REFERENCES dim_cliente (id_cliente),
    CONSTRAINT fk_f_estado  FOREIGN KEY (estado_canonico) REFERENCES dim_estado (estado_canonico)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Carga dimensiones
INSERT INTO dim_estado (estado_canonico, nombre_oficial)
SELECT estado_canonico, nombre_oficial FROM catalogo_estados
UNION ALL
SELECT 'NE', 'No Especificado'
ON DUPLICATE KEY UPDATE nombre_oficial = VALUES(nombre_oficial);

INSERT INTO dim_cliente (id_cliente, nombre, email, estado_canonico, fecha_registro)
SELECT id_cliente, nombre, email, estado_canonico, fecha_registro FROM stg_clientes
ON DUPLICATE KEY UPDATE 
    nombre = VALUES(nombre), email = VALUES(email), estado_canonico = VALUES(estado_canonico), fecha_registro = VALUES(fecha_registro);

-- Primera ejecución de carga de hechos
INSERT INTO fact_ordenes (id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido)
SELECT id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido FROM stg_pedidos_limpios
ON DUPLICATE KEY UPDATE 
    id_cliente = VALUES(id_cliente), estado_canonico = VALUES(estado_canonico), fecha_pedido = VALUES(fecha_pedido), importe = VALUES(importe), estado_pedido = VALUES(estado_pedido);

SET @hechos_corrida_1 := (SELECT COUNT(*) FROM fact_ordenes);

-- Segunda ejecución para verificar idempotencia
INSERT INTO fact_ordenes (id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido)
SELECT id_pedido, id_cliente, estado_canonico, fecha_pedido, importe, estado_pedido FROM stg_pedidos_limpios
ON DUPLICATE KEY UPDATE 
    id_cliente = VALUES(id_cliente), estado_canonico = VALUES(estado_canonico), fecha_pedido = VALUES(fecha_pedido), importe = VALUES(importe), estado_pedido = VALUES(estado_pedido);

SET @hechos_corrida_2 := (SELECT COUNT(*) FROM fact_ordenes);

-- ------------------------------------------------------------------------------
-- FASE 7: CONCILIACIÓN Y AUDITORÍA (PASO 6)
-- ------------------------------------------------------------------------------
CREATE TABLE etl_auditoria (
    id_auditoria            INT AUTO_INCREMENT PRIMARY KEY,
    proceso_nombre          VARCHAR(100) NOT NULL,
    filas_raw               INT NOT NULL,
    filas_stg_limpias       INT NOT NULL,
    filas_rechazadas        INT NOT NULL,
    filas_fact              INT NOT NULL,
    diferencia_filas        INT NOT NULL,
    balance_cuadrado        ENUM('SI', 'NO') NOT NULL,
    importe_bruto_raw       DECIMAL(14,2) NOT NULL,
    importe_rechazado       DECIMAL(14,2) NOT NULL,
    importe_stg_limpio      DECIMAL(14,2) NOT NULL,
    importe_fact            DECIMAL(14,2) NOT NULL,
    desvio_stg_vs_fact      DECIMAL(14,2) NOT NULL,
    estado_ejecucion        ENUM('EXITOSO', 'FALLIDO') NOT NULL,
    fecha_ejecucion         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO etl_auditoria (
    proceso_nombre, filas_raw, filas_stg_limpias, filas_rechazadas, filas_fact,
    diferencia_filas, balance_cuadrado, importe_bruto_raw, importe_rechazado,
    importe_stg_limpio, importe_fact, desvio_stg_vs_fact, estado_ejecucion
)
SELECT 
    'Pipeline Maestro ETL' AS proceso_nombre,
    r.cnt_raw, s.cnt_stg, rc.cnt_rechazados, f.cnt_fact,
    (r.cnt_raw - (s.cnt_stg + rc.cnt_rechazados)) AS dif_filas,
    IF((r.cnt_raw - (s.cnt_stg + rc.cnt_rechazados)) = 0, 'SI', 'NO') AS balance_cuadrado,
    r.monto_raw, rc.monto_rechazado, s.monto_stg, f.monto_fact,
    (s.monto_stg - f.monto_fact) AS desvio,
    IF((r.cnt_raw - (s.cnt_stg + rc.cnt_rechazados)) = 0 AND (s.monto_stg - f.monto_fact) = 0.00, 'EXITOSO', 'FALLIDO')
FROM (SELECT COUNT(*) AS cnt_raw, SUM(CASE WHEN TRIM(importe) REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN CAST(TRIM(importe) AS DECIMAL(12,2)) ELSE 0 END) AS monto_raw FROM raw_pedidos) r
CROSS JOIN (SELECT COUNT(*) AS cnt_stg, SUM(importe) AS monto_stg FROM stg_pedidos_limpios) s
CROSS JOIN (SELECT COUNT(*) AS cnt_rechazados, SUM(CASE WHEN TRIM(importe_raw) REGEXP '^-?[0-9]+(\\.[0-9]+)?$' THEN CAST(TRIM(importe_raw) AS DECIMAL(12,2)) ELSE 0 END) AS monto_rechazado FROM pedidos_rechazados) rc
CROSS JOIN (SELECT COUNT(*) AS cnt_fact, SUM(importe) AS monto_fact FROM fact_ordenes) f;

-- ------------------------------------------------------------------------------
-- FASE 8: CONSULTA FINAL DE INDICADORES (PASO 7)
-- ------------------------------------------------------------------------------
-- Indicadores por Fecha y Estado:
SELECT 
    f.fecha_pedido,
    e.estado_canonico,
    e.nombre_oficial AS estado_destino,
    COUNT(CASE WHEN f.estado_pedido = 'Entregado' THEN f.id_pedido END) AS pedidos_entregados,
    COALESCE(SUM(CASE WHEN f.estado_pedido = 'Entregado' THEN f.importe END), 0.00) AS ventas_netas
FROM fact_ordenes f
JOIN dim_estado e ON f.estado_canonico = e.estado_canonico
GROUP BY f.fecha_pedido, e.estado_canonico, e.nombre_oficial
HAVING pedidos_entregados > 0
ORDER BY f.fecha_pedido ASC, ventas_netas DESC;
