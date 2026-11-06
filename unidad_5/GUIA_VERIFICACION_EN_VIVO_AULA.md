# 🎓 Guía de Verificación en Tiempo Real para el Aula (Equipo 8)
**Laboratorio Unidad 5 · Del Data Mart al Dashboard Ejecutivo**  
**Materia:** Inteligencia de Negocios · FIME UANL (2026)

Esta guía contiene el **protocolo paso a paso para la defensa y verificación en vivo frente al profesor y la clase**. El equipo cuenta con **tres modalidades complementarias** preparadas para cualquier solicitud del docente.

---

## 🎯 ¿Qué busca evaluar el maestro en tiempo real?
1. **Que los datos sean reales y no un reporte estático "foto":** Al mover filtros, las cifras deben recalcularse en milisegundos.
2. **Que el balance cuadre al centavo:** Al quitar todos los filtros, las ventas deben dar exactamente **$2,416,376.00 MXN**.
3. **Que entiendan el modelo subyacente:** Saber explicar qué es la tabla de hechos, las dimensiones y las medidas DAX.

---

## 💻 Modalidad 1: Demostración en Excel 365 con Power Pivot Nativo

> [!IMPORTANT]
> **Diferencia entre Archivo CI/CD y Modelo Nativo de Power Pivot:**  
> - El archivo `U5_Dashboard_Equipo08.xlsx` generado por el pipeline de Docker/Python contiene las hojas de cálculo, gráficos y conciliación numérica ($0.00 de diferencia) para validación en integración continua.  
> - Para la evaluación presencial de **Power Pivot (Esquema Estrella, relaciones 1:N y medidas DAX)**, Microsoft Excel 365 requiere su motor tabular en memoria (**VertiPaq**).  
> - El equipo cuenta con el script de automatización de 1 clic: [`construir_modelo_powerpivot.bas`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/construir_modelo_powerpivot.bas) y la [`guia_paso_a_paso_powerpivot_excel365.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/guia_paso_a_paso_powerpivot_excel365.md).

### Paso 1: Mostrar el Modelo Nativo de Power Pivot (Vista de Diagrama)
1. En Excel 365, abre la pestaña **Power Pivot** → haz clic en **Administrar**.
2. En la ventana emergente, haz clic en **Vista de diagrama** (icono superior derecho).
3. **Muestra el Esquema Estrella en pantalla:**
   - Señala la tabla central: `FACT_VENTAS` (1,200 transacciones).
   - Señala las 3 dimensiones conectadas: `DIM_PRODUCTO`, `DIM_CLIENTE` y `DIM_TIEMPO`.
   - Muestra las líneas de relación dimensional de **1 a Varios (1:N)**:
     * `DIM_PRODUCTO[id_producto]` (1) ──── (N) `FACT_VENTAS[id_producto]`
     * `DIM_CLIENTE[id_cliente]` (1) ──────── (N) `FACT_VENTAS[id_cliente]`
     * `DIM_TIEMPO[id_tiempo]` (1) ────────── (N) `FACT_VENTAS[id_tiempo]`
   - *Qué decir al maestro:* *«Profesor, aquí está el Esquema Estrella configurado en el Modelo de Datos. Las dimensiones están en el lado '1' con valores únicos y la tabla de hechos en el lado 'Muchos', permitiendo la propagación natural de filtros analíticos»*.

### Paso 2: Mostrar el Catálogo de Medidas DAX en el Área de Cálculo
1. En la misma ventana de Power Pivot, haz clic en **Vista de datos** y selecciona la pestaña inferior `FACT_VENTAS`.
2. Muestra las 6 medidas DAX calculadas en el **Área de cálculo** inferior:
   * `Ventas:=SUM(FACT_VENTAS[monto])`
   * `Costo:=SUM(FACT_VENTAS[costo])`
   * `Margen Bruto:=[Ventas] - [Costo]`
   * `Margen %:=DIVIDE([Margen Bruto], [Ventas], 0)`
   * `Transacciones:=DISTINCTCOUNT(FACT_VENTAS[id_venta])`
   * `Ticket Promedio:=DIVIDE([Ventas], [Transacciones], 0)`
3. *Qué decir al maestro:* *«Las medidas están modeladas en DAX con la función `DIVIDE` para prevenir errores de división entre cero y garantizar el cálculo dinámico sobre el contexto de filtro»*.

### Paso 3: Interactuar en vivo con la Tabla Dinámica y Segmentadores (Slicers)
Regresa a la hoja de cálculo del Dashboard:
1. **Filtrar por Región "Norte":**
   * *Qué pasa en pantalla:* La tabla dinámica y gráficos dinámicos se recalculan automáticamente: Ventas bajan a **$475,003.00 MXN** en 251 transacciones.
   * *Qué decir al maestro:* *«Al filtrar el Norte, vemos que representa el 19.66% de la facturación nacional, evidenciando un rezago comercial respecto a Occidente y Centro»*.
2. **Filtrar por Región "Sur":**
   * *Qué pasa en pantalla:* Ventas marcan **$608,288.00 MXN** y el Margen % sube a **30.39%**.
   * *Qué decir al maestro:* *«El Sur es nuestra región con mayor margen porcentual, superando la media global de la compañía»*.
3. **Filtrar por Categoría "Tecnología":**
   * *Qué pasa en pantalla:* Facturación de **$889,916.00 MXN** (36.8%) impulsada por el Producto 12 ($346,902.00 MXN y 32.0% margen).
4. **Quitar filtros (Borrar filtro en Slicer):**
   * Mostrar que el total regresa de inmediato a **$2,416,376.00 MXN**, confirmando integridad referencial total.

### Paso 4: Mostrar la pestaña de control
* Ve a la pestaña **`Cifras_Control_DAX`**:
  * Muestra la tabla donde el valor calculado y el valor esperado arrojan una **Diferencia de $0.00 (100% Exacto)**.

---

## 🌐 Modalidad 2: Verificador y Tablero Web Interactivo en Vivo (Docker)

Si el profesor pide ver una aplicación interactiva en vivo o si se proyecta desde una laptop con navegador:

### Paso 1: Iniciar el servidor web en 1 comando
En la terminal de la computadora, ejecuta:
```bash
./unidad_5/iniciar_dashboard_en_vivo.sh
```

### Paso 2: Abrir el navegador
Abre en Chrome/Firefox:  
👉 **[http://localhost:8085](http://localhost:8085)**

### Paso 3: Demostración visual en proyector
1. **Pruebas Rápidas con 1 Clic:**
   * Haz clic en el botón **`Norte (Rezago)`**: La gráfica de regiones resalta el Norte y los KPIs cambian en vivo.
   * Haz clic en **`Sur (Margen 30.4%)`**: Los KPIs cambian y el mix de categorías se recalcula con animación de Chart.js.
   * Haz clic en **`Tecnología (Motor)`**: La dona de categorías se enfoca en Tecnología y el Top 5 muestra el Producto 12.
   * Haz clic en **`🔄 Reset`**: Vuelve instantáneamente al total consolidado.
2. **Botón `⚖️ Validar Cifras ($0.00 Dif)`:**
   * Haz clic en el botón verde superior: Despliega una alerta modal de auditoría en vivo certificando el 100.00% de coincidencia matemática.

---

## 💻 Modalidad 3: Auditoría en Consola / Terminal en Tiempo Real

Si el profesor pide ver la ejecución del código o la auditoría técnica desde terminal:

```bash
./unidad_5/verificacion_en_vivo_terminal.sh
```

* **Qué muestra en pantalla:**
  1. Conteo de los 4 CSVs (1,200 transacciones, 12 productos, 80 clientes, 96 tiempos).
  2. Diagrama de relaciones del Star Schema (1:N).
  3. Ejecución de las 6 medidas DAX en vivo contra las cifras de control con semáforos verdes.
  4. Simulación interactiva de filtros de región.

---

## 🙋 Preguntas Clave del Maestro y Respuestas Exactas

### 1. "¿Por qué no usaron la función SAMEPERIODLASTYEAR de DAX?"
* **Respuesta del alumno:**  
  *«Porque `DIM_TIEMPO.csv` tiene granularidad semanal (4 cortes por mes, 96 registros en total) y no un calendario diario continuo de 730 días. Las funciones nativas de Time Intelligence de DAX exigen estrictamente una tabla de fechas continua sin huecos. Por eso, en apego a las buenas prácticas y las instrucciones del laboratorio, las comparativas YoY se hicieron agrupando por Año y Mes o mediante filtros DAX con `CALCULATE`».*

### 2. "¿Cómo se asegura que las ventas no se dupliquen al filtrar?"
* **Respuesta del alumno:**  
  *«Porque las dimensiones tienen llaves primarias únicas estrictas (80 clientes únicos, 12 productos únicos) y la relación con la tabla de hechos es 1 a Varios (1:N) con dirección de filtro unidireccional. El filtro fluye de la dimensión hacia los hechos, evitando duplicidades».*

### 3. "¿Por qué afirman que falta frecuencia en el Norte y no que falta inventario?"
* **Respuesta del alumno:**  
  *«Por rigor metodológico. El dataset de este laboratorio no contiene datos de inventario, stock en almacén ni campañas de marketing. Por tanto, éticamente no podemos inventar que 'faltó stock'. Observamos que los 20 clientes del Norte compraron 76 veces menos que los 20 de Occidente, y planteamos como **hipótesis diagnóstica** una posible fricción comercial o logística a verificar con el ERP».*
