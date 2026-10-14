# 📋 Ficha de Decisiones de Negocio y Reglas Analíticas

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239
- **Materia:** Inteligencia de Negocios - FIME 2026

---

## 🎯 1. Propósito del Documento

Este documento formaliza las definiciones de negocio, reglas de cálculo, criterios de filtro y acuerdos analíticos previos a la construcción de las consultas SQL empresariales y el procedimiento almacenado para el Data Mart de **Casa&Estilo**, dando cumplimiento estricto a las especificaciones de la **Unidad 3**.

---

## ❓ 2. Resolución de las 5 Preguntas Previas a la Programación

Antes de redactar el código SQL, el equipo analizó y consensuó las siguientes respuestas basadas en el modelo dimensional de Casa&Estilo:

### 1. ¿La región corresponde a la sucursal, al cliente o a otra dimensión de su modelo?
* **Decisión:** La región corresponde a la **sucursal / showroom** a través del campo `Dim_Showroom.zona`.
* **Justificación de Negocio:** Casa&Estilo gestiona sus operaciones, asignación de inventarios, directores de zona y objetivos comerciales a partir de sus puntos de venta físicos y centros regionales (`Dim_Showroom`). Aunque `Dim_Cliente` también contiene un atributo de zona para propósitos de marketing demográfico, el desempeño de ventas y la rentabilidad territorial se imputan a la sucursal que concreta y despacha la transacción.
* **Valores modelados en `zona`:** `Norte`, `Centro`, `Occidente`, `Sur`, `Bajío`.

### 2. ¿Qué columna representa ventas netas y qué columna representa costo?
* **Ventas Netas:** `Fact_Ventas.monto_venta_neta`.
  $$\text{monto\_venta\_neta} = \text{monto\_subtotal} - \text{monto\_descuento\_prorrateado}$$
  Representa el ingreso real percibido por la empresa tras descontar promociones directas aplicadas a la orden.
* **Costo Directo de Producto:** `Fact_Ventas.monto_costo_total`.
  $$\text{monto\_costo\_total} = \text{cantidad} \times \text{costo\_unitario}$$
* **Costo Específico de Caso para Casa&Estilo (Entrega e Instalación):** `Fact_Ventas.monto_envio_prorrateado`.
  De acuerdo con la especificación de la práctica: *"Casa&Estilo: Rentabilidad considerando entrega o instalación cuando esos costos formen parte del modelo"*.
  Por lo tanto, la métrica oficial de **Rentabilidad Neta Operativa** utilizada en el reporte es:
  $$\text{Rentabilidad} = \text{monto\_venta\_neta} - \text{monto\_costo\_total} - \text{monto\_envio\_prorrateado}$$
  O de manera equivalente:
  $$\text{Rentabilidad} = \text{ganancia\_bruta} - \text{monto\_envio\_prorrateado}$$

### 3. ¿Cómo se excluirán o ajustarán las ventas canceladas y las devoluciones?
* **Regla de Negocio:** En el diseño dimensional de Casa&Estilo, las transacciones registradas en `Fact_Ventas` corresponden a órdenes en firme formalizadas en punto de venta o pasarela e-commerce.
* **Tratamiento:**
  - Los pedidos sin fecha de entrega (`fecha_real_entrega_sk IS NULL`) representan mercancía en fabricación, en tránsito logístico o pedidos cancelados antes del despacho físico.
  - Para el reporte de rentabilidad devengada, se incluyen todas las órdenes con ingreso neto consolidado (`monto_venta_neta > 0`). En caso de devoluciones mercantiles posteriores, el estándar de Kimball estipula registrar una línea de ajuste con importes negativos o un estado en dimensión; en nuestro data mart, se filtran ventas con montos nulos o no formalizados.

### 4. ¿Qué ocurrirá cuando un producto no tenga registros en el trimestre anterior?
* **Estrategia Técnica:**
  - Se utiliza un `LEFT JOIN` uniendo los productos vendidos en el periodo actual ($Q_2$ de 2026) con los del periodo base anterior ($Q_1$ de 2026) por `(region, producto_id_bk)`.
  - Para la métrica anterior, se emplea `COALESCE(rentabilidad_q1, 0.00)` para evitar valores nulos en sumatorias.
  - **Variación Absoluta:**
    $$\Delta_{\text{abs}} = \text{Rentabilidad}_{Q2} - \text{COALESCE}(\text{Rentabilidad}_{Q1}, 0.00)$$
  - **Variación Porcentual:**
    Para evitar el error de división entre cero (`division by zero` / `NULL`), se evalúa mediante `CASE WHEN`:
    $$\Delta_{\%} = \begin{cases} \text{NULL}, & \text{si } \text{Rentabilidad}_{Q1} \text{ es NULL o } = 0 \\ \left(\frac{\text{Rentabilidad}_{Q2} - \text{Rentabilidad}_{Q1}}{|\text{Rentabilidad}_{Q1}|}\right) \times 100, & \text{en otro caso} \end{cases}$$
  - **Indicador Cualitativo de Estatus:**
    Un campo descriptivo categórico clasifica la situación histórica del producto:
    - `'Nuevo en periodo (Sin histórico)'` si no existieron ventas en $Q_1$.
    - `'Crecimiento'` si $\text{Rentabilidad}_{Q2} > \text{Rentabilidad}_{Q1}$.
    - `'Decrecimiento'` si $\text{Rentabilidad}_{Q2} < \text{Rentabilidad}_{Q1}$.
    - `'Sin cambio'` si la rentabilidad fue idéntica.

### 5. ¿Cómo comprobarán que cada región devuelve como máximo cinco productos?
* **Mecanismo de Ventana:**
  Se calcula la función analítica:
  $$\text{posicion\_region} = \text{DENSE\_RANK}() \text{ OVER } (\text{PARTITION BY } \text{region} \text{ ORDER BY } \text{rentabilidad\_q2} \text{ DESC})$$
  (o `ROW_NUMBER()` para desempates estrictos).
* **Filtro de Corte:** En la cláusula exterior se filtra estrictamente `WHERE posicion_region <= 5`.
* **Auditoría de Control:** Se incluye una consulta de verificación automatizada:
  ```sql
  SELECT region, COUNT(*) AS total_productos_reportados
  FROM (...) resultado
  GROUP BY region
  HAVING COUNT(*) > 5;
  ```
  La consulta debe retornar 0 filas para certificar que ninguna región excede los 5 productos.

---

## 📊 3. Especificación de Columnas de Salida Requeridas

| # | Nombre de Columna | Tipo de Dato | Origen / Fórmula |
|---|---|---|---|
| 1 | `region` | `VARCHAR` | `Dim_Showroom.zona` |
| 2 | `posicion_region` | `INT / BIGINT` | `DENSE_RANK() OVER (PARTITION BY region ORDER BY rentabilidad_q2 DESC)` |
| 3 | `producto_id_bk` | `INT` | Clave de negocio del producto (`Dim_Producto.producto_id_bk`) |
| 4 | `nombre_producto` | `VARCHAR` | `Dim_Producto.nombre_producto` |
| 5 | `rentabilidad_q2_2026` | `NUMERIC(14,2)` | $\sum (\text{venta\_neta} - \text{costo\_total} - \text{envio\_prorrateado})$ en Q2 |
| 6 | `rentabilidad_q1_2026` | `NUMERIC(14,2)` | $\sum (\text{venta\_neta} - \text{costo\_total} - \text{envio\_prorrateado})$ en Q1 |
| 7 | `variacion_absoluta` | `NUMERIC(14,2)` | $\text{rentabilidad}_{Q2} - \text{COALESCE}(\text{rentabilidad}_{Q1}, 0)$ |
| 8 | `variacion_porcentual` | `NUMERIC(7,2)` | $((\text{rentabilidad}_{Q2} - \text{rentabilidad}_{Q1}) / |\text{rentabilidad}_{Q1}|) * 100$ |
| 9 | `indicador_periodo_anterior` | `VARCHAR(50)` | Etiqueta cualitativa ('Crecimiento', 'Decrecimiento', 'Nuevo...') |

---

## 🛠️ 4. Compatibilidad y Motores Soportados

1. **Motor Principal del Proyecto:** **PostgreSQL 16** (desplegado en contenedor Docker oficial `postgres:16-alpine` y validado en el pipeline CI de GitHub Actions).
2. **Compatibilidad con MySQL 8:** Se proporcionan las notas de traducción sintáctica correspondientes (modos de agregación estricta, funciones de fecha `EXTRACT` vs `QUARTER`, y sintaxis de Stored Procedures `CREATE PROCEDURE` con `DELIMITER //`).
