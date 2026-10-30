# 🧠 Reflexión Crítica sobre Decisiones de Limpieza y Negocio (Paso 8)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/08_reflexion/reflexion_decisiones_limpieza.md`  
**Autor:** Equipo 8 (Casa&Estilo)

---

## ❓ Pregunta 1: ¿Qué ocurre si un cliente tiene estado vacío? ¿Se rechaza el cliente o se agrupa como no identificado?

### Análisis y Decisión de Diseño:
En la arquitectura implementada en este laboratorio se optó por **agrupar al cliente como 'No Identificado' (`NE` - No Especificado)** en lugar de rechazarlo o descartarlo.

### Fundamentación Técnica y de Negocio:
1. **Preservación del Embudo de Clientes:** En una plataforma de comercio electrónico moderna, un usuario puede registrarse completando únicamente su nombre y correo electrónico antes de ingresar una dirección física de facturación. Si el pipeline ETL descartara al cliente por carecer de estado geográfico, cualquier orden de compra futura realizada por este cliente provocaría un error de clave foránea huérfana (`CLIENTE_INEXISTENTE`), rompiendo la trazabilidad del negocio.
2. **Buenas Prácticas Dimensionales (Metodología Ralph Kimball):** El estándar de la industria recomienda crear un registro centinela en las dimensiones (ej. `SK = -1`, `estado_canonico = 'NE'`, `nombre_oficial = 'No Especificado'`). De este modo, la clave foránea no queda nula ni viola restricciones referenciales.
3. **Acción Operativa Posterior:** El Data Mart expone el volumen de clientes en estatus `NE`, lo que permite al equipo de Marketing y CRM detonar campañas de notificación dirigidas ("Completa tu perfil y obtén 10% de descuento").
4. **Diferencia con el Pedido:** A diferencia del cliente, si un *pedido* reporta un estado de destino vacío o inexistente, la orden **sí debe ser enviada a la mesa de rechazos**, ya que la logística física no puede despachar un paquete sin un destino geográfico válido.

---

## ❓ Pregunta 2: ¿Cómo detectarías pedidos que llegaron tarde?

### Diagnóstico del Modelo Actual:
En el modelo actual del laboratorio, únicamente se captura la fecha de compra (`fecha_pedido`). Con este único punto temporal es matemáticamente imposible determinar la puntualidad logística.

### Propuesta de Extensión Técnica:
Para monitorear y auditar la puntualidad logística (cumplimiento de SLA), se deben incorporar al menos dos campos temporales adicionales en el sistema transaccional y en `fact_ordenes`:
- `fecha_prometida_entrega DATE` (o `dias_sla_prometidos INT` acordados en el checkout).
- `fecha_entrega_real DATE` (registrada por el transportista o API de paquetería).

### Lógica de Detección en SQL:
```sql
SELECT 
    f.id_pedido,
    f.id_cliente,
    f.fecha_pedido,
    f.fecha_prometida_entrega,
    f.fecha_entrega_real,
    DATEDIFF(f.fecha_entrega_real, f.fecha_prometida_entrega) AS dias_retraso,
    CASE 
        WHEN f.fecha_entrega_real > f.fecha_prometida_entrega THEN 'Tardío'
        WHEN f.fecha_entrega_real <= f.fecha_prometida_entrega THEN 'A Tiempo'
        WHEN f.fecha_entrega_real IS NULL AND CURRENT_DATE > f.fecha_prometida_entrega THEN 'Atrasado en Tránsito'
        ELSE 'En Tiempo de Entrega'
    END AS clasificacion_sla
FROM fact_ordenes f
WHERE f.estado_pedido = 'Entregado';
```

### Indicadores Clave Derivados:
- **OTIF (On-Time In-Full):** Porcentaje de pedidos entregados a tiempo respecto al total de órdenes despachadas.
- **Lead Time Promedio por Estado:** Identificar en qué regiones geográficas las paqueterías presentan mayores cuellos de botella.

---

## ❓ Pregunta 3: ¿Cómo modificarías el proceso para admitir devoluciones?

### Impacto en el Modelo Dimensional y en el Flujo ETL:
Para incorporar devoluciones sin desvirtuar la integridad contable se deben realizar las siguientes adaptaciones:

### 1. Extensión de Fuentes de Entrada
Ingestar un archivo transaccional adicional `devoluciones.csv` con los campos:
`id_devolucion, id_pedido, fecha_devolucion, importe_devuelto, motivo_devolucion, estado_articulo`.

### 2. Reglas de Validación en Staging
- **Integridad Referencial:** Comprobar que el `id_pedido` asociado exista en `fact_ordenes` y se encuentre en estatus `'Entregado'`.
- **Coherencia Temporal:** Verificar que `fecha_devolucion >= fecha_pedido`.
- **Consistencia Financiera:** Asegurar que `importe_devuelto <= importe_pedido_original`.

### 3. Alternativas de Modelado en el Data Mart:
- **Opción A (Hecho Acumulado en `fact_ordenes`):**
  Añadir columnas `monto_devuelto DECIMAL(12,2) DEFAULT 0.00`, `fecha_devolucion DATE NULL` y actualizar el `estado_pedido` a `'Devuelto Parcial'` o `'Devuelto Total'`.
- **Opción B (Tabla de Hechos Independiente `fact_devoluciones` - Recomendada):**
  Mantener `fact_ordenes` inalterada y crear `fact_devoluciones` con su propia clave de fecha (`fecha_devolucion_sk`) y dimensión de motivos (`dim_motivo_devolucion`), lo que permite analizar devoluciones en el periodo contable exacto en que ocurrieron (que puede ser meses después de la compra).

### 4. Recálculo del Indicador de Ventas Netas:
$$\text{Ventas Netas Reales} = \sum \text{Ventas Entregadas} - \sum \text{Importe Devoluciones}$$

---

## 💡 Conclusión sobre Decisiones de Limpieza y Balance de Calidad
El diseño del pipeline ETL demostró que la limpieza de datos no consiste en descartar arbitrariamente registros con defectos, sino en **clasificarlos conforme a su naturaleza de negocio**:
- Los defectos recuperables (formatos de fecha mixtos, alias estatales) se homologan mediante funciones deterministas y catálogos maestros.
- Los defectos que comprometen la estructura relacional (claves duplicadas, clientes inexistentes) se aíslan en una mesa de rechazos auditable.
- La aplicación de claves naturales estables y comandos UPSERT garantiza que el pipeline sea 100% reproducible, resiliente e idempotente ante cualquier re-ejecución.
