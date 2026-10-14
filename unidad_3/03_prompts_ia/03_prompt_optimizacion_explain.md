# ⚡ Prompt y Optimización: Reto 3 (Análisis de Planes de Ejecución EXPLAIN)

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
### 🎯 Propósito: Diagnosticar cuellos de botella con EXPLAIN y formular estrategias de optimización con IA.

---

## 📝 1. Prompt Enviado a la Inteligencia Artificial

```text
Actúa como Administrador de Base de Datos (DBA) y especialista en rendimiento de PostgreSQL 16 y MySQL 8.
Ejecutamos un EXPLAIN (ANALYZE, BUFFERS) sobre la consulta analítica del Top 5 de rentabilidad regional Q2 vs Q1 2026 en nuestro Data Mart de Casa&Estilo.

Observamos los siguientes puntos en el plan de ejecución:
1. Escaneos secuenciales completos sobre la tabla Dim_Tiempo (Seq Scan on public.dim_tiempo t_1, cost=0.00..26.43, rows=90, eliminando 1,005 filas por filtro de anio=2026 y trimestre=1 o 2).
2. La consulta original estructura dos CTEs independientes (ventas_q2 y ventas_q1), lo que ocasiona que Fact_Ventas sea escaneada dos veces consecutivas (1,250 filas en cada rama) y que las dimensiones Dim_Tiempo, Dim_Showroom y Dim_Producto sean unidas dos veces en memoria mediante Hash Joins y Nested Loops.
3. El plan requiere un Hash Join intermedio adicional entre ambas CTEs sobre (region, producto_id_bk).

Solicitamos tu asesoría técnica para:
a) Proponer una estrategia de indexación B-Tree en las dimensiones y tabla de hechos para eliminar los escaneos secuenciales y permitir Index Only Scans.
b) Evaluar si es posible reescribir la consulta SQL para consolidar el cálculo en una sola pasada sobre Fact_Ventas (Single-Pass Aggregation) utilizando agregaciones condicionales (CASE WHEN / FILTER), reduciendo el costo computacional.
c) Justificar técnica y matemáticamente por qué la combinación de índices y reescritura es superior a la consulta base.
```

---

## 💡 2. Respuesta y Propuesta Técnica de la IA

### Recomendación A: Estrategia de Indexación
1. **Índice Compuesto en Dim_Tiempo:**
   ```sql
   CREATE INDEX idx_dim_tiempo_anio_trimestre ON Dim_Tiempo(anio, trimestre, fecha_sk);
   ```
   *Beneficio:* Permite al optimizador resolver los filtros de año y trimestre mediante un **Index Only Scan**, reduciendo el costo de 26.43 a ~6.10 y eliminando la lectura de bloques de tabla (`Heap Fetches = 0`).
2. **Índice Compuesto de Cobertura en Fact_Ventas:**
   ```sql
   CREATE INDEX idx_fact_ventas_analitico ON Fact_Ventas(fecha_orden_sk, showroom_sk, producto_sk);
   ```
   *Beneficio:* Acelera drásticamente los `Hash Joins` y `Nested Loops` al navegar directamente por las llaves foráneas más consultadas.

### Recomendación B: Reescritura a Escaneo Único (Single-Pass Aggregation)
En lugar de forzar dos lecturas completas de `Fact_Ventas` con dos CTEs separadas unidas por un `LEFT JOIN`, se consolida la agregación en una sola pasada:
```sql
SUM(CASE WHEN t.trimestre = 2 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE 0 END) AS rentabilidad_q2,
SUM(CASE WHEN t.trimestre = 1 THEN (f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) ELSE NULL END) AS rentabilidad_q1
```
*Filtro Where Unificado:* `WHERE t.anio = 2026 AND t.trimestre IN (1, 2)`.

---

## 🔍 3. Decisión y Validación Experimental del Equipo

El equipo aprobó e implementó ambas propuestas en la base de datos PostgreSQL, ejecutando pruebas reales documentadas en [`unidad_3/05_validacion_y_explain/reporte_optimizacion_explain.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/reporte_optimizacion_explain.md):

1. **Evidencia del Índice:**
   - `Dim_Tiempo` pasó de `Seq Scan` (costo 26.43) a `Index Only Scan` (costo 6.10, 0.231 ms de ejecución).
2. **Evidencia de la Reescritura:**
   - La tabla `Fact_Ventas` pasó de leerse 2 veces (2,500 filas procesadas) a leerse **1 sola vez** (1,250 filas).
   - Se eliminó el `Hash Join` intermedio entre CTEs, optimizando el uso de memoria de trabajo (`work_mem`).
