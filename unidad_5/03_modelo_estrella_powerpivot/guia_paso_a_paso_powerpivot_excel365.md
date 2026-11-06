# 📘 Guía Maestra: Construcción y Verificación Nativa de Power Pivot en Excel 365

> **Laboratorio Guiado · Unidad 5: Del Data Mart al Dashboard Ejecutivo y al Comité Directivo**  
> **Equipo 8:** Arely Carrillo Sustaita, Rafael Jesús Collazo Hernández, Sergio Jaziel Butzmann Martinez  
> **Institución:** Facultad de Ingeniería Mecánica y Eléctrica (FIME · UANL 2026)

---

## 🧭 1. Entendiendo la Diferencia Técnica: ¿Por qué el Excel generado en Linux no muestra Power Pivot?

Cuando abres el archivo generado automáticamente por Python (`U5_Dashboard_Equipo08.xlsx`) en Excel:
- Ves hojas de cálculo formateadas, números exactos, fórmulas como `=SUM(...)` y gráficos estáticos.
- Sin embargo, al ir a la pestaña **Power Pivot** → **Administrar**, el modelo aparece vacío o sin tablas.

### ¿Por qué ocurre esto?
1. **Power Pivot no es una simple hoja de Excel:** Power Pivot es un motor de base de datos analítica en memoria de nivel empresarial (**Microsoft Analysis Services VertiPaq**). Este motor compila y almacena los datos en un formato binario propietario (`xl/model/item.data`).
2. **Limitación de librerías en Linux/Python:** Las librerías de código abierto como `openpyxl` en Linux sólo pueden escribir etiquetas XML estándar de hojas de cálculo (`.xlsx`). Ninguna librería de software libre en Linux puede compilar el motor binario VertiPaq ni generar los paquetes propietarios `DataMashup` de Power Query.
3. **El propósito del archivo Python:** El archivo generado por Docker/Python sirve para **validar al 100% las cifras de control y la matemática del negocio** en el flujo de CI/CD automatizado.
4. **La exigencia del laboratorio:** Para la entrega académica y la demostración ante el profesor, debes contar con el modelo nativo en **Excel 365 de escritorio (Windows)**.

---

## ⚡ 2. Las Dos Vías de Solución

Tienes **dos opciones inmediatas** para tener tu Modelo de Datos al 100%:
* **Opción A (Ultra-rápida · 1 Clic con Macro VBA):** Si quieres que Excel haga todo solo en 5 segundos.
* **Opción B (Manual Nativa · 2 Minutos):** Si el profesor te pide hacerlo paso a paso en el pizarrón o proyector.

---

## 🚀 Opción A: Automatización de 1 Clic mediante Macro VBA

Hemos preparado el archivo [`construir_modelo_powerpivot.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas) que invoca las APIs nativas de Excel en Windows:

1. Abre un libro nuevo en blanco en **Excel 365 (Windows)**.
2. Guárdalo como libro habilitado para macros: `U5_Dashboard_Equipo08.xlsm` dentro de la carpeta `unidad_5` (donde está la subcarpeta `01_datos_crudos`).
3. Presiona la combinación de teclas: `ALT + F11` para abrir el editor de Visual Basic.
4. En el menú superior: haz clic en **Archivo** → **Importar archivo...** y selecciona:  
   `unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas`.  
   *(O bien: haz clic en Insertar → Módulo y pega todo el contenido del archivo .bas).*
5. Pon el cursor dentro del código de la macro `ConstruirModeloPowerPivotCompleto` y presiona `F5` (o botón Ejecutar ▶️).
6. **¡Listo!** En 5 segundos, la macro:
   - Importará los 4 CSVs mediante Power Query.
   - Creará las conexiones al Modelo de Datos.
   - Establecerá las 3 relaciones 1:N en el Esquema Estrella.
   - Registrará las 6 medidas DAX oficiales formateadas.
   - Insertará una hoja `Dashboard_PowerPivot` con una Tabla Dinámica conectada a `ThisWorkbookDataModel`.

---

## 🛠️ Opción B: Construcción Manual en Vivo (Paso a Paso en 2 Minutos)

Esta es la forma estándar que el profesor evaluará si te pide realizarlo frente al salón de clases:

### Paso 1: Activar el complemento Power Pivot (Sólo se hace una vez)
1. En Excel: Ve a **Archivo** → **Opciones** → **Complementos**.
2. En el desplegable inferior *Administrar*, selecciona **Complementos COM** y presiona **Ir...**
3. Marca la casilla **Microsoft Power Pivot for Excel** y haz clic en **Aceptar**.
4. Verás aparecer la pestaña **Power Pivot** en la cinta superior de Excel.

---

### Paso 2: Importar los 4 CSVs con Power Query al Modelo de Datos
1. En Excel: Ve a **Datos** → **Obtener datos** → **Desde un archivo** → **Desde texto/CSV**.
2. Selecciona `FACT_VENTAS.csv` (en `unidad_5/01_datos_crudos/`).
3. En la ventana emergente, verifica delimitador coma y codificación UTF-8. Haz clic en el botón **Transformar datos** (NO en Cargar).
4. En el editor de Power Query:
   - Confirma que la primera fila sean encabezados.
   - Verifica tipos: `id_venta`, `id_producto`, `id_cliente`, `id_tiempo`, `cantidad` como *Entero*; `monto` y `costo` como *Número decimal*.
5. **EL CLIC CRÍTICO:**
   - Haz clic en la flechita del botón **Cerrar y cargar** (esquina superior izquierda) → selecciona **Cerrar y cargar en...**
   - En la pequeña ventana que aparece:
     * Selecciona el botón de radio: **⚪ Solo crear conexión**.
     * Marca obligatoriamente la casilla: **☑️ Agregar estos datos al Modelo de datos**.
     * Haz clic en **Aceptar**.
6. **Repite exactamente lo mismo para las otras 3 tablas:**
   - `DIM_PRODUCTO.csv` (tipos: `id_producto` = Entero, `producto` = Texto, `categoria` = Texto).
   - `DIM_CLIENTE.csv` (tipos: `id_cliente` = Entero, `cliente` = Texto, `region` = Texto).
   - `DIM_TIEMPO.csv` (tipos: `id_tiempo` = Entero, `fecha` = Fecha, `anio` = Entero, `mes` = Entero).
   *En todas: Cerrar y cargar en... → Solo crear conexión + Agregar al Modelo de datos.*

> **Resultado visible:** En el panel lateral *Consultas y conexiones*, verás las 4 consultas con el texto *"1200 filas cargadas en el modelo de datos"*, *"12 filas..."*, etc.

---

### Paso 3: Configurar el Esquema Estrella en Vista de Diagrama
1. Haz clic en la pestaña **Power Pivot** → botón **Administrar** (se abrirá la ventana de Power Pivot).
2. En la pestaña Inicio de Power Pivot, haz clic en **Vista de diagrama** (icono de organigrama a la derecha).
3. Verás las 4 tablas flotando. Acomoda `FACT_VENTAS` en el centro y las tres `DIM_*` alrededor.
4. **Crea las 3 relaciones arrastrando con el ratón:**
   - Arrastra `id_producto` de `DIM_PRODUCTO` y suéltalo sobre `id_producto` de `FACT_VENTAS`.
   - Arrastra `id_cliente` de `DIM_CLIENTE` y suéltalo sobre `id_cliente` de `FACT_VENTAS`.
   - Arrastra `id_tiempo` de `DIM_TIEMPO` y suéltalo sobre `id_tiempo` de `FACT_VENTAS`.
5. Comprueba que las líneas muestren un **"1"** en el lado de la dimensión y un asterisco **"*"** en el lado de `FACT_VENTAS`.

```
        +------------------+
        |   DIM_PRODUCTO   |
        | [1] id_producto  |
        +--------+---------+
                 |
                 | (1:N)
                 v
        +--------+---------+          (1:N)         +-----------------+
        |   FACT_VENTAS    |<-----------------------|   DIM_CLIENTE   |
        | [*] id_producto  |                        | [1] id_cliente  |
        | [*] id_cliente   |                        +-----------------+
        | [*] id_tiempo    |
        +--------+---------+
                 ^
                 | (1:N)
                 |
        +--------+---------+
        |    DIM_TIEMPO    |
        | [1] id_tiempo    |
        +------------------+
```

---

### Paso 4: Dar de alta las 6 Medidas DAX Oficiales
1. En la misma ventana de Power Pivot, cambia a **Vista de datos** (botón junto a Vista de diagrama).
2. Selecciona abajo la pestaña de la tabla `FACT_VENTAS`.
3. Observa la división horizontal inferior: es el **Área de cálculo** (si no se ve, activa el botón *Área de cálculo* en la cinta Inicio).
4. Haz clic en una celda vacía del Área de cálculo y escribe en la barra de fórmulas superior una por una (puedes copiar y pegar):

```dax
Ventas:=SUM(FACT_VENTAS[monto])
```
*(Presiona Enter. Haz clic en el icono de Moneda `$` en la cinta para darle formato MXN).*

```dax
Costo:=SUM(FACT_VENTAS[costo])
```
*(Formato: Moneda `$`).*

```dax
Margen Bruto:=[Ventas] - [Costo]
```
*(Formato: Moneda `$`).*

```dax
Margen %:=DIVIDE([Margen Bruto], [Ventas], 0)
```
*(Formato: Porcentaje `%`, 2 decimales).*

```dax
Transacciones:=DISTINCTCOUNT(FACT_VENTAS[id_venta])
```
*(Formato: Número entero con separador de miles).*

```dax
Ticket Promedio:=DIVIDE([Ventas], [Transacciones], 0)
```
*(Formato: Moneda `$`).*

---

### Paso 5: Construir el Dashboard con Tablas y Gráficos Dinámicos
1. Cierra o minimiza la ventana de Power Pivot para volver a la hoja de Excel.
2. Crea una hoja nueva llamada **`Dashboard`**.
3. Ve a **Insertar** → **Tabla dinámica** → selecciona la opción **⚪ Desde el modelo de datos** (o *Usar el modelo de datos de este libro*).
4. Coloca la tabla dinámica en la celda `B11`.
5. En el panel derecho de *Campos de tabla dinámica*:
   - Despliega `DIM_CLIENTE` y arrastra **`region`** a **Filas**.
   - Despliega `FACT_VENTAS` y marca las medidas DAX (con icono `fx`): **`Ventas`**, **`Margen Bruto`**, **`Margen %`**.
   - ¡Comprueba de inmediato que las cifras coincidan con el control!:
     * Occidente: `$677,408.00`
     * Centro: `$655,677.00`
     * Sur: `$608,288.00`
     * Norte: `$475,003.00`
     * **Total General: `$2,416,376.00`**
6. **Insertar Gráfico Dinámico:**
   - Con la tabla dinámica seleccionada, ve a **Insertar** → **Gráfico dinámico** → selecciona **Barras agrupadas**.
7. **Insertar Segmentadores de Datos (Slicers):**
   - Ve a **Insertar** → **Segmentación de datos**.
   - En la pestaña *TODAS*, marca `DIM_CLIENTE[region]`, `DIM_PRODUCTO[categoria]` y `DIM_TIEMPO[anio]`.
   - Haz clic en un botón de región (ej. *Sur*) y observa cómo todos los gráficos y KPIs se filtran instantáneamente.

---

## 🎯 3. Lista de Cotejo para la Evaluación del Profesor

| Criterio del Profesor | ¿Dónde se demuestra? | ¿Qué debe verse? |
| :--- | :--- | :--- |
| **1. Consultas Power Query** | Panel lateral *Consultas y conexiones* | 4 consultas con el texto *"Cargadas en el modelo de datos"*. |
| **2. Esquema Estrella** | Power Pivot → *Vista de diagrama* | 3 relaciones 1:N uniendo `DIM_*` hacia `FACT_VENTAS`. |
| **3. Medidas DAX** | Panel de campos o Área de cálculo | 6 medidas con el icono `fx` y fórmulas DAX auténticas. |
| **4. Cifras de Control ($0.00 dif)** | Hoja `Cifras_Control_DAX` o Tabla Dinámica | Ventas = `$2,416,376.00`, Margen = `$712,195.62` (29.47%). |
| **5. Interactividad en Vivo** | Segmentadores de datos (Slicers) | Al hacer clic en un filtro, los gráficos y valores se actualizan en tiempo real. |
