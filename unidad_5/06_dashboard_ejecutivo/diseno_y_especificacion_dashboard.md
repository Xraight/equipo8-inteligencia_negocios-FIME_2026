# 🖥️ Fase E · Diseño y Especificación del Dashboard Ejecutivo

## 🎯 Objetivo de la Fase
Diseñar y estructurar un **Dashboard Ejecutivo interactivo, claro y profesional** en la hoja `Dashboard` del libro de Excel `U5_Dashboard_Equipo08.xlsx`, utilizando tablas dinámicas conectadas al Modelo de Datos, tarjetas KPI, gráficos ejecutivos y segmentadores sincronizados.

---

## 📐 Maquetación y Distribución Visual (Layout)

```text
+---------------------------------------------------------------------------------------------------+
|  📊 EMPRESA COMERCIAL · DASHBOARD EJECUTIVO DE VENTAS Y RENTABILIDAD (EQUIPO 8)                   |
|  Monitoreo Estratégico Multidimensional | Período Fiscal 2025 - 2026                              |
+---------------------------------------------------------------------------------------------------+
|  [FILTROS / SEGMENTADORES ACTIVOS]: [ Año: Todos ]  [ Región: Todas ]  [ Categoría: Todas ]       |
+----------------------------------+----------------------------------+------------------------------+
|  KPI 1: VENTAS TOTALES           |  KPI 2: MARGEN BRUTO             |  KPI 3: MARGEN %             |
|  $2,416,376.00                   |  $712,195.62                     |  29.5%                       |
|  1,200 Transacciones             |  Costo: $1,704,180.38            |  Ticket Prom: $2,013.65      |
+----------------------------------+----------------------------------+------------------------------+
|  VISTA 1: TENDENCIA MENSUAL (2025 vs 2026)                          |  VISTA 2: VENTAS POR REGIÓN  |
|  [Gráfico de Líneas / Columnas Agrupadas por Mes 1 a 12]            |  [Gráfico de Barras Horiz.]  |
|  - Comparativo YoY mes a mes                                        |  - Occidente ($677.4k)       |
|  - Detección de picos en Jul/Ago/Nov y valles en Jun/Sep            |  - Centro ($655.7k)          |
|                                                                     |  - Sur ($608.3k)             |
|                                                                     |  - Norte ($475.0k)           |
+---------------------------------------------------------------------+------------------------------+
|  VISTA 3: MIX POR CATEGORÍA                                         |  VISTA 4: TOP 5 PRODUCTOS    |
|  [Gráfico Circular / Columnas de Ventas y Margen]                   |  [Gráfico de Barras Rank]    |
|  - Tecnología: $889,916 (36.8%, Margen 30.1%)                       |  1. Producto 12 ($346.9k)    |
|  - Oficina: $801,265 (33.2%, Margen 28.6%)                          |  2. Producto 10 ($285.7k)    |
|  - Hogar: $725,195 (30.0%, Margen 29.6%)                           |  3. Producto 11 ($285.7k)    |
|                                                                     |  4. Producto 09 ($245.4k)    |
|                                                                     |  5. Producto 08 ($234.0k)    |
+---------------------------------------------------------------------+------------------------------+
|  TABLA DINÁMICA CONCILIADA Y CONEXIONES DE INFORME SINCRONIZADAS                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 🎛️ Componentes y Especificación Técnica

### 1. Fila de KPIs (Tarjetas Superiores)
- **Ventas Totales:** Medida `[Ventas]`. Formato: `$#,##0.00`. Muestra el volumen financiero total captado.
- **Margen Bruto:** Medida `[Margen Bruto]`. Formato: `$#,##0.00`. Indica la ganancia bruta antes de gastos administrativos y operativos.
- **Margen %:** Medida `[Margen %]`. Formato: `0.0%`. Mide la eficiencia de rentabilidad de la cartera.
- **Métricas Secundarias de Soporte:** Transacciones (`1,200`) y Ticket Promedio (`$2,013.65`).

### 2. Gráfico 1 · Ventas Mensuales y Comparativa YoY (2025 vs 2026)
- **Tipo:** Columnas agrupadas o líneas de tendencia.
- **Eje Horizontal (Categoría):** `DIM_TIEMPO[mes]` (Mes 1 al 12).
- **Series:** Año 2025 vs Año 2026.
- **Propósito:** Responder si las ventas aumentaron o cayeron en el mismo mes del año anterior.

### 3. Gráfico 2 · Ventas y Margen por Región
- **Tipo:** Barras horizontales ordenadas de mayor a menor.
- **Eje Vertical:** `DIM_CLIENTE[region]` (Occidente, Centro, Sur, Norte).
- **Valores:** Ventas totales y Margen Bruto.
- **Propósito:** Identificar la concentración de ingresos e individualizar el desempeño regional.

### 4. Gráfico 3 · Ventas y Participación por Categoría
- **Tipo:** Columnas con desglose de ventas y porcentaje de margen.
- **Eje:** `DIM_PRODUCTO[categoria]` (Tecnología, Oficina, Hogar).
- **Propósito:** Diagnosticar cuál categoría genera mayor retorno y cuál requiere optimización de costos.

### 5. Gráfico 4 · Top 5 Productos Estrella
- **Tipo:** Barras horizontales filtradas con los 5 productos con mayor monto de ventas.
- **Propósito:** Mostrar los productos que concentran el flujo de ingresos de la empresa.

---

## 🔗 Conexiones de Informe e Interactividad
- **Segmentadores Insertados:**
  1. `DIM_CLIENTE[region]` (Segmentador de Región).
  2. `DIM_PRODUCTO[categoria]` (Segmentador de Categoría).
  3. `DIM_TIEMPO[anio]` (Filtro / Segmentador de Año).
- **Configuración de Conexiones:** A través de `Segmentador de datos` → `Conexiones de informe`, cada segmentador está conectado a todas las tablas dinámicas subyacentes del dashboard. Al seleccionar una región (ej. Norte), los KPIs, el mix de categorías, la tendencia mensual y el ranking de productos se recalculan instantáneamente.
