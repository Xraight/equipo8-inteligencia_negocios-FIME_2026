# 🔄 Documentación de Carga Incremental e Idempotencia (Paso 5)
**Materia:** Inteligencia de Negocios · FIME 2026 · **Unidad 4: Laboratorio ETL**  
**Documento:** `unidad_4/05_carga_incremental/documentacion_upsert_idempotencia.md`  
**Autor:** Equipo 8

---

## 📌 Concepto Clave: Idempotencia en Pipelines de Datos

En ingeniería de datos, una operación o pipeline es **idempotente** si ejecutarlo repetidas veces con el mismo conjunto de datos de entrada produce exactamente el mismo estado final en el destino, sin generar efectos secundarios no deseados como duplicación de filas o inflación de importes numéricos:

$$f(f(x)) = f(x)$$

Si un proceso ETL falla a la mitad y debe re-ejecutarse, o si se corre de forma programada cada hora sin nuevos datos, la idempotencia asegura que el Data Mart no duplique las ventas.

---

## 🔑 ¿Por qué una Clave Estable Permite Idempotencia?

Para que la instrucción `INSERT ... ON DUPLICATE KEY UPDATE` (UPSERT) opere con éxito, la tabla destino debe poseer una **clave primaria estable y determinista**:

1. **Definición de Clave Estable:** Es un identificador único que permanece constante a través del tiempo para una entidad u ocurrencia transaccional específica (`id_cliente` en la dimensión y `id_pedido` en los hechos).
2. **Mecanismo del Motor Relacional:**
   - Si el motor de base de datos recibe un registro cuyo `id_pedido` no existe en el índice primario de `fact_ordenes`, efectúa una inserción física (`INSERT`).
   - Si el `id_pedido` ya se encuentra presente en el árbol B-Tree del índice primario, el motor intercepta la colisión y conmuta a una actualización controlada en sitio (`UPDATE`).
3. **Contraste con Claves Autoincrementales como PK Única:** Si `fact_ordenes` utilizara únicamente un `id_hecho INT AUTO_INCREMENT` sin restricción única en `id_pedido`, cada re-ejecución del ETL generaría nuevas filas con nuevos identificadores autoincrementales, duplicando la facturación total y corrompiendo los reportes analíticos.

---

## 🧪 Evidencia Experimental de la Prueba

Durante la ejecución de `04_carga_incremental_upsert.sql`:

```text
+------------------------+--------------------------+--------------------------+--------------------+----------------------------+----------------------------+----------------------+
| prueba                 | filas_primera_ejecucion  | filas_segunda_ejecucion  | resultado_volumen  | importe_primera_ejecucion  | importe_segunda_ejecucion  | resultado_financiero |
+------------------------+--------------------------+--------------------------+--------------------+----------------------------+----------------------------+----------------------+
| Prueba de Idempotencia |                       22 |                       22 | IDEMPOTENTE (EXITO)|                   38120.50 |                   38120.50 | INTEGRO (SIN DESVIO) |
+------------------------+--------------------------+--------------------------+--------------------+----------------------------+----------------------------+----------------------+
```

- **Volumen de hechos:** 22 filas exactas en la Corrida 1 y 22 filas en la Corrida 2 ($\Delta = 0$).
- **Monto total de ventas:** \$38,120.50 en ambas corridas ($\Delta = \$0.00$).
