# ⚙️ Documentación Técnica: Stored Procedure y Automatización (Reto 4)

## 🏢 Empresa Asignada: Casa&Estilo
### 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239
- **Materia:** Inteligencia de Negocios - FIME 2026

---

## 🎯 1. Propósito de la Automatización

De acuerdo con el Reto 4 de la Unidad 3:
> *"Conviertan el reporte final en un stored procedure que reciba parámetros de año y trimestre, o fechas de inicio y fin. El procedimiento debe reutilizar la lógica validada y permitir una ejecución de prueba. Documenten el comando utilizado para llamarlo y la salida obtenida, sin duplicar manualmente la consulta fuera del procedimiento."*

---

## 📐 2. Especificación Técnica de la Rutina

### 2.1. Firma de la Función Principal (PostgreSQL 16)
```sql
CREATE OR REPLACE FUNCTION sp_reporte_rentabilidad_top5(
    p_anio INT,
    p_trimestre INT
)
RETURNS TABLE (
    region VARCHAR(100),
    posicion_region BIGINT,
    producto_id_bk INT,
    nombre_producto VARCHAR(150),
    rentabilidad_actual NUMERIC(14,2),
    rentabilidad_anterior NUMERIC(14,2),
    variacion_absoluta NUMERIC(14,2),
    variacion_porcentual NUMERIC(7,2),
    indicador_periodo_anterior VARCHAR(50)
)
```

### 2.2. Parámetros de Entrada
| Parámetro | Tipo | Restricción / Validación | Descripción |
|---|---|---|---|
| `p_anio` | `INT` | Debe ser un año calendario válido (ej. 2026). | Año objeto del análisis. |
| `p_trimestre` | `INT` | `1 <= p_trimestre <= 4`. Lanza excepción si es inválido. | Trimestre que se desea reportar como periodo actual. |

### 2.3. Lógica Algorítmica Interna
1. **Validación de Rango:** Se asegura que el trimestre esté entre 1 y 4 mediante un bloque `IF ... RAISE EXCEPTION`.
2. **Cálculo de Periodo Previo Relativo:**
   - Si `p_trimestre > 1`: `v_anio_ant := p_anio` y `v_trimestre_ant := p_trimestre - 1`.
   - Si `p_trimestre = 1`: Realiza el cruce interanual automático estableciendo `v_anio_ant := p_anio - 1` y `v_trimestre_ant := 4`.
3. **Reutilización de Lógica Validada:** Se ejecutan las etapas de cálculo con descuento de flete (`monto_envio_prorrateado`) y consolidación por producto.
4. **Protección Aritmética:** Si `rentabilidad_anterior` es nula o 0, la variación porcentual devuelve `NULL` para prevenir excepciones de división entre cero en tiempo de ejecución.
5. **Clasificación Automática:** Asigna dinámicamente etiquetas como `'Nuevo en periodo (Sin histórico)'`, `'Crecimiento'`, `'Decrecimiento'` o `'Sin cambio'`.

---

## 💻 3. Comandos de Invocación y Ejecución de Prueba

### Caso 1: Consulta del Periodo Objetivo (Q2 2026 frente a Q1 2026)
```sql
SELECT * FROM sp_reporte_rentabilidad_top5(2026, 2);
```

### Salida Real Obtenida en Consola:
```text
  region   | posicion_region | producto_id_bk |       nombre_producto       | rentabilidad_actual | rentabilidad_anterior | variacion_absoluta | variacion_porcentual | indicador_periodo_anterior 
-----------+-----------------+----------------+-----------------------------+---------------------+-----------------------+--------------------+----------------------+----------------------------
 Bajío     |               1 |            408 | Cama King Size Estocolmo    |           247227.10 |             271605.21 |          -24378.11 |                -8.98 | Decrecimiento
 Bajío     |               2 |            412 | Silla Ergonómica Zurich     |           236064.37 |             236757.05 |            -692.68 |                -0.29 | Decrecimiento
 Bajío     |               3 |            403 | Sillón Ocasional Bergen     |            92194.65 |              96781.19 |           -4586.54 |                -4.74 | Decrecimiento
 Bajío     |               4 |            416 | Espejo de Piso Verona       |            71762.33 |              68434.55 |            3327.78 |                 4.86 | Crecimiento
 Bajío     |               5 |            406 | Silla de Comedor Copenhague |            35792.07 |              34061.30 |            1730.77 |                 5.08 | Crecimiento
 Centro    |               1 |            401 | Sofá Seccional Oslo         |           821165.30 |             875647.83 |          -54482.53 |                -6.22 | Decrecimiento
 Centro    |               2 |            408 | Cama King Size Estocolmo    |           259762.40 |             259632.88 |             129.52 |                 0.05 | Crecimiento
 Centro    |               3 |            412 | Silla Ergonómica Zurich     |           236734.74 |             221736.30 |           14998.44 |                 6.76 | Crecimiento
 Centro    |               4 |            403 | Sillón Ocasional Bergen     |           101403.69 |              92194.65 |            9209.04 |                 9.99 | Crecimiento
 Centro    |               5 |            416 | Espejo de Piso Verona       |            71914.82 |              75313.41 |           -3398.59 |                -4.51 | Decrecimiento
 Norte     |               1 |            401 | Sofá Seccional Oslo         |          1153664.59 |            1112910.82 |           40753.77 |                 3.66 | Crecimiento
 Norte     |               2 |            405 | Mesa de Comedor Kioto       |          1115932.22 |            1068351.01 |           47581.21 |                 4.45 | Crecimiento
 Norte     |               3 |            408 | Cama King Size Estocolmo    |           955971.22 |             896798.00 |           59173.22 |                 6.60 | Crecimiento
 Norte     |               4 |            402 | Sofá Chaiselongue Malmö     |           334334.59 |             318213.40 |           16121.19 |                 5.07 | Crecimiento
 Norte     |               5 |            407 | Credenza Buffet Milán       |           224368.20 |             235703.24 |          -11335.04 |                -4.81 | Decrecimiento
 Occidente |               1 |            405 | Mesa de Comedor Kioto       |           846878.10 |             902541.54 |          -55663.44 |                -6.17 | Decrecimiento
 Occidente |               2 |            401 | Sofá Seccional Oslo         |           291741.94 |             277571.45 |           14170.49 |                 5.11 | Crecimiento
 Occidente |               3 |            407 | Credenza Buffet Milán       |           246776.06 |             224368.20 |           22407.86 |                 9.99 | Crecimiento
 Occidente |               4 |            410 | Cómoda 6 Cajones Viena      |           192269.46 |             182947.70 |            9321.76 |                 5.10 | Crecimiento
 Occidente |               5 |            414 | Lámpara Colgante Vintage    |            35293.23 |              35291.85 |               1.38 |                 0.00 | Crecimiento
 Sur       |               1 |            408 | Cama King Size Estocolmo    |           956828.55 |             956953.83 |            -125.28 |                -0.01 | Decrecimiento
 Sur       |               2 |            402 | Sofá Chaiselongue Malmö     |           349504.02 |             334130.26 |           15373.76 |                 4.60 | Crecimiento
 Sur       |               3 |            405 | Mesa de Comedor Kioto       |           212256.37 |             201853.80 |           10402.57 |                 5.15 | Crecimiento
 Sur       |               4 |            411 | Escritorio Ejecutivo Berlín |           175843.25 |             167336.10 |            8507.15 |                 5.08 | Crecimiento
 Sur       |               5 |            415 | Tapete Geométrico Lyon      |            82495.85 |              90882.34 |           -8386.49 |                -9.23 | Decrecimiento
(25 rows)
```

---

## 🛡️ 4. Verificación de Caso Límite (Edge Case)

Para verificar la robustez del procedimiento cuando se evalúa el primer trimestre registrado en el Data Mart (`Q1 2026`), se ejecutó:
```sql
SELECT * FROM sp_reporte_rentabilidad_top5(2026, 1);
```
* **Comportamiento:** El motor detectó automáticamente que el periodo previo corresponde a `Q4 2025`. Al no haber registros en dicho trimestre, asignó `rentabilidad_anterior = 0.00`, `variacion_absoluta = rentabilidad_actual`, `variacion_porcentual = NULL` e `indicador_periodo_anterior = 'Nuevo en periodo (Sin histórico)'`, evitando cualquier aborto o error de ejecución.
