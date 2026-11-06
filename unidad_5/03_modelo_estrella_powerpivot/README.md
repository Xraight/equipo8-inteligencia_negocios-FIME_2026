# 📂 Unidad 5 · 03 Modelo Estrella en Power Pivot

Este módulo documenta la arquitectura dimensional del **Data Mart**, la configuración de relaciones en Power Pivot y las consideraciones técnicas de filtrado y modelado temporal.

---

## 📑 Documentos del Módulo

- [`modelo_dimensional_estrella.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/03_modelo_estrella_powerpivot/modelo_dimensional_estrella.md): Especificación del esquema estrella, cardinalidades 1:N, diagnóstico de relaciones y directrices de inteligencia de tiempo.

---

## 🔑 Conceptos Centrales
- **Tabla de Hechos (`FACT_VENTAS`):** Contiene métricas cuantitativas acumulativas (cantidad, monto, costo) a nivel de transacción individual.
- **Dimensiones (`DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_TIEMPO`):** Proveen el contexto analítico y los atributos de corte para slicing y dicing.
- **Filtrado Unidireccional:** El contexto de filtro fluye desde las dimensiones hacia la tabla de hechos, garantizando segmentaciones eficientes y sin ambigüedad.
