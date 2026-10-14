# 📄 Informe Ejecutivo y Conclusiones: Proyecto Data Mart Casa&Estilo

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630 (Responsable de Modelo y Reglas de Negocio)
- **Rafael Jesús Collazo Hernández** - 2169304 (Responsable de IA y Auditoría de Datos)
- **Sergio Jaziel Butzmann Martinez** - 2163239 (Analista SQL y Optimización de BD)
- **Materia:** Inteligencia de Negocios - FIME 2026
- **Entregable:** Unidad 3 - Entregable 9 (Conclusión y Hallazgos)

---

## 💼 1. Hallazgos de Negocio y Decisiones Estratégicas para Casa&Estilo

El análisis comparativo del segundo trimestre ($Q_2$) frente al primer trimestre ($Q_1$) de 2026 reveló patrones comerciales contundentes para la dirección de Casa&Estilo:

### 1.1. Dominancia Territorial de la Zona Norte y Margen Neto
- **Hallazgo:** La Región Norte concentra los productos de mayor margen neto de toda la cadena: el *Sofá Seccional Oslo* generó **$1,153,664.59** (+3.66% vs $Q_1$) y la *Mesa de Comedor Kioto* alcanzó **$1,115,932.22** (+4.45% vs $Q_1$). La *Cama King Size Estocolmo* creció un notable **+6.60%**, aportando $955,971.22.
- **Decisión de Negocio Recomendada:** Expandir el inventario de exhibición en los showrooms de San Pedro Garza García y Valle Oriente para estas tres familias estrella, y negociar convenios de volumen con los proveedores nórdicos (*Nordic Living* y *Casa&Estilo Signature*) para mitigar los costos de adquisición en el segundo semestre.

### 1.2. Impacto Crítico del Costo de Envío en la Rentabilidad Neta
- **Hallazgo:** Al deducir el costo logístico de entrega e instalación (`monto_envio_prorrateado`) —requisito neurálgico modelado para Casa&Estilo— se constató que piezas de gran volumen y peso (como el *Sofá Chaiselongue Malmö* y la *Credenza Buffet Milán*) absorbieron entre el 3.5% y el 5.2% de su margen bruto en costos de transporte hacia zonas foráneas o despachos e-commerce.
- **Decisión de Negocio Recomendada:** Implementar un esquema de tarificación dinámica de flete o requerir un monto mínimo de compra en líneas pesadas para subsidiar la entrega en compras en línea.

### 1.3. Contracción de Demanda en Zonas Centro y Bajío
- **Hallazgo:** En la Región Centro, el *Sofá Seccional Oslo* experimentó una caída del **-6.22%** ($54,482.53 pesos menos de margen) y en el Bajío la *Cama Estocolmo* descendió un **-8.98%**. En contraparte, artículos de oficina y accesorios como la *Silla Ergonómica Zurich* (+6.76% en Centro) y el *Espejo Verona* (+4.86% en Bajío) amortiguaron el desempeño.
- **Decisión de Negocio Recomendada:** Lanzar una campaña de financiamiento a meses sin intereses enfocada en salas y recámaras en Polanco y Santa Fe, aprovechando el repunte de diseño interior corporativo.

---

## ⚠️ 2. Limitaciones del Modelo Dimensional y Propuestas de Ajuste

Durante la implementación y consulta del Data Mart se identificaron las siguientes restricciones estructurales:
1. **Ausencia de Dimensión de Proveedor Logístico:** Actualmente, el flete prorrateado se almacena como una métrica en `Fact_Ventas`. Para un análisis más profundo de costos de transporte, se recomienda incorporar una dimensión `Dim_Transportista` que detalle tipo de unidad (propia vs. paquetería externa) y zona de cobertura.
2. **Falta de Desglose de Motivos de Cancelación / Devolución:** Aunque se modelaron campos de entrega y retrasos, no existe una dimensión degenerada de causalidad (ej. defecto de fábrica, daño en flete, arrepentimiento del cliente). Integrar este atributo en la Unidad 4 enriquecerá el cálculo de pérdida neta.

---

## 🤖 3. Aprendizaje sobre el Uso de Inteligencia Artificial

La asistencia de IA generativa a lo largo de los cuatro retos técnicos brindó lecciones metodológicas invaluables:
1. **Aceleración Inicial y Esqueleto SQL:** La IA demostró una capacidad sobresaliente para estructurar sintácticamente la consulta base (CTEs, proyecciones y funciones de ventana), reduciendo el tiempo de desarrollo inicial en más de un 60%.
2. **Peligro de Alucinación y Pérdida de Contexto del Negocio:** La IA inicialmente omitió el costo de envío prorrateado en la fórmula de rentabilidad y agrupó erróneamente por variante (`producto_sk`) en lugar de por producto maestro (`producto_id_bk`), repitiendo artículos en el Top 5. **Esto evidencia que una consulta generada por IA sin auditoría humana estricta es inviable en entornos empresariales.**
3. **Alto Valor en Diagnóstico y Explicación:** La IA fue sumamente precisa al explicar la causa raíz del error 1055 (`ONLY_FULL_GROUP_BY`), permitiendo al equipo comprender con rigor el estándar SQL y justificar matemáticamente la solución.

---

## 🎤 4. Guión para la Presentación Oral (Defensa de 5 Minutos)

| Minuto | Integrante Responsable | Tema de Exposición | Apoyo Visual en Vivo |
|---|---|---|---|
| **0:00 - 1:00** | **Arely Carrillo** | **Presentación de Casa&Estilo y Modelo Dimensional:** Explicación del Star Schema de Unidad 2, justificación del grano (línea de orden) y cómo se definió la rentabilidad restando el costo de entrega e instalación prorrateado. | Diagrama ER en Draw.io y ficha de decisiones. |
| **1:00 - 2:15** | **Sergio Jaziel Butzmann** | **Decisión Clave en SQL y Prevención de Errores:** Explicación de la consulta con CTEs, uso de `DENSE_RANK()` para el Top 5 regional y demostración de cómo se diagnosticó y resolvió el error de agrupación 1055 / 42803. | Código SQL en `02_consulta_final_validada.sql` y terminal con error 1055. |
| **2:15 - 3:30** | **Sergio Jaziel Butzmann** | **Optimización y Benchmarking con EXPLAIN:** Demostración del plan de ejecución antes vs. después, mostrando la reducción del 76.9% en costo con el índice B-Tree compuesto y la reescritura Single-Pass. | Planes de `EXPLAIN (ANALYZE, BUFFERS)` en `reporte_optimizacion_explain.md`. |
| **3:30 - 4:15** | **Rafael Collazo** | **Automatización con Stored Procedure:** Demostración de la llamada parametrizada (`sp_reporte_rentabilidad_top5(2026, 2)`) y manejo dinámico del trimestre previo y casos sin histórico. | Ejecución en vivo de `sp_reporte_rentabilidad_top5` en PostgreSQL. |
| **4:15 - 5:00** | **Todo el Equipo** | **Hallazgos de Negocio y Cierre:** Síntesis de los 5 productos líderes en Norte, Centro y Sur, recomendaciones para inventario y sesión de preguntas del docente. | Tabla de resultados del Top 5 consolidado. |
