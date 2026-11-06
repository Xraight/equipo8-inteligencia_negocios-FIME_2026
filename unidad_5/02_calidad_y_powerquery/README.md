# 📂 Unidad 5 · 02 Calidad y Power Query

Este módulo contiene la documentación técnica del proceso de extracción, transformación y carga (ETL) ligera ejecutada mediante **Power Query**.

---

## 📄 Archivos del Módulo

- [`perfilado_y_calidad.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/02_calidad_y_powerquery/perfilado_y_calidad.md): Matriz completa de validación, perfilado de columnas, control de nulos, duplicados y reglas de negocio para las cuatro tablas.
- [`scripts_m_powerquery.m`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/02_calidad_y_powerquery/scripts_m_powerquery.m): Código formal en lenguaje M para las consultas `FACT_VENTAS`, `DIM_PRODUCTO`, `DIM_CLIENTE` y `DIM_TIEMPO`.

---

## 💡 Aspectos Clave de Calidad
1. **Conservación de Granularidad:** 1,200 transacciones íntegras sin pérdida de filas.
2. **Coerción de Tipos:** Montos y costos como decimales precisos; cantidades y llaves como enteros de 64 bits; fechas como objetos nativos de fecha.
3. **Carga en Modelo:** Opción "Solo crear conexión" + "Agregar al Modelo de datos" para habilitar las funcionalidades de Power Pivot.
