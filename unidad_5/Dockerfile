# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 (EQUIPO 8)
# DOCKERFILE: ENTORNO REPRODUCIBLE DE VALIDACIÓN Y GENERACIÓN DE ENTREGABLES
# ==============================================================================
FROM python:3.12-slim

WORKDIR /workspace

# Instalación de librerías de analítica y generación de artefactos
RUN pip install --no-cache-dir \
    openpyxl==3.1.5 \
    python-pptx==1.0.2 \
    reportlab==5.1.0 \
    matplotlib==3.11.2 \
    pandas==3.1.0

CMD ["python3", "unidad_5/scripts_generacion/validar_datos.py"]
