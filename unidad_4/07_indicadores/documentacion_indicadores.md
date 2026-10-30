# 📊 Documentación de Indicadores de Negocio (Paso 7)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/07_indicadores/documentacion_indicadores.md`  
**Autor:** Equipo 8

---

## 📌 Definición de Métricas y Supuestos de Negocio

### Definición Operativa de Métricas:
1. **Pedidos Entregados:** Conteo de transacciones únicas donde la orden cumplió exitosamente su ciclo de vida logístico (`estado_pedido = 'Entregado'`). Se excluyen órdenes en estatus `'Pendiente'`, `'En tránsito'` o `'Cancelado'`.
2. **Ventas Netas (Supuesto Académico):**
   $$\text{Ventas Netas} = \sum_{\text{estado\_pedido} = \text{'Entregado'}} \text{importe}$$

### ⚠️ Aclaración Metodológica y Contable
En la contabilidad financiera real de un retail o e-commerce, las **Ventas Netas** se obtienen a partir de una fórmula multidimensional:

$$\text{Ventas Netas (Real)} = \text{Ingresos Brutos Facturados} - \text{Descuentos Comerciales} - \text{Devoluciones / Notas de Crédito} - \text{Rebajas y Bonificaciones}$$

En este laboratorio, por especificación académica, no se modelaron catálogos de impuestos (IVA), esquemas de descuentos ni tablas de devoluciones. Por consiguiente, asumir que las órdenes entregadas equivalen a las ventas netas es un supuesto simplificado de ingeniería de datos y no debe confundirse con un estado de resultados contable normado por NIF o IFRS.

---

## 📈 Resultados Analíticos Consolidados por Estado

```text
+-----------------+--------------------+---------------------------+--------------------+-------------------------+-----------------+
| estado_canonico | estado             | total_pedidos_entregados  | total_ventas_netas | porcentaje_participacion| ticket_promedio |
+-----------------+--------------------+---------------------------+--------------------+-------------------------+-----------------+
| YUC             | Yucatán            |                         3 |            6330.00 |                   18.23 |         2110.00 |
| PUE             | Puebla             |                         3 |            6100.00 |                   17.57 |         2033.33 |
| CDMX            | Ciudad de México   |                         2 |            3550.00 |                   10.22 |         1775.00 |
| VER             | Veracruz           |                         1 |            3400.00 |                    9.79 |         3400.00 |
| JAL             | Jalisco            |                         2 |            3950.00 |                   11.38 |         1975.00 |
| QRO             | Querétaro          |                         3 |            4400.00 |                   12.67 |         1466.67 |
| COAH            | Coahuila           |                         2 |            2810.00 |                    8.09 |         1405.00 |
| NL              | Nuevo León         |                         2 |            2090.50 |                    6.02 |         1045.25 |
| GTO             | Guanajuato         |                         2 |            2080.00 |                    5.99 |         1040.00 |
| TAM             | Tamaulipas         |                         1 |            1100.00 |                    3.17 |         1100.00 |
+-----------------+--------------------+---------------------------+--------------------+-------------------------+-----------------+
TOTAL GENERAL:                             19 pedidos entregados       $34,720.50 (100%)
```

*(Nota: De las 22 órdenes válidas totales en `fact_ordenes`, 19 fueron entregadas (\$34,720.50), 1 está cancelada (\$1,800.00), 1 en tránsito (\$950.00) y 1 pendiente (\$650.00), sumando exactamente los \$38,120.50 validados).*
