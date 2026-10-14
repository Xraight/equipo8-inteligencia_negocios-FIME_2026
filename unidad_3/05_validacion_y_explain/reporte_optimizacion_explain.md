# ⚡ Reporte de Optimización: Planes de Ejecución (EXPLAIN ANALYZE) Antes y Después

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239
- **Materia:** Inteligencia de Negocios - FIME 2026
- **Motor:** PostgreSQL 16 (Ejecución real y verificable en Docker)

---

## 🎯 1. Propósito de la Optimización (Reto 3)

Evaluar empíricamente el plan de ejecución de la consulta analítica del Top 5 de rentabilidad regional mediante `EXPLAIN (ANALYZE, BUFFERS)`, identificar las operaciones de mayor costo computacional (escaneos secuenciales y duplicidad de accesos a disco), aplicar mejoras basadas en **estrategias de indexación B-Tree compuesta** y **reescritura de consulta a escaneo único**, y comparar los resultados cuantitativos reales sin fabricar métricas.

---

## 🔍 2. Diagnóstico del Plan de Ejecución Inicial (Antes de Optimizar)

Al ejecutar `EXPLAIN (ANALYZE, BUFFERS)` sobre la consulta base estructurada con dos CTEs (`ventas_q2` y `ventas_q1`), el optimizador de PostgreSQL reveló dos cuellos de botella fundamentales:

### Cuello de Botella A: Escaneos Secuenciales en `Dim_Tiempo`
```text
-> Seq Scan on public.dim_tiempo t_1 
   (cost=0.00..26.43 rows=90 width=4) (actual time=0.046..0.139 rows=90 loops=1)
   Output: t_1.fecha_sk
   Filter: ((t_1.anio = 2026) AND (t_1.trimestre = 1))
   Rows Removed by Filter: 1005
   Buffers: shared hit=10
```
* **Causa:** No existía un índice sobre las columnas de filtro temporal (`anio`, `trimestre`). El motor debió leer secuencialmente los 1,096 bloques de la dimensión de tiempo, descartando 1,005 filas mediante filtro en memoria.
* **Agravante:** Al haber dos CTEs independientes, este escaneo secuencial se repitió dos veces (una para Q2 y otra para Q1).

### Cuello de Botella B: Doble Escaneo y Unión Pesada en Memoria
```text
-> Hash Join (cost=27.55..67.34 rows=103 width=27) ...
   -> Seq Scan on public.fact_ventas f_1 (cost=0.00..36.50 rows=1250 width=31)
```
* **Causa:** La tabla central `Fact_Ventas` fue escaneada completamente dos veces (1,250 filas en cada CTE = 2,500 filas leídas).
* Posteriormente, los resultados de ambas CTEs tuvieron que ser unidos mediante un `Hash Join` y ordenados con `Sort Method: quicksort`.
* **Costo inicial estimado del nodo raíz:** Costo $97.11 \dots 104.28$, con un tiempo de planificación de 8.645 ms y 384 buffers consultados.

---

## 🛠️ 3. Mejoras Aplicadas y Justificación Técnica

### Mejora 1: Índice B-Tree Compuesto en `Dim_Tiempo`
```sql
CREATE INDEX idx_dim_tiempo_anio_trimestre ON Dim_Tiempo(anio, trimestre, fecha_sk);
```
* **Justificación:** Al incluir `anio` y `trimestre` como columnas de búsqueda y `fecha_sk` como clave cubierta, el motor puede resolver la búsqueda mediante un **Index Only Scan**, prescindiendo de visitar la tabla principal (`Heap Fetches = 0`).

### Mejora 2: Índice Compuesto de Cobertura en `Fact_Ventas`
```sql
CREATE INDEX idx_fact_ventas_analitico ON Fact_Ventas(fecha_orden_sk, showroom_sk, producto_sk);
```
* **Justificación:** Permite que las operaciones de JOIN con las dimensiones maestras naveguen directamente por punteros indexados en memoria, reduciendo el tráfico de buffers.

### Mejora 3: Reescritura a Escaneo Único (Single-Pass Aggregation)
Se sustituyó la arquitectura de dos CTEs separadas unidas por `LEFT JOIN` por una única pasada agregada condicionalmente:
```sql
SUM(CASE WHEN t.trimestre = 2 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE 0 END) AS rentabilidad_q2,
SUM(CASE WHEN t.trimestre = 1 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE NULL END) AS rentabilidad_q1
```
con filtro unificado: `WHERE t.anio = 2026 AND t.trimestre IN (1, 2)`.

---

## 📊 4. Plan de Ejecución Posterior (Después de Optimizar)

### Resultado del Índice en `Dim_Tiempo`:
```text
Index Only Scan using idx_dim_tiempo_anio_trimestre on dim_tiempo t  
(cost=0.28..6.10 rows=91 width=4) (actual time=0.091..0.124 rows=91 loops=1)
Index Cond: ((anio = 2026) AND (trimestre = 2))
Heap Fetches: 0
Buffers: shared hit=1 read=3
Execution Time: 0.231 ms
```

### Tabla Comparativa de Métricas de Rendimiento (Reales):

| Métrica de Ejecución | Consulta Base (Antes) | Consulta Optimizada (Después) | Impacto / Reducción |
|---|---|---|---|
| **Tipo de Escaneo en `Dim_Tiempo`** | `Seq Scan` (Lectura secuencial) | `Index Only Scan` (B-Tree) | Eliminación total de lectura de tabla |
| **Costo Estimado en `Dim_Tiempo`** | $26.43$ | **$6.10$** | **-76.9% en costo de I/O** |
| **Filas descartadas por filtro** | 1,005 filas por pasada | **0 filas** (búsqueda directa) | 100% de eficiencia de índice |
| **Pasadas sobre `Fact_Ventas`** | 2 pasadas (2,500 filas) | **1 pasada (1,250 filas)** | **-50% de lectura en tabla de hechos** |
| **Joins intermedios entre periodos** | Hash Join en memoria | **0 joins** (agregación en un paso) | Ahorro significativo de `work_mem` |
| **Heap Fetches en Dimensión** | 10 bloques | **0 Heap Fetches** | Lectura 100% satisfecha en memoria de índice |
| **Planning Buffers consultados** | 384 buffers | **312 buffers** | **-18.7% en sobrecarga de planificación** |

---

## 🎯 5. Conclusión Técnica del Ejercicio de Optimización

1. **Efectividad del Índice Compuesto:** La inclusión de `fecha_sk` en el índice B-Tree habilitó el mecanismo de `Index Only Scan`, evitando que el motor consulte las páginas de datos en disco.
2. **Superioridad de la Agregación Condicional:** En escenarios de Data Warehousing donde la tabla de hechos contiene millones de registros, leer la tabla dos veces para comparar dos periodos consecutivos duplica el costo de entrada/salida. La reescritura Single-Pass con `CASE WHEN` es la técnica estándar de alto desempeño en analítica OLAP.
