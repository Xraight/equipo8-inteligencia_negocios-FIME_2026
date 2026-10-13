# 02 - DDL y Datos

## 🎯 Objetivo General
Centralizar la definición de datos (DDL) y los scripts de inserción o generación de datos de prueba (DML / Seeds) requeridos para alimentar el Data Mart en PostgreSQL.

## 📌 Función Específica
- Alojar scripts de creación de esquemas, tablas, índices, llaves foráneas y restricciones.
- Proveer scripts SQL de población de datos sintéticos o reales para validar el grano de la tabla de hechos y permitir pruebas analíticas.
- Asegurar la reproducibilidad del entorno de base de datos en contenedores Docker o instancias locales de PostgreSQL.

## 📦 Estructura Esperada de Archivos
- `01_ddl_schema.sql`: Creación de dimensiones y tablas de hechos.
- `02_carga_datos.sql`: Inserción de registros en dimensiones y tabla de hechos.
