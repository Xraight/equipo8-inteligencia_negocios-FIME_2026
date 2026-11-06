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

## 💻 Modalidad 1: Demostración en Excel 365 (Requisito Principal del Laboratorio)

### Paso 1: Abrir el archivo
1. Abre [`U5_Dashboard_Equipo08.xlsx`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/U5_Dashboard_Equipo08.xlsx).
2. Proyecta la pestaña principal: **`Dashboard`**.

### Paso 2: Mostrar el estado inicial sin filtros
Señala al proyector las 5 tarjetas de KPI superiores:
* **Ventas Totales:** `$2,416,376.00 MXN`
* **Costo Total:** `$1,704,180.38 MXN`
* **Margen Bruto:** `$712,195.62 MXN`
* **Margen %:** `29.5%` (29.47%)
* **Ticket Promedio:** `$2,013.65 MXN` en `1,200` transacciones.

### Paso 3: Interactuar en tiempo real frente al profesor
Realiza los siguientes movimientos dinámicos:
1. **Filtrar por Región "Norte":**
   * *Qué pasa en pantalla:* Las ventas se reducen a **$475,003.00 MXN** en 251 transacciones.
   * *Qué decir al maestro:* *«Profesor, aquí observamos en tiempo real el rezago del Norte: representa solo el 19.66% de la venta nacional a pesar de tener 20 clientes registrados al igual que las demás regiones»*.
2. **Filtrar por Región "Sur":**
   * *Qué pasa en pantalla:* Las ventas marcan **$608,288.00 MXN** y el Margen % sube a **30.39%**.
   * *Qué decir al maestro:* *«El Sur es nuestra región más rentable porcentualmente, superando el promedio de la compañía»*.
3. **Filtrar por Categoría "Tecnología":**
   * *Qué pasa en pantalla:* Se aísla el motor de facturación: **$889,916.00 MXN** (36.8%) con el **Producto 12** liderando con $346,902.00 MXN y 32.0% de margen.
4. **Quitar filtros:**
   * Mostrar que el total regresa de inmediato a **$2,416,376.00 MXN** (comprobando que no hay duplicados ni pérdidas).

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
