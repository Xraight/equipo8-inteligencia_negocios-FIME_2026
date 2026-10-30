# 🔍 Reporte de Perfilado de Datos (Paso 1)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/02_perfilado/reporte_perfilado.md`  
**Autor:** Equipo 8

---

## 📌 Objetivo del Perfilado
El perfilado de datos es el diagnóstico preliminar de calidad de datos ejecutado sobre las zonas de aterrizaje crudas (`raw_*`) y catálogos de referencia (`catalogo_estados`). Su objetivo es cuantificar la volumetría real, identificar claves candidatas, diagnosticar el tipado técnico y detectar anomalías deliberadas o inherentes a las fuentes transaccionales sin alterar los archivos de origen.

---

## 🗄️ Metadatos e Identificación de Tablas

| Tabla Origen | Clave Candidata Primaria | Grano de la Información | Columnas Crudas | Tipos de Datos Asignados |
| :--- | :--- | :--- | :--- | :--- |
| `raw_clientes` | `fila_id` (Técnica) / `id_cliente` (Natural) | Un registro por cliente recibido en el CSV | 6 (`fila_id`, `id_cliente`, `nombre`, `email`, `estado`, `fecha_registro`) | `INT` (PK), `VARCHAR(50)`, `VARCHAR(150)`, `VARCHAR(150)`, `VARCHAR(100)`, `VARCHAR(50)` |
| `raw_pedidos` | `fila_id` (Técnica) / `id_pedido` (Natural) | Una transacción de orden de compra | 7 (`fila_id`, `id_pedido`, `id_cliente`, `fecha_pedido`, `importe`, `estado_pedido`, `estado_envio`) | `INT` (PK), `VARCHAR(50)`, `VARCHAR(50)`, `VARCHAR(50)`, `VARCHAR(50)`, `VARCHAR(50)`, `VARCHAR(100)` |
| `catalogo_estados` | `estado_canonico` | Un registro por entidad federativa reconocida | 3 (`estado_canonico`, `nombre_oficial`, `alias`) | `VARCHAR(10)` (PK), `VARCHAR(100)`, `TEXT` |

---

## 📊 Matriz de Hallazgos en `observaciones_perfilado`

A continuación se resume el inventario de hallazgos capturados automáticamente por `01_perfilado_datos.sql`:

```text
+----------------+------------------------------------+---------------------+-----------+-------------------------------------------------------------+
| Tabla Origen   | Regla o Métrica                    | Registros Afectados | Severidad | Detalle del Hallazgo                                        |
+----------------+------------------------------------+---------------------+-----------+-------------------------------------------------------------+
| raw_clientes   | VOLUMETRIA_TOTAL                   |                  21 | INFO      | Total registros ingresados desde clientes.csv               |
| raw_pedidos    | VOLUMETRIA_TOTAL                   |                  30 | INFO      | Total transacciones ingresadas desde pedidos.sql            |
| catalogo_estados| VOLUMETRIA_TOTAL                  |                  10 | INFO      | Entidades federativas canónicas registradas                 |
| raw_clientes   | DUPLICADOS_ID_CLIENTE              |                   1 | ALTA      | Cliente CLI-005 con 2 apariciones (diferentes estados)      |
| raw_pedidos    | DUPLICADOS_ID_PEDIDO               |                   2 | ALTA      | Pedidos PED-1001 y PED-1010 duplicados                      |
| raw_clientes   | ESTADOS_NO_ESTANDARIZADOS_O_VACIOS |                   9 | MEDIA     | Uso de alias ('N.L.', 'D.F.'), vacíos ('') o desconocidos   |
| raw_pedidos    | ESTADOS_ENVIO_NO_CANONICOS         |                   8 | MEDIA     | Alias de estados ('Nuevo Leon', 'D.F.') o 'ESTADO_INEXISTENTE'|
| raw_clientes   | FECHAS_CLIENTE_NO_ISO_O_VACIAS     |                   5 | MEDIA     | Formatos DD/MM/AAAA ('14/02/2026') o fechas vacías ('')     |
| raw_pedidos    | FECHAS_PEDIDO_INVALIDAS_O_NO_ISO   |                   6 | ALTA      | Formatos DD/MM/AAAA, fecha vacía ('') y fecha rota          |
| raw_pedidos    | MONTOS_NO_POSITIVOS                |                   2 | ALTA      | Importe negativo ('-350.00' en PED-1021) y cero ('0.00')    |
| raw_pedidos    | CLIENTES_HUERFANOS                 |                   1 | ALTA      | Pedido PED-1023 apunta a CLI-999 inexistente en clientes    |
+----------------+------------------------------------+---------------------+-----------+-------------------------------------------------------------+
```

---

## 🛠️ Justificación Técnica de Severidades

1. **Severidad ALTA (Bloqueantes de Integridad Dimensional):**
   - **Claves duplicadas (`DUPLICADOS_ID_PEDIDO` y `DUPLICADOS_ID_CLIENTE`):** Violarían la clave primaria de las tablas finales (`dim_cliente` y `fact_ordenes`), provocando errores de colisión o sobreestimación de ventas.
   - **Clientes huérfanos (`CLIENTES_HUERFANOS`):** Violarían la integridad referencial ($FK$), impidiendo que la tabla de hechos pueda vincularse con la dimensión de clientes.
   - **Montos no positivos (`MONTOS_NO_POSITIVOS`):** Distorsionan las métricas de ingresos, promedios y balances contables del negocio.
   - **Fechas corruptas (`FECHAS_PEDIDO_INVALIDAS`):** Imposibilitan el análisis temporal por año, mes o trimestre.

2. **Severidad MEDIA (Requieren Limpieza y Transformación en Staging):**
   - **Variantes de estado y formatos de fecha:** No implican descarte inmediato del registro si pueden ser homologados determinísticamente a través de catálogos y funciones de casteo (`STR_TO_DATE`).
