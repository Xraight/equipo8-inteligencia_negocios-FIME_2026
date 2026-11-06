-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: script_maestro_pia_etl.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Script maestro unificado y 100% reproducible para inicializar la base de
-- datos `ce_bi`, desplegar las tablas de staging y datamart, ingestar los CSVs,
-- compilar los procedimientos almacenados, ejecutar el pipeline ETL completo
-- y validar el balance de masa contable.
--
-- FUNCIÓN ESPECÍFICA:
-- Proporcionar un único punto de entrada SQL para entornos de CI/CD (GitHub Actions),
-- demostraciones ante el sínodo evaluador y despliegues automáticos en Docker.
-- ==============================================================================

-- 1. Inicialización de BD y Tablas de Auditoría
SOURCE /workspace/PIA/02_datamart_mysql/00_inicializacion_bd_y_logs.sql;

-- 2. DDL de Capa Staging (11 tablas temporales)
SOURCE /workspace/PIA/02_datamart_mysql/01_ddl_staging.sql;

-- 3. Ingesta Masiva desde CSV mediante LOAD DATA INFILE
SOURCE /workspace/PIA/02_datamart_mysql/01b_cargar_csv_a_staging.sql;

-- 4. DDL del Data Mart Dimensional (Esquema Estrella y Constelación)
SOURCE /workspace/PIA/02_datamart_mysql/02_ddl_datamart.sql;

-- 5. Procedimientos Almacenados de Limpieza y Generación de Calendario
SOURCE /workspace/PIA/02_datamart_mysql/03_sp_limpieza_transformacion.sql;

-- 6. Procedimientos Almacenados de Carga de Dimensiones y Hechos
SOURCE /workspace/PIA/02_datamart_mysql/04_sp_carga_dimensiones_hechos.sql;

-- 7. Procedimiento Almacenado Maestro Orquestador ETL
SOURCE /workspace/PIA/02_datamart_mysql/05_sp_orquestador_etl.sql;

-- 8. Vistas Analíticas de Negocio y KPIs Ejecutivos
SOURCE /workspace/PIA/02_datamart_mysql/06_vistas_analiticas_kpi.sql;

-- 9. Ejecución del Pipeline ETL Maestro
USE `ce_bi`;
CALL `sp_orquestador_etl_maestro`();

-- 10. Auditoría de Balance de Masa y Verificación Numérica
SOURCE /workspace/PIA/02_datamart_mysql/07_auditoria_balance_masa.sql;
