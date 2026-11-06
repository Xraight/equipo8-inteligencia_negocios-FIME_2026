# 📐 Fase C · Catálogo de Medidas DAX

## 🎯 Objetivo de la Fase
Definir, documentar e implementar las **seis medidas DAX fundamentales** y las medidas complementarias de inteligencia analítica en el área de cálculo de `FACT_VENTAS` dentro de Power Pivot (Excel 365).

---

## 📑 Catálogo de Medidas Fundamentales

### 1. Ventas
- **Fórmula DAX:**
  ```dax
  Ventas := SUM(FACT_VENTAS[monto])
  ```
- **Interpretación de Negocio:** Suma acumulada de los ingresos brutos generados por todas las transacciones dentro del contexto de filtro actual.
- **Tipo de Dato y Formato:** Moneda (`MXN $#,##0.00`).
- **Valor Global sin Filtros:** `$2,416,376.00`.

---

### 2. Costo
- **Fórmula DAX:**
  ```dax
  Costo := SUM(FACT_VENTAS[costo])
  ```
- **Interpretación de Negocio:** Suma total del costo de los bienes vendidos (COGS) asociado a las transacciones registradas.
- **Tipo de Dato y Formato:** Moneda (`MXN $#,##0.00`).
- **Valor Global sin Filtros:** `$1,704,180.38`.

---

### 3. Margen Bruto
- **Fórmula DAX:**
  ```dax
  Margen Bruto := [Ventas] - [Costo]
  ```
- **Interpretación de Negocio:** Utilidad bruta directa resultante de descontar el costo de adquisición a los ingresos por venta antes de gastos operativos.
- **Tipo de Dato y Formato:** Moneda (`MXN $#,##0.00`).
- **Valor Global sin Filtros:** `$712,195.62`.

---

### 4. Margen %
- **Fórmula DAX:**
  ```dax
  Margen % := DIVIDE([Margen Bruto], [Ventas], 0)
  ```
- **Interpretación de Negocio:** Proporción porcentual del ingreso que la empresa conserva como margen bruto. Permite comparar la rentabilidad relativa entre productos y regiones con volúmenes dispares.
- **Tipo de Dato y Formato:** Porcentaje (`0.0%` o `0.00%`).
- **Valor Global sin Filtros:** `29.47%` (~`29.5%`).

---

### 5. Transacciones
- **Fórmula DAX:**
  ```dax
  Transacciones := DISTINCTCOUNT(FACT_VENTAS[id_venta])
  ```
- **Interpretación de Negocio:** Conteo cardinal de identificadores únicos de venta. Al estar a grano de transacción, refleja el volumen total de pedidos o notas procesadas.
- **Tipo de Dato y Formato:** Número entero (`#,##0`).
- **Valor Global sin Filtros:** `1,200`.

---

### 6. Ticket Promedio
- **Fórmula DAX:**
  ```dax
  Ticket Promedio := DIVIDE([Ventas], [Transacciones], 0)
  ```
- **Interpretación de Negocio:** Ingreso monetario medio generado por cada transacción individual efectuada.
- **Tipo de Dato y Formato:** Moneda (`MXN $#,##0.00`).
- **Valor Global sin Filtros:** `$2,013.65`.

---

## 📈 Medidas Analíticas Complementarias (Comparativas y YoY)

### 7. Unidades Vendidas
```dax
Unidades Vendidas := SUM(FACT_VENTAS[cantidad])
```
- **Valor Global:** `3,622` unidades.

### 8. Ventas 2025 y Ventas 2026
```dax
Ventas 2025 := CALCULATE([Ventas], DIM_TIEMPO[anio] = 2025)
Ventas 2026 := CALCULATE([Ventas], DIM_TIEMPO[anio] = 2026)
```
- **Valores:** Ventas 2025 = `$1,214,067.00` | Ventas 2026 = `$1,202,309.00`.

### 9. Crecimiento YoY (Anual)
```dax
Crecimiento YoY := DIVIDE([Ventas 2026] - [Ventas 2025], [Ventas 2025], 0)
```
- **Valor Global:** `-0.97%` (Variación nominal de `-$11,758.00`).

---

## 🌐 Nota de Configuración Regional en DAX
Dependiendo del idioma y configuración regional de Windows/Excel:
- **Configuración Inglés / Estándar:** Las funciones separan argumentos con comas:  
  `DIVIDE([Margen Bruto], [Ventas], 0)`
- **Configuración Español (España/Latinoamérica con coma decimal):** Las funciones separan argumentos con punto y coma:  
  `DIVIDE([Margen Bruto]; [Ventas]; 0)`
