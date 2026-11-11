# Guía Completa de Construcción y Activación en Power Pivot (Excel 365)
## Modelo Constelación (10 Tablas), 21 Medidas DAX y Dashboard de 3 Vistas

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Empresa:** Casa&Estilo
- **Libros Compatibles:** `PIA_Dashboard_CasaEstilo_Equipo08.xlsx` y `PIA_Dashboard_CasaEstilo_Completo_v2.xlsx`
- **Función General:** Guiar paso a paso la carga del modelo tabular completo (10 tablas: 4 hechos + 6 dimensiones conformes), el registro de las 21 medidas DAX y el ensamblaje manual de un Dashboard Ejecutivo sincronizado en 3 pestañas.

---

## 1. Arquitectura de Datos: ¿Qué Tablas Cargar?

Puedes cargar los datos de **dos formas equivalentes** (ambas producen exactamente las mismas cifras oficiales de MySQL `ce_bi` sin distorsión temporal ni truncamientos):

1. **Vía Rápida (desde las hojas del propio libro `.xlsx`):** Cada hoja ya contiene su `ListObject` oficial (`TablaFactVentas` con las 331,758 líneas atómicas, `TablaFactDevoluciones` con 9,952 devoluciones, `TablaFactInstalaciones` con 6,500 órdenes, `TablaFactInventario` con 21,440 combinaciones y las 6 dimensiones). Solo haz clic dentro de cada tabla $\to$ pestaña **Power Pivot** $\to$ **Agregar a modelo de datos**.
2. **Vía Externa (desde CSV en `datos_exportados/` con Power Query):** Ve a **Datos** $\to$ **Obtener datos** $\to$ **De un archivo** $\to$ **De texto/CSV**, usa codificación **UTF-8** y configura **Cerrar y cargar en...** $\to$ marca **"Crear únicamente conexión"** y **"Agregar estos datos al Modelo de datos"**.

---

## 2. Relaciones en Vista de Diagrama (Constelación de Hechos Kimball)

En **Power Pivot $\to$ Administrar $\to$ Vista de diagrama**, acomoda las **6 dimensiones arriba** y las **4 tablas de hechos abajo**, y traza estas **15 relaciones ($1:\infty$)** arrastrando siempre de la **Dimensión** hacia la **Fact**:

### Estrella 1: Ventas (`TablaFactVentas` — 331,758 filas)
- `TablaDimTiempo[tiempo_id]` $\to$ `TablaFactVentas[tiempo_id]`
- `TablaDimProducto[producto_key]` $\to$ `TablaFactVentas[producto_key]`
- `TablaDimSucursal[sucursal_key]` $\to$ `TablaFactVentas[sucursal_key]`
- `TablaDimCanal[canal_id]` $\to$ `TablaFactVentas[canal_id]`
- `TablaDimCliente[cliente_key]` $\to$ `TablaFactVentas[cliente_key]`
- `TablaDimMetodoPago[metodo_pago_id]` $\to$ `TablaFactVentas[metodo_pago_id]`

### Estrella 2: Devoluciones (`TablaFactDevoluciones` — 9,952 filas)
- `TablaDimTiempo[tiempo_id]` $\to$ `TablaFactDevoluciones[tiempo_id]`
- `TablaDimProducto[producto_key]` $\to$ `TablaFactDevoluciones[producto_key]`
- `TablaDimSucursal[sucursal_key]` $\to$ `TablaFactDevoluciones[sucursal_key]`
- `TablaDimCliente[cliente_key]` $\to$ `TablaFactDevoluciones[cliente_key]`

### Estrella 3: Instalaciones (`TablaFactInstalaciones` — 6,500 filas)
- `TablaDimTiempo[tiempo_id]` $\to$ `TablaFactInstalaciones[tiempo_id]`
- `TablaDimSucursal[sucursal_key]` $\to$ `TablaFactInstalaciones[sucursal_key]`
- `TablaDimCliente[cliente_key]` $\to$ `TablaFactInstalaciones[cliente_key]`

### Estrella 4: Inventario (`TablaFactInventario` — 21,440 filas)
- `TablaDimSucursal[sucursal_key]` $\to$ `TablaFactInventario[sucursal_key]`
- `TablaDimProducto[producto_key]` $\to$ `TablaFactInventario[producto_key]`

> ⚠️ **Paso obligatorio para Time Intelligence (`SAMEPERIODLASTYEAR`):** En Vista de Datos de Power Pivot, selecciona `TablaDimTiempo` $\to$ pestaña **Diseño** $\to$ **Marcar como tabla de fechas** $\to$ elige la columna `fecha`.

---

## 3. Las 21 Medidas DAX a Crear (Copiar y Pegar)

Desde **Power Pivot $\to$ Medidas $\to$ Nueva medida**, crea las 21 medidas documentadas en [`01_catalogo_medidas_dax.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/03_dashboard_excel/01_catalogo_medidas_dax.md):

- **Pilar Financiero:** `Ventas Brutas` (`$1,402.50M`), `Descuentos Totales` (`$91.76M`), `Ventas Netas` (`$1,310.75M`), `Costo de Ventas (COGS)` (`$1,029.87M`), `Utilidad Bruta` (`$280.87M`), `Margen Bruto %` (`21.43%`), `Tasa de Descuento %` (`6.54%`), `Ventas Netas LY` y `Crecimiento YoY %` (`+0.86%`).
- **Pilar Comercial:** `Total Tickets` (`140,000`), `Unidades Vendidas` (`831,382`), `Ticket Promedio` (`$9,362.47`), `Unidades por Ticket (UPT)` (`5.94`), `Venta por m2` (`$58,226.93`), `Clientes Activos` (`10,800`).
- **Pilar Calidad:** `Monto Devuelto` (`$22.90M`), `Tasa de Devolucion %` (`1.63%`).
- **Pilar Logística:** `Cumplimiento SLA %` (`36.91%`), `Dias Promedio Retraso` (`+3.41`), `Satisfaccion CSAT` (`2.99`).
- **Pilar Inventario:** `Valor Inventario (Costo)` (`$2,373.72M`), `SKUs en Rotura Stock` (`126`).

---

## 4. Armado Manual del Dashboard en 3 Vistas Sincronizadas

1. Crea una hoja auxiliar oculta llamada `AUX_DINAMICAS` donde coloques las **Tablas Dinámicas** del Modelo de Datos (una TD por gráfico y una TD de 1 fila para tarjetas KPI).
2. En tus 3 hojas visuales (`DASHBOARD_EJECUTIVO`, `COMERCIAL_Y_CLIENTES`, `OPERACIONES_Y_STOCK`):
   - **Tarjetas KPI:** Inserta rectángulos redondeados y en la barra de fórmulas apunta al valor de la TD en `AUX_DINAMICAS` (ej. `=AUX_DINAMICAS!$B$4`).
   - **Gráficos Dinámicos:** Inserta el gráfico desde cada TD (`Insertar -> Gráfico`), quita los botones de campo grises (*Analizar gráfico dinámico -> Botones de campo -> Ocultar todos*) y córtalo/pégalo en tu hoja visual.
   - **Segmentadores (Slicers):** En una TD $\to$ *Insertar segmentación de datos* para `TablaDimTiempo[anio]`, `TablaDimTiempo[trimestre_nombre]`, `TablaDimCanal[canal_nombre]`, `TablaDimSucursal[ciudad]`, `TablaDimProducto[categoria]` y `TablaDimCliente[segmento]`.
   - **Sincronización Total:** Clic derecho en cada segmentador $\to$ **Conexiones de informes...** $\to$ marca **TODAS las Tablas Dinámicas** del libro. Con eso, un solo clic filtra simultáneamente ventas, utilidad, clientes, devoluciones, SLA e inventario en todas las pestañas.
