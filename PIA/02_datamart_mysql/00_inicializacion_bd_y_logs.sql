-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 00_inicializacion_bd_y_logs.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Inicializar el catálogo de base de datos analítica `ce_bi` y estructurar las
-- tablas de auditoría y trazabilidad del pipeline ETL (`etl_log` y `etl_balance_masa`).
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Crear la base de datos `ce_bi` con codificación UTF-8 MB4.
-- 2. Crear la tabla `etl_log` para registrar ejecuciones, microsegundos, filas
--    leídas, cargadas y rechazadas por cada procedimiento del pipeline.
-- 3. Crear la tabla `etl_balance_masa` para almacenar conciliaciones contables
--    y cuantitativas entre fuentes RAW, Staging y Data Mart.
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS `ce_bi`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `ce_bi`;

-- ------------------------------------------------------------------------------
-- Tabla de Bitácora de Ejecución del Pipeline ETL
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `etl_log`;
CREATE TABLE `etl_log` (
  `run_id` BIGINT AUTO_INCREMENT PRIMARY KEY,
  `proceso` VARCHAR(120) NOT NULL COMMENT 'Nombre del procedimiento almacenado o etapa ejecutada',
  `inicio` DATETIME NOT NULL COMMENT 'Marca temporal de inicio de la etapa',
  `fin` DATETIME NULL COMMENT 'Marca temporal de finalización de la etapa',
  `duracion_segundos` DECIMAL(10,3) NULL COMMENT 'Tiempo transcurrido en segundos',
  `filas_leidas` BIGINT DEFAULT 0 COMMENT 'Registros extraídos desde origen o staging',
  `filas_cargadas` BIGINT DEFAULT 0 COMMENT 'Registros insertados exitosamente en destino',
  `filas_rechazadas` BIGINT DEFAULT 0 COMMENT 'Registros omitidos o catalogados con anomalías',
  `estatus` VARCHAR(25) NOT NULL COMMENT 'EXITOSO, ADVERTENCIA o FALLIDO',
  `detalle` VARCHAR(500) NULL COMMENT 'Observaciones técnicas, balance y notas del proceso',
  INDEX `idx_log_proceso_inicio` (`proceso`, `inicio`)
) ENGINE=InnoDB COMMENT='Bitácora de trazabilidad y auditoría de ejecución del pipeline ETL';

-- ------------------------------------------------------------------------------
-- Tabla de Balance de Masa y Conciliación Numérica Cuantitativa
-- ------------------------------------------------------------------------------
DROP TABLE IF EXISTS `etl_balance_masa`;
CREATE TABLE `etl_balance_masa` (
  `balance_id` INT AUTO_INCREMENT PRIMARY KEY,
  `fecha_auditoria` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `concepto` VARCHAR(100) NOT NULL COMMENT 'Métrica o tabla auditada',
  `conteo_origen_raw` BIGINT NOT NULL COMMENT 'Registros contabilizados en archivos fuente RAW',
  `conteo_staging` BIGINT NOT NULL COMMENT 'Registros ingresados en capa staging',
  `conteo_datamart` BIGINT NOT NULL COMMENT 'Registros cargados en tablas finales del Data Mart',
  `discrepancia` BIGINT GENERATED ALWAYS AS (conteo_staging - conteo_datamart) STORED,
  `porcentaje_integridad` DECIMAL(6,2) GENERATED ALWAYS AS (
    CASE WHEN conteo_staging = 0 THEN 100.00
         ELSE ROUND((conteo_datamart / conteo_staging) * 100, 2)
    END
  ) STORED,
  `estatus_validacion` VARCHAR(20) NOT NULL COMMENT 'CONCILIADO o DESCUADRE',
  `notas` VARCHAR(255) NULL
) ENGINE=InnoDB COMMENT='Auditoría de balance de masa para verificar que no existe pérdida de datos';

SELECT 'Inicialización de Base de Datos ce_bi y Tablas de Auditoría completada con éxito.' AS resultado;
