#!/usr/bin/env bash
# ==============================================================================
# PIPELINE CI/CD LOCAL & AUTOMATIZADO: VALIDACIÓN DE PRESENTACIÓN EN DOCKER
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "========================================================================"
echo "🚀 [CI/CD] INICIANDO VALIDACIÓN DE PRESENTACIÓN HACKWITHINFY"
echo "========================================================================"

# 1. Verificar existencia de artefactos requeridos
echo "🔍 1. Verificando estructura de archivos..."
test -f "generar_presentacion_pptx.py" || { echo "❌ Falta generar_presentacion_pptx.py"; exit 1; }
test -f "presentacion_interactiva.html" || { echo "❌ Falta presentacion_interactiva.html"; exit 1; }
test -f "SLIDES_DOCUMENTATION.md" || { echo "❌ Falta SLIDES_DOCUMENTATION.md"; exit 1; }
echo "   ✅ Archivos fuente verificados correctamente."

# 2. Ejecutar generación de PPTX dentro del contenedor Docker
echo "🐳 2. Ejecutando generador PPTX en contenedor Docker aislado..."
docker run --rm \
  -v "${SCRIPT_DIR}":/workspace \
  -w /workspace \
  localhost/equipo8-u5-generator \
  python3 generar_presentacion_pptx.py

# 3. Validar integridad del archivo binario .pptx
echo "📊 3. Validando integridad de presentacion_hackwithinfy_butzmann.pptx..."
if [ ! -s "presentacion_hackwithinfy_butzmann.pptx" ]; then
  echo "❌ El archivo presentacion_hackwithinfy_butzmann.pptx está vacío o no fue generado."
  exit 1
fi

FILE_SIZE=$(wc -c < "presentacion_hackwithinfy_butzmann.pptx")
if [ "${FILE_SIZE}" -lt 20000 ]; then
  echo "❌ El tamaño del archivo PPTX (${FILE_SIZE} bytes) es anormalmente bajo."
  exit 1
fi
echo "   ✅ Archivo PPTX válido (${FILE_SIZE} bytes)."

# 4. Validar contenido HTML interactivo
echo "🌐 4. Validando visor interactivo HTML..."
grep -q "Sergio Jaziel Butzmann Martínez" presentacion_interactiva.html || { echo "❌ Falta nombre en HTML"; exit 1; }
grep -q "HackWithInfy México" presentacion_interactiva.html || { echo "❌ Falta referencia HackWithInfy"; exit 1; }
grep -q "slide-1" presentacion_interactiva.html || { echo "❌ Falta slide-1"; exit 1; }
grep -q "slide-2" presentacion_interactiva.html || { echo "❌ Falta slide-2"; exit 1; }
grep -q "slide-3" presentacion_interactiva.html || { echo "❌ Falta slide-3"; exit 1; }
echo "   ✅ Visor interactivo HTML verificado exitosamente."

echo "========================================================================"
echo "🎉 [CI/CD] TODOS LOS CHECKS PASARON EXITOSAMENTE (100% DOCKERIZADO)"
echo "========================================================================"
