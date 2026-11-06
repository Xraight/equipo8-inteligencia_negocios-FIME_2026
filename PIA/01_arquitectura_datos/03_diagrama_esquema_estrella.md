# Esquema Estrella Analítico (Data Mart) — Casa&Estilo
## Modelo Dimensional para Analítica de Negocio (MySQL 8.0 & Power Pivot)

---

### Metadatos
- **Materia:** Analítica e Inteligencia de Negocios
- **Institución:** FIME — UANL
- **Equipo:** Equipo 8
- **Función General:** Documentar el diseño del modelo dimensional en esquema estrella (constelación de hechos) implementado en el Data Mart de Casa&Estilo.
- **Función Específica:** Definir las tablas de hechos, dimensiones conformes, atributos de análisis y cardinalidades que alimentan los tableros de control ejecutivos y cálculos en DAX.

---

## 1. Diagrama de la Arquitectura Dimensional (Esquema Estrella)

```mermaid
classDiagram
    direction TB

    class DIM_TIEMPO {
        +int tiempo_id PK
        +date fecha
        +smallint anio
        +tinyint trimestre
        +varchar trimestre_nombre
        +tinyint mes
        +varchar mes_nombre
        +varchar mes_anio
        +tinyint semana_anio
        +tinyint dia_mes
        +tinyint dia_semana
        +varchar dia_semana_nombre
        +tinyint es_fin_semana
    }

    class DIM_PRODUCTO {
        +int producto_key PK
        +varchar producto_id
        +varchar sku
        +varchar producto
        +varchar categoria
        +varchar marca
        +decimal costo
        +decimal precio_lista
        +decimal margen_teorico_pct
        +char activo
        +char requiere_instalacion
    }

    class DIM_CLIENTE {
        +int cliente_key PK
        +varchar cliente_id
        +varchar nombre
        +varchar sexo
        +date fecha_alta
        +varchar ciudad
        +varchar segmento
        +varchar email
    }

    class DIM_SUCURSAL {
        +int sucursal_key PK
        +varchar sucursal_id
        +varchar sucursal
        +varchar ciudad
        +varchar estado
        +int m2
        +varchar categoria_tamano
        +date fecha_apertura
    }

    class DIM_CANAL {
        +tinyint canal_id PK
        +varchar canal_nombre
    }

    class DIM_METODO_PAGO {
        +tinyint metodo_pago_id PK
        +varchar metodo_nombre
    }

    class FACT_VENTAS_DETALLE {
        +varchar venta_id PK
        +int linea PK
        +int tiempo_id FK
        +int producto_key FK
        +int cliente_key FK
        +int sucursal_key FK
        +tinyint canal_id FK
        +tinyint metodo_pago_id FK
        +time hora_venta
        +int cantidad
        +decimal precio_unitario
        +decimal descuento_pct
        +decimal monto_bruto
        +decimal monto_descuento
        +decimal monto_neto
        +decimal costo_unitario
        +decimal costo_total
        +decimal utilidad_bruta
        +decimal margen_pct
        +tinyint es_devuelto
    }

    class FACT_DEVOLUCIONES {
        +varchar devolucion_id PK
        +varchar venta_id
        +int tiempo_id FK
        +int producto_key FK
        +int sucursal_key FK
        +int cliente_key FK
        +int cantidad_devuelta
        +decimal importe_devuelto
        +varchar motivo
    }

    class FACT_INSTALACIONES {
        +varchar instalacion_id PK
        +varchar venta_id
        +int tiempo_id FK
        +int cliente_key FK
        +int sucursal_key FK
        +int dias_programados
        +int dias_reales
        +int dias_desviacion
        +tinyint cumplio_sla
        +int satisfaccion
    }

    class FACT_INVENTARIO_SNAPSHOT {
        +int sucursal_key PK,FK
        +int producto_key PK,FK
        +int stock_actual
        +int punto_reorden
        +int deficit_unidades
        +decimal valor_inventario_costo
    }

    DIM_TIEMPO "1" <-- "*" FACT_VENTAS_DETALLE : tiempo_id
    DIM_PRODUCTO "1" <-- "*" FACT_VENTAS_DETALLE : producto_key
    DIM_CLIENTE "1" <-- "*" FACT_VENTAS_DETALLE : cliente_key
    DIM_SUCURSAL "1" <-- "*" FACT_VENTAS_DETALLE : sucursal_key
    DIM_CANAL "1" <-- "*" FACT_VENTAS_DETALLE : canal_id
    DIM_METODO_PAGO "1" <-- "*" FACT_VENTAS_DETALLE : metodo_pago_id

    DIM_TIEMPO "1" <-- "*" FACT_DEVOLUCIONES : tiempo_id
    DIM_PRODUCTO "1" <-- "*" FACT_DEVOLUCIONES : producto_key
    DIM_SUCURSAL "1" <-- "*" FACT_DEVOLUCIONES : sucursal_key
    DIM_CLIENTE "1" <-- "*" FACT_DEVOLUCIONES : cliente_key

    DIM_TIEMPO "1" <-- "*" FACT_INSTALACIONES : tiempo_id
    DIM_CLIENTE "1" <-- "*" FACT_INSTALACIONES : cliente_key
    DIM_SUCURSAL "1" <-- "*" FACT_INSTALACIONES : sucursal_key

    DIM_PRODUCTO "1" <-- "*" FACT_INVENTARIO_SNAPSHOT : producto_key
    DIM_SUCURSAL "1" <-- "*" FACT_INVENTARIO_SNAPSHOT : sucursal_key
```

---

## 2. Descripción de Dimensiones y Métricas Clave

### 2.1. Métricas Hecho Principal: `FACT_VENTAS_DETALLE`
- **Monto Bruto:** Facturación antes de promociones y bonificaciones ($Cantidad \times PrecioUnitario$).
- **Monto Descuento:** Ahorro trasladado al cliente según campañas comerciales.
- **Monto Neto:** Ingreso efectivo de la caja de Casa&Estilo ($MontoBruto - MontoDescuento$).
- **Costo Total (COGS):** Costo histórico de los bienes adquiridos al proveedor ($Cantidad \times CostoUnitario$).
- **Utilidad Bruta:** Margen de contribución comercial generado ($MontoNeto - CostoTotal$).
- **Margen Porcentual:** Rentabilidad porcentual sobre el ingreso neto ($\frac{UtilidadBruta}{MontoNeto} \times 100$).

### 2.2. Métricas de Hechos Secundarios
- **Tasa de Reembolsos por Devolución:** Monto total devuelto contrastado con ventas brutas de la categoría.
- **Índice de Nivel de Servicio (SLA) de Instalación:** Porcentaje de instalaciones completadas en un tiempo $\le$ a los días programados.
- **Varianza Promedio de Retraso:** $\text{Días Reales} - \text{Días Programados}$.
- **Riesgo de Desabasto en Inventario:** Unidades en déficit frente al punto de reorden por tienda.
