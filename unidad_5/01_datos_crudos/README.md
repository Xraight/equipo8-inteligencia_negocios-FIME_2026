# 📁 Unidad 5 · 01 Datos Crudos (Data Mart CSV)

Este directorio contiene los cuatro archivos CSV originales e inmutables que componen el Data Mart transaccional y dimensional de la empresa comercial (**Data Mart de Ventas**).

---

## 📑 Inventario de Archivos y Metadatos

| Archivo | Tipo de Tabla | Registros | Clave Primaria / Foránea | Descripción del Grano |
| :--- | :--- | :--- | :--- | :--- |
| [`FACT_VENTAS.csv`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/01_datos_crudos/FACT_VENTAS.csv) | Hechos (Fact) | 1,200 transacciones | `id_venta` (PK)<br>`id_producto`, `id_cliente`, `id_tiempo` (FKs) | Cada fila representa una transacción de venta individual registrada en el sistema. |
| [`DIM_PRODUCTO.csv`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/01_datos_crudos/DIM_PRODUCTO.csv) | Dimensión | 12 productos | `id_producto` (PK) | Catálogo de artículos clasificados en Hogar, Oficina y Tecnología. |
| [`DIM_CLIENTE.csv`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/01_datos_crudos/DIM_CLIENTE.csv) | Dimensión | 80 clientes | `id_cliente` (PK) | Directorio de clientes asociados a una región geográfica (Centro, Sur, Occidente, Norte). |
| [`DIM_TIEMPO.csv`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/01_datos_crudos/DIM_TIEMPO.csv) | Dimensión | 96 períodos | `id_tiempo` (PK) | Calendario de cortes periódicos con granularidad semanal entre 2025 y 2026. |

---

## 🔒 Regla de Inmutabilidad
De acuerdo con la metodología del laboratorio guiado y las buenas prácticas de Ingeniería de Datos:
1. **Los archivos CSV fuente jamás deben editarse manualmente ni sobreescribirse.**
2. Cualquier transformación, limpieza o tipado debe realizarse a través de canalizaciones reproducibles (Power Query M / scripts automatizados).
3. La codificación obligatoria es **UTF-8** con delimitador por coma (`,`).
