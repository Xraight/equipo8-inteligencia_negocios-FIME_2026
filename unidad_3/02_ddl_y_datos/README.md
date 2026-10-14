# 02 - DDL del Esquema y Carga de Datos Simulados

## 🎯 Objetivo General
Suministrar los scripts DDL de creación física del esquema estrella y la población determinista de datos simulados para el Data Mart de **Casa&Estilo**, asegurando una base de datos reproducible y ejecutable en contenedores Docker y en el pipeline de CI/CD.

---

## 📦 Contenido del Directorio

| Archivo | Tipo | Descripción |
|---|---|---|
| [`01_ddl_schema.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/01_ddl_schema.sql) | DDL SQL | Script de creación idempotente de las 6 dimensiones y la tabla de hechos con claves primarias, foráneas e índices base en PostgreSQL 16. |
| [`02_carga_datos.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/02_carga_datos.sql) | DML SQL | Población determinista de 1,250 filas en `Fact_Ventas` y dimensiones maestras con fórmulas de prorrateo de descuentos y costos de flete. |
| [`03_verificacion_calidad_datos.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/03_verificacion_calidad_datos.sql) | Auditoría SQL | Consultas automatizadas que certifican integridad referencial, volumen (>1000 filas), cobertura Q1/Q2 2026 y ausencia de inconsistencias matemáticas. |

---

## 📋 Requisitos Cumplidos (Rúbrica Unidad 3)

| Aspecto | Requisito de Rúbrica | Estado en Casa&Estilo | Evidencia |
|---|---|---|---|
| **Periodos** | Dos trimestres consecutivos completos | ✅ Cumple | $Q_1$ 2026 (621 filas, Ene-Mar) y $Q_2$ 2026 (629 filas, Abr-Jun). |
| **Cobertura Regional** | Al menos tres regiones con suficientes productos | ✅ Cumple (5 regiones) | Norte (15 variantes), Centro (10), Sur (5), Bajío (5), Occidente (5). |
| **Volumen** | Mínimo 1,000 filas en tabla de hechos | ✅ Cumple | 1,250 filas generadas en `Fact_Ventas`. |
| **Integridad** | Claves foráneas válidas y montos coherentes | ✅ Cumple | 0 huérfanos, subtotales y costos validados contra cantidades unitarias. |
| **Particularidad** | Considerar costo de entrega/instalación | ✅ Cumple | `monto_envio_prorrateado` integrado a nivel línea. |

---

## 🐳 Instrucciones de Ejecución con Docker

Para reproducir la base de datos en un entorno limpio sin instalar herramientas en el sistema operativo:

```bash
# 1. Iniciar el servicio PostgreSQL con Docker Compose
docker compose up -d postgres

# 2. Ejecutar la creación de tablas
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/01_ddl_schema.sql"

# 3. Poblar los datos simulados
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/02_carga_datos.sql"

# 4. Validar la calidad de los datos cargados
docker exec -i casa_estilo_postgres psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/03_verificacion_calidad_datos.sql"
```
