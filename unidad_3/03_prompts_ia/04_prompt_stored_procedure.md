# ⚙️ Prompt y Automatización: Reto 4 (Stored Procedure Parametrizado)

## 🏢 Empresa: Casa&Estilo
### 👥 Equipo 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
### 🎯 Propósito: Parametrizar la lógica analítica en un Stored Procedure / Función reutilizable.

---

## 📝 1. Prompt Enviado a la Inteligencia Artificial

```text
Actúa como desarrollador de bases de datos relacionales en PostgreSQL (PL/pgSQL) y MySQL 8.
Necesitamos encapsular la lógica analítica validada del reporte de rentabilidad regional (Top 5 por región) en un Procedimiento Almacenado o Función parametrizada.

Requisitos específicos:
1. Parámetros de entrada:
   - p_anio INT (ej. 2026)
   - p_trimestre INT (ej. 2 para el segundo trimestre)
2. Lógica de cálculo dinámico del periodo anterior:
   - Si el usuario solicita p_trimestre = 2, el periodo anterior automático debe ser trimestre 1 del mismo año.
   - Si el usuario solicita p_trimestre = 1, el periodo anterior automático debe ser trimestre 4 del año (p_anio - 1).
3. Manejo de Casos Límite:
   - Si en el periodo anterior no existen registros para un producto, la rentabilidad anterior debe mostrarse como 0.00, la variación absoluta debe ser igual a la rentabilidad actual, la variación porcentual debe ser NULL (evitando división por cero) y el indicador de periodo anterior debe retornar 'Nuevo en periodo (Sin histórico)'.
4. Formato de salida:
   - En PostgreSQL: Implementar como FUNCTION ... RETURNS TABLE (...) para permitir invocaciones idiomáticas (SELECT * FROM sp_reporte_rentabilidad_top5(2026, 2)) o como PROCEDURE que sea compatible con herramientas de visualización y reporting.
   - Proveer además la sintaxis equivalente para MySQL 8 (CREATE PROCEDURE con DELIMITER //).
5. Documentar el comando exacto para llamarlo y ejemplos de salida.
```

---

## 💡 2. Respuesta y Código Propuesto por la IA

La IA generó la estructura en **PL/pgSQL**:
- Determinación dinámica de `v_anio_ant` y `v_trimestre_ant` con un bloque condicional `IF ... ELSE`.
- Estructura modular con CTEs internas unidas por `LEFT JOIN`.
- Clasificación de posiciones con `DENSE_RANK() OVER (PARTITION BY region ORDER BY rentabilidad DESC)`.
- Filtro `posicion <= 5`.

---

## 🔍 3. Revisión del Equipo y Pruebas Realizadas

El equipo verificó la implementación en la base de datos de Docker ejecutando dos escenarios de prueba clave:
1. **Llamada Regular ($Q_2$ 2026 vs $Q_1$ 2026):**
   ```sql
   SELECT * FROM sp_reporte_rentabilidad_top5(2026, 2);
   ```
   *Resultado:* Retornó exitosamente las 25 filas (5 regiones $\times$ 5 productos) con variaciones absolutas y porcentuales coherentes.
2. **Llamada de Caso Límite ($Q_1$ 2026 vs $Q_4$ 2025):**
   ```sql
   SELECT * FROM sp_reporte_rentabilidad_top5(2026, 1);
   ```
   *Resultado:* Dado que en 2025 no existen órdenes en la base de datos, todos los productos fueron clasificados automáticamente como `'Nuevo en periodo (Sin histórico)'`, sin errores de ejecución ni divisiones por cero.

El script definitivo se encuentra en [`unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/01_sp_reporte_rentabilidad_top5.sql).
