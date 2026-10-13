# 🛋️ Unidad 2: Modelado Dimensional y Arquitectura del Data Mart

## 👥 Miembros del Equipo
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239

---

## 🎯 Objetivo General
Diseñar y estructurar la arquitectura dimensional de un Data Mart de Ventas para **"Casa&Estilo"**, empresa de retail especializada en muebles, decoración y artículos para el hogar. El enfoque se centra en consolidar los datos operativos para soportar el análisis histórico de ventas y el cumplimiento logístico de entregas.

---

## 📌 Función Específica de los Entregables
- **Modelado Dimensional (Esquema Estrella):** Definición del grano a nivel línea de orden/variante de producto, tablas de dimensiones normalizadas para análisis (`Dim_Tiempo`, `Dim_Cliente`, `Dim_Producto`, `Dim_Showroom`, `Dim_Asesor`, `Dim_Canal`, `Dim_Metodo_Pago`, `Dim_Estado_Entrega`) y tabla de hechos (`Hechos_Ventas`).
- **Definición de Datos (DDL):** Creación del esquema relacional en PostgreSQL asegurando tipos de datos óptimos, claves subrogadas (surrogate keys `_sk`), claves de negocio (`_bk`) e integridad referencial.
- **Documentación y Reportes Académicos:** Reportes detallados de la práctica y presentación formal de la arquitectura dimensional.

---

## 📂 Archivos de la Unidad 2

| Archivo | Formato | Descripción |
|---|---|---|
| [`Casa_Estilo_Diagrama_ER.drawio`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/Casa_Estilo_Diagrama_ER.drawio) | Diagrama draw.io | Diagrama Entidad-Relación y Esquema Estrella del Data Mart. |
| [`script dll.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/script%20dll.sql) | SQL (PostgreSQL) | Script DDL para creación de tablas dimensionales, hechos y restricciones. |
| [`script_datos_simulados.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/script_datos_simulados.sql) | SQL (PostgreSQL) | Script DML de población de datos simulados con prorrateo matemático exacto. |
| [`documentacion_datos_simulados.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/documentacion_datos_simulados.md) | Documento Markdown | Documentación técnica detallada de la función general y específicas de los datos simulados. |
| [`Equipo8_Practica_Unidad_2.pdf`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/Equipo8_Practica_Unidad_2.pdf) | Documento PDF | Reporte formal del entregable de la Práctica de Unidad 2. |
| [`Retail Equipo 8 Practica Unidad 2.pdf`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/Retail%20Equipo%208%20Practica%20Unidad%202.pdf) | Documento PDF | Presentación y caso de estudio de Retail Casa&Estilo. |

---

## 🐳 Ejecución de DDL y Datos Simulados en Docker

```bash
# Iniciar contenedor temporal de PostgreSQL 16
docker run --name pg-casa-estilo -e POSTGRES_PASSWORD=password -e POSTGRES_DB=casa_estilo_bi -p 5432:5432 -d postgres:16-alpine

# Ejecutar el script DDL
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script dll.sql"

# Poblar el esquema con datos simulados
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script_datos_simulados.sql"
```

---

## 🛠️ Tecnologías y Herramientas
- **Motor de Base de Datos:** PostgreSQL 16 (vía Docker)
- **Modelado Visual:** draw.io
- **Paradigma de Modelado:** Modelado Dimensional (Kimball / Esquema Estrella)

