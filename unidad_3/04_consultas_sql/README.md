# 04 - Consultas SQL Analíticas y Validación de Negocio

## 🎯 Objetivo General
Contener las consultas analíticas empresariales en lenguaje SQL orientadas a responder el reto de negocio de la Unidad 3 para **Casa&Estilo**: identificación del Top 5 de productos más rentables por región en el segundo trimestre de 2026 frente al primer trimestre, respetando el grano y las reglas comerciales del caso.

---

## 📦 Contenido del Directorio

| Archivo | Tipo | Descripción |
|---|---|---|
| [`01_consulta_inicial_ia.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/01_consulta_inicial_ia.sql) | SQL Inicial | Primera propuesta generada por IA (conservada para trazabilidad y contraste con los errores de grano y omisión de flete). |
| [`02_consulta_final_validada.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/02_consulta_final_validada.sql) | SQL Validado | Consulta compleja definitiva: CTEs, consolidación a nivel producto, descuento de flete, `DENSE_RANK()` particionado y control de división entre cero. |
| [`03_consultas_control_auditoria.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/03_consultas_control_auditoria.sql) | Auditoría SQL | Pruebas de control numérico: verificación de $\le 5$ productos por región, preservación estricta del grano (sin producto cartesiano) y muestra manual contrastada. |
| [`04_diferencias_sintaxis_motores.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/04_diferencias_sintaxis_motores.sql) | Comparativa | Especificación de equivalencias sintácticas entre PostgreSQL 16 y MySQL 8. |

---

## 📊 Resumen de Resultados del Top 5 por Región (Q2 vs Q1 2026)

La consulta final arroja exactamente 25 filas (5 regiones $\times$ 5 productos líderes):

- **Región Norte:** Liderada por el *Sofá Seccional Oslo* ($1,153,664.59 en Q2, +3.66%) y la *Mesa de Comedor Kioto* ($1,115,932.22, +4.45%).
- **Región Centro:** Encabezada por el *Sofá Seccional Oslo* ($821,165.30) y la *Cama King Size Estocolmo* ($259,762.40).
- **Región Sur:** Liderada por la *Cama King Size Estocolmo* ($956,828.55) y el *Sofá Chaiselongue Malmö* ($349,504.02).
- **Región Occidente:** Dominada por la *Mesa de Comedor Kioto* ($846,878.10) y el *Sofá Seccional Oslo* ($291,741.94).
- **Región Bajío:** Encabezada por la *Cama King Size Estocolmo* ($247,227.10) y la *Silla Ergonómica Zurich* ($236,064.37).
