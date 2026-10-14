# 🐞 Prompt y Diagnóstico: Reto 2 (Error de Agrupación 1055 / ONLY_FULL_GROUP_BY)

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
### 🎯 Propósito: Provocar intencionalmente, diagnosticar con apoyo de IA y corregir el error de agregación incompleta.

---

## 📝 1. Prompt Enviado a la Inteligencia Artificial

```text
Actúa como especialista en motores de bases de datos relacionales (MySQL 8 y PostgreSQL 16).
Ejecutamos la siguiente consulta analítica sobre nuestro Data Mart de Casa&Estilo:

SELECT 
    s.zona AS region,
    p.nombre_producto,
    p.categoria,
    SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_total
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY s.zona;

El motor de base de datos arrojó el siguiente error:
- En MySQL 8:
  ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'casa_estilo_bi.p.nombre_producto' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by.
- En PostgreSQL 16:
  ERROR: column "p.nombre_producto" must appear in the GROUP BY clause or be used in an aggregate function (LINE 4: p.nombre_producto, SQLSTATE 42803).

Por favor:
1. Explica cuál es la causa raíz de este error según el estándar SQL ANSI/ISO y la configuración de agrupación estricta.
2. ¿Por qué agrupar únicamente por 's.zona' produce un resultado conceptualmente ambiguo e indeterminado para el negocio?
3. Proporciona la consulta corregida que mantenga la coherencia del grano (rentabilidad por producto dentro de cada región) y explica por qué es la solución matemáticamente correcta.
```

---

## 💡 2. Respuesta y Explicación Técnica de la IA

### Causa Raíz según Estándar SQL:
El error **1055** en MySQL (asociado a la bandera `sql_mode=only_full_group_by`) y el error **42803** en PostgreSQL se fundamentan en el estándar **SQL:1999 / SQL:2003**:
1. Cuando una cláusula `GROUP BY` se ejecuta, el motor colapsa todas las filas que comparten el mismo valor de la clave de agrupación (`s.zona`) en una sola fila consolidada de salida.
2. Las columnas no agregadas que se colocan en el `SELECT` (`p.nombre_producto`, `p.categoria`) tienen múltiples valores diferentes para cada una de las regiones.
3. Si el motor no forzara el error, tendría que seleccionar de manera arbitraria o no determinista qué nombre de producto mostrar para representar la suma de toda la zona (como sucedía erróneamente en versiones obsoletas de MySQL pre-5.7).
4. El estándar exige que **toda columna proyectada en el `SELECT` debe formar parte de la cláusula `GROUP BY` o estar envuelta dentro de una función de agregación (`SUM`, `AVG`, `MAX`, `MIN`, etc.)**, a menos que exista una dependencia funcional estricta garantizada por la clave primaria.

### Consulta Corregida Propuesta por la IA:
```sql
SELECT 
    s.zona AS region,
    p.producto_id_bk,
    p.nombre_producto,
    p.categoria,
    SUM(f.monto_venta_neta - f.monto_costo_total - f.monto_envio_prorrateado) AS rentabilidad_total
FROM Fact_Ventas f
JOIN Dim_Showroom s ON f.showroom_sk = s.showroom_sk
JOIN Dim_Producto p ON f.producto_sk = p.producto_sk
GROUP BY 
    s.zona, 
    p.producto_id_bk, 
    p.nombre_producto, 
    p.categoria
ORDER BY 
    region, 
    rentabilidad_total DESC;
```

---

## 🔍 3. Evaluación del Equipo y Justificación del Grano

El equipo analizó la respuesta y determinó que la explicación de la IA es **100% certera y alineada a las mejores prácticas de BI**:
- **Coherencia con el Grano:** El reporte no busca la rentabilidad total de la región como un único número, sino la rentabilidad de cada producto dentro de su respectiva región.
- **Resolución Determinista:** Al incorporar `p.producto_id_bk`, `p.nombre_producto` y `p.categoria` en la cláusula `GROUP BY`, cada combinación `(región, producto)` se convierte en un grupo analítico único y unívoco.
- **Evidencia en Repositorio:** El script ejecutable y los planes de validación se encuentran documentados en [`unidad_3/05_validacion_y_explain/01_depuracion_error_1055.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/01_depuracion_error_1055.sql).
