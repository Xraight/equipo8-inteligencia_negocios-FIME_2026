-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 06_conciliacion_auditoria / 05_conciliacion_auditoria.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Paso 6 - Conciliación cuantitativa, balance de masa y etl_auditoria
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- Limpieza preventiva
DROP TABLE IF EXISTS etl_auditoria;

-- ------------------------------------------------------------------------------
-- 1. TABLA: etl_auditoria
-- DESCRIPCIÓN: Bitácora centralizada de control, conciliación y balance de masa
--              entre la capa cruda (raw), cuarentena (rechazos) y Data Mart (fact).
-- ------------------------------------------------------------------------------
CREATE TABLE etl_auditoria (
    id_auditoria            INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador de la corrida de auditoría',
    proceso_nombre          VARCHAR(100) NOT NULL COMMENT 'Nombre del pipeline o flujo ejecutado',
    filas_raw               INT NOT NULL COMMENT 'Total de transacciones recibidas en raw_pedidos',
    filas_stg_limpias       INT NOT NULL COMMENT 'Total de transacciones que superaron la validación',
    filas_rechazadas        INT NOT NULL COMMENT 'Total de transacciones enviadas a pedidos_rechazados',
    filas_fact              INT NOT NULL COMMENT 'Total de transacciones persistidas en fact_ordenes',
    diferencia_filas        INT NOT NULL COMMENT 'Balance de masa: raw - (limpias + rechazadas)',
    balance_cuadrado        ENUM('SI', 'NO') NOT NULL COMMENT 'Indicador booleano de balance perfecto',
    importe_bruto_raw       DECIMAL(14,2) NOT NULL COMMENT 'Suma aritmética de importes procesables en raw',
    importe_rechazado       DECIMAL(14,2) NOT NULL COMMENT 'Suma de importes en cuarentena',
    importe_stg_limpio      DECIMAL(14,2) NOT NULL COMMENT 'Suma de importes en staging limpio',
    importe_fact            DECIMAL(14,2) NOT NULL COMMENT 'Suma de importes en la tabla de hechos',
    desvio_stg_vs_fact      DECIMAL(14,2) NOT NULL COMMENT 'Diferencia financiera stg - fact',
    estado_ejecucion        ENUM('EXITOSO', 'FALLIDO') NOT NULL COMMENT 'Estatus global de la corrida',
    fecha_ejecucion         TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Marca de tiempo de conciliación'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------------------------
-- 2. REGISTRO DE AUDITORÍA Y CONCILIACIÓN
-- ------------------------------------------------------------------------------
INSERT INTO etl_auditoria (
    proceso_nombre,
    filas_raw,
    filas_stg_limpias,
    filas_rechazadas,
    filas_fact,
    diferencia_filas,
    balance_cuadrado,
    importe_bruto_raw,
    importe_rechazado,
    importe_stg_limpio,
    importe_fact,
    desvio_stg_vs_fact,
    estado_ejecucion
)
WITH metricas_raw AS (
    SELECT 
        COUNT(*) AS total_raw,
        SUM(
            CASE 
                WHEN TRIM(importe) REGEXP '^-?[0-9]+(\\.[0-9]+)?$' 
                THEN CAST(TRIM(importe) AS DECIMAL(12,2)) 
                ELSE 0.00 
            END
        ) AS suma_monto_raw
    FROM raw_pedidos
),
metricas_stg AS (
    SELECT 
        COUNT(*) AS total_stg,
        COALESCE(SUM(importe), 0.00) AS suma_monto_stg
    FROM stg_pedidos_limpios
),
metricas_rechazos AS (
    SELECT 
        COUNT(*) AS total_rechazados,
        SUM(
            CASE 
                WHEN TRIM(importe_raw) REGEXP '^-?[0-9]+(\\.[0-9]+)?$' 
                THEN CAST(TRIM(importe_raw) AS DECIMAL(12,2)) 
                ELSE 0.00 
            END
        ) AS suma_monto_rechazado
    FROM pedidos_rechazados
),
metricas_fact AS (
    SELECT 
        COUNT(*) AS total_fact,
        COALESCE(SUM(importe), 0.00) AS suma_monto_fact
    FROM fact_ordenes
)
SELECT 
    'Pipeline ETL: Raw a Data Mart' AS proceso_nombre,
    r.total_raw,
    s.total_stg,
    rc.total_rechazados,
    f.total_fact,
    (r.total_raw - (s.total_stg + rc.total_rechazados)) AS diferencia_filas,
    CASE 
        WHEN (r.total_raw - (s.total_stg + rc.total_rechazados)) = 0 THEN 'SI'
        ELSE 'NO'
    END AS balance_cuadrado,
    r.suma_monto_raw,
    rc.suma_monto_rechazado,
    s.suma_monto_stg,
    f.suma_monto_fact,
    (s.suma_monto_stg - f.suma_monto_fact) AS desvio_stg_vs_fact,
    CASE 
        WHEN (r.total_raw - (s.total_stg + rc.total_rechazados)) = 0 
         AND (s.suma_monto_stg - f.suma_monto_fact) = 0.00 
        THEN 'EXITOSO'
        ELSE 'FALLIDO'
    END AS estado_ejecucion
FROM metricas_raw r
CROSS JOIN metricas_stg s
CROSS JOIN metricas_rechazos rc
CROSS JOIN metricas_fact f;

-- ------------------------------------------------------------------------------
-- 3. REPORTES VISUALES DE CONCILIACIÓN
-- ------------------------------------------------------------------------------

-- Reporte 1: Balance cuantitativo de registros
SELECT 
    filas_raw AS `Total Recibido (Raw)`,
    filas_stg_limpias AS `Aceptadas Únicas (Stg)`,
    filas_rechazadas AS `Rechazadas (Cuarentena)`,
    (filas_stg_limpias + filas_rechazadas) AS `Total Justificado`,
    diferencia_filas AS `Discrepancia`,
    balance_cuadrado AS `Balance Cuadrado`
FROM etl_auditoria;

-- Reporte 2: Balance monetario e integridad financiera
SELECT 
    importe_bruto_raw AS `Monto Bruto Total Raw`,
    importe_rechazado AS `Monto Descartado Cuarentena`,
    importe_stg_limpio AS `Monto Válido Staging`,
    importe_fact AS `Monto Cargado Fact`,
    desvio_stg_vs_fact AS `Diferencial Stg vs Fact`,
    estado_ejecucion AS `Estado General`
FROM etl_auditoria;
