# ⚖️ Fase D · Validación Numérica y Cifras de Control

## 🎯 Objetivo de la Fase
Contrastar rigurosamente los cálculos agregados obtenidos en el Modelo de Datos contra las cifras de control institucionales provistas en el material del laboratorio, documentando cualquier discrepancia y auditando los subtotales por corte dimensional.

---

## 📊 Matriz de Validación de Cifras de Control Globales

| Indicador | Fórmula DAX | Valor Esperado (Control) | Valor Calculado (Modelo) | Discrepancia Absoluta | Discrepancia Relativa (%) | Estado de Calidad |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Transacciones** | `DISTINCTCOUNT(FACT_VENTAS[id_venta])` | `1,200` | `1,200` | `0` | `0.00%` | ✅ **Exacto** |
| **Ventas Totales** | `SUM(FACT_VENTAS[monto])` | `MXN $2,416,376.00` | `MXN $2,416,376.00` | `$0.00` | `0.00%` | ✅ **Exacto** |
| **Costo Total** | `SUM(FACT_VENTAS[costo])` | `MXN $1,704,180.38` | `MXN $1,704,180.38` | `$0.00` | `0.00%` | ✅ **Exacto** |
| **Margen Bruto** | `[Ventas] - [Costo]` | `MXN $712,195.62` | `MXN $712,195.62` | `$0.00` | `0.00%` | ✅ **Exacto** |
| **Ticket Promedio**| `DIVIDE([Ventas], [Transacciones], 0)` | `MXN $2,013.65` | `MXN $2,013.6467...` ≈ `$2,013.65` | `$0.00` | `0.00%` | ✅ **Exacto** |

> [!NOTE]
> **Conclusión de Control:** La conciliación cuantitativa demuestra una coincidencia del **100.00%** en todas las cifras de control. No existen registros duplicados, omisiones de carga ni errores en el separador decimal.

---

## 🔍 Subtotales de Control por Dimensión

### 1. Control Temporal (Por Año)
| Año | Transacciones | Unidades | Ventas (MXN) | Costo (MXN) | Margen Bruto (MXN) | Margen % | Ticket Promedio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2025** | 603 | 1,841 | $1,214,067.00 | $855,921.74 | $358,145.26 | 29.50% | $2,013.38 |
| **2026** | 597 | 1,781 | $1,202,309.00 | $848,258.64 | $354,050.36 | 29.45% | $2,013.92 |
| **Total Global** | **1,200** | **3,622** | **$2,416,376.00** | **$1,704,180.38** | **$712,195.62** | **29.47%** | **$2,013.65** |

---

### 2. Control Geográfico (Por Región)
| Región | Clientes en Dimensión | Transacciones | Ventas (MXN) | Participación (%) | Margen Bruto (MXN) | Margen % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Occidente** | 20 | 327 | $677,408.00 | 28.03% | $197,187.02 | 29.11% |
| **Centro** | 20 | 324 | $655,677.00 | 27.13% | $192,170.15 | 29.31% |
| **Sur** | 20 | 298 | $608,288.00 | 25.17% | $184,829.89 | 30.39% |
| **Norte** | 20 | 251 | $475,003.00 | 19.66% | $138,008.56 | 29.05% |
| **Total** | **80** | **1,200** | **$2,416,376.00** | **100.00%** | **$712,195.62** | **29.47%** |

---

### 3. Control por Categoría de Producto
| Categoría | Productos en Catálogo | Transacciones | Ventas (MXN) | Participación (%) | Margen Bruto (MXN) | Margen % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tecnología** | 4 | 407 | $889,916.00 | 36.83% | $268,103.26 | 30.13% |
| **Oficina** | 4 | 401 | $801,265.00 | 33.16% | $229,328.32 | 28.62% |
| **Hogar** | 4 | 392 | $725,195.00 | 30.01% | $214,764.04 | 29.61% |
| **Total** | **12** | **1,200** | **$2,416,376.00** | **100.00%** | **$712,195.62** | **29.47%** |

---

### 4. Ranking de Productos (Top 5 en Ventas)
| Posición | Producto | Categoría | Transacciones | Unidades | Ventas (MXN) | Margen Bruto (MXN) | Margen % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Producto 12** | Tecnología | 106 | 322 | $346,902.00 | $111,004.30 | 32.00% |
| **2** | **Producto 10** | Hogar | 106 | 307 | $285,698.00 | $84,661.20 | 29.63% |
| **3** | **Producto 11** | Oficina | 95 | 285 | $285,677.00 | $80,171.08 | 28.06% |
| **4** | **Producto 09** | Tecnología | 103 | 287 | $245,429.00 | $70,910.65 | 28.89% |
| **5** | **Producto 08** | Oficina | 96 | 298 | $233,984.00 | $67,314.65 | 28.77% |
