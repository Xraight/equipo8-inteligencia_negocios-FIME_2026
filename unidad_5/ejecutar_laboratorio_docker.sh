#!/usr/bin/env bash
# ==============================================================================
# PROYECTO: LABORATORIO GUIADO · UNIDAD 5 (DEL DATA MART AL DASHBOARD EJECUTIVO)
# RUNNER AUTOMATIZADO DE VALIDACIÓN Y GENERACIÓN EN DOCKER
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

set -e

# Resolución dinámica del entorno (portabilidad desde raíz o desde unidad_5)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

IMAGE_NAME="equipo8-u5-generator:latest"

echo "=============================================================================="
echo "🚀 INICIANDO PIPELINE AUTOMATIZADO · LABORATORIO UNIDAD 5 (EQUIPO 8)"
echo "=============================================================================="

# 1. Asegurar que la imagen Docker esté construida
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "📦 Construyendo imagen Docker local: ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" -f unidad_5/Dockerfile .
fi

echo "✅ Imagen Docker lista: ${IMAGE_NAME}"

# Función auxiliar para ejecutar scripts dentro de Docker
run_in_docker() {
    local script_name="$1"
    local desc="$2"
    echo ""
    echo "------------------------------------------------------------------------------"
    echo "▶️  ${desc} (${script_name})"
    echo "------------------------------------------------------------------------------"
    docker run --rm \
        -v "${REPO_ROOT}:/workspace" \
        -w /workspace \
        "${IMAGE_NAME}" \
        python3 "${script_name}"
}

# 2. Paso 1: Validación y Conciliación de Datos contra Cifras de Control
run_in_docker "unidad_5/scripts_generacion/validar_datos.py" "Fase D: Validación Numérica y Cifras de Control"

# 3. Paso 2: Generación del Dashboard Ejecutivo en Excel (XLSX)
run_in_docker "unidad_5/scripts_generacion/generar_dashboard_excel.py" "Fase E: Construcción de U5_Dashboard_Equipo08.xlsx"

# 4. Paso 3: Generación de la Presentación Ejecutiva para Comité Directivo (PPTX)
run_in_docker "unidad_5/scripts_generacion/generar_presentacion_pptx.py" "Fase G: Construcción de U5_Comite_Equipo08.pptx (7 Slides)"

# 5. Paso 4: Generación del Reporte Formal de Evidencias (PDF)
run_in_docker "unidad_5/scripts_generacion/generar_reporte_pdf.py" "Fases A-G: Construcción de U5_Evidencias_Equipo08.pdf"

echo ""
echo "=============================================================================="
echo "🎉 LABORATORIO UNIDAD 5 EJECUTADO CON ÉXITO Y 100% REPRODUCIBLE EN DOCKER"
echo "=============================================================================="
echo "📁 ENTREGABLES GENERADOS EN unidad_5/:"
ls -lh unidad_5/U5_Dashboard_Equipo08.xlsx unidad_5/U5_Comite_Equipo08.pptx unidad_5/U5_Evidencias_Equipo08.pdf
echo "=============================================================================="
