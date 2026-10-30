-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 01_datos_crudos / 01_creacion_bd.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Creación de la base de datos y tablas de aterrizaje crudo (Raw Zone)
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

-- 1. Creación y selección de la base de datos
CREATE DATABASE IF NOT EXISTS tienda_bi
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE tienda_bi;

-- 2. Limpieza de tablas previas (en orden inverso de dependencias si aplica)
DROP TABLE IF EXISTS raw_pedidos;
DROP TABLE IF EXISTS raw_clientes;
DROP TABLE IF EXISTS catalogo_estados;

-- ------------------------------------------------------------------------------
-- TABLA: catalogo_estados
-- DESCRIPCIÓN: Catálogo canónico de entidades federativas/estados con alias.
-- ------------------------------------------------------------------------------
CREATE TABLE catalogo_estados (
    estado_canonico VARCHAR(10) NOT NULL PRIMARY KEY COMMENT 'Clave oficial o código canónico (ej. NL, CDMX)',
    nombre_oficial  VARCHAR(100) NOT NULL COMMENT 'Nombre completo oficial de la entidad federativa',
    alias           TEXT NOT NULL COMMENT 'Lista de abreviaturas y variantes separadas por coma'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- TABLA: raw_clientes
-- DESCRIPCIÓN: Zona de aterrizaje inmutable para clientes.csv.
--              Mantiene tipos de texto flexible para preservar datos crudos.
-- ------------------------------------------------------------------------------
CREATE TABLE raw_clientes (
    fila_id         INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador secuencial de ingesta técnica',
    id_cliente      VARCHAR(50) NULL COMMENT 'Clave natural del cliente en el sistema fuente',
    nombre          VARCHAR(150) NULL COMMENT 'Nombre completo del cliente',
    email           VARCHAR(150) NULL COMMENT 'Correo electrónico proporcionado',
    estado          VARCHAR(100) NULL COMMENT 'Estado o provincia capturado sin estandarizar',
    fecha_registro  VARCHAR(50) NULL COMMENT 'Fecha de registro en texto (formatos mixtos)'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- TABLA: raw_pedidos
-- DESCRIPCIÓN: Zona de aterrizaje inmutable para pedidos.sql.
--              Almacena transacciones crudas para auditoría forense.
-- ------------------------------------------------------------------------------
CREATE TABLE raw_pedidos (
    fila_id         INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador secuencial de ingesta técnica',
    id_pedido       VARCHAR(50) NULL COMMENT 'Identificador de la orden en el punto de venta',
    id_cliente      VARCHAR(50) NULL COMMENT 'Identificador del cliente comprador',
    fecha_pedido    VARCHAR(50) NULL COMMENT 'Fecha de compra en texto crudo',
    importe         VARCHAR(50) NULL COMMENT 'Importe de la orden en texto (posibles números negativos o nulos)',
    estado_pedido   VARCHAR(50) NULL COMMENT 'Estatus de la orden (Entregado, En tránsito, Cancelado, etc.)',
    estado_envio    VARCHAR(100) NULL COMMENT 'Estado federativo de destino del pedido'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
