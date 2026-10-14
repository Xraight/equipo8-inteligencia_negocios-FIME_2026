# 📊 Unidad 3: Consultas SQL Empresariales con Apoyo de IA

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630 (Responsable del Modelo y Reglas de Negocio)
- **Rafael Jesús Collazo Hernández** - 2169304 (Responsable de IA y Auditoría)
- **Sergio Jaziel Butzmann Martinez** - 2163239 (Analista SQL y Optimización de BD)
- **Materia:** Inteligencia de Negocios - FIME 2026
- **Continuidad:** Actividad 2 de la Unidad 2

---

## 🎯 Propósito del Módulo

Desarrollar y validar un reporte analítico en SQL reproducible para **Casa&Estilo** que identifique los **cinco productos más rentables en cada región geográfica durante el segundo trimestre de 2026 ($Q_2$)**, comparando su desempeño frente al **primer trimestre de 2026 ($Q_1$)**, incorporando la deducción del costo de flete e instalación prorrateado (`monto_envio_prorrateado`), depurando errores estrictos de agregación (Error 1055 / SQLSTATE 42803), optimizando el plan de ejecución (`EXPLAIN`) mediante indexación compuesta y consolidando la lógica en un **Stored Procedure** parametrizado.

---

## 📁 Mapeo de Entregables a la Estructura del Repositorio

La entrega se encuentra estrictamente organizada en las 7 carpetas recomendadas por la rúbrica oficial:

| Núm | Entregable Oficial | Archivo o Evidencia | Carpeta / Enlace Directo |
|:---:|---|---|---|
| **1** | **Modelo de referencia** | Diagrama estrella de la Unidad 2 y definición formal del grano. | [`01_modelo_unidad_2/grano_y_diccionario_datos.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/01_modelo_unidad_2/grano_y_diccionario_datos.md)<br>[`Casa_Estilo_Diagrama_ER.drawio`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/01_modelo_unidad_2/Casa_Estilo_Diagrama_ER.drawio) |
| **2** | **Base reproducible** | DDL y script de carga determinista de 1,250 filas simuladas (>1,000 req.). | [`02_ddl_y_datos/01_ddl_schema.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/01_ddl_schema.sql)<br>[`02_ddl_y_datos/02_carga_datos.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/02_carga_datos.sql)<br>[`02_ddl_y_datos/03_verificacion_calidad_datos.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/03_verificacion_calidad_datos.sql) |
| **3** | **Definiciones** | Ficha de decisiones: rentabilidad con flete, región, periodos y las 5 preguntas resueltas. | [`01_modelo_unidad_2/ficha_decisiones_negocio.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/01_modelo_unidad_2/ficha_decisiones_negocio.md) |
| **4** | **Prompts** | Prompt inicial bajo plantilla obligatoria, respuestas de IA, auditoría e iteraciones. | [`03_prompts_ia/01_prompt_inicial_reto1.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/03_prompts_ia/01_prompt_inicial_reto1.md)<br>[`03_prompts_ia/registro_decisiones_ia.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/03_prompts_ia/registro_decisiones_ia.md) |
| **5** | **Consulta SQL** | Versión inicial de IA y versión final validada (ambas identificadas). | [`04_consultas_sql/01_consulta_inicial_ia.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/01_consulta_inicial_ia.sql)<br>[`04_consultas_sql/02_consulta_final_validada.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/02_consulta_final_validada.sql)<br>[`04_consultas_sql/03_consultas_control_auditoria.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/03_consultas_control_auditoria.sql) |
| **6** | **Depuración** | Provocación de error 1055 (`ONLY_FULL_GROUP_BY` / 42803), diagnóstico y corrección. | [`05_validacion_y_explain/01_depuracion_error_1055.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/01_depuracion_error_1055.sql)<br>[`05_validacion_y_explain/reporte_depuracion_1055.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/reporte_depuracion_1055.md) |
| **7** | **Optimización** | Planes de ejecución `EXPLAIN (ANALYZE, BUFFERS)` antes y después con índice compuesto y reescritura. | [`05_validacion_y_explain/02_optimizacion_explain.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/02_optimizacion_explain.sql)<br>[`05_validacion_y_explain/reporte_optimizacion_explain.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/reporte_optimizacion_explain.md) |
| **8** | **Stored procedure** | Script de creación de la rutina parametrizada, llamadas de prueba y evidencia de salida. | [`06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql)<br>[`06_stored_procedure/02_llamadas_de_prueba.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/02_llamadas_de_prueba.sql)<br>[`06_stored_procedure/documentacion_stored_procedure.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/documentacion_stored_procedure.md) |
| **9** | **Conclusión** | Informe analítico de 1 página: hallazgos comerciales, limitaciones, juicio crítico de IA y guión oral de 5 min. | [`07_conclusion/conclusion_final.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/07_conclusion/conclusion_final.md) |

---

## 🚀 Guía Rápida de Ejecución Reproducible con Docker

De acuerdo con la regla del proyecto de **no instalar dependencias en el sistema anfitrión**:

```bash
# 1. Asegurar que el contenedor de PostgreSQL 16 esté activo
docker compose up -d postgres

# 2. Recrear el esquema limpio y cargar los datos simulados
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/01_ddl_schema.sql"
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/02_carga_datos.sql"

# 3. Auditar la calidad de los datos (> 1000 filas, 5 regiones, Q1 y Q2 2026)
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/03_verificacion_calidad_datos.sql"

# 4. Ejecutar la consulta final validada del Reto de Negocio
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/04_consultas_sql/02_consulta_final_validada.sql"

# 5. Ejecutar los scripts de control y auditoría de grano
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/04_consultas_sql/03_consultas_control_auditoria.sql"

# 6. Compilar y probar el Stored Procedure
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql"
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/06_stored_procedure/02_llamadas_de_prueba.sql"
```

---

## 🔄 Integración Continua (CI/CD)

El pipeline configurado en [`.github/workflows/ci.yml`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/.github/workflows/ci.yml) valida automáticamente en cada `push` o `pull request`:
1. Compilación del esquema DDL en una base de datos PostgreSQL limpia.
2. Población y pruebas de calidad de datos sintéticos.
3. Compilación y llamadas de prueba del Stored Procedure.
4. Ejecución íntegra de las consultas analíticas SQL sin errores.
