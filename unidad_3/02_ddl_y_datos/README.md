# 02 - DDL y Datos

## 🎯 Objetivo General
Centralizar la definición de datos (DDL) y los scripts de inserción o generación de datos de prueba (DML / Seeds) requeridos para alimentar el Data Mart de **Casa&Estilo** en PostgreSQL 16.

---

## 📌 Función Específica de los Módulos

### 1. `01_ddl_schema.sql` (Definición de Datos Idempotente)
- **Función General:** Crea la estructura física del esquema estrella (`Dim_Tiempo`, `Dim_Cliente`, `Dim_Producto`, `Dim_Showroom`, `Dim_Asesor`, `Dim_Canal` y `Fact_Ventas`).
- **Funciones Específicas:**
  - Garantiza compatibilidad e idempotencia mediante cláusulas `CREATE TABLE IF NOT EXISTS`.
  - Establece claves primarias subrogadas (`_sk`), claves de negocio (`_bk`) e integridad referencial foránea.
  - Genera índices B-Tree (`CREATE INDEX IF NOT EXISTS`) sobre llaves foráneas de la tabla de hechos para acelerar operaciones de agregación y uniones dimensionales.

### 2. `02_carga_datos.sql` (Población de Datos Simulados)
- **Función General:** Carga registros sintéticos representativos diseñados para pruebas analíticas (OLAP), validación de planes de ejecución (`EXPLAIN`) y procedimientos almacenados.
- **Funciones Específicas:**
  - **Reinicio Limpio:** Ejecuta `TRUNCATE ... RESTART IDENTITY CASCADE` para evitar duplicidad o desbordamiento de identificadores.
  - **Dimensión Tiempo:** Genera 1,096 días (2025-2027) con atributos en español y trimestres analíticos.
  - **Catálogo y Geografía:** Modela 8 showrooms en México, 8 asesores con comisiones, 25 clientes multiclase y 20 variantes de productos en 6 categorías de muebles y decoración.
  - **Prorrateo Matemático Exacto:** Distribuye los descuentos globales y costos de envío a nivel línea de orden en base al peso monetario del renglón sobre el subtotal total de la orden.
  - **Métricas de Cumplimiento Logístico:** Calcula días transcurridos para entrega y desvíos respecto a la fecha prometida (`retraso_dias`), reflejando escenarios reales de productos en stock vs sobre pedido.

---

## 📦 Archivos Implementados

| Archivo | Tipo | Descripción |
|---|---|---|
| [`01_ddl_schema.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/01_ddl_schema.sql) | SQL (DDL) | Creación idempotente de tablas dimensionales, tabla de hechos e índices. |
| [`02_carga_datos.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/02_carga_datos.sql) | SQL (DML) | Inserción determinista de dimensiones y hechos con fórmulas de prorrateo. |

---

## 🐳 Ejecución en Docker

Siguiendo la política de reproducibilidad e independencia del sistema anfitrión:

```bash
# Iniciar contenedor temporal de PostgreSQL 16
docker run --name pg-casa-estilo -e POSTGRES_PASSWORD=password -e POSTGRES_DB=casa_estilo_bi -p 5432:5432 -d postgres:16-alpine

# Ejecutar DDL e inserción de datos en orden
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/01_ddl_schema.sql"
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_3/02_ddl_y_datos/02_carga_datos.sql"

# Comprobar estado de la base de datos
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi -c "SELECT COUNT(*) FROM Fact_Ventas;"
```

---

## 🔄 Integración con CI/CD

Estos scripts son validados automáticamente en el flujo de GitHub Actions ([`.github/workflows/ci.yml`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/.github/workflows/ci.yml)) en cada push y pull request hacia la rama `main`, garantizando que la estructura y los datos se carguen sin errores de sintaxis o violaciones de integridad referencial.
