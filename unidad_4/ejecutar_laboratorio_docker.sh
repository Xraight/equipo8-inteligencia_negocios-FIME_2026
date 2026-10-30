#!/usr/bin/env bash
# ==============================================================================
# PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
# UNIDAD 4: RUNNER DE EJECUCIÓN TOTAL EN DOCKER (MYSQL 8.0)
# EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
# ==============================================================================

set -e

CONTAINER_NAME="casa_estilo_mysql"
DB_NAME="tienda_bi"
DB_USER="root"
DB_PASS="password"

echo "=============================================================================="
echo "🚀 INICIANDO EJECUCIÓN AUTOMATIZADA: LABORATORIO ETL (UNIDAD 4)"
echo "=============================================================================="

# 1. Asegurar que el contenedor MySQL esté activo
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "📦 Levantando servicio de base de datos MySQL 8.0 en Docker..."
    docker compose up -d mysql
    echo "⏳ Esperando disponibilidad de MySQL Server 8.0..."
    until docker exec ${CONTAINER_NAME} mysqladmin ping -u ${DB_USER} -p${DB_PASS} --silent &>/dev/null; do
        sleep 2
    done
fi

echo "✅ Contenedor MySQL 8.0 activo y respondiendo."

# Función auxiliar para ejecutar archivos SQL
run_sql_file() {
    local step_title="$1"
    local sql_path="$2"
    echo ""
    echo "------------------------------------------------------------------------------"
    echo "▶️  ${step_title} (${sql_path})"
    echo "------------------------------------------------------------------------------"
    docker exec -i ${CONTAINER_NAME} mysql -u ${DB_USER} -p${DB_PASS} -t ${DB_NAME} < "${sql_path}"
}

# 2. Paso 0: Creación de BD y estructuras crudas
echo ""
echo "------------------------------------------------------------------------------"
echo "▶️  Fase 0: Creación de Base de Datos y Tablas Raw"
echo "------------------------------------------------------------------------------"
docker exec -i ${CONTAINER_NAME} mysql -u ${DB_USER} -p${DB_PASS} < "unidad_4/01_datos_crudos/01_creacion_bd.sql"

# 3. Ingesta de datos crudos
run_sql_file "Fase 1: Ingesta de Catálogo y Clientes Crudos" "unidad_4/01_datos_crudos/02_carga_datos_iniciales.sql"
run_sql_file "Fase 1: Ingesta de Pedidos Crudos (pedidos.sql)" "unidad_4/01_datos_crudos/pedidos.sql"

# 4. Paso 1: Perfilado de Datos
run_sql_file "Paso 1: Perfilado y Detección de Anomalías" "unidad_4/02_perfilado/01_perfilado_datos.sql"

# 5. Pasos 2 y 3: Staging y Normalización
run_sql_file "Pasos 2 y 3: Staging, Estandarización Estatal y Tipado de Fechas" "unidad_4/03_staging_y_normalizacion/02_staging_y_normalizacion.sql"

# 6. Paso 4: Validación y Aislamiento en Cuarentena
run_sql_file "Paso 4: Validación de Reglas de Negocio y Mesa de Rechazos" "unidad_4/04_validacion_y_rechazos/03_validacion_y_rechazos.sql"

# 7. Paso 5: Carga Incremental al Data Mart y Demostración de Idempotencia
run_sql_file "Paso 5: Carga Incremental (UPSERT) e Idempotencia" "unidad_4/05_carga_incremental/04_carga_incremental_upsert.sql"

# 8. Paso 6: Conciliación Cuantitativa y Balance de Masa
run_sql_file "Paso 6: Conciliación Cuantitativa y etl_auditoria" "unidad_4/06_conciliacion_auditoria/05_conciliacion_auditoria.sql"

# 9. Paso 7: Indicadores de Negocio
run_sql_file "Paso 7: Indicadores Analíticos de Ventas Netas y Pedidos Entregados" "unidad_4/07_indicadores/06_indicadores_negocio.sql"

echo ""
echo "=============================================================================="
echo "🎉 LABORATORIO ETL EJECUTADO CON ÉXITO Y 100% REPRODUCIBLE"
echo "=============================================================================="
