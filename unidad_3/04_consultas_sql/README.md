# 04 - Consultas SQL Analíticas

## 🎯 Objetivo General
Almacenar y documentar las consultas analíticas en lenguaje SQL diseñadas para responder a las preguntas de negocio clave planteadas para el Data Mart de Casa&Estilo.

## 📌 Función Específica
- Implementar consultas de agregación multidimensional (ventas por dimensión tiempo, showroom, categoría de producto, asesor, etc.).
- Utilizar funciones de ventana (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `SUM OVER`), cláusulas analíticas (`ROLLUP`, `CUBE`, `GROUPING SETS`) y filtros de rendimiento.
- Proveer la respuesta cuantitativa a los objetivos del negocio: margen bruto, cumplimiento de entregas, comisiones de asesores y rendimiento de showrooms.

## 📦 Estructura Sugerida
- `01_kpis_ventas_tiempo.sql`: Consultas históricas por año, trimestre, mes.
- `02_rendimiento_showrooms_asesores.sql`: Métricas de venta por asesor y showroom.
- `03_cumplimiento_entregas_logistica.sql`: Tiempos de entrega y estatus por zona/ciudad.
- `04_analisis_productos_categorias.sql`: Top productos y categorías más rentables.
