# 📘 Documentación Técnica de Datos Simulados para `script dll.sql`

## 👥 Equipo 8
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239

---

## 🎯 1. Función General

El script [`script_datos_simulados.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/script_datos_simulados.sql) tiene como **función general** poblar de manera integral, determinista y consistente el Data Mart de Ventas de **Casa&Estilo**, cuyo modelo físico relacional fue establecido en [`script dll.sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/script%20dll.sql).

Su objetivo es suministrar un conjunto de datos analíticos realistas que permita ejecutar consultas OLAP, validar KPIs estratégicos, auditar planes de ejecución (`EXPLAIN ANALYZE`), evaluar cuellos de botella de indexación y probar procedimientos almacenados bajo las restricciones operacionales y de logística del negocio.

---

## ⚙️ 2. Funciones Específicas del Proceso

### 2.1. Gestión de Idempotencia y Secuencias
- **Función:** Reiniciar el estado de la base de datos sin alterar la estructura DDL mediante `TRUNCATE ... RESTART IDENTITY CASCADE`.
- **Sincronización:** Reajusta los contadores internos de secuencias (`SERIAL`) para las dimensiones con clave subrogada (`_sk`) utilizando `pg_get_serial_sequence()` y `setval()`, previniendo colisiones de llaves primarias en ejecuciones sucesivas.

### 2.2. Generación Analítica de `Dim_Tiempo`
- **Función:** Cubre 3 años continuos (2025-01-01 a 2027-12-31, 1,096 días) a través de `generate_series()`.
- **Atributos Dimensionales:** Genera la clave subrogada en formato entero `YYYYMMDD` (`fecha_sk`), mes, día, año, nombre de mes en español, trimestre (1 a 4) y día de la semana (`Lunes` a `Domingo`), habilitando agregaciones por estacionalidad y análisis temporal.

### 2.3. Modelado de Canales (`Dim_Canal`)
- **Función:** Clasifica los 4 canales comerciales clave de Casa&Estilo:
  1. `Showroom Físico`
  2. `E-commerce Web`
  3. `Venta Telefónica / WhatsApp Concierge`
  4. `Diseño por Proyecto / B2B`

### 2.4. Modelado de Puntos de Venta Físicos (`Dim_Showroom`)
- **Función:** Representa 8 showrooms estratégicos distribuidos por zonas geográficas de México:
  - **Zona Norte:** San Pedro Luxury, Valle Oriente, Cumbres Lifestyle.
  - **Zona Centro:** Polanco Design, Santa Fe Living.
  - **Zona Occidente:** Andares Prestige (Guadalajara).
  - **Zona Sur:** Angelópolis Elite (Puebla).
  - **Zona Bajío:** Juriquilla Modern (Querétaro).

### 2.5. Modelado del Personal Comercial (`Dim_Asesor`)
- **Función:** Estructura a los asesores de venta con sus porcentajes contractuales de comisión (entre 3.50% y 6.00%), base fundamental para el cálculo automatizado de comisiones y rendimiento comercial en Unidad 3.

### 2.6. Segmentación de Clientes (`Dim_Cliente`)
- **Función:** Modela 25 perfiles de compradores representativos que abarcan los 4 segmentos de mercado:
  - `Consumidor final` (clientes residenciales).
  - `Diseñador` (estudios de interiorismo).
  - `Arquitecto` (despachos de arquitectura).
  - `Corporativo` (hoteles boutique, torres corporativas y residenciales).

### 2.7. Desnormalización de Catálogo (`Dim_Producto`)
- **Función:** Consolida la jerarquía de productos y variantes operacionales (20 variantes clave) integrando atributos como:
  - Categorías (`Salas y Sofás`, `Comedores`, `Recámaras`, `Estudio y Oficina`, `Iluminación`, `Decoración y Tapetes`).
  - Colecciones (`Nórdica Elegance`, `Industrial Loft`, `Minimalista Zen`, `Clásica Contemporánea`, `Boho Chic`, `Art Déco Moderna`).
  - Marcas (`Casa&Estilo Signature`, `Nordic Living`, `Urban Wood`, `Luxe Deco`, `Artesan Home`).
  - Color, Material y Tamaño específico.

---

## 🧮 3. Lógica Matemática de Población de `Fact_Ventas`

La población de la tabla de hechos sigue estrictamente las fórmulas del diseño dimensional documentado en la Práctica de Unidad 2:

### 3.1. Grano
$$\text{Una fila} = \text{Un producto o variante específica dentro de una línea de detalle de una orden de venta.}$$

### 3.2. Métricas Aditivas Base
$$\text{monto\_subtotal} = \text{cantidad} \times \text{precio\_unitario}$$
$$\text{monto\_costo\_total} = \text{cantidad} \times \text{costo\_unitario}$$

### 3.3. Fórmulas de Prorrateo a Nivel Línea de Orden
Cuando una orden contiene múltiples renglones, el descuento global y el costo de flete/envío se distribuyen proporcionalmente al valor monetario de cada renglón:

$$\text{Descuento Prorrateado} = \left(\frac{\text{monto\_subtotal de la línea}}{\text{subtotal total de la orden}}\right) \times \text{Descuento Total de la Orden}$$

$$\text{Envío Prorrateado} = \left(\frac{\text{monto\_subtotal de la línea}}{\text{subtotal total de la orden}}\right) \times \text{Envío Total de la Orden}$$

### 3.4. Métricas Derivadas
$$\text{monto\_venta\_neta} = \text{monto\_subtotal} - \text{monto\_descuento\_prorrateado}$$
$$\text{ganancia\_bruta} = \text{monto\_venta\_neta} - \text{monto\_costo\_total}$$

### 3.5. Métricas de Desempeño Logístico
$$\text{dias\_para\_entrega} = \text{fecha\_real\_entrega} - \text{fecha\_orden}$$
$$\text{retraso\_dias} = \text{fecha\_real\_entrega} - \text{fecha\_prometida}$$

*Interpretación de `retraso_dias`:*
- $\le 0$: Entrega realizada a tiempo o anticipada (cumplimiento exitoso).
- $> 0$: Entrega con retraso logístico (incumplimiento).
- `NULL`: Pedido en curso o en tránsito sin fecha de entrega aún reportada.

---

## 🏢 4. Casos de Negocio Modelados en los Datos

1. **Ventas Cruzadas y Canastas Multi-Línea:** Órdenes con múltiples renglones (ej. comedor + sillas + credenza o sala + mesa de centro + alfombra) para validar sumas acumuladas y prorrateos de descuentos promocionales.
2. **Productos en Stock vs. Sobre Pedido:**
   - *Stock:* Tiempos ágiles de entrega (2 a 7 días) y alto índice de puntualidad.
   - *Sobre pedido:* Tiempos de fabricación y logística extendidos (20 a 45 días), incluyendo casos con retrasos reales (3 a 10 días) para probar métricas de cumplimiento de promesa de entrega.
3. **Picos de Demanda y Estacionalidad:** Órdenes distribuidas a lo largo de 2026 con incrementos de volumen en *Buen Fin* (noviembre) y temporada decembrina.
4. **Ventas B2B y Proyectos:** Grandes volúmenes adquiridos por empresas y despachos con descuentos por volumen y asesor asignado.

---

## 🐳 5. Instrucciones de Ejecución con Docker

Para garantizar el cumplimiento de la política de no instalar dependencias en el sistema anfitrión:

```bash
# 1. Iniciar contenedor temporal de PostgreSQL 16
docker run --name pg-casa-estilo \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=casa_estilo_bi \
  -p 5432:5432 \
  -d postgres:16-alpine

# 2. Ejecutar el script DDL de creación de tablas
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script dll.sql"

# 3. Ejecutar el script de carga de datos simulados
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script_datos_simulados.sql"

# 4. Verificar datos interactuando con la base de datos
docker exec -it pg-casa-estilo psql -U postgres -d casa_estilo_bi -c "SELECT COUNT(*) FROM Fact_Ventas;"
```
