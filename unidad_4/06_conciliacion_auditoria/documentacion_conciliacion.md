# ⚖️ Documentación de Conciliación y Auditoría (Paso 6)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/06_conciliacion_auditoria/documentacion_conciliacion.md`  
**Autor:** Equipo 8

---

## 📌 Balance de Masa (Cuadratura Cuantitativa)

El principio de balance de masa en ingeniería de datos establece que cada registro recibido en la capa de aterrizaje debe estar plenamente justificado en las capas subsiguientes:

$$\text{Filas Raw} = \text{Filas Aceptadas Únicas} + \text{Filas Rechazadas}$$

### Cuadratura Obtenida en el Laboratorio:
- **Total Filas en `raw_pedidos`:** 30 registros.
- **Total Filas en `stg_pedidos_limpios`:** 22 registros.
- **Total Filas en `pedidos_rechazados`:** 8 registros.
- **Discrepancia Matemática:** $30 - (22 + 8) = 0$ (Balance 100% Cuadrado).

```text
+----------------------+-----------------------+-------------------------+-------------------+--------------+------------------+
| Total Recibido (Raw) | Aceptadas Únicas (Stg)| Rechazadas (Cuarentena) | Total Justificado | Discrepancia | Balance Cuadrado |
+----------------------+-----------------------+-------------------------+-------------------+--------------+------------------+
|                   30 |                    22 |                       8 |                30 |            0 | SI               |
+----------------------+-----------------------+-------------------------+-------------------+--------------+------------------+
```

---

## 💰 Comparación de Importes: Staging vs. Hechos

La conciliación entre `stg_pedidos_limpios` y `fact_ordenes` verifica que la carga al Data Mart no haya perdido precisión decimal ni omitido registros válidos:

- **Suma de importes en `stg_pedidos_limpios`:** \$38,120.50
- **Suma de importes en `fact_ordenes`:** \$38,120.50
- **Desvío Financiero:** \$0.00 (Integridad Financiera Absoluta).

---

## ❓ ¿Por qué el Total Bruto Difiere del Total Válido?

El total monetario bruto calculado directamente sobre la capa cruda (`raw_pedidos`) difiere drásticamente del total válido consolidado en el Data Mart por las siguientes razones analíticas y contables:

1. **Exclusión de Transacciones Corruptas o Inválidas:**
   - La capa raw contiene importes no positivos (como `-$350.00` o `$0.00`) que no representan intercambios de valor válidos bajo las reglas del negocio de e-commerce.
   - Contiene pedidos con destino a estados no reconocidos (`$1,400.00` a `ESTADO_INEXISTENTE`) o con clientes inexistentes (`$1,500.00` de `CLI-999`), los cuales no pueden ser entregados ni atribuidos a ninguna cuenta.
   - Contiene pedidos con fechas no computables (`$1,200.00` y `$980.00`), que distorsionarían las series temporales analíticas.
2. **Eliminación de Registros Duplicados:**
   - En `raw_pedidos`, transacciones como `PED-1001` (`$1,250.00`) y `PED-1010` (`$2,650.00`) se recibieron duplicadas por reintentos de red o fallas en el webhook. Sumar el archivo crudo inflaría artificialmente la facturación en `$3,900.00`.
3. **Conclusión Contable:**
   El total bruto de la capa raw es una medida de tráfico operacional crudo, mientras que el total válido del Data Mart representa la **verdad transaccional única y gobernada** para la toma de decisiones directivas.
