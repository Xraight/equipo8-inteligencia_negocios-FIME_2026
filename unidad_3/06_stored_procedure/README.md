# 06 - Stored Procedures y Automatización Analítica

## 🎯 Objetivo General
Encapsular y automatizar la lógica analítica validada del Data Mart en un Stored Procedure / Función parametrizada que permita generar reportes periódicos de rentabilidad regional por año y trimestre de manera reutilizable.

---

## 📦 Contenido del Directorio

| Archivo | Tipo | Descripción |
|---|---|---|
| [`01_sp_reporte_rentabilidad_top5.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql) | DDL / PL/pgSQL | Definición de la función `sp_reporte_rentabilidad_top5(p_anio INT, p_trimestre INT)` y procedimiento `pr_ejecutar_reporte_rentabilidad`, incluyendo versión para MySQL 8. |
| [`02_llamadas_de_prueba.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/02_llamadas_de_prueba.sql) | Script de Prueba | Invocaciones ejecutables para el escenario objetivo (Q2 vs Q1 2026), escenario límite (Q1 2026 vs Q4 2025) y llamada procedural con `CALL`. |
| [`documentacion_stored_procedure.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/documentacion_stored_procedure.md) | Documento Técnico | Especificación detallada de parámetros, lógica interna, mitigación de fallos por división entre cero y evidencia de salida capturada. |

---

## 🚀 Instrucciones de Ejecución

```bash
# 1. Compilar la función y procedimiento en PostgreSQL (Docker)
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql"

# 2. Ejecutar las pruebas unitarias y de integración
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/06_stored_procedure/02_llamadas_de_prueba.sql"
```
