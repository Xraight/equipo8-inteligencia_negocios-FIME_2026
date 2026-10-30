# 🛑 Documentación de Validación y Rechazos (Paso 4)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/04_validacion_y_rechazos/documentacion_rechazos.md`  
**Autor:** Equipo 8

---

## 📌 Enfoque Metodológico: Cuarentena de Datos (Error Mart)

En lugar de descartar silenciosamente filas corruptas o detener abruptamente el pipeline con un error de base de datos, el pipeline implementa un patrón de **Mesa de Rechazos (Quarantine / Error Mart)** mediante la tabla `pedidos_rechazados`.

### Ventajas de la Cuarentena
1. **Trazabilidad Total:** Cada registro corrupto retiene su valor crudo original (`importe_raw`, `fecha_pedido_raw`), la fila de origen (`fila_id`) y el motivo exacto de su descalificación.
2. **Reclamación a Sistemas Origen:** Permite generar reportes operativos para que el equipo del sistema transaccional corrija bugs de captura o bugs en la API de ventas.
3. **Protección del Data Mart:** Garantiza que a `fact_ordenes` solo lleguen hechos con integridad referencial completa y coherencia matemática.

---

## 📋 Diccionario de Reglas de Rechazo

| Código de Rechazo | Regla de Calidad Evaluada | Expresión Lógica de Fallo | Impacto en Caso de Carga no Controlada |
| :--- | :--- | :--- | :--- |
| `ID_PEDIDO_DUPLICADO` | Unicidad transaccional | `ROW_NUMBER() OVER (PARTITION BY id_pedido ORDER BY fila_id ASC) > 1` | Colisión de clave primaria ($PK$) o duplicación en el cálculo de ingresos. |
| `CLIENTE_INEXISTENTE` | Integridad referencial | `id_cliente NOT IN (SELECT id_cliente FROM stg_clientes)` | Error de clave foránea ($FK$) o ventas atribuidas a entidades fantasmas. |
| `FECHA_INVALIDA` | Validez temporal | `fecha_pedido_norm IS NULL` (fechas vacías o corruptas) | Imposibilidad de agregar métricas en la jerarquía de tiempo. |
| `IMPORTE_NO_POSITIVO` | Validez económica | `importe_norm IS NULL OR importe_norm <= 0` | Distorsión del valor económico (ventas en cero o montos negativos). |
| `ESTADO_NO_RECONOCIDO` | Validez geográfica | `estado_envio_canonico IS NULL` | Imposibilidad de segmentación regional de la logística. |

---

## 📊 Resultados Esperados de la Cuarentena

En nuestro conjunto de datos de prueba (30 filas en `raw_pedidos`):

```text
+----------------------+------------------+----------------------+
| Motivo de Rechazo    | Total Rechazados | Pedidos Afectados    |
+----------------------+------------------+----------------------+
| FECHA_INVALIDA       |                2 | PED-1024, PED-1025   |
| IMPORTE_NO_POSITIVO  |                2 | PED-1021, PED-1022   |
| ID_PEDIDO_DUPLICADO  |                2 | PED-1001, PED-1010   |
| CLIENTE_INEXISTENTE  |                1 | PED-1023             |
| ESTADO_NO_RECONOCIDO |                1 | PED-1026             |
+----------------------+------------------+----------------------+
TOTAL EN CUARENTENA: 8 transacciones
TOTAL EN STAGING LIMPIO: 22 transacciones válidas
```
