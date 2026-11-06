#!/usr/bin/env bash
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 (EQUIPO 8)
# SCRIPT: INICIAR BI LIVE STUDIO (DASHBOARD WEB EN TIEMPO REAL EN DOCKER)
# PUERTO: http://localhost:8085
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

IMAGE_NAME="equipo8-u5-generator:latest"
PORT="8085"

echo "=============================================================================="
echo "🚀 INICIANDO SERVIDOR EN VIVO DE UNIDAD 5 (BI LIVE STUDIO) EN DOCKER"
echo "=============================================================================="

# 1. Verificar o construir imagen Docker
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "📦 Construyendo imagen Docker: ${IMAGE_NAME}..."
    docker build -t "${IMAGE_NAME}" -f unidad_5/Dockerfile .
fi

echo "✅ Imagen lista. Iniciando servidor en puerto ${PORT}..."
echo "------------------------------------------------------------------------------"
echo "🌐 PANEL DE CONTROL EN TIEMPO REAL:  http://localhost:${PORT}"
echo "------------------------------------------------------------------------------"
echo "Para detener el servidor presiona Ctrl + C"
echo ""

docker run --rm -it \
    -p "${PORT}:${PORT}" \
    -e PORT="${PORT}" \
    -v "${REPO_ROOT}:/workspace" \
    -w /workspace \
    "${IMAGE_NAME}" \
    python3 unidad_5/scripts_generacion/servidor_en_vivo.py
