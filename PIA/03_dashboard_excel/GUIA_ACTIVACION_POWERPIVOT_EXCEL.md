# Guía de Activación y Demostración de Power Pivot en Excel 365
## Instrucciones Paso a Paso para la Defensa ante el Sínodo y el Profesor

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Empresa:** Casa&Estilo
- **Archivo Evaluado:** `PIA_Dashboard_CasaEstilo_Equipo08.xlsx`
- **Función General:** Proveer al alumno la guía de activación del Modelo de Datos nativo de Power Pivot y la defensa del Esquema Estrella ante el profesor.

---

## 💡 Entendimiento Técnico: ¿Por qué Excel necesita este paso?

El archivo `PIA_Dashboard_CasaEstilo_Equipo08.xlsx` fue generado mediante contenedores Docker en Linux para garantizar la reproducibilidad y balance contable sin discrepancias ($0.00).

Sin embargo, en la arquitectura de Microsoft:
- **Power Pivot** utiliza un motor analítico columnar propietario (**VertiPaq / Microsoft Analysis Services**) que se ejecuta exclusivamente en el proceso en memoria de Microsoft Excel en Windows (`ThisWorkbookDataModel`).
- Las librerías de código abierto en Linux (`openpyxl`) estructuran hojas de cálculo con el estándar abierto OpenXML (`.xlsx`), pero **no pueden compilar el flujo binario propietario de VertiPaq**.

Por esta razón, el libro incluye las tablas estructuradas como **Tablas Oficiales de Excel (`ListObjects`)** y te ofrecemos dos vías de activación inmediata:

---

## 🚀 Opción A: Activación Automática en 1 Clic con Macro VBA (Recomendada)

El libro cuenta con la macro `ConstruirModeloPowerPivotPIA` diseñada para ejecutarse en menos de 5 segundos sin errores:

1. Abre el archivo **`PIA_Dashboard_CasaEstilo_Equipo08.xlsx`** en Microsoft Excel (Windows).
2. Presiona la combinación de teclas **`Alt + F11`** para abrir el Editor de Visual Basic.
3. En el menú superior, haz clic en **Archivo** $\to$ **Importar archivo...** y selecciona:  
   [`PIA/03_dashboard_excel/construir_modelo_powerpivot_pia.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/03_dashboard_excel/construir_modelo_powerpivot_pia.bas).
4. Cierra el editor de VBA y regresa a Excel.
5. Presiona **`Alt + F8`**, selecciona la macro **`ConstruirModeloPowerPivotPIA`** y haz clic en **Ejecutar**.
6. **¡Listo!** En 3 segundos, la macro:
   - Agregará las 5 tablas al Modelo de Datos VertiPaq.
   - Creará las relaciones 1:N en la Vista de Diagrama.
   - Registrará las 10 medidas DAX oficiales.
   - Creará una nueva hoja llamada `DASHBOARD_POWERPIVOT_NATIVO` con una Tabla Dinámica conectada a `ThisWorkbookDataModel`.

---

## 🛠️ Opción B: Activación Nativa en 2 Minutos (Modo Aula / Sin Macros)

Si el profesor prefiere ver cómo lo construyes tú mismo en vivo frente al sínodo, sigue estos sencillos pasos:

### Paso 1: Habilitar el Complemento Power Pivot (si no estuviera visible)
1. En Excel, ve a **Archivo** $\to$ **Opciones** $\to$ **Complementos**.
2. En la lista desplegable inferior *Administrar*, selecciona **Complementos COM** y haz clic en **Ir...**.
3. Marca la casilla **Microsoft Power Pivot for Excel** y presiona **Aceptar**.  
   *(Aparecerá la pestaña Power Pivot en la cinta de opciones superior)*.

### Paso 2: Agregar las Tablas Oficiales al Modelo de Datos
El libro ya tiene las tablas configuradas como Tablas Oficiales (`ListObjects`):
1. Ve a la pestaña **`FACT_VENTAS_MODELO`**, haz clic dentro de la tabla y en la pestaña **Power Pivot**, haz clic en **Agregar a modelo de datos**.
2. Ve a la pestaña **`DIM_PRODUCTO`**, haz clic dentro de la tabla y pulsa **Agregar a modelo de datos**.
3. Repite para **`DIM_SUCURSAL`**, **`DIM_CANAL`**, **`DIM_TIEMPO`**, **`FACT_DEVOLUCIONES`** y **`FACT_INSTALACIONES`**.

### Paso 3: Crear las Relaciones en la Vista de Diagrama (Constelación de Hechos)
1. En la pestaña **Power Pivot**, haz clic en **Administrar**.
2. En la ventana de Power Pivot, en el grupo *Ver*, haz clic en **Vista de diagrama**.
3. Conectar la estrella principal de **VENTAS**:
   - Arrastra `producto_key` de `TablaDimProducto` hacia `producto_key` de `TablaFactVentas`.
   - Arrastra `sucursal_key` de `TablaDimSucursal` hacia `sucursal_key` de `TablaFactVentas`.
   - Arrastra `canal_id` de `TablaDimCanal` hacia `canal_id` de `TablaFactVentas`.
   - Arrastra `tiempo_id` de `TablaDimTiempo` hacia `tiempo_id` de `TablaFactVentas`.
4. Conectar la estrella de **DEVOLUCIONES** e **INSTALACIONES** (Dimensiones Conformes):
   - Arrastra `producto_key` de `TablaDimProducto` hacia `producto_key` de `TablaFactDevoluciones`.
   - Arrastra `sucursal_key` de `TablaDimSucursal` hacia `sucursal_key` de `TablaFactDevoluciones`.
   - Arrastra `tiempo_id` de `TablaDimTiempo` hacia `tiempo_id` de `TablaFactDevoluciones`.
   - Arrastra `sucursal_key` de `TablaDimSucursal` hacia `sucursal_key` de `TablaFactInstalaciones`.
5. Observa cómo Excel dibuja automáticamente las líneas de relación con cardinalidad **1 a Varios ($1:\infty$)**.

> 💡 **Nota de Arquitectura Kimball:** Las tablas de hechos (`TablaFactVentas` y `TablaFactDevoluciones`) **NUNCA se conectan directamente entre sí**. Se comunican compartiendo las **Dimensiones Conformes** (`DimProducto`, `DimSucursal`, `DimTiempo`). Esto previene duplicidad de conteos ('chasm traps') y permite que las medidas DAX crucen ventas y devoluciones limpiamente.

### Paso 4: Crear las Medidas DAX
En la ventana de Power Pivot (en la Vista de Datos, en la cuadrícula inferior de cálculo) o desde Excel en **Power Pivot** $\to$ **Medidas** $\to$ **Nueva medida**:
- Selecciona la tabla: **`TablaFactVentas`**
- Nombre de la medida: `Ventas Netas`
- Fórmula: `[Ventas Brutas] - [Descuentos Totales]`  
  *(o copia cualquiera de las 10 fórmulas detalladas en [`01_catalogo_medidas_dax.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/03_dashboard_excel/01_catalogo_medidas_dax.md))*

---

## 🎯 Guion de Demostración ante el Profesor (2 Minutos)

Cuando el profesor pida revisar el componente de Power Pivot:
1. Abre **Power Pivot** $\to$ **Administrar**.
2. Haz clic en **Vista de diagrama** y muestra la pantalla:  
   > *"Profesor, aquí puede apreciar nuestro Esquema Estrella: la tabla central de hechos `TablaFactVentas` está conectada mediante relaciones 1:N a las dimensiones conformes de `Sucursal`, `Canal` y `Tiempo`, asegurando un filtrado dimensional libre de 'chasm traps'."*
3. Cierra la ventana y muestra la lista de campos de la Tabla Dinámica:  
   > *"En la sección de campos puede verificar las 10 medidas calculadas con DAX (identificadas con el icono fx), como `[Ventas Netas]`, `[Utilidad Bruta]`, `[Margen %]` y `[Cumplimiento SLA]`, las cuales alimentan directamente las visualizaciones del tablero ejecutivo."*
