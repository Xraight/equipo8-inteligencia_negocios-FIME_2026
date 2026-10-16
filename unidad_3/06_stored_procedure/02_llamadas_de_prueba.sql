-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- UNIDAD 3: 06_stored_procedure / 02_llamadas_de_prueba.sql
-- OBJETIVO: Ejecución de Pruebas y Evidencia del Stored Procedure (Reto 4)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CASO 1: EJECUCIÓN REGULAR ESTÁNDAR (AÑO 2026, TRIMESTRE 2 vs TRIMESTRE 1)
-- Evalúa el Top 5 de cada región en Q2 comparado automáticamente contra Q1.
-- ------------------------------------------------------------------------------
SELECT 
    'Caso de Prueba 1: Q2 2026 vs Q1 2026' AS escenario_prueba,
    region,
    posicion_region,
    producto_id_bk,
    nombre_producto,
    rentabilidad_actual,
    rentabilidad_anterior,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM sp_reporte_rentabilidad_top5(2026, 2);

-- ------------------------------------------------------------------------------
-- CASO 2: EJECUCIÓN DE CASO LÍMITE (AÑO 2026, TRIMESTRE 1 vs TRIMESTRE 4 2025)
-- Evalúa el cálculo automático del periodo previo (año anterior Q4) y el manejo
-- de ausencia de datos previos (indicador 'Nuevo en periodo', variación % nula).
-- ------------------------------------------------------------------------------
SELECT 
    'Caso de Prueba 2: Q1 2026 vs Q4 2025 (Sin Histórico)' AS escenario_prueba,
    region,
    posicion_region,
    producto_id_bk,
    nombre_producto,
    rentabilidad_actual,
    rentabilidad_anterior,
    variacion_absoluta,
    variacion_porcentual,
    indicador_periodo_anterior
FROM sp_reporte_rentabilidad_top5(2026, 1);

-- ------------------------------------------------------------------------------
-- CASO 3: EJECUCIÓN DEL PROCEDIMIENTO PROCEDURAL MEDIANTE 'CALL'
-- Demuestra compatibilidad procedural para entornos de ejecución por lotes (Batch).
-- ------------------------------------------------------------------------------
CALL pr_ejecutar_reporte_rentabilidad(2026, 2);
