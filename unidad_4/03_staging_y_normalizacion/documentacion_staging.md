# 📦 Documentación de Staging y Normalización (Pasos 2 y 3)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/03_staging_y_normalizacion/documentacion_staging.md`  
**Autor:** Equipo 8

---

## 🎯 1. Fundamentación de Arquitectura de Capas: ¿Por qué la Capa Raw es Inmutable?

En una arquitectura de datos moderna y profesional (Data Warehouse / Lakehouse), la zona de aterrizaje cruda (**`raw_*`**) debe permanecer **estrictamente inmutable**. Nunca se debe ejecutar un `UPDATE`, `DELETE` o transformación destructiva sobre esta capa por las siguientes razones:

1. **Reprocesabilidad e Idempotencia:** Si se descubren nuevas reglas de negocio, errores en el código de transformación o si se actualizan los catálogos maestros, contar con los datos crudos originales permite reconstruir todo el Data Mart desde cero sin necesidad de solicitar reenvíos de datos al sistema operacional fuente.
2. **Auditoría Forense y Trazabilidad:** Ante discrepancias contables o fiscales, la capa raw constituye la evidencia legal inalterada del estado en que los datos llegaron al almacén.
3. **Desacoplamiento Operacional:** Aísla el proceso de ingesta rápida del proceso de cómputo analítico intensivo, evitando bloqueos en bases de datos transaccionales.

La zona de **`stg_*` (Staging)** actúa como la primera frontera de refinamiento: traduce formatos de texto flexible a tipos de datos nativos fuertemente tipados (`DATE`, `DECIMAL`), aplica deduplicación determinista y resuelve equivalencias referenciales.

---

## 🗺️ 2. Estrategia de Normalización Geográfica

### Mapeo Canónico mediante `catalogo_estados`
Las fuentes operacionales suelen permitir captura libre de texto, produciendo variantes como `'Nuevo Leon'`, `'Nuevo León'`, `'N.L.'`, `'NL.'` o `'NL'`.

Para normalizarlas se utilizó una técnica de cruce flexible en MySQL:
```sql
LEFT JOIN catalogo_estados ce 
    ON TRIM(p.estado_envio) = ce.estado_canonico 
    OR TRIM(p.estado_envio) = ce.nombre_oficial
    OR FIND_IN_SET(TRIM(p.estado_envio), REPLACE(ce.alias, ', ', ',')) > 0
```

### Tratamiento de Estados sin Equivalencia o Desconocidos
Cuando un estado ingresa vacío, con caracteres especiales o con valores geográficos inexistentes (ej. `'DESCONOCIDO'`, `'NARNIA'` o `''`):
1. **En la Dimensión Cliente (`stg_clientes`):** No se descarta al cliente; se le asigna la clave canónica `'NE'` (*No Especificado*). Esto asegura que no se pierda la trazabilidad del cliente si posteriormente realiza compras.
2. **En las Transacciones de Pedidos (`stg_pedidos`):** Se mantiene `estado_envio_canonico` como `NULL`. En la fase de validación (Paso 4), esta condición activa la regla de rechazo `ESTADO_NO_RECONOCIDO`, debido a que un e-commerce no puede despachar físicamente una orden hacia un destino geográfico indefinido.

---

## 📅 3. Conversión de Formatos Heterogéneos de Fecha

Se identificaron dos patrones temporales predominantes en el archivo de origen:
- **Formato ISO 8601:** `YYYY-MM-DD` (ej. `2026-03-01`).
- **Formato Tradicional/Latino:** `DD/MM/AAAA` (ej. `14/02/2026`).

Se implementó una expresión regular condicional con `CASE` y `STR_TO_DATE`:
```sql
CASE 
    WHEN TRIM(fecha_raw) REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 
        THEN STR_TO_DATE(TRIM(fecha_raw), '%Y-%m-%d')
    WHEN TRIM(fecha_raw) REGEXP '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$' 
        THEN STR_TO_DATE(TRIM(fecha_raw), '%d/%m/%Y')
    ELSE NULL
END
```
Cualquier fecha que no cumpla con estos patrones (`''`, `'FECHA_ROTA'`) se convierte de manera segura a `NULL`, permitiendo que el validador del Paso 4 clasifique el registro como `FECHA_INVALIDA` sin provocar la interrupción del script.
