# 📐 Definición del Grano y Diccionario de Datos del Data Mart

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239
- **Grupo:** Inteligencia de Negocios - FIME 2026

---

## 🎯 1. Definición Formal del Grano de la Tabla de Hechos

> **Declaración de Grano:**  
> *"Una fila en la tabla `Fact_Ventas` representa un producto o variante específica dentro de una línea de detalle de una orden de venta efectuada a través de un canal comercial, atendida por un asesor en un showroom o centro de distribución, en un día determinado."*

### 🔍 Impacto del Grano en las Operaciones Analíticas:
1. **Conteo de Pedidos / Órdenes:**  
   Dado que una orden puede contener múltiples productos (venta cruzada o surtido coordinado de muebles), el conteo de pedidos no puede realizarse mediante `COUNT(*)`. Debe calcularse obligatoriamente utilizando `COUNT(DISTINCT orden_id)`.
2. **Conteo de Clientes:**  
   Un cliente puede realizar múltiples órdenes y adquirir múltiples líneas de producto a lo largo del tiempo. El conteo de clientes únicos requiere la agregación `COUNT(DISTINCT cliente_sk)`.
3. **Conteo de Productos y Variantes:**  
   - Si se requiere cuantificar unidades físicas vendidas, se aplica `SUM(cantidad)`.
   - Si se analiza la diversidad de variantes vendidas, se utiliza `COUNT(DISTINCT producto_sk)`.
   - Si se analiza a nivel de producto comercial (descartando variantes de color o tamaño), se utiliza `COUNT(DISTINCT producto_id_bk)`.
4. **Métricas Prorrateadas a Nivel Línea:**  
   Conceptos como el **descuento comercial global** o el **costo de envío/instalación** aplican originalmente a nivel cabecera de orden. Para no duplicar importes al sumarizar líneas, el modelo dimensional almacena estas métricas **prorrateadas ponderadamente** por el peso monetario del subtotal de cada línea de producto.

---

## 📚 2. Diccionario de Datos del Esquema Estrella

El Data Mart está estructurado como un **Star Schema** compuesto por 6 tablas de dimensiones y 1 tabla central de hechos.

```
                    ┌─────────────────┐
                    │   Dim_Tiempo    │
                    └────────┬────────┘
                             │
┌────────────────┐           │           ┌────────────────┐
│  Dim_Cliente   │────────┐  │  ┌────────│  Dim_Producto  │
└────────────────┘        │  │  │        └────────────────┘
                          ▼  ▼  ▼
                    ┌─────────────────┐
                    │   Fact_Ventas   │
                    └─────────────────┘
                          ▲  ▲  ▲
┌────────────────┐        │  │  │        ┌────────────────┐
│  Dim_Showroom  │────────┘  │  └────────│   Dim_Canal    │
└────────────────┘           │           └────────────────┘
                    ┌────────┴────────┐
                    │   Dim_Asesor    │
                    └─────────────────┘
```

### 2.1. Tabla de Hechos: `Fact_Ventas`
Tabla central transaccional periódica y acumulativa.

| Columna | Tipo de Dato | Clave | Nullable | Descripción y Regla de Negocio |
|---|---|---|---|---|
| `fact_venta_id` | `SERIAL` | PK | NO | Identificador subrogado único de la línea de hecho. |
| `fecha_orden_sk` | `INT` | FK | NO | Fecha en que se originó la compra (`Dim_Tiempo.fecha_sk`). |
| `fecha_prometida_sk` | `INT` | FK | SÍ | Fecha comprometida con el cliente para la entrega. |
| `fecha_real_entrega_sk`| `INT` | FK | SÍ | Fecha en que la mercancía fue entregada físicamente. |
| `cliente_sk` | `INT` | FK | NO | Referencia al cliente comprador (`Dim_Cliente.cliente_sk`). |
| `producto_sk` | `INT` | FK | NO | Referencia a la variante de producto (`Dim_Producto.producto_sk`). |
| `showroom_sk` | `INT` | FK | NO | Punto de venta o showroom que registra la venta (`Dim_Showroom.showroom_sk`). |
| `asesor_sk` | `INT` | FK | NO | Asesor comercial comisionable (`Dim_Asesor.asesor_sk`). |
| `canal_sk` | `INT` | FK | NO | Canal de venta utilizado (`Dim_Canal.canal_sk`). |
| `orden_id` | `VARCHAR(50)` | Degenerada | NO | Identificador transaccional de la orden (`ORD-2026-XXXX`). |
| `tipo_surtido` | `VARCHAR(50)` | Degenerada | SÍ | `Stock` (entrega inmediata) o `Sobre pedido` (fabricación). |
| `cantidad` | `INT` | Métrica Aditiva | NO | Número de unidades adquiridas de la variante. |
| `precio_unitario` | `NUMERIC(10,2)` | Atributo Numérico | NO | Precio de catálogo unitario al momento de la transacción. |
| `costo_unitario` | `NUMERIC(10,2)` | Atributo Numérico | NO | Costo de adquisición o manufactura unitario. |
| `monto_subtotal` | `NUMERIC(10,2)` | Métrica Aditiva | NO | `cantidad * precio_unitario`. |
| `monto_costo_total` | `NUMERIC(10,2)` | Métrica Aditiva | NO | `cantidad * costo_unitario`. |
| `monto_descuento_prorrateado` | `NUMERIC(10,2)` | Métrica Aditiva | SÍ | Descuento de cabecera distribuido proporcionalmente al subtotal. |
| `monto_envio_prorrateado` | `NUMERIC(10,2)` | Métrica Aditiva | SÍ | Costo de flete/entrega distribuido proporcionalmente. |
| `monto_venta_neta` | `NUMERIC(10,2)` | Métrica Aditiva | NO | Ingreso neto: `monto_subtotal - monto_descuento_prorrateado`. |
| `ganancia_bruta` | `NUMERIC(10,2)` | Métrica Aditiva | NO | Margen bruto: `monto_venta_neta - monto_costo_total`. |
| `dias_para_entrega` | `INT` | Métrica Logística | SÍ | Tiempo real de despacho: `fecha_real_entrega - fecha_orden`. |
| `retraso_dias` | `INT` | Métrica Logística | SÍ | Incumplimiento: `fecha_real_entrega - fecha_prometida`. |

---

### 2.2. Tablas de Dimensiones

#### 🕒 `Dim_Tiempo`
Contiene el calendario continuo para análisis de estacionalidad, trimestres y cumplimiento.
- `fecha_sk` (PK, `INT`): Clave subrogada formato numérico `YYYYMMDD`.
- `fecha_completa` (`DATE`): Fecha ISO 8601.
- `anio` (`INT`): Año numérico (ej. 2026).
- `mes` (`INT`): Mes del año (1 a 12).
- `dia` (`INT`): Día del mes (1 a 31).
- `nombre_mes` (`VARCHAR(20)`): Nombre completo en español (ej. 'Abril', 'Mayo').
- `trimestre` (`INT`): Trimestre de negocio (1 a 4). Clave para la comparativa Q2 vs Q1.
- `dia_semana` (`VARCHAR(20)`): Día de la semana ('Lunes' a 'Domingo').

#### 🛋️ `Dim_Producto`
Desnormaliza el catálogo corporativo integrando producto, variante, categoría y colección.
- `producto_sk` (PK, `SERIAL`): Clave subrogada a nivel variante.
- `variante_id_bk` (`INT`): Clave de negocio de la variante física.
- `producto_id_bk` (`INT`): Clave de negocio del producto maestro (ej. 401 para Sofá Oslo).
- `nombre_producto` (`VARCHAR(150)`): Denominación comercial del producto.
- `categoria` (`VARCHAR(100)`): Línea de mobiliario (`Salas y Sofás`, `Comedores`, etc.).
- `coleccion` (`VARCHAR(100)`): Línea de diseño (`Nórdica Elegance`, `Industrial Loft`, etc.).
- `marca` (`VARCHAR(100)`): Marca fabricante (`Casa&Estilo Signature`, `Nordic Living`, etc.).
- `color` (`VARCHAR(50)`): Variante de color (`Gris Oxford`, `Beige Arena`, etc.).
- `material` (`VARCHAR(50)`): Material principal (`Lino Premium`, `Madera de Roble`, etc.).
- `tamano` (`VARCHAR(50)`): Especificación dimensional (`3 Cuerpos`, `King Size`, etc.).

#### 📍 `Dim_Showroom`
Modela la red territorial de sucursales físicas y centros de distribución.
- `showroom_sk` (PK, `SERIAL`): Clave subrogada del showroom.
- `showroom_id_bk` (`INT`): Clave de negocio de la sucursal.
- `nombre_showroom` (`VARCHAR(100)`): Nombre comercial de la tienda (ej. 'San Pedro Luxury').
- `ciudad` (`VARCHAR(100)`): Ciudad de operación.
- `zona` (`VARCHAR(100)`): **Región geográfica de negocio** (`Norte`, `Centro`, `Occidente`, `Sur`, `Bajío`). Corresponde directamente a la dimensión de agrupación solicitada por el reto.

#### 👥 `Dim_Cliente`
Segmentación de compradores para personalización comercial.
- `cliente_sk` (PK, `SERIAL`): Clave subrogada del cliente.
- `cliente_id_bk` (`INT`): Clave de negocio del cliente.
- `nombre` (`VARCHAR(150)`): Razón social o nombre del comprador ficticio.
- `tipo_cliente` (`VARCHAR(50)`): Segmento comercial (`Consumidor final`, `Diseñador`, `Arquitecto`, `Corporativo`).
- `ciudad` (`VARCHAR(100)`): Ciudad de residencia o facturación.
- `zona` (`VARCHAR(100)`): Zona territorial del cliente.

#### 💼 `Dim_Asesor`
Representa al equipo de ventas consultivas de Casa&Estilo.
- `asesor_sk` (PK, `SERIAL`): Clave subrogada del asesor.
- `asesor_id_bk` (`INT`): Clave de negocio del empleado.
- `nombre_asesor` (`VARCHAR(150)`): Nombre del profesional de ventas.
- `porcentaje_comision` (`NUMERIC(5,2)`): Tasa pactada de incentivo (3.5% a 6.0%).

#### 🛒 `Dim_Canal`
Canal de comercialización omnicanal.
- `canal_sk` (PK, `SERIAL`): Clave subrogada del canal.
- `nombre_canal` (`VARCHAR(50)`): `Showroom Físico`, `E-commerce Web`, `Venta Telefónica / WhatsApp Concierge`, `Diseño por Proyecto / B2B`.
