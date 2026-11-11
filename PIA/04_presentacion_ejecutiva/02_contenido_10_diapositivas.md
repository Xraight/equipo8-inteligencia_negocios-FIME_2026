# Contenido Estructurado del Deck Ejecutivo (10 Diapositivas)
## Presentación Formal del PIA ante el Comité Directivo — Casa&Estilo

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Formato:** 16:9 Panorámico
- **Número Exacto de Diapositivas:** 10 Diapositivas (Criterio de Excelencia Rúbrica Oficial)
- **Función General:** Documentar el contenido textual, métricas clave, gráficos recomendados y mensajes fuerza de cada diapositiva de la presentación ejecutiva.
- **Función Específica:** Alimentar el generador automatizado de la presentación en PowerPoint (`PIA_Comite_CasaEstilo_Equipo08.pptx`).

---

## Diapositiva 1: Portada Institucional y Ejecutiva
- **Título:** Solución Integral de Business Intelligence para Casa&Estilo
- **Subtítulo:** De los Datos Crudos a las Decisiones Estratégicas de Negocio
- **Metadatos:**
  - Universidad Autónoma de Nuevo León | Facultad de Ingeniería Mecánica y Eléctrica
  - Unidad de Aprendizaje: Analítica e Inteligencia de Negocios
  - Producto Integrador de Aprendizaje (PIA) — Noviembre 2026
  - Equipo 8 (Ingeniería de Datos & Analítica Empresarial)
- **Mensaje Fuerza:** *"Los datos por sí solos no toman decisiones; el valor está en convertirlos en información accionable."*

---

## Diapositiva 2: Contexto del Negocio y Problemática Operativa
- **Título:** Contexto Empresarial y Ecosistema de Datos
- **Puntos Clave:**
  - **Giro:** Cadena retail omnicanal de muebles finos y decoración del hogar.
  - **Alcance Operativo:** 16 tiendas físicas (1,000 - 1,800 $m^2$), portal Web y App móvil.
  - **Ecosistema RAW:** 11 fuentes desarticuladas (POS, ERP, CRM, Almacén, Logística) totalizando >530,000 registros históricos.
  - **Síntomas Críticos Detectados:**
    1. Ceguera analítica sobre el margen comercial neto real.
    2. Elevado costo de reembolsos por devoluciones de mercancía.
    3. Quejas recurrentes y pérdida de clientes por retrasos en instalaciones.
    4. Quiebres de stock en tiendas clave contrastados con exceso de inventario inmovilizado.
- **KPIs de Auditoría Inicial:** 140,000 transacciones de cabecera | 331,758 líneas de detalle | 10,800 clientes | 1,340 productos.

---

## Diapositiva 3: Arquitectura Tecnológica y Pipeline ETL
- **Título:** Arquitectura de Datos y Pipeline ETL en MySQL 8.0
- **Puntos Clave:**
  - **Arquitectura de 3 Capas:** RAW (Inmutable) $\to$ Staging (`stg_ce_*`) $\to$ Data Mart Dimensional (`ce_bi`).
  - **Ingesta Masiva:** Carga ultrarrápida mediante `LOAD DATA INFILE` procesando 331k filas en segundos.
  - **Saneamiento y Calidad:**
    - Eliminación de UTF-8 BOM en archivos fuente.
    - Imputación fundamentada en CRM (20 ciudades nulas, 43 correos ausentes, estandarización de género).
    - **Corrección Crítica:** Separación contable entre subtotal bruto y descuento comercial en POS.
  - **Trazabilidad y Balance de Masa:** Bitácora en `etl_log` y conciliación al 100.00% con discrepancia $0.00.
- **Métrica Clave:** Cero errores de ejecución | Cero registros huérfanos | Tiempo de ejecución: 23 segundos.

---

## Diapositiva 4: Modelo Dimensional en Esquema Estrella
- **Título:** Esquema Estrella y Decisiones de Modelado
- **Puntos Clave:**
  - **Elección Metodológica:** Star Schema de Ralph Kimball en lugar de Snowflake para eliminar cuellos de botella y optimizar el motor columnar VertiPaq.
  - **Granularidad Atómica:** Modelado al nivel más fino (línea de ticket) para preservar la capacidad de filtrado cruzado sin sesgos de agregación.
  - **Dimensiones Conformes:** `dim_tiempo` (calendario continuo 2024-2026), `dim_producto`, `dim_cliente`, `dim_sucursal`, `dim_canal`, `dim_metodo_pago`.
  - **Constelación de Hechos:**
    - Hecho Principal: `fact_ventas_detalle` (331,758 filas).
    - Hechos Satélites: `fact_devoluciones` (9,952 filas), `fact_instalaciones` (6,500 filas), `fact_inventario_snapshot` (21,440 filas).
  - **Claves Sustitutas:** Claves artificiales enteras (`INT AUTO_INCREMENT`) con registro comodín `-1` para blindar la integridad referencial.

---

## Diapositiva 5: Desempeño Comercial y Rentabilidad Global
- **Título:** Diagnóstico Financiero: Ventas, Descuentos y Márgenes
- **Cifras Oficiales de Control (2024 - 2026):**
  - **Venta Bruta Global:** `$1,402,502,128.39 MXN`
  - **Descuentos Comerciales:** `$91,755,708.99 MXN` (6.54% de la facturación bruta)
  - **Venta Neta Real:** `$1,310,746,491.89 MXN`
  - **Costo de Ventas (COGS):** `$1,029,871,626.89 MXN`
  - **Utilidad Bruta:** `$280,874,853.71 MXN`
  - **Margen Bruto Real:** `21.43%`
  - **Ticket Promedio:** `$9,362.47 MXN` por compra
- **Hallazgo de Negocio:** La detección y corrección de la fórmula del POS evitó presentar un estado financiero falseado por casi $92M MXN ante los accionistas.

---

## Diapositiva 6: Análisis de Categorías y Omnicanalidad
- **Título:** Cartera de Productos y Estrategia Omnicanal
- **Desempeño por Categoría:**
  - **Recámara:** Líder en volumen ($221.4M en ventas netas | 146.6k unidades | 21.14% margen).
  - **Comedor:** Segundo motor ($194.5M en ventas netas | 121.1k unidades | 21.07% margen).
  - **Salas y Exterior:** Mayor rentabilidad relativa (21.98% y 21.72% de margen bruto).
  - **Iluminación, Oficina y Decoración:** Aportan entre $166M y $184M con márgenes estables de ~21.5%.
- **Distribución Omnicanal:**
  - **Tienda Física:** 68.0% de ventas netas ($891.8M | 95,152 transacciones | Ticket $9,372).
  - **Portal Web:** 22.1% de ventas netas ($290.2M | 30,970 transacciones | Ticket $9,371).
  - **App Móvil:** 9.8% de ventas netas ($128.8M | 13,878 transacciones | Ticket $9,278).
- **Insight Estratégico:** El ticket promedio y el margen son idénticos entre canales; la App representa una oportunidad latente de triplicar ventas digitales.

---

## Diapositiva 7: Calidad y Costo de Devoluciones
- **Título:** Diagnóstico de No Calidad: Fuga en Devoluciones
- **Puntos Clave:**
  - **Magnitud del Impacto:** 9,952 eventos de devolución que representaron **$22,897,836.87 MXN** en reembolsos emitidos (1.63% de la venta bruta).
  - **Distribución por Causa Raíz:**
    - Daño en transporte / manipulación: $4.50M (1,983 eventos | 2,706 piezas).
    - Defecto de fabricación: $4.42M (1,914 eventos | 2,651 piezas).
    - Talla / Incompatibilidad con espacio: $4.67M (2,008 eventos | 2,753 piezas).
    - No era lo esperado (diferencia vs foto): $4.58M (2,027 eventos | 2,807 piezas).
    - Otros motivos: $4.73M (2,020 eventos | 2,795 piezas).
- **Riesgo:** Pérdida de margen directo más costos logísticos inversos duplicados en muebles voluminosos.

---

## Diapositiva 8: Experiencia del Cliente y SLA de Instalaciones
- **Título:** Logística de Instalaciones: Cuello de Botella Crítico
- **Puntos Clave:**
  - **Universo Auditado:** 6,500 órdenes de instalación técnica especializada en domicilios.
  - **Cumplimiento Global de SLA:** **36.91% a tiempo** (2,399 de 6,500; 63.09% de las instalaciones sufren retraso).
  - **Varianza Temporal:** Retraso promedio global de **+3.41 días adicionales** a la fecha prometida (CSAT global: 2.99 / 5.0).
  - **Sucursales Críticas:**
    - Monterrey 11: Cumplimiento SLA 29.66% | Retraso promedio 4.2 días | Satisfacción 3.05.
    - Santa Catarina 6: Cumplimiento SLA 34.18% | Retraso promedio 3.6 días | Satisfacción 2.94.
    - Apodaca 2: Cumplimiento SLA 34.72% | Retraso promedio 3.7 días | Satisfacción 2.86.
- **Correlación Directa:** Cada día de retraso reduce en 0.4 puntos la calificación CSAT, generando detrimento severo en la reputación de marca.

---

## Diapositiva 9: Abastecimiento y Desbalance de Inventario
- **Título:** Cadena de Suministro: Roturas vs Capital Inmovilizado
- **Puntos Clave:**
  - **Diagnóstico del Snapshot de Existencias (21,440 combinaciones tienda-SKU):**
    - **126 ítems en Rotura Total de Stock (Stock = 0):** Pérdida de ventas inmediata con déficit acumulado de 2,738 piezas en tiendas clave.
    - **2,566 ítems en Alerta de Reorden:** Stock por debajo del punto de seguridad con déficit de 33,908 unidades y $43.4M MXN en inventario vulnerable.
    - **$2,330 Millones MXN en Inventario Excedente:** Concentrado en líneas de baja rotación en formatos grandes.
  - **Desempeño de Proveedores:** 1,348 órdenes de compra pendientes con lead times de hasta 28 días que estrangulan el reabastecimiento en tiendas periféricas.
- **Oportunidad:** Liberación de flujo de efectivo reduciendo el sobreinventario y reasignando compras hacia SKUs críticos.

---

## Diapositiva 10: Conclusiones y Hoja de Ruta Prescriptiva
- **Título:** Hoja de Ruta Estratégica para el C-Level (Top 5 Acciones)
- **Cinco Recomendaciones Accionables:**
  1. **Rediseño del SLA de Armado e Instalación:** Contratación de cuadrillas logísticas regionales y ruteo dinámico para elevar el cumplimiento del 36.9% al 85% en 90 días (Impacto: +1.5 pts CSAT).
  2. **Certificación de Proveedores y Embalaje Reforzado:** Protocolo de inspección en muelle y penalizaciones a proveedores por defectos para abatir en 40% las devoluciones (Ahorro: ~$9.2M MXN anuales).
  3. **Planificación de Inventarios con Algoritmo Min/Max Dinámico:** Automatización de órdenes de compra vinculando el punto de reorden a la velocidad de venta semanal por tienda (Eliminación de 126 roturas).
  4. **Campaña de Adopción Digital en App Móvil:** Programa de lealtad omnicanal y visualizador 3D/AR en App para reducir devoluciones por "talla/expectativa" y duplicar la cuota de la App del 10% al 20%.
  5. **Institucionalización del Data Mart en Comités Mensuales:** Establecer el tablero Power Pivot/DAX como la fuente única de verdad para la toma de decisiones directivas.
- **Cierre:** *"La ventaja competitiva de Casa&Estilo no está en vender más muebles, sino en operarlos con inteligencia analítica."*
