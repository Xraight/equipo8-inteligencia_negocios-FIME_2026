# 🔍 Fase A · Perfilado de Calidad e Ingesta en Power Query

## 🎯 Objetivo de la Fase
Importar y transformar los cuatro archivos CSV fuente mediante **Power Query** (M-Language) sin alterar los datos originales, garantizando la integridad de tipos, ausencia de duplicados en claves primarias, validación de reglas de negocio y carga exclusiva en el Modelo de Datos de Excel (conexión de solo datos).

---

## 📊 Matriz de Perfilado y Reglas de Calidad

| Consulta / Tabla | Columna | Tipo M Esperado | Validación de Regla | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FACT_VENTAS** | `id_venta` | `Int64.Type` | Clave primaria transaccional, sin nulos | 1,200 valores únicos [1..1200] | ✅ Válido |
| **FACT_VENTAS** | `id_producto` | `Int64.Type` | Integridad referencial con DIM_PRODUCTO | Rango [1..12], 0 nulos | ✅ Válido |
| **FACT_VENTAS** | `id_cliente` | `Int64.Type` | Integridad referencial con DIM_CLIENTE | Rango [1..80], 0 nulos | ✅ Válido |
| **FACT_VENTAS** | `id_tiempo` | `Int64.Type` | Integridad referencial con DIM_TIEMPO | Rango [1..96], 0 nulos | ✅ Válido |
| **FACT_VENTAS** | `cantidad` | `Int64.Type` | `cantidad > 0` (unidades vendidas) | Mín: 1, Máx: 5, Promedio: 3.02 | ✅ Válido |
| **FACT_VENTAS** | `monto` | `type number` | `monto >= 0.0` (ingreso bruto) | Mín: $249.00, Máx: $5,505.00 | ✅ Válido |
| **FACT_VENTAS** | `costo` | `type number` | `costo >= 0.0` y `costo <= monto` | Mín: $147.49, Máx: $4,442.36 | ✅ Válido |
| **DIM_PRODUCTO** | `id_producto` | `Int64.Type` | Unicidad estricta (PK) | 12 valores únicos [1..12] | ✅ Válido |
| **DIM_PRODUCTO** | `producto` | `type text` | Cadena no vacía ni nula | 12 nombres normalizados | ✅ Válido |
| **DIM_PRODUCTO** | `categoria` | `type text` | Categorías canónicas autorizadas | 3 categorías: Hogar, Oficina, Tecnología | ✅ Válido |
| **DIM_CLIENTE** | `id_cliente` | `Int64.Type` | Unicidad estricta (PK) | 80 valores únicos [1..80] | ✅ Válido |
| **DIM_CLIENTE** | `cliente` | `type text` | Cadena no vacía | 80 clientes normalizados [Cliente 001..080] | ✅ Válido |
| **DIM_CLIENTE** | `region` | `type text` | Regiones geográficas estándar | 4 regiones: Centro, Sur, Occidente, Norte | ✅ Válido |
| **DIM_TIEMPO** | `id_tiempo` | `Int64.Type` | Unicidad estricta (PK) | 96 valores únicos [1..96] | ✅ Válido |
| **DIM_TIEMPO** | `fecha` | `type date` | Formato fecha ISO `YYYY-MM-DD` | 96 fechas válidas (2025-01-05 a 2026-12-26) | ✅ Válido |
| **DIM_TIEMPO** | `anio` | `Int64.Type` | Año fiscal válido | 2025 (48 cortes) y 2026 (48 cortes) | ✅ Válido |
| **DIM_TIEMPO** | `mes` | `Int64.Type` | Rango mensual [1..12] | 12 meses representados equitativamente | ✅ Válido |

---

## 🛠️ Procedimiento Paso a Paso en Power Query (Excel 365)

1. **Obtención de Datos:**
   - En la cinta de Excel: `Datos` → `Obtener datos` → `Desde archivo` → `Desde texto/CSV`.
   - Seleccionar individualmente cada archivo: `FACT_VENTAS.csv`, `DIM_PRODUCTO.csv`, `DIM_CLIENTE.csv`, `DIM_TIEMPO.csv`.
   - Confirmar **Delimitador: Coma** y **Codificación: 65001: Unicode (UTF-8)**.
   - Presionar **Transformar datos** (evitar cargar directamente para asegurar la verificación de tipos).

2. **Renombrado y Verificación de Encabezados:**
   - Confirmar que la primera fila se promueva automáticamente como encabezado (`Table.PromoteHeaders`).
   - Asignar nombres limpios a las consultas: `FACT_VENTAS`, `DIM_PRODUCTO`, `DIM_CLIENTE`, `DIM_TIEMPO`.

3. **Tipado Explícito y Manejo Regional:**
   - En `DIM_TIEMPO`, forzar la conversión de `fecha` a tipo Fecha (`type date`). Si la configuración local de Windows utiliza formato `DD/MM/AAAA`, emplear `Cambiar tipo usando configuración regional` → `Fecha` con configuración `Inglés (Estados Unidos)` o `Español (México)` según el estándar ISO `YYYY-MM-DD`.
   - En `FACT_VENTAS`, verificar que `monto` y `costo` sean números decimales y no cadenas de texto.

4. **Auditoría con Herramientas de Perfilado:**
   - Ir a la pestaña `Vista` y marcar:
     * `Calidad de columnas` (confirmando 100% Válido, 0% Error, 0% Vacío).
     * `Distribución de columnas` (confirmando cardinalidad en claves primarias).
     * `Perfil de columna`.

5. **Carga en el Modelo de Datos:**
   - En `Inicio` → `Cerrar y cargar en...`.
   - Seleccionar: **Solo crear conexión**.
   - Marcar obligatoriamente la casilla: **☑ Agregar estos datos al Modelo de datos**.
