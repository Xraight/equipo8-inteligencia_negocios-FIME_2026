# 🤖 Prompt Inicial e Iteraciones: Reto 1 (Consulta Compleja Top 5)

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
### 🎯 Propósito: Generar la consulta compleja de rentabilidad regional Q2 vs Q1 2026

---

## 📝 1. Prompt Enviado a la Inteligencia Artificial (Plantilla Obligatoria)

```text
Actúa como analista SQL sénior especializado en PostgreSQL 16 y MySQL 8.
Trabajamos con la empresa Casa&Estilo (retail de muebles, diseño interior y decoración de alta gama) y necesitamos construir un reporte analítico que identifique los cinco productos con mayor rentabilidad neta en cada región geográfica durante el segundo trimestre de 2026 (Q2 2026: 2026-04-01 al 2026-06-30), comparando su desempeño frente al primer trimestre de 2026 (Q1 2026: 2026-01-01 al 2026-03-31).

El grano de la tabla de hechos es: una fila representa un producto o variante específica dentro de una línea de detalle de una orden de venta.

El esquema disponible es el siguiente:
- Fact_Ventas (fact_venta_id PK, fecha_orden_sk FK, cliente_sk FK, producto_sk FK, showroom_sk FK, asesor_sk FK, canal_sk FK, orden_id, cantidad, precio_unitario, costo_unitario, monto_subtotal, monto_costo_total, monto_descuento_prorrateado, monto_envio_prorrateado, monto_venta_neta, ganancia_bruta, dias_para_entrega, retraso_dias).
- Dim_Tiempo (fecha_sk PK [YYYYMMDD], fecha_completa, anio, mes, dia, nombre_mes, trimestre [1..4], dia_semana).
- Dim_Producto (producto_sk PK, variante_id_bk, producto_id_bk, nombre_producto, categoria, coleccion, marca, color, material, tamano).
- Dim_Showroom (showroom_sk PK, showroom_id_bk, nombre_showroom, ciudad, zona [Región de negocio: Norte, Centro, Occidente, Sur, Bajío]).
- Dim_Cliente (cliente_sk PK, cliente_id_bk, nombre, tipo_cliente, ciudad, zona).
- Dim_Canal (canal_sk PK, nombre_canal).
- Dim_Asesor (asesor_sk PK, nombre_asesor, porcentaje_comision).

Las reglas para calcular rentabilidad y filtrar registros son:
1. Región: Se obtiene de la dimensión de la sucursal (Dim_Showroom.zona).
2. Ventas Netas: Fact_Ventas.monto_venta_neta.
3. Costo Total: Fact_Ventas.monto_costo_total.
4. Particularidad de Casa&Estilo: La rentabilidad debe considerar el costo de entrega e instalación prorrateado (Fact_Ventas.monto_envio_prorrateado). Por tanto:
   Rentabilidad = monto_venta_neta - monto_costo_total - monto_envio_prorrateado.
5. Agrupación: La pregunta de negocio solicita el Top 5 de "productos", no de "variantes". Se debe consolidar por producto_id_bk y nombre_producto.
6. Periodos: Comparar Trimestre 2 de 2026 con Trimestre 1 de 2026.
7. Casos sin histórico: Si un producto no registra ventas en Q1 2026, evitar división por cero en la variación porcentual y clasificarlo con un indicador de periodo anterior.

La salida debe contener las siguientes columnas exactas:
- region (Zona del showroom)
- posicion_region (Ranking del 1 al 5 dentro de su región)
- producto_id_bk (Identificador del producto)
- nombre_producto (Nombre del producto)
- rentabilidad_q2_2026 (Rentabilidad acumulada en Q2)
- rentabilidad_q1_2026 (Rentabilidad acumulada en Q1, mostrar 0.00 si no hubo)
- variacion_absoluta (rentabilidad_q2 - rentabilidad_q1)
- variacion_porcentual (Variación % evitando división entre cero)
- indicador_periodo_anterior ('Crecimiento', 'Decrecimiento', 'Sin cambio' o 'Nuevo en periodo (Sin histórico)')

Antes de escribir SQL, enumera tus supuestos técnicos y de negocio. Después explica detalladamente cada CTE, JOIN y función de ventana utilizada.
```

---

## 💡 2. Respuesta Inicial Propuesta por la IA

### Supuestos declarados por la IA:
1. Cada línea de hecho ya contiene los importes prorrateados de flete y descuento, por lo que sumarlos directamente no generará duplicación de importes.
2. La clave `Dim_Showroom.zona` provee la granularidad regional adecuada para la segmentación.
3. Se asume que `DENSE_RANK()` es la función apropiada para ordenar por rentabilidad descendente reiniciando el contador por región.
4. Para la variación porcentual, cuando $Q_1$ sea nulo o cero se retornará `NULL` para salvaguardar la operación aritmética.

### Código SQL propuesto por la IA (Consulta Inicial):
```sql
WITH ventas_q2 AS (
    SELECT 
        s.zona AS region,
        p.producto_sk,
        p.nombre_producto,
        SUM(f.monto_venta_neta - f.monto_costo_total) AS rentabilidad_q2
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 2
    GROUP BY s.zona, p.producto_sk, p.nombre_producto
),
ventas_q1 AS (
    SELECT 
        s.zona AS region,
        p.producto_sk,
        SUM(f.monto_venta_neta - f.monto_costo_total) AS rentabilidad_q1
    FROM Fact_Ventas f
    JOIN Dim_Tiempo t ON f.fecha_orden_sk = t.fecha_sk
    JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
    JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
    WHERE t.anio = 2026 AND t.trimestre = 1
    GROUP BY s.zona, p.producto_sk
),
consolidado AS (
    SELECT 
        q2.region,
        q2.producto_sk,
        q2.nombre_producto,
        q2.rentabilidad_q2,
        COALESCE(q1.rentabilidad_q1, 0) AS rentabilidad_q1,
        (q2.rentabilidad_q2 - COALESCE(q1.rentabilidad_q1, 0)) AS variacion_absoluta,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL OR q1.rentabilidad_q1 = 0 THEN NULL
            ELSE ROUND(((q2.rentabilidad_q2 - q1.rentabilidad_q1) / q1.rentabilidad_q1) * 100, 2)
        END AS variacion_porcentual,
        CASE 
            WHEN q1.rentabilidad_q1 IS NULL THEN 'Sin datos previos'
            WHEN q2.rentabilidad_q2 > q1.rentabilidad_q1 THEN 'Crecimiento'
            ELSE 'Decrecimiento'
        END AS indicador_periodo_anterior,
        RANK() OVER (PARTITION BY q2.region ORDER BY q2.rentabilidad_q2 DESC) AS posicion_region
    FROM ventas_q2 q2
    LEFT JOIN ventas_q1 q1 ON q2.region = q1.region AND q2.producto_sk = q1.producto_sk
)
SELECT * 
FROM consolidado 
WHERE posicion_region <= 5
ORDER BY region, posicion_region;
```

---

## 🔍 3. Auditoría Crítica del Equipo: Hallazgos, Errores y Decisiones

El equipo revisó la propuesta línea por línea contra el DDL, el caso de estudio de Casa&Estilo y la rúbrica docente, detectando **4 discrepancias críticas**:

| # | Observación / Error en Propuesta IA | Decisión del Equipo | Evidencia / Justificación |
|---|---|---|---|
| **1** | **Omisión del costo de entrega en la rentabilidad:** La IA calculó `monto_venta_neta - monto_costo_total`, ignorando el costo de flete. | **Corregir la fórmula:** Restar explícitamente `f.monto_envio_prorrateado`. | Requisito explícito de la página 2 del PDF: *"Casa&Estilo: Rentabilidad considerando entrega o instalación"*. |
| **2** | **Confusión de grano (Variante vs Producto):** La IA agrupó por `p.producto_sk` (variante), lo que provocó que el mismo producto apareciera repetido en el Top 5 de una región (ej. Sofá Oslo gris y Sofá Oslo beige). | **Agrupar a nivel producto:** Agrupar por `p.producto_id_bk` y `p.nombre_producto`. | El reto exige los 5 *productos* más rentables. La suma debe consolidar todas las variantes de un producto. |
| **3** | **Uso de `RANK()` en lugar de `DENSE_RANK()`:** `RANK()` deja huecos numéricos ante empates, lo cual puede truncar arbitrariamente los puestos 4 y 5. | **Adoptar `DENSE_RANK()`:** Asegura una secuencia estricta de posiciones $1, 2, 3, 4, 5$. | Buenas prácticas de analítica OLAP y rúbrica técnica. |
| **4** | **Inclusión de columna BK requerida:** La IA devolvió `producto_sk` en vez del identificador de negocio del producto (`producto_id_bk`). | **Incluir `p.producto_id_bk`** en la proyección final. | Cumplimiento del contrato de salida: *"Identificador y nombre del producto"*. |

---

## 🚀 4. Iteración y Versión Final Validada

Tras incorporar las correcciones del equipo, se generó la versión final almacenada en [`unidad_3/04_consultas_sql/02_consulta_final_validada.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/02_consulta_final_validada.sql), la cual fue ejecutada y verificada exitosamente en el contenedor PostgreSQL de Docker.
