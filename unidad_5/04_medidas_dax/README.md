# 📂 Unidad 5 · 04 Medidas DAX

Este módulo recopila la especificación formal, fórmulas y guías de implementación de las medidas calculadas en el lenguaje **DAX (Data Analysis Expressions)**.

---

## 📑 Archivos del Módulo

- [`catalogo_medidas_dax.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/04_medidas_dax/catalogo_medidas_dax.md): Especificación detallada de las 6 medidas requeridas por el laboratorio más 4 medidas analíticas complementarias (unidades, ventas por año y crecimiento YoY).
- [`formulas_dax.dax`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/04_medidas_dax/formulas_dax.dax): Código plano DAX listo para ser copiado y pegado en el área de cálculo de Excel Power Pivot o Power BI.

---

## 🎯 Buenas Prácticas DAX Aplicadas
1. **Uso de `DIVIDE` sobre operador `/`:** Previene excepciones por división entre cero (`#¡DIV/0!`), retornando un valor alternativo seguro (`0` o `BLANK()`).
2. **Medidas Explícitas sobre Columnas Calculadas:** Todas las métricas se definen como medidas dinámicas para optimizar el consumo de memoria del motor VertiPaq.
3. **Reutilización de Medidas:** `[Margen Bruto]`, `[Margen %]` y `[Ticket Promedio]` referencian medidas existentes (`[Ventas]`, `[Costo]`, `[Transacciones]`), garantizando coherencia matemática.
