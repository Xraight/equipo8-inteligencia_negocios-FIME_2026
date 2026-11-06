# Especificación de Diseño del Dashboard Ejecutivo en Excel
## Guía de Maquetación, Estructura Visual y Experiencia de Usuario

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Software:** Microsoft Excel 365
- **Función General:** Documentar el diseño de interfaz, maquetación, paleta de colores y componentes visuales del libro de trabajo analítico.
- **Función Específica:** Guiar la construcción del tablero ejecutivo interactivo para asegurar legibilidad gerencial, navegación fluida y jerarquía visual.

---

## 1. Identidad Visual y Paleta Corporativa

Para reflejar la seriedad académica de la FIME y la elegancia del sector de muebles finos de Casa&Estilo, se adoptó la siguiente paleta de diseño:

| Color | Hex | Uso en el Tablero |
| :--- | :---: | :--- |
| **Azul FIME / Deep Navy** | `#1A365D` | Encabezados principales, barras de navegación y tarjetas de KPI maestras. |
| **Dorado / Amber Gold** | `#D69E2E` | Acentos de métricas de margen, destacados y bordes activos. |
| **Gris Pizarra / Slate Grey** | `#2D3748` | Textos secundarios, etiquetas de ejes y cabeceras de tablas secundarias. |
| **Fondo Neutro Ejecutivo** | `#F7FAFC` | Fondo general de las hojas del tablero para evitar fatiga visual. |
| **Verde Éxito / SLA Ok** | `#38A169` | Indicador positivo en semaforización (márgenes >20%, SLA alcanzado). |
| **Rojo Alerta / Defecto** | `#E53E3E` | Indicador de riesgo crítico (SLA retrasado, devoluciones, roturas de stock). |

---

## 2. Estructura de Hojas del Libro de Trabajo

El libro corporativo `PIA_Dashboard_CasaEstilo_Equipo08.xlsx` se compone de las siguientes pestañas:

1. **`PORTADA`:**
   - Logotipos institucionales y tipografía ejecutiva.
   - Datos del equipo (Integrantes Equipo 8, Matrículas, Materia, Fecha: Noviembre 2026).
   - Menú de navegación rápida con hipervínculos a cada hoja del modelo.
2. **`DASHBOARD_EJECUTIVO`:**
   - **Banda de Filtros / Segmentadores:** Año, Mes, Canal, Categoría, Estado.
   - **Fila Superior de KPIs (Scorecard Gerencial):**
     - Tarjeta 1: Ventas Netas Globales (`$1,310.75M MXN`).
     - Tarjeta 2: Utilidad Bruta (`$280.87M MXN`).
     - Tarjeta 3: Margen Bruto Porcentual (`21.43%`).
     - Tarjeta 4: Ticket Promedio (`$9,362.47 MXN`).
     - Tarjeta 5: Cumplimiento SLA Instalaciones (`34.77%` - Alerta Crítica).
     - Tarjeta 6: Tasa de Devoluciones (`1.63%` - `$22.90M MXN`).
   - **Cuadrante 1:** Gráfico de Tendencia Histórica Mensual de Ventas Netas y Utilidad.
   - **Cuadrante 2:** Gráfico de Pareto de Categorías Comerciales (Recámara, Comedor, etc.).
   - **Cuadrante 3:** Distribución de Ingresos por Canal Omnicanal (Tienda 68%, Web 22%, App 10%).
   - **Cuadrante 4:** Matriz de Desempeño Regional de Sucursales (Venta por $m^2$).
3. **`ANALISIS_COMERCIAL`:**
   - Tablas dinámicas y desglose detallado de ventas brutas vs netas, descuentos otorgados y rentabilidad por marca y categoría.
4. **`OPERACIONES_Y_CALIDAD`:**
   - Diagnóstico profundo de logística de instalaciones (días promedio de retraso por tienda y correlación con satisfacción).
   - Análisis de devoluciones por motivo raíz (defecto, daño, expectativa).
   - Monitoreo de inventarios: catálogo de productos con alerta de reorden y rotura de stock.
5. **`DATA_MODEL` (Tablas Alimentadoras):**
   - Hojas con los datos exportados desde las vistas del Data Mart de MySQL para garantizar la portabilidad y actualización del libro sin dependencia de conexión remota externa.
6. **`DICCIONARIO_DAX`:**
   - Memoria técnica con las fórmulas, descripción y formato de cada medida analítica.
