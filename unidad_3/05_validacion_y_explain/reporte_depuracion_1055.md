# 🛠️ Reporte de Depuración: Error de Agrupación 1055 (ONLY_FULL_GROUP_BY)

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239
- **Materia:** Inteligencia de Negocios - FIME 2026

---

## 🎯 1. Contexto del Reto Técnico (Reto 2)

De acuerdo con las directrices de la Unidad 3:
> *"Construyan, a partir de sus propias tablas, una versión que seleccione región, producto y una medida agregada, pero que agrupe de forma incompleta. Ejecútenla con la configuración de agrupación estricta de MySQL y conserven el mensaje de error 1055. Soliciten a la IA una explicación, corrijan la consulta y expliquen por qué la nueva agrupación es coherente con el resultado solicitado."*

---

## 💥 2. Consulta con Agrupación Incompleta (Provocación del Fallo)

Se construyó una consulta analítica que proyecta la región (`s.zona`), el nombre del producto (`p.nombre_producto`), la categoría (`p.categoria`) y la rentabilidad total agregada (`SUM(...)`), pero en la cláusula `GROUP BY` únicamente se especificó `s.zona`:

```sql
SELECT 
    s.zona AS region,
    p.nombre_producto,
    p.categoria,
    SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_total
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY s.zona;
```

---

## 🛑 3. Mensajes de Error Exactos del Motor

### A. Mensaje en MySQL 8 (sql_mode=ONLY_FULL_GROUP_BY)
```text
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause 
and contains nonaggregated column 'casa_estilo_bi.p.nombre_producto' 
which is not functionally dependent on columns in GROUP BY clause; 
this is incompatible with sql_mode=only_full_group_by
```

### B. Mensaje en PostgreSQL 16 (Motor Contenedorizado del Proyecto)
```text
ERROR:  column "p.nombre_producto" must appear in the GROUP BY clause or be used in an aggregate function
LINE 3:     p.nombre_producto,
            ^
SQLSTATE: 42803
```

---

## 🧠 4. Diagnóstico Técnico y Explicación del Equipo

### 4.1. Fundamento en el Estándar SQL ANSI/ISO
Los estándares SQL:1999 y SQL:2003 definen el principio de **determinismo en la agregación**:
1. Una consulta con `GROUP BY s.zona` colapsa todas las transacciones de una región (por ejemplo, los cientos de ventas de la Zona Norte) en una **única fila física de salida** por cada zona.
2. Sin embargo, dentro de la Zona Norte coexisten decenas de productos distintos (`Sofá Seccional Oslo`, `Mesa de Comedor Kioto`, `Cama Estocolmo`, etc.).
3. Al solicitar `p.nombre_producto` y `p.categoria` en el `SELECT` sin agregarlos (`MAX`, `MIN`, `STRING_AGG`) ni incluirlos en el `GROUP BY`, el motor se enfrenta a una **ambigüedad irresoluble**: *¿cuál de todos los nombres de producto de la región debe estampar en la única celda de resultado?*
4. En motores legados o configuraciones permisivas (como MySQL pre-5.7 sin `ONLY_FULL_GROUP_BY`), la base de datos elegía arbitrariamente el valor de la primera fila leída en disco. Esto producía reportes de BI matemáticamente falsos y no reproducibles.

### 4.2. Incoherencia con el Objetivo de Negocio
El requerimiento empresarial no pide la rentabilidad agregada de toda la región con una etiqueta de producto aleatoria; solicita la rentabilidad **de cada producto dentro de su respectiva región**. Agrupar solo por zona destruye el grano requerido.

---

## ✅ 5. Consulta Corregida y Coherencia con el Grano

Para corregir el fallo y respetar el estándar estricto, se añaden al `GROUP BY` todas las columnas dimensionales proyectadas que definen la entidad producto (`producto_id_bk`, `nombre_producto`, `categoria`):

```sql
SELECT 
    s.zona AS region,
    p.producto_id_bk,
    p.nombre_producto,
    p.categoria,
    COUNT(*) AS total_transacciones,
    SUM(f.cantidad) AS volumen_unidades,
    ROUND(SUM(f.monto_venta_neta), 2) AS venta_neta_total,
    ROUND(SUM(f.monto_costo_total), 2) AS costo_mercancia_total,
    ROUND(SUM(f.monto_envio_prorrateado), 2) AS costo_entrega_total,
    ROUND(SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado), 2) AS rentabilidad_neta_total
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY 
    s.zona, 
    p.producto_id_bk, 
    p.nombre_producto, 
    p.categoria
ORDER BY 
    region ASC, 
    rentabilidad_neta_total DESC;
```

### 🎯 Por qué esta solución es coherente:
- **Unicidad:** La combinación `(s.zona, p.producto_id_bk)` define una clave compuesta unívoca para cada grupo.
- **Trazabilidad:** Cada cifra de rentabilidad corresponde exactamente a la sumatoria de las ventas de ese producto específico en esa región.
- **Determinismo:** El plan de ejecución genera un `HashAggregate` o `GroupAggregate` con dependencias funcionales satisfechas al 100%.
- **Evidencia de Ejecución:** Validada en [`01_depuracion_error_1055.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/01_depuracion_error_1055.sql).
