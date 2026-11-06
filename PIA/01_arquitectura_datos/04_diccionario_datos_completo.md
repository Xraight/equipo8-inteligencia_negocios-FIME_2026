# Diccionario de Datos Completo — Data Mart `ce_bi`
## Especificación Técnica de Tablas, Atributos, Restricciones y Reglas

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Función General:** Documentar exhaustivamente cada tabla, campo, tipo de dato, nulos, llaves y regla de transformación del Data Mart en MySQL 8.0.
- **Función Específica:** Servir como guía de referencia para los scripts DDL, validación del ETL y consumo analítico en Power Pivot/Excel.

---

## 1. Tablas de Dimensiones

### 1.1. `dim_tiempo`
- **Propósito:** Dimensión conforme de fecha que permite navegación jerárquica temporal (Año $\to$ Trimestre $\to$ Mes $\to$ Semana $\to$ Día).
- **Rango cubierto:** 2024-01-01 al 2026-12-31 (1,096 registros continuos sin huecos).

| Campo | Tipo SQL | Null | PK/FK | Descripción | Origen / Regla de Transformación |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `tiempo_id` | `INT` | NO | PK | Llave primaria numérica formato YYYYMMDD | `YEAR(d)*10000 + MONTH(d)*100 + DAY(d)` |
| `fecha` | `DATE` | NO | UQ | Fecha calendario estándar | Generada por secuencia de calendario continuo |
| `anio` | `SMALLINT` | NO | - | Año calendario de cuatro dígitos | `YEAR(fecha)` |
| `trimestre` | `TINYINT` | NO | - | Trimestre numérico del año (1 a 4) | `QUARTER(fecha)` |
| `trimestre_nombre`| `VARCHAR(10)`| NO | - | Etiqueta de negocio de trimestre | `CONCAT('Q', QUARTER(fecha))` |
| `mes` | `TINYINT` | NO | - | Mes numérico del año (1 a 12) | `MONTH(fecha)` |
| `mes_nombre` | `VARCHAR(15)`| NO | - | Nombre completo del mes en español | Función CASE / `ELT(MONTH(fecha))` |
| `mes_anio` | `VARCHAR(10)`| NO | - | Formato YYYY-MM para ordenamiento cronológico | `DATE_FORMAT(fecha, '%Y-%m')` |
| `semana_anio` | `TINYINT` | NO | - | Semana del año calendario (1 a 53) | `WEEK(fecha, 3)` |
| `dia_mes` | `TINYINT` | NO | - | Día del mes (1 a 31) | `DAY(fecha)` |
| `dia_semana` | `TINYINT` | NO | - | Día de la semana (1=Lunes a 7=Domingo) | `WEEKDAY(fecha) + 1` |
| `dia_semana_nombre`| `VARCHAR(12)`| NO | - | Nombre en español del día de la semana | Función CASE / `ELT(dia_semana)` |
| `es_fin_semana` | `TINYINT` | NO | - | Flag indicador de fin de semana (1 o 0) | `IF(dia_semana IN (6,7), 1, 0)` |

---

### 1.2. `dim_producto`
- **Propósito:** Catálogo maestro de productos comercializados por Casa&Estilo.

| Campo | Tipo SQL | Null | PK/FK | Descripción | Origen / Regla de Transformación |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `producto_key` | `INT` | NO | PK | Clave sustituta artificial del Data Mart | `AUTO_INCREMENT` |
| `producto_id` | `VARCHAR(20)`| NO | UQ | Código transaccional de negocio en ERP | `TRIM(producto_id)` de `ERP/productos.csv` |
| `sku` | `VARCHAR(20)`| NO | - | Código SKU para logística y almacén | `TRIM(sku)` |
| `producto` | `VARCHAR(150)`| NO | - | Nombre comercial del producto | `TRIM(producto)` |
| `categoria` | `VARCHAR(50)`| NO | - | Categoría comercial (Recámara, Comedor...) | `TRIM(categoria)` |
| `marca` | `VARCHAR(50)`| NO | - | Marca fabricante | `TRIM(marca)` |
| `costo` | `DECIMAL(12,2)`| NO | - | Costo estándar de compra al proveedor | `CAST(costo AS DECIMAL(12,2))` |
| `precio_lista` | `DECIMAL(12,2)`| NO | - | Precio base de venta al público en general | `CAST(precio_lista AS DECIMAL(12,2))` |
| `margen_teorico_pct`| `DECIMAL(6,2)`| NO | - | Margen sobre costo teórico porcentual | `ROUND(((precio_lista - costo)/precio_lista)*100, 2)` |
| `activo` | `CHAR(2)` | NO | - | Indicador de disponibilidad operativa ('SI'/'NO') | `UPPER(TRIM(activo))` |
| `requiere_instalacion`| `CHAR(2)`| NO | - | Bandera de armado técnico requerido ('SI'/'NO') | `UPPER(TRIM(requiere_instalacion))` |

---

### 1.3. `dim_cliente`
- **Propósito:** Registro maestro de clientes con tratamiento de calidad en atributos demográficos.

| Campo | Tipo SQL | Null | PK/FK | Descripción | Origen / Regla de Transformación |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `cliente_key` | `INT` | NO | PK | Clave sustituta artificial | `AUTO_INCREMENT` |
| `cliente_id` | `VARCHAR(20)`| NO | UQ | Código transaccional de cliente en CRM | `TRIM(cliente_id)` de `CRM/clientes.csv` |
| `nombre` | `VARCHAR(150)`| NO | - | Nombre completo del cliente | `TRIM(nombre)` |
| `sexo` | `VARCHAR(20)`| NO | - | Género estandarizado para analítica | `CASE WHEN sexo='M' THEN 'Masculino' WHEN sexo='F' THEN 'Femenino' ELSE 'No Especificado' END` |
| `fecha_alta` | `DATE` | NO | - | Fecha de registro inicial en CRM | `STR_TO_DATE(fecha_alta, '%Y-%m-%d')` |
| `ciudad` | `VARCHAR(80)`| NO | - | Ciudad de residencia | `COALESCE(NULLIF(TRIM(ciudad), ''), 'No Especificada')` |
| `segmento` | `VARCHAR(30)`| NO | - | Clasificación de valor (Premium, Frecuente...) | `TRIM(segmento)` |
| `email` | `VARCHAR(150)`| NO | - | Correo electrónico institucional o personal | `COALESCE(NULLIF(TRIM(email), ''), 'sin_correo@ejemplo.com')` |

---

### 1.4. `dim_sucursal`
- **Propósito:** Red comercial física con atributos espaciales y de escala.

| Campo | Tipo SQL | Null | PK/FK | Descripción | Origen / Regla de Transformación |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `sucursal_key` | `INT` | NO | PK | Clave sustituta de la sucursal | `AUTO_INCREMENT` |
| `sucursal_id` | `VARCHAR(20)`| NO | UQ | Código de tienda (CE-S001..S016) | `TRIM(sucursal_id)` |
| `sucursal` | `VARCHAR(100)`| NO | - | Denominación de la tienda | `TRIM(sucursal)` |
| `ciudad` | `VARCHAR(80)`| NO | - | Ciudad donde radica la sucursal | `TRIM(ciudad)` |
| `estado` | `VARCHAR(80)`| NO | - | Estado federativo | `TRIM(estado)` |
| `m2` | `INT` | NO | - | Área comercial en metros cuadrados | `CAST(m2 AS SIGNED)` |
| `categoria_tamano`| `VARCHAR(30)`| NO | - | Segmentación de capacidad de exhibición | `CASE WHEN m2 < 1200 THEN 'Pequeña (<1200 m2)' WHEN m2 <= 1600 THEN 'Mediana (1200-1600 m2)' ELSE 'Grande (>1600 m2)' END` |
| `fecha_apertura` | `DATE` | NO | - | Fecha de inauguración de la tienda | `STR_TO_DATE(fecha_apertura, '%Y-%m-%d')` |

---

### 1.5. `dim_canal` y `dim_metodo_pago`
- **`dim_canal`:**
  - `canal_id` (`TINYINT` PK): 1 = 'Tienda', 2 = 'Web', 3 = 'App'.
  - `canal_nombre` (`VARCHAR(30)`).
- **`dim_metodo_pago`:**
  - `metodo_pago_id` (`TINYINT` PK): 1 = 'Tarjeta', 2 = 'Efectivo', 3 = 'Transferencia', 4 = 'Wallet'.
  - `metodo_nombre` (`VARCHAR(30)`).

---

## 2. Tablas de Hechos

### 2.1. `fact_ventas_detalle`
- **Propósito:** Registrar transacciones comerciales completas a nivel ítem de venta.
- **Granularidad:** 1 registro por cada renglón de ticket vendido.
- **Conteo real esperado:** 331,758 filas.

| Campo | Tipo SQL | Null | PK/FK | Descripción | Regla de Transformación / Fórmula |
| :--- | :--- | :---: | :---: | :--- | :--- |
| `venta_id` | `VARCHAR(20)` | NO | PK | Folio del ticket de venta | `v.venta_id` |
| `linea` | `INT` | NO | PK | Número de renglón en ticket | `d.linea` |
| `tiempo_id` | `INT` | NO | FK | Clave de fecha de compra | `YEAR(v.fecha)*10000 + MONTH(v.fecha)*100 + DAY(v.fecha)` |
| `producto_key` | `INT` | NO | FK | Llave sustituta del producto | `dp.producto_key` |
| `cliente_key` | `INT` | NO | FK | Llave sustituta del cliente | `dc.cliente_key` |
| `sucursal_key` | `INT` | NO | FK | Llave sustituta de la sucursal | `ds.sucursal_key` |
| `canal_id` | `TINYINT` | NO | FK | Llave del canal comercial | `cn.canal_id` |
| `metodo_pago_id` | `TINYINT` | NO | FK | Llave del método de pago | `mp.metodo_pago_id` |
| `hora_venta` | `TIME` | NO | - | Hora de venta | `v.hora` |
| `cantidad` | `INT` | NO | - | Unidades físicas vendidas | `d.cantidad` |
| `precio_unitario`| `DECIMAL(12,2)`| NO | - | Precio unitario real cobrado | `d.precio_unitario` |
| `descuento_pct` | `DECIMAL(5,2)` | NO | - | Porcentaje de descuento comercial | `d.descuento_pct` |
| `monto_bruto` | `DECIMAL(14,2)`| NO | - | Facturación previa a descuentos | `ROUND(d.cantidad * d.precio_unitario, 2)` |
| `monto_descuento`| `DECIMAL(14,2)`| NO | - | Descuento en pesos concedido | `ROUND(monto_bruto * (d.descuento_pct / 100), 2)` |
| `monto_neto` | `DECIMAL(14,2)`| NO | - | Ingreso real percibido | `monto_bruto - monto_descuento` |
| `costo_unitario` | `DECIMAL(12,2)`| NO | - | Costo unitario ERP | `p.costo` |
| `costo_total` | `DECIMAL(14,2)`| NO | - | Costo de adquisición total (COGS)| `ROUND(d.cantidad * p.costo, 2)` |
| `utilidad_bruta` | `DECIMAL(14,2)`| NO | - | Margen bruto en pesos | `monto_neto - costo_total` |
| `margen_pct` | `DECIMAL(6,2)` | NO | - | Rentabilidad porcentual real | `ROUND((utilidad_bruta / monto_neto) * 100, 2)` |
| `es_devuelto` | `TINYINT` | NO | - | Flag de devolución posterior | `IF(dev.venta_id IS NOT NULL, 1, 0)` |

---

### 2.2. `fact_devoluciones`
- **Granularidad:** 1 fila por evento de devolución de producto (9,952 filas).
- **Campos:** `devolucion_id` (PK, `VARCHAR(20)`), `venta_id`, `tiempo_id`, `producto_key`, `sucursal_key`, `cliente_key`, `cantidad_devuelta`, `importe_devuelto`, `motivo`.

### 2.3. `fact_instalaciones`
- **Granularidad:** 1 fila por servicio de instalación programado (6,500 filas).
- **Campos:** `instalacion_id` (PK, `VARCHAR(20)`), `venta_id`, `tiempo_id`, `cliente_key`, `sucursal_key`, `dias_programados`, `dias_reales`, `dias_desviacion` (`dias_reales - dias_programados`), `cumplio_sla` (`IF(dias_reales <= dias_programados, 1, 0)`), `satisfaccion` (1 a 5).

### 2.4. `fact_inventario_snapshot`
- **Granularidad:** 1 fila por par (sucursal, producto) (21,440 filas).
- **Campos:** `sucursal_key`, `producto_key`, `stock_actual`, `punto_reorden`, `deficit_unidades` (`GREATEST(0, punto_reorden - stock_actual)`), `valor_inventario_costo` (`stock_actual * costo`).
