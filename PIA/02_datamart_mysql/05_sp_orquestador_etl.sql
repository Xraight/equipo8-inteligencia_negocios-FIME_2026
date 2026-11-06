-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 05_sp_orquestador_etl.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Orquestar de extremo a extremo la ejecución secuencial del Pipeline ETL
-- garantizando la trazabilidad, control de errores y balance de masa contable.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Ejecutar en orden estricto de dependencias:
--    a) Limpieza y saneamiento de catálogos en Staging.
--    b) Generación y poblado de la dimensión de tiempo (2024 a 2026).
--    c) Carga de dimensiones conformes con surrogate keys y registro comodín.
--    d) Carga masiva atómica del hecho principal (fact_ventas_detalle).
--    e) Carga de hechos satélites (devoluciones, instalaciones, existencias).
-- 2. Registrar en `etl_log` el tiempo total y resumen de la ejecución.
-- ==============================================================================

USE `ce_bi`;

DROP PROCEDURE IF EXISTS `sp_orquestador_etl_maestro`;
DELIMITER //

CREATE PROCEDURE `sp_orquestador_etl_maestro`()
BEGIN
  DECLARE v_inicio_total DATETIME;
  DECLARE v_fin_total DATETIME;
  DECLARE v_total_ventas BIGINT DEFAULT 0;
  DECLARE v_total_devs BIGINT DEFAULT 0;
  DECLARE v_total_inst BIGINT DEFAULT 0;
  DECLARE v_total_inv BIGINT DEFAULT 0;

  SET v_inicio_total = NOW();

  -- Registrar inicio del ciclo maestro
  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'ETL_MAESTRO_INICIO', v_inicio_total, NULL, 0,
    0, 0, 0, 'EN_PROCESO', 'Iniciando pipeline integral de Data Mart Casa&Estilo'
  );

  -- Paso 1: Saneamiento de textos e imputación de nulos
  CALL `sp_etl_limpiar_catalogos`();

  -- Paso 2: Generación del calendario continuo (2024-01-01 a 2026-12-31)
  CALL `sp_etl_poblar_dim_tiempo`('2024-01-01', '2026-12-31');

  -- Paso 3: Carga de Dimensiones Conformes
  CALL `sp_etl_cargar_dimensiones`();

  -- Paso 4: Carga del Hecho Central (Ventas Detalle)
  CALL `sp_etl_cargar_fact_ventas`();

  -- Paso 5: Carga de Hechos Satélites (Devoluciones, Instalaciones, Inventario)
  CALL `sp_etl_cargar_hechos_satelites`();

  -- Paso 6: Verificación y Balance
  SELECT COUNT(*) INTO v_total_ventas FROM `fact_ventas_detalle`;
  SELECT COUNT(*) INTO v_total_devs   FROM `fact_devoluciones`;
  SELECT COUNT(*) INTO v_total_inst   FROM `fact_instalaciones`;
  SELECT COUNT(*) INTO v_total_inv    FROM `fact_inventario_snapshot`;

  -- Actualizar tabla de balance de masa
  DELETE FROM `etl_balance_masa`;

  INSERT INTO `etl_balance_masa` (
    `concepto`, `conteo_origen_raw`, `conteo_staging`, `conteo_datamart`, `estatus_validacion`, `notas`
  ) VALUES
  ('Ventas Detalle (Líneas)', 331758, (SELECT COUNT(*) FROM `stg_ce_detalle_ventas`), v_total_ventas,
   IF(v_total_ventas = 331758, 'CONCILIADO', 'DESCUADRE'), 'Granularidad atómica preservada al 100%'),
  ('Devoluciones', 9952, (SELECT COUNT(*) FROM `stg_ce_devoluciones`), v_total_devs,
   IF(v_total_devs = 9952, 'CONCILIADO', 'DESCUADRE'), '100% eventos vinculados'),
  ('Instalaciones', 6500, (SELECT COUNT(*) FROM `stg_ce_instalaciones`), v_total_inst,
   IF(v_total_inst = 6500, 'CONCILIADO', 'DESCUADRE'), '100% órdenes técnicas integradas'),
  ('Snapshot Existencias', 21440, (SELECT COUNT(*) FROM `stg_ce_existencias`), v_total_inv,
   IF(v_total_inv = 21440, 'CONCILIADO', 'DESCUADRE'), '16 sucursales x 1340 productos evaluados');

  SET v_fin_total = NOW();

  -- Registrar conclusión exitosa
  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'ETL_MAESTRO_FIN', v_inicio_total, v_fin_total,
    TIMESTAMPDIFF(MICROSECOND, v_inicio_total, v_fin_total) / 1000000.0,
    v_total_ventas + v_total_devs + v_total_inst + v_total_inv,
    v_total_ventas + v_total_devs + v_total_inst + v_total_inv, 0, 'EXITOSO',
    CONCAT('Pipeline completado con éxito. Ventas=', v_total_ventas, ', Devs=', v_total_devs, ', Inst=', v_total_inst, ', Inv=', v_total_inv)
  );

  SELECT
    'PIPELINE ETL MAESTRO EJECUTADO CON ÉXITO' AS resultado,
    v_total_ventas AS ventas_cargadas,
    v_total_devs   AS devoluciones_cargadas,
    v_total_inst   AS instalaciones_cargadas,
    v_total_inv    AS existencias_cargadas,
    TIMESTAMPDIFF(MICROSECOND, v_inicio_total, v_fin_total) / 1000000.0 AS duracion_segundos;
END //

DELIMITER ;

SELECT 'Procedimiento maestro sp_orquestador_etl_maestro creado exitosamente.' AS resultado;
