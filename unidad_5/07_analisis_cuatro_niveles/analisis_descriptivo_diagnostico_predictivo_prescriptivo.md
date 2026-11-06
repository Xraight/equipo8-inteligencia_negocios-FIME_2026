# 🧠 Fase F · Los Cuatro Niveles de Análisis de Negocio

## 🎯 Pregunta Rectora del Negocio
> *¿Cómo se comportan las ventas y la rentabilidad por período, región y categoría, y qué decisión justificada con datos podemos recomendar al Comité Directivo?*

---

## 1️⃣ Nivel Descriptivo (¿Qué pasó?)
*Hallazgos cuantificados estrictamente observados en los datos validados del Data Mart:*

1. **Estabilidad Anual de Ingresos y Contracción Marginal:**  
   Durante el bienio 2025-2026, la empresa generó **$2,416,376.00 MXN** en 1,200 transacciones. Las ventas anuales pasaron de **$1,214,067.00 MXN** en 2025 (603 transacciones) a **$1,202,309.00 MXN** en 2026 (597 transacciones), lo que representa una variación interanual nominal de **-$11,758.00 MXN** (**-0.97% YoY**), demostrando una alta estabilidad en el volumen total pero con estancamiento en la captación.
2. **Liderazgo Comercial y Rentabilidad de Tecnología:**  
   La categoría de **Tecnología** encabezó la facturación con **$889,916.00 MXN (36.83% de participación)** y el mayor margen porcentual relativo (**30.13%**, con $268,103.26 MXN de margen bruto), superando a Oficina ($801,265.00 MXN, margen 28.62%) y Hogar ($725,195.00 MXN, margen 29.61%). El **Producto 12** (Tecnología) es el artículo individual más rentable y de mayor venta de todo el catálogo ($346,902.00 MXN y 32.00% de margen).
3. **Concentración Geográfica y Rezago de la Región Norte:**  
   Las regiones de **Occidente** ($677,408.00 MXN, 28.03%) y **Centro** ($655,677.00 MXN, 27.13%) concentran más del **55.16%** de los ingresos globales. En contraste, la región **Norte** se ubica en el último lugar con **$475,003.00 MXN (19.66%)** y 251 transacciones, generando una brecha comercial de **$202,405.00 MXN (-29.88%)** respecto a la región líder (Occidente).

---

## 2️⃣ Nivel Diagnóstico (¿Dónde se concentró y por qué?)
*Desglose analítico y formulación de dos hipótesis sujetas a validación externa:*

### Desglose Dimensional:
- **Rentabilidad Regional:** La región **Sur**, aunque aporta el 25.17% de los ingresos ($608,288.00 MXN), exhibe el margen bruto porcentual más alto de la compañía (**30.39%**), debido a una mezcla de venta inclinada hacia productos de mayor margen unitario.
- **Volatilidad Intermensual Compensatoria:** Aunque el total anual es plano (-0.97%), la dinámica mensual muestra fuertes fluctuaciones interanuales: julio (+47.11% YoY), agosto (+28.38% YoY) y diciembre (+34.78% YoY) registraron incrementos notables en 2026, mientras que marzo (-20.78% YoY), junio (-25.74% YoY), septiembre (-26.93% YoY) y noviembre (-25.03% YoY) sufrieron caídas pronunciadas.

### 🧪 Hipótesis Explicativas (Sin Afirmar Causalidad No Demostrada):
> [!IMPORTANT]
> **Aviso de Rigor Metodológico:** El dataset no contiene registros de inventarios, stock en almacén, gasto publicitario, promociones ni tráfico web/tienda. Por tanto, las siguientes proposiciones se plantean formalmente como hipótesis y no como hechos consumados:

- **Hipótesis H1 (Desfase en Ciclos de Reabastecimiento o Calendario Comercial):**  
  La fuerte caída en noviembre 2026 ($104,199 vs $138,994 en 2025) y el simultáneo repunte en diciembre 2026 ($113,815 vs $84,445 en 2025) sugiere la posibilidad de un corrimiento o postergación en las decisiones de compra de fin de año o entregas de pedidos institucionales, y no necesariamente una pérdida estructural de clientes.
- **Hipótesis H2 (Desbalance en Capacidad de Cobertura o Penetración en el Norte):**  
  El menor número de transacciones en la región Norte (251 transacciones frente a 327 en Occidente) a pesar de tener el mismo número de clientes registrados en el catálogo (20 clientes por región) podría obedecer a una menor frecuencia de recompra o menor efectividad del canal de distribución en esa zona geográfica.

---

## 3️⃣ Nivel Predictivo (¿Qué podría pasar?)
*Proyección de tendencia con supuestos explícitos y análisis de incertidumbre:*

### Modelo de Tendencia y Supuestos:
- **Supuesto Base:** Se mantiene la estabilidad observada en el comportamiento de compras de la base de 80 clientes, sin variaciones drásticas en la política de precios de los 12 productos ni en la estructura de costos de los proveedores (margen promedio proyectado en ~29.5%).
- **Proyección 2027 (Escenario Inercial):**  
  De no implementarse acciones comerciales correctivas, la facturación se proyecta en **~$1,195,000.00 MXN ± $35,000.00 MXN** con un margen bruto de **~$352,000.00 MXN**.
- **Riesgo Predictivo (Incertidumbre):**  
  Si la tendencia decreciente en la región Norte persiste (-2.5% anual) y se prolonga el estancamiento de Oficina y Hogar, la utilidad bruta de la compañía continuará erosionándose marginalmente. Existe una alta exposición al depender en un 44.8% del margen bruto de únicamente dos productos clave (**Producto 12** y **Producto 10**).

---

## 4️⃣ Nivel Prescriptivo (¿Qué conviene hacer?)
*Plan de acción justificado con evidencia cuantitativa:*

| Elemento | Especificación Ejecutiva |
| :--- | :--- |
| **Acción Estratégica Propuesta** | **Programa Integral de Expansión Comercial Norte y Potenciación del Portafolio Tecnológico:**<br>1. Lanzar una campaña de reactivación comercial dirigida específicamente a los 20 clientes de la región Norte para elevar su frecuencia de compra.<br>2. Empaquetar artículos de alta rentabilidad (Producto 12, margen 32%) en bundles con artículos de oficina (Producto 11, margen 28%) para elevar el ticket promedio.<br>3. Investigar causas del rezago logístico/comercial en el Norte mediante auditoría de servicio. |
| **Responsable Principal** | Dirección de Ventas y Mercadotecnia en coordinación con Logística Regional. |
| **Plazo de Ejecución** | 6 meses (Q1 y Q2 del siguiente ejercicio fiscal). |
| **KPIs de Seguimiento** | 1. **Ventas en Región Norte:** Meta de crecimiento del **+15%** (alcanzar $275,000 MXN semestrales).<br>2. **Transacciones en el Norte:** Incrementar de 125 a 155 transacciones semestrales.<br>3. **Margen Bruto de la Categoría Oficina:** Elevar del **28.62% al 29.50%** mediante bundles.<br>4. **Ticket Promedio Global:** Mantener por encima de **$2,100.00 MXN**. |
