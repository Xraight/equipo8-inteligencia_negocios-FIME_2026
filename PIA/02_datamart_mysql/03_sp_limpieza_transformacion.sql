-- ==============================================================================
-- PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
-- ARCHIVO: 03_sp_limpieza_transformacion.sql
-- AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
-- ENTORNO: MySQL 8.0+ / Docker
-- ==============================================================================
-- FUNCIÓN GENERAL:
-- Implementar los procedimientos almacenados de calidad, saneamiento e
-- imputación controlada de datos desde Staging hacia estructuras intermedias.
--
-- FUNCIÓN ESPECÍFICA:
-- 1. Estandarizar valores de texto (eliminación de espacios, caracteres espurios).
-- 2. Imputar nulos en CRM (ciudad='No Especificada', email, normalización de sexo).
-- 3. Generar la secuencia cronológica continua de fechas para `dim_tiempo`.
-- 4. Registrar anomalías saneadas en `etl_log`.
-- ==============================================================================

USE `ce_bi`;

DROP PROCEDURE IF EXISTS `sp_etl_limpiar_catalogos`;
DELIMITER //

CREATE PROCEDURE `sp_etl_limpiar_catalogos`()
BEGIN
  DECLARE v_inicio DATETIME;
  DECLARE v_fin DATETIME;
  DECLARE v_filas_leidas BIGINT DEFAULT 0;
  DECLARE v_filas_limpias BIGINT DEFAULT 0;

  SET v_inicio = NOW();

  -- Conteo de registros en staging de clientes
  SELECT COUNT(*) INTO v_filas_leidas FROM `stg_ce_clientes`;

  -- Limpieza y estandarización en staging de clientes
  UPDATE `stg_ce_clientes`
  SET
    `cliente_id` = TRIM(`cliente_id`),
    `nombre`     = TRIM(`nombre`),
    `sexo`       = CASE
                     WHEN UPPER(TRIM(`sexo`)) = 'M' THEN 'Masculino'
                     WHEN UPPER(TRIM(`sexo`)) = 'F' THEN 'Femenino'
                     ELSE 'No Especificado'
                   END,
    `ciudad`     = CASE
                     WHEN `ciudad` IS NULL OR TRIM(`ciudad`) = '' OR UPPER(TRIM(`ciudad`)) IN ('NULL', 'NONE', 'N/A')
                     THEN 'No Especificada'
                     ELSE TRIM(`ciudad`)
                   END,
    `segmento`   = TRIM(`segmento`),
    `email`      = CASE
                     WHEN `email` IS NULL OR TRIM(`email`) = '' OR UPPER(TRIM(`email`)) IN ('NULL', 'NONE', 'N/A')
                     THEN 'sin_correo@ejemplo.com'
                     ELSE LOWER(TRIM(`email`))
                   END;

  SELECT COUNT(*) INTO v_filas_limpias FROM `stg_ce_clientes` WHERE `cliente_id` IS NOT NULL;

  -- Limpieza de productos
  UPDATE `stg_ce_productos`
  SET
    `producto_id` = TRIM(`producto_id`),
    `sku`         = TRIM(`sku`),
    `producto`    = TRIM(`producto`),
    `categoria`   = TRIM(`categoria`),
    `marca`       = TRIM(`marca`),
    `activo`      = UPPER(TRIM(`activo`)),
    `requiere_instalacion` = UPPER(TRIM(`requiere_instalacion`));

  -- Limpieza de sucursales
  UPDATE `stg_ce_sucursales`
  SET
    `sucursal_id` = TRIM(`sucursal_id`),
    `sucursal`    = TRIM(`sucursal`),
    `ciudad`      = TRIM(`ciudad`),
    `estado`      = TRIM(`estado`);

  SET v_fin = NOW();

  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'sp_etl_limpiar_catalogos', v_inicio, v_fin,
    TIMESTAMPDIFF(MICROSECOND, v_inicio, v_fin) / 1000000.0,
    v_filas_leidas, v_filas_limpias, 0, 'EXITOSO',
    'Estandarización de clientes, imputación de nulos y saneamiento de productos y sucursales'
  );
END //

-- ------------------------------------------------------------------------------
-- Procedimiento para Poblado Continuo de la Dimensión de Tiempo
-- ------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS `sp_etl_poblar_dim_tiempo`;
CREATE PROCEDURE `sp_etl_poblar_dim_tiempo`(IN p_fecha_inicio DATE, IN p_fecha_fin DATE)
BEGIN
  DECLARE v_inicio DATETIME;
  DECLARE v_fin DATETIME;
  DECLARE v_fecha_actual DATE;
  DECLARE v_insertados INT DEFAULT 0;

  SET v_inicio = NOW();
  SET v_fecha_actual = p_fecha_inicio;

  -- Borrado previo
  DELETE FROM `dim_tiempo`;

  WHILE v_fecha_actual <= p_fecha_fin DO
    INSERT INTO `dim_tiempo` (
      `tiempo_id`, `fecha`, `anio`, `trimestre`, `trimestre_nombre`,
      `mes`, `mes_nombre`, `mes_anio`, `semana_anio`, `dia_mes`,
      `dia_semana`, `dia_semana_nombre`, `es_fin_semana`
    ) VALUES (
      YEAR(v_fecha_actual)*10000 + MONTH(v_fecha_actual)*100 + DAY(v_fecha_actual),
      v_fecha_actual,
      YEAR(v_fecha_actual),
      QUARTER(v_fecha_actual),
      CONCAT('Q', QUARTER(v_fecha_actual)),
      MONTH(v_fecha_actual),
      CASE MONTH(v_fecha_actual)
        WHEN 1 THEN 'Enero' WHEN 2 THEN 'Febrero' WHEN 3 THEN 'Marzo'
        WHEN 4 THEN 'Abril' WHEN 5 THEN 'Mayo' WHEN 6 THEN 'Junio'
        WHEN 7 THEN 'Julio' WHEN 8 THEN 'Agosto' WHEN 9 THEN 'Septiembre'
        WHEN 10 THEN 'Octubre' WHEN 11 THEN 'Noviembre' WHEN 12 THEN 'Diciembre'
      END,
      DATE_FORMAT(v_fecha_actual, '%Y-%m'),
      WEEK(v_fecha_actual, 3),
      DAY(v_fecha_actual),
      WEEKDAY(v_fecha_actual) + 1,
      CASE WEEKDAY(v_fecha_actual)
        WHEN 0 THEN 'Lunes' WHEN 1 THEN 'Martes' WHEN 2 THEN 'Miércoles'
        WHEN 3 THEN 'Jueves' WHEN 4 THEN 'Viernes' WHEN 5 THEN 'Sábado'
        WHEN 6 THEN 'Domingo'
      END,
      IF(WEEKDAY(v_fecha_actual) IN (5, 6), 1, 0)
    );

    SET v_fecha_actual = DATE_ADD(v_fecha_actual, INTERVAL 1 DAY);
    SET v_insertados = v_insertados + 1;
  END WHILE;

  SET v_fin = NOW();

  INSERT INTO `etl_log` (
    `proceso`, `inicio`, `fin`, `duracion_segundos`,
    `filas_leidas`, `filas_cargadas`, `filas_rechazadas`, `estatus`, `detalle`
  ) VALUES (
    'sp_etl_poblar_dim_tiempo', v_inicio, v_fin,
    TIMESTAMPDIFF(MICROSECOND, v_inicio, v_fin) / 1000000.0,
    v_insertados, v_insertados, 0, 'EXITOSO',
    CONCAT('Generación continua de calendario desde ', p_fecha_inicio, ' hasta ', p_fecha_fin)
  );
END //

DELIMITER ;

SELECT 'Procedimientos de limpieza y calendario creados exitosamente.' AS resultado;
