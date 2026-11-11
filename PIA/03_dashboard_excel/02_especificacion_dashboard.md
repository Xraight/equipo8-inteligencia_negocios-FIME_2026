# Especificación de Diseño del Dashboard Ejecutivo en Excel (v2.0)
## Guía de Maquetación de 3 Vistas Ejecutivas, 5 Pilares y Segmentación Sincronizada

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Software:** Microsoft Excel 365 / Power Pivot (VertiPaq)
- **Archivos Generados:** `PIA_Dashboard_CasaEstilo_Equipo08.xlsx` y `PIA_Dashboard_CasaEstilo_Completo_v2.xlsx`
- **Función General:** Documentar el diseño visual, paleta corporativa, estructura de 3 pestañas ejecutivas y arquitectura tabular de los libros Excel de Casa&Estilo.
- **Función Específica:** Proveer al usuario y al Comité de Evaluación un plano claro para navegar o construir manualmente Tablas Dinámicas, Gráficos Dinámicos y Segmentadores sobre las 21 medidas DAX.

---

## 1. Identidad Visual y Paleta Corporativa

| Color | Hex | Uso en el Tablero |
| :--- | :---: | :--- |
| **Azul FIME / Deep Navy** | `#1A365D` | Encabezados principales, barras de título y tarjetas KPI financieras. |
| **Dorado / Amber Gold** | `#D69E2E` | Acentos de rentabilidad, filas de totales generales y KPIs comerciales. |
| **Gris Pizarra / Slate Grey** | `#2D3748` | Textos secundarios, ejes y cabeceras de soporte. |
| **Azul Medio / Accent Blue** | `#2B6CB0` | Series comparativas, clientes activos y gráficos de barras/columnas. |
| **Fondo Neutro Ejecutivo** | `#F7FAFC` | Sombreado alternado (zebra) y contraste suave sin fatiga visual. |
| **Verde Éxito** | `#2F855A` | Indicadores saludables (Utilidad Bruta, Óptimo en Inventario, CSAT meta). |
| **Rojo Alerta** | `#C53030` | Riesgos operativos (`SLA 36.91%`, `+3.41` días retraso, `126` roturas de stock). |

---

## 2. Arquitectura de 3 Vistas Ejecutivas (Scorecards + 10 Gráficos Nativos)

El libro se organiza en **3 pestañas gerenciales**, complementadas por `PORTADA`, `GUIA_POWERPIVOT`, `DICCIONARIO_DAX` (21 medidas) y las **10 hojas dimensionales/hechos en formato `ListObject`**:

### Vista 1: `DASHBOARD_EJECUTIVO` (Visión C-Level)
- **Scorecard Superior (6 Tarjetas KPI):**
  1. `Ventas Netas`: `$1,310,746,491.89`
  2. `Utilidad Bruta`: `$280,874,853.71`
  3. `Margen Bruto %`: `21.43%`
  4. `Crecimiento YoY (2025 vs 2024)`: `+0.86%` (`$479.81M` vs `$475.74M`)
  5. `Ticket Promedio`: `$9,362.47` (`140,000` tickets)
  6. `Cumplimiento SLA`: `36.91%` (*Alerta Crítica: 63.09% con retraso*)
- **Tablas y Gráficos (4 Visuales):**
  - Desempeño Comercial por Categoría (`Recámara`, `Comedor`, `Exterior`, `Oficina`, `Iluminación`, `Sala`, `Decoración`) + Gráfico de Columnas Agrupadas.
  - Desempeño Omnicanal (`Tienda 68.0%`, `Web 22.1%`, `App 9.8%`) + Gráfico de Anillo.
  - Mix de Métodos de Pago (`Tarjeta`, `Efectivo`, `Transferencia`, `Wallet`) + Gráfico de Anillo.
  - Evolución Histórica Mensual (`33 meses: 2024-01 a 2026-09`) + Resumen Anual (`2024`, `2025`, `2026`) + Gráfico de Líneas de Tendencia.

### Vista 2: `COMERCIAL_Y_CLIENTES` (Productividad de Tiendas, Promociones y CRM)
- **Scorecard Comercial (5 Tarjetas KPI):**
  1. `Total Tickets`: `140,000`
  2. `Unidades Vendidas`: `831,382`
  3. `Unidades por Ticket (UPT)`: `5.94`
  4. `Clientes Activos`: `10,800`
  5. `Tasa Descuento Promedio`: `6.54%` (`$91.76M`)
- **Tablas y Gráficos (3 Visuales):**
  - Ranking de las 16 Sucursales Físicas (`Venta Neta`, `Venta/m²`, `Margen %`) + Gráfico Horizontal de Ranking + Gráfico de Columnas `$/m²`.
  - Segmentación CRM (`Frecuente $590.9M`, `Nuevo $327.7M`, `Inactivo $245.1M`, `Premium $147.1M`) + Gráfico de Barras por Segmento.
  - Matriz de Descuentos vs Margen por Categoría + Top 15 Productos Líderes en Venta Neta.

### Vista 3: `OPERACIONES_Y_STOCK` (Calidad, Logística e Inventario)
- **Scorecard Operacional (6 Tarjetas KPI):**
  1. `Monto Devuelto`: `$22,897,836.87` (`9,952` eventos)
  2. `Tasa de Devolución`: `1.63%`
  3. `Cumplimiento SLA`: `36.91%` (`2,399 / 6,500`)
  4. `Retraso Promedio`: `+3.41 días` (`10.93` vs `7.52` pactados)
  5. `Satisfacción CSAT`: `2.99 / 5.0`
  6. `Valor Inventario / Roturas`: `$2,373.72M` (`126` roturas / `2,738 u.` déficit)
- **Tablas y Gráficos (3 Visuales):**
  - Causas Raíz de Devoluciones (5 motivos completos sobre 9,952 eventos) + Gráfico de Anillo.
  - SLA de Instalaciones por Sucursal + Gráfico de Columnas `% Cumplimiento SLA`.
  - Salud de Inventario por Estatus y Categoría (*Óptimo vs Alerta Reorden vs Rotura Stock*) + Gráfico de Barras Apiladas de Riesgo de Abasto (`Roturas` + `Alertas`) por Categoría.

---

## 3. Hojas del Modelo Tabular y Memoria Técnica

| Pestaña | Nombre `ListObject` | Fuente CSV / Granularidad | Filas |
| :--- | :--- | :--- | :---: |
| `FACT_VENTAS_MODELO` | `TablaFactVentas` | `fact_ventas_detalle.csv` (Atómica línea de ticket 2024–2026) | `331,758` |
| `FACT_DEVOLUCIONES` | `TablaFactDevoluciones` | `fact_devoluciones_completo.csv` (Universo completo) | `9,952` |
| `FACT_INSTALACIONES` | `TablaFactInstalaciones` | `fact_instalaciones_completo.csv` | `6,500` |
| `FACT_INVENTARIO` | `TablaFactInventario` | `fact_inventario_snapshot.csv` | `21,440` |
| `DIM_TIEMPO` | `TablaDimTiempo` | `dim_tiempo.csv` (Calendario 2024-01-01 a 2026-12-31) | `1,096` |
| `DIM_PRODUCTO` | `TablaDimProducto` | `dim_producto.csv` | `1,341` |
| `DIM_SUCURSAL` | `TablaDimSucursal` | `dim_sucursal.csv` | `17` |
| `DIM_CANAL` | `TablaDimCanal` | `dim_canal.csv` | `3` |
| `DIM_CLIENTE` | `TablaDimCliente` | `dim_cliente.csv` | `10,801` |
| `DIM_METODO_PAGO` | `TablaDimMetodoPago` | `dim_metodo_pago.csv` | `4` |
| `DICCIONARIO_DAX` | — | Memoria de las 21 medidas DAX oficiales | `21` |
