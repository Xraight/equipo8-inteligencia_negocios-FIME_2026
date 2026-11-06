#!/usr/bin/env bash
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 (EQUIPO 8)
# DEMOSTRACIÓN EN TIEMPO REAL PARA EL SALÓN DE CLASES (RUNNER EN TERMINAL)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

IMAGE_NAME="equipo8-u5-generator:latest"

# 1. Asegurar imagen Docker
if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "Construyendo imagen Docker..."
    docker build -t "${IMAGE_NAME}" -f unidad_5/Dockerfile .
fi

# 2. Ejecutar la demostración interactiva
docker run --rm \
    -v "${REPO_ROOT}:/workspace" \
    -w /workspace \
    "${IMAGE_NAME}" \
    python3 unidad_5/scripts_generacion/demo_terminal_interactiva.py
