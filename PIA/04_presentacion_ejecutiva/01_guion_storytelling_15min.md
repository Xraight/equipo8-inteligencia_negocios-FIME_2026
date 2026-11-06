# Guion de Defensa y Storytelling Ejecutivo (15 Minutos)
## Presentación ante el Comité Directivo Simulado — Casa&Estilo

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Audiencia:** Comité Directivo (CEO, CFO, COO, Director Comercial, Director de TI)
- **Tiempo Límite:** 15 minutos de exposición + 5 minutos de preguntas y respuestas
- **Función General:** Proveer la estructura narrativa de persuasión y defensa fundamentada en datos duros del Data Mart.
- **Función Específica:** Guiar a los expositores del equipo minuto a minuto para articular el problema de negocio, la arquitectura técnica, los hallazgos críticos y las recomendaciones accionables.

---

## 1. Cronograma de Exposición (Minuto a Minuto)

| Minuto | Diapositiva | Tema Central | Portavoz / Rol | Objetivo Comunicativo |
| :---: | :---: | :--- | :--- | :--- |
| **00:00 - 01:15** | Slide 1 | Portada e Introducción al Proyecto | Líder de Proyecto | Establecer credenciales, alcance del proyecto y objetivo de transformar datos en decisiones accionables. |
| **01:15 - 02:45** | Slide 2 | Contexto de Negocio y Ecosistema RAW | Analista de Datos | Exponer los retos de dispersión de 11 fuentes RAW y las anomalías de calidad detectadas. |
| **02:45 - 04:15** | Slide 3 | Arquitectura Tecnológica y Pipeline ETL | Ingeniero de Datos | Demostrar la robustez del Staging, la bitácora `etl_log` y el balance de masa sin pérdida de registros. |
| **04:15 - 05:45** | Slide 4 | Modelo Dimensional en Esquema Estrella | Arquitecto de Datos | Defender la elección del Star Schema, granularidad atómica y surrogate keys frente a alternativas. |
| **05:45 - 07:15** | Slide 5 | Diagnóstico Comercial Global y Márgenes | Director Comercial BI | Revelar las cifras clave: $1,310M en ventas netas, 21.43% de margen y advertir el impacto de la corrección del POS. |
| **07:15 - 08:45** | Slide 6 | Rentabilidad por Categoría y Omnicanalidad | Especialista en Canales | Contrastar el volumen de Recámara y Comedor frente al margen, y analizar el canal físico vs digital (App/Web). |
| **08:45 - 10:15** | Slide 7 | Calidad y Costo de Devoluciones | Analista de Operaciones | Cuantificar el costo de no calidad ($22.9M en reembolsos) y desglosar las causas raíz (daño, defecto, expectativas). |
| **10:15 - 11:45** | Slide 8 | Experiencia del Cliente y SLA de Instalaciones | Especialista en Logística | **Punto de Inflexión:** Revelar que sólo el 34.7% de instalaciones cumplen SLA y cómo destruye el CSAT. |
| **11:45 - 13:00** | Slide 9 | Desbalance de Inventarios y Abastecimiento | Ingeniero de SCM | Alertar sobre 126 ítems en rotura total de stock coexistiendo con $2,330M inmovilizados en exceso. |
| **13:00 - 15:00** | Slide 10 | Conclusiones y Hoja de Ruta Prescriptiva | Líder de Proyecto | Presentar 5 recomendaciones estratégicas inmediatas, cuantificando su ROI y cerrando con firmeza. |

---

## 2. Desarrollo Narrativo Diapositiva por Diapositiva

### Minuto 0:00 - 1:15 | Slide 1: Portada y Apertura
> *"Buenos días, miembros del Comité Directivo. Hoy el Equipo 8 tiene el honor de presentar la Solución Integral de Business Intelligence para Casa&Estilo. En el entorno minorista actual, donde la omnicanalidad y el servicio al cliente definen la supervivencia de una cadena, contar con datos no es suficiente: el verdadero valor reside en convertirlos en información accionable para maximizar la rentabilidad y asegurar la lealtad del cliente. A lo largo de los próximos 15 minutos, demostraremos cómo transformamos un ecosistema de más de medio millón de registros dispersos en un motor analítico reproducible de toma de decisiones."*

### Minuto 1:15 - 2:45 | Slide 2: Contexto de Negocio y Fuentes RAW
> *"Casa&Estilo opera en un mercado altamente competitivo de muebles y decoración, respaldada por 16 sucursales físicas y canales digitales en expansión. Sin embargo, al auditar los datos transaccionales, identificamos cuatro síntomas de ceguera analítica: falta de consolidación omnicanal, costos ocultos en devoluciones, quejas severas en instalaciones y desbalance de inventarios. Al perfilar los 11 archivos de datos provistos, descubrimos problemas intencionales de calidad, siendo el más crítico un error en el punto de venta donde la columna 'importe' facturaba importes brutos sin descontar promociones. Nuestro primer mandato técnico fue no tocar los archivos fuente originales y construir una solución que sanee y concilie estos datos desde la ingeniería de datos."*

### Minuto 2:45 - 4:15 | Slide 3: Arquitectura Tecnológica y Pipeline ETL
> *"Para resolver esta problemática implementamos una arquitectura moderna de tres capas en MySQL 8.0, 100% contenerizada en Docker. Creamos una zona de Staging tolerante a fallos que ingesta 11 archivos CSV en solo segundos. Diseñamos procedimientos almacenados modulares con control transaccional estricto y una bitácora institucional llamada `etl_log`. Cada corrida calcula microsegundos de ejecución y balance de masa. Como certifica nuestra auditoría, procesamos 331,758 transacciones de detalle sin una sola discrepancia ni pérdida de registros: 100% de conciliación contable y cero registros huérfanos."*

### Minuto 4:15 - 5:45 | Slide 4: Modelo Dimensional en Esquema Estrella
> *"El corazón analítico de nuestra solución es un Esquema Estrella con constelación de hechos basada en la metodología de Ralph Kimball. Elegimos la estrella en lugar de copo de nieve para eliminar cadenas de uniones costosas y maximizar el rendimiento columnar en Power Pivot. Situamos la granularidad en el nivel más atómico posible: cada línea de ticket de venta. Además, adoptamos claves sustitutas enteras que reducen en 60% el consumo en memoria e implementamos registros comodín con clave -1 para blindar la base contra datos desconocidos. Este diseño no sólo responde al qué pasó hoy, sino que permite cruzar simultáneamente sucursal, canal, cliente, producto y tiempo."*

### Minuto 5:45 - 7:15 | Slide 5: Diagnóstico Comercial Global
> *"Hablemos de los números que mueven a Casa&Estilo. En el periodo analizado, la empresa generó una facturación bruta de $1,402 millones de pesos. Tras deducir $91.7 millones en promociones, las Ventas Netas reales se situaron en $1,310.7 millones de pesos, generando una Utilidad Bruta de $280.8 millones con un margen del 21.43% y un ticket promedio de $9,362 pesos por cliente. Aquí es donde nuestra corrección técnica cobró valor estratégico: de haber tomado el archivo crudo sin saneamiento, habríamos presentado al consejo una sobreestimación de ingresos de casi 92 millones de pesos. Nuestras cifras son contablemente exactas."*

### Minuto 7:15 - 8:45 | Slide 6: Rentabilidad por Categoría y Omnicanalidad
> *"Al desglosar la cartera por categoría, observamos que Recámara y Comedor son los motores de volumen, aportando más de $415 millones de pesos en ventas conjuntas. Sin embargo, Sala y Exterior ofrecen márgenes brutos superiores, rozando el 22%. En cuanto a canales, las tiendas físicas representan el 68% de los ingresos ($891M), pero el canal digital es una realidad contundente: Web aporta el 22.1% y la App el 9.8%. Lo más revelador es que el margen y el ticket promedio son prácticamente idénticos entre canales (~$9,370 pesos), lo que demuestra que el cliente digital tiene el mismo poder adquisitivo que el visitante de sala de exhibición."*

### Minuto 8:45 - 10:15 | Slide 7: Costo de Calidad y Devoluciones
> *"No todo es crecimiento: detectamos una fuga financiera significativa en las devoluciones. Se registraron 9,952 eventos de devolución que representaron $22.9 millones de pesos en reembolsos. Lo más preocupante no es la tasa global del 1.63%, sino las causas raíz: más del 40% de las devoluciones se originaron por daños físicos en el traslado o defectos de fábrica, mientras que otro 20% correspondió a insatisfacción con el producto en sala vs realidad. Esto evidencia una falla combinada entre el control de calidad del proveedor y los protocolos de embalaje y transporte de la flota propia."*

### Minuto 10:15 - 11:45 | Slide 8: Servicio al Cliente y Logística de Instalaciones
> *"Llegamos al hallazgo más alarmante de nuestra auditoría. En Casa&Estilo, el servicio de armado e instalación es un factor crítico de valor para comedores y recámaras. Sin embargo, de 6,500 órdenes de instalación, **únicamente el 34.7% se completó dentro del tiempo pactado**. En promedio, el cliente sufre un retraso de 3.8 días adicionales a la fecha comprometida. La consecuencia es directa: en las tiendas con peor cumplimiento como Monterrey 11 y Santa Catarina 6, el índice de satisfacción del cliente cae a 2.8 sobre 5. Estamos perdiendo lealtad en la última milla."*

### Minuto 11:45 - 13:00 | Slide 9: Diagnóstico de Abastecimiento e Inventarios
> *"En la cadena de suministro encontramos una paradoja operacional clásica de desbalance. Por un lado, tenemos 126 productos en rotura total de stock (existencia cero) en sucursales de alta demanda, perdiendo ventas inmediatas. Por otro lado, mantenemos $43.4 millones en productos en alerta de reorden tardío, coexistiendo con más de $2,300 millones de pesos inmovilizados en inventario excedente. Además, 1,348 órdenes de compra con proveedores permanecen en estatus pendiente con lead times que llegan a superar los 25 días. Falta una política de reposición orientada por la demanda real."*

### Minuto 13:00 - 15:00 | Slide 10: Hoja de Ruta Prescriptiva y Recomendaciones
> *"Para transformar estos hallazgos en resultados de negocio, sometemos a su consideración cinco recomendaciones estratégicas de ejecución inmediata:
> 1. **Reestructuración de la Logística de Instalación:** Implementar un sistema de ruteo dinámico y penalización por incumplimiento de SLA para elevar el cumplimiento del 34.7% al 85% en 90 días.
> 2. **Auditoría de Proveedores y Embalaje:** Establecer un protocolo estricto de recepción en muelle para reducir en 50% las devoluciones por daño y defecto, ahorrando $9.2 millones anuales.
> 3. **Optimización de Inventario Dinámico:** Configurar puntos de reorden automáticos basados en la velocidad de venta por sucursal, erradicando las 126 roturas de stock.
> 4. **Aceleración del Canal App:** Incentivar la compra en la App móvil (que hoy representa solo el 10%) mediante ofertas exclusivas en líneas de alta rentabilidad como Exterior y Salas.
> 5. **Monitoreo Continuo con el Data Mart:** Desplegar formalmente este modelo de Power Pivot y DAX en los comités mensuales para gobernar la empresa con datos auditados y una sola versión de la verdad.
> Con esto concluimos nuestra presentación. Agradecemos su atención y quedamos a su entera disposición para responder a sus preguntas. Muchas gracias."*
