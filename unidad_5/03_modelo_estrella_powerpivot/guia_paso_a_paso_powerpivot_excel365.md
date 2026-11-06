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

## ⚡ 2. Las Tres Vías de Solución

Tienes **tres opciones inmediatas** para tener tu Modelo de Datos al 100%:
* **Opción A (La Más Recomendada y Rápida · 30 Segundos):** Usar las tablas ya existentes en `U5_Dashboard_Equipo08.xlsx` con el botón *"Agregar a modelo de datos"* (0 macros, 0 errores, 100% nativo).
* **Opción B (Automatizada con Macro VBA):** Con el módulo corregido [`construir_modelo_powerpivot.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas) (protegido contra el Error 9 multilingüe).
* **Opción C (Demostración Manual Completa Desde CSVs · 2 Minutos):** Importando desde Power Query si el profesor te pide ver todo el flujo ETL desde cero.

---

## 🌟 Opción A (Recomendada): El Método de los 30 Segundos ("Agregar a modelo de datos")

Tu archivo [`U5_Dashboard_Equipo08.xlsx`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/U5_Dashboard_Equipo08.xlsx) **ya contiene los 4 datasets estructurados como Tablas Oficiales de Excel** (`FACT_VENTAS`, `DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_TIEMPO`).

Por lo tanto, no necesitas programar ni lidiar con macros:
1. Abre [`U5_Dashboard_Equipo08.xlsx`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/U5_Dashboard_Equipo08.xlsx) en Excel 365 (Windows).
2. Haz clic en la pestaña de la hoja **`FACT_VENTAS`** y selecciona cualquier celda dentro de la tabla.
3. En la cinta de opciones superior, ve a la pestaña **Power Pivot** y haz clic en el botón:  
   👉 **"Agregar a modelo de datos"** (Add to Data Model).
   *(Se abrirá instantáneamente la ventana de Power Pivot con FACT_VENTAS cargada en el motor VertiPaq).*
4. Regresa a la ventana principal de Excel y repite ese mismo clic para las otras 3 hojas:
   - En `DIM_PRODUCTO` ➔ clic en cualquier celda ➔ **Power Pivot** ➔ **Agregar a modelo de datos**.
   - En `DIM_CLIENTE` ➔ clic en cualquier celda ➔ **Power Pivot** ➔ **Agregar a modelo de datos**.
   - En `DIM_TIEMPO` ➔ clic en cualquier celda ➔ **Power Pivot** ➔ **Agregar a modelo de datos**.
5. En la ventana de Power Pivot:
   - Haz clic en **Vista de diagrama** (esquina superior derecha).
   - Arrastra con el ratón las 3 claves hacia `FACT_VENTAS`:
     * `DIM_PRODUCTO[id_producto]` ➔ `FACT_VENTAS[id_producto]`
     * `DIM_CLIENTE[id_cliente]` ➔ `FACT_VENTAS[id_cliente]`
     * `DIM_TIEMPO[id_tiempo]` ➔ `FACT_VENTAS[id_tiempo]`
6. En la pestaña *Vista de datos* de `FACT_VENTAS`, pega en el área de cálculo inferior las 6 medidas DAX (ver Paso 4).

> **Ventaja indiscutible:** Toma 30 segundos, funciona en cualquier versión de Excel (Español o Inglés), y nunca arroja errores de VBA o permisos.

---

## 🚀 Opción B: Automatización mediante Macro VBA (Sin Error 9)

Si deseas utilizar la macro automatizada, hemos actualizado [`construir_modelo_powerpivot.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas) para solucionar de raíz el `subscript out of range (code 9)`:

### ¿Por qué ocurrió el Error 9?
El error 9 en VBA significa *"Subíndice fuera del intervalo"*. Ocurría porque la versión anterior intentaba llamar por nombre en inglés a `wb.Connections("ModelConnection_ThisWorkbookDataModel")`. En Excel en Español o antes de que el motor VertiPaq esté poblado, esa clave de texto no existe en la colección, detonando el error 9.

### Solución aplicada en el nuevo código:
1. Reemplazamos la clave de texto por la propiedad nativa de Excel: `wb.Model.WorkbookConnection`.
2. Se agregó un escaneo inteligente de conexiones que detecta automáticamente cualquier conexión de tipo Modelo en español o inglés (`Type = xlConnectionTypeModel`).
3. Se añadió detección automática: si el libro ya tiene las hojas de datos (`FACT_VENTAS`, etc.), las aprovecha directamente.

### Pasos para ejecutar la macro actualizada:
1. Abre tu libro en Excel 365.
2. Presiona `ALT + F11`.
3. Si tenías el módulo anterior, haz clic derecho sobre él en el árbol de la izquierda y selecciona *Quitar Módulo...* (No guardar).
4. Menú **Archivo** → **Importar archivo...** y selecciona el nuevo [`construir_modelo_powerpivot.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas).
5. Presiona `F5` para ejecutar.

---

## 🛠️ Opción C: Construcción Manual en Vivo Desde Cero (Paso a Paso en 2 Minutos)

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
