# 06 - Stored Procedures y Funciones

## 🎯 Objetivo General
Implementar rutinas almacenadas en base de datos (procedimientos y funciones en PL/pgSQL) para automatizar cálculos complejos, transformaciones analíticas o procesos periódicos en el Data Mart.

## 📌 Función Específica
- Encapsular lógica de negocio recurrente (p. ej., cálculo mensual de comisiones para asesores, actualización de agregaciones, validaciones de integridad).
- Mejorar el rendimiento al reducir el tráfico de red entre la aplicación cliente y el motor de base de datos.
- Proveer interfaces limpias para ejecución parametrizada por analistas de inteligencia de negocios.

## 📦 Estructura Sugerida
- `01_sp_calculo_comisiones.sql`: Procedimiento para procesar comisiones por periodo o showroom.
- `02_sp_resumen_mensual_ventas.sql`: Procedimiento o vista materializada para poblar tablas resumen.
- `documentacion_procedimientos.md`: Descripción técnica de parámetros de entrada, salida y lógica interna.
