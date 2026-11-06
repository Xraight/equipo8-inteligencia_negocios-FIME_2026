# Justificación Técnica de Decisiones de Diseño
## Memoria Arquitectónica y Defensa de Modelado — Casa&Estilo

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Función General:** Proporcionar la fundamentación teórica, matemática y operativa detrás de cada decisión de diseño arquitectónico y modelado dimensional del PIA.
- **Función Específica:** Servir como base de sustentación para la defensa oral de 15 minutos ante el Comité Directivo / Sínodo Evaluador.

---

## 1. Defensa del Modelo Estrella (Star Schema) vs Copo de Nieve (Snowflake)

### 1.1. Fundamentación Teórica
El paradigma de Ralph Kimball establece que en un entorno analítico orientado a la toma de decisiones, la prioridad es la simplicidad cognitiva para el usuario de negocio y la eficiencia computacional en agregaciones masivas.
- En un **Snowflake**, la normalización de dimensiones (ej. separar Categorías $\to$ Marcas $\to$ Productos, o Ciudades $\to$ Estados $\to$ Sucursales) genera cadenas de `JOIN` multinivel. Para una base con 331,758 transacciones de detalle, cada salto relacional adicional en consultas analíticas degrada el tiempo de respuesta y aumenta el riesgo de "Fan Traps".
- En el **Star Schema** implementado, cada dimensión se encuentra a un único salto de distancia de la tabla de hechos. Esto permite que el optimizador de costos de MySQL 8.0 y el motor columnar VertiPaq de Power Pivot ejecuten filtros vectorizados directos con índices B-Tree de alta selectividad.

---

## 2. Granularidad Atómica y Eliminación de "Chasm Traps"

### 2.1. Nivel de Detalle Transaccional
Una alternativa comúnmente evaluada es agregar las ventas a nivel de ticket (cabecera). Sin embargo, esto impediría responder preguntas de negocio fundamentales en el sector mueblero:
1. *¿Cuál es el margen real de la categoría Recámara frente a Iluminación cuando se aplican descuentos promocionales?*
2. *¿Qué productos específicos presentan la mayor tasa de devolución por defecto o daño?*
3. *¿Cuál es la tasa de canibalización entre líneas de producto premium y estándar?*

Al situar la granularidad en la **línea de artículo por ticket**, conservamos el 100% de la fidelidad operativa y podemos agregar hacia arriba en cualquier dimensión sin pérdida de varianza.

---

## 3. Estrategia de Claves Sustitutas (`Surrogate Keys`) e Integridad Referencial

### 3.1. Claves Enteras Artificiales
Se asignaron claves enteras autoincrementales (`INT`) para las dimensiones `dim_producto`, `dim_cliente` y `dim_sucursal`, preservando las claves de negocio (`producto_id`, `cliente_id`, `sucursal_id`) como atributos informativos indexados.
- **Ventaja de Almacenamiento e Indexación:** Una clave entera ocupa 4 bytes frente a los 20-30 bytes de un `VARCHAR`. En una tabla de hechos de cientos de miles de registros con 6 claves foráneas, el uso de claves enteras compacta la tabla en memoria caché en más de un 60%, acelerando los recorridos de índice.
- **Manejo de Valores Huérfanos o No Identificados:** Se definió la inserción mandatoria del registro comodín `Key = -1` ('No Identificado' / 'No Asignado') en cada dimensión. Si una venta futura o dato histórico carece de cliente o sucursal válida, el pipeline ETL mapea la FK a `-1` en lugar de generar un error de integridad o rechazar la transacción, preservando el balance de masa contable.

---

## 4. Detección y Resolución del Problema de Calidad en el POS RAW

### 4.1. El Hallazgo Crítico
Durante el perfilado minucioso de `POS/detalle_ventas.csv` y `POS/devoluciones.csv`, se descubrió que el campo `importe` en el archivo origen NO aplicaba el descuento registrado en `descuento_pct`.
$$\text{En el RAW:} \quad \text{importe} = \text{cantidad} \times \text{precio\_unitario} \quad (\text{Subtotal Bruto})$$

### 4.2. Impacto Financiero si no se Corrige
Si el analista de BI asumiera ciegamente que `importe` es el total cobrado al cliente, el estado de resultados de Casa&Estilo presentaría una sobreestimación artificial de ventas de más de **$18,000,000 MXN**, alterando severamente la utilidad bruta y conduciendo al Comité Directivo a decisiones erróneas sobre presupuestos y comisiones de venta.

### 4.3. Resolución en el Pipeline ETL
En staging se formalizó la separación en tres medidas contables estrictas:
$$\text{monto\_bruto} = \text{cantidad} \times \text{precio\_unitario}$$
$$\text{monto\_descuento} = \text{monto\_bruto} \times \left(\frac{\text{descuento\_pct}}{100}\right)$$
$$\text{monto\_neto} = \text{monto\_bruto} - \text{monto\_descuento}$$
$$\text{utilidad\_bruta} = \text{monto\_neto} - (\text{cantidad} \times \text{costo\_unitario})$$
Esta separación garantiza una conciliación contable sin discrepancias ($0.00).

---

## 5. Tratamiento de Valores Atípicos, Nulos y Calidad en CRM

En `CRM/clientes.csv` se identificaron 20 ciudades vacías, 43 correos nulos y 235 registros con sexo 'N/E'.
- **Regla de Imputación Consciente:**
  - `ciudad` $\to$ 'No Especificada' (permite agrupar en dashboards sin distorsionar los totales geográficos).
  - `email` $\to$ 'sin_correo@ejemplo.com' (mantiene la validez sintáctica sin inventar dominios).
  - `sexo` $\to$ 'No Especificado' (respeta la no declaración del cliente sin sesgar análisis demográficos).
