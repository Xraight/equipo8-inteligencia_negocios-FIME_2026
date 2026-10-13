# 👁️ Guía de Visualización de Tablas y Datos para el Equipo

Esta guía está diseñada para que todos los integrantes del **Equipo 8** (**Arely Carrillo**, **Rafael Collazo**, **Sergio Jaziel Butzmann**) puedan visualizar, explorar e interactuar con las tablas del Data Mart de **Casa&Estilo** de forma sencilla, rápida y **sin instalar motores de base de datos ni dependencias en sus computadoras personales**, utilizando contenedores Docker.

---

## 🌟 Método 1 (Recomendado para Exponer y Trabajar): Casa&Estilo BI Studio

Es una **aplicación web moderna, visual y amigable** diseñada a la medida del Equipo 8 y los requerimientos del PDF de la Unidad 3:

👉 **Abre directamente en tu navegador:** [**http://localhost:8080**](http://localhost:8080)
*(No requiere contraseñas complejas ni configuraciones)*

### 🎯 Lo que incluye Casa&Estilo BI Studio:
1. **🎙️ Modo Exposición (5 Minutos):**
   - Una guía de diapositivas interactivas preparada para la presentación oral descrita en la página 8 del PDF.
   - Explica el caso de estudio, el grano del modelo, las fórmulas de prorrateo, la consulta con CTEs y Window Functions, y la evidencia del error de agrupación (`Error 1055`) con su optimización `EXPLAIN`.
2. **📊 Explorador Visual de Tablas:**
   - Visualiza cualquiera de las 7 tablas del Data Mart (`Dim_Tiempo`, `Dim_Cliente`, `Dim_Producto`, `Dim_Showroom`, `Dim_Asesor`, `Dim_Canal`, `Fact_Ventas`).
   - Formato moderno de hoja de cálculo con búsqueda instantánea, paginación ágil y botón de exportar a CSV.
3. **🏆 Reto Unidad 3: Top 5 Rentabilidad por Región:**
   - Tabla interactiva que compara el **Q2 2026 frente al Q1 2026**.
   - Muestra variaciones absolutas ($ MXN), porcentuales (%) e indicadores de productos nuevos por región con filtro interactivo.
4. **⚡ Playground SQL & EXPLAIN:**
   - Permite seleccionar consultas analíticas precargadas o escribir código SQL en vivo, ejecutándolo contra PostgreSQL 16 y mostrando tiempos de respuesta en milisegundos y el árbol de `EXPLAIN ANALYZE`.
5. **📐 Esquema Estrella Interactivo:**
   - Diagrama visual de la tabla central de hechos y sus 6 dimensiones conectadas con sus diccionarios de datos.

---

## 🛠️ Método 2: Administración Tradicional con pgAdmin 4 (Web)

Si algún integrante desea la consola tradicional de base de datos para inspección profunda de índices o secuencias:

👉 **[http://localhost:5050](http://localhost:5050)**
- **Email:** `equipo8@fime.uanl.mx`
- **Contraseña:** `password`
- **Contraseña de BD:** `password` (servidor *Casa&Estilo Data Mart* ya registrado)

### Paso 4: Visualizar las tablas y datos
1. En el panel izquierdo, despliega **Servers** ➔ **Equipo 8 - BI** ➔ **Casa&Estilo Data Mart (PostgreSQL)**.
2. Cuando te solicite la contraseña de la base de datos, ingresa: `password`.
3. Navega a:
   `Databases` ➔ `casa_estilo_bi` ➔ `Schemas` ➔ `public` ➔ `Tables`.
4. Verás las 7 tablas:
   - `dim_tiempo`
   - `dim_cliente`
   - `dim_producto`
   - `dim_showroom`
   - `dim_asesor`
   - `dim_canal`
   - `fact_ventas`
5. **Para ver las filas:** Haz clic derecho sobre cualquier tabla ➔ **View/Edit Data** ➔ **All Rows**. Podrás ver los datos en formato hoja de cálculo, ordenar columnas y aplicar filtros.
6. **Para escribir SQL analítico:** Haz clic en el ícono de rayo o selecciona **Tools** ➔ **Query Tool**.

### Paso 5: Detener el entorno cuando termines
```bash
docker compose down
```

---

## 💻 Método 2: Conexión con Clientes GUI de Escritorio (DBeaver, DataGrip, VS Code)

Si algún integrante ya cuenta con una herramienta visual instalada en su computadora (como **DBeaver Community**, **DataGrip** o la extensión **SQLTools** en VS Code):

1. Asegúrate de tener encendido el contenedor de PostgreSQL con:
   ```bash
   docker compose up -d postgres
   ```
2. Crea una nueva conexión de tipo **PostgreSQL** con estos parámetros:
   - **Host:** `localhost`
   - **Puerto:** `5432`
   - **Base de datos:** `casa_estilo_bi`
   - **Usuario:** `postgres`
   - **Contraseña:** `password`
3. En **DBeaver**, haz doble clic en el esquema `public` y selecciona la pestaña **ER Diagram** para ver automáticamente el esquema estrella visual generado en tiempo real.

---

## 📄 Método 3: Consulta Directa en Markdown (Sin encender Docker)

Para consultar rápidamente los campos, tipos y registros de muestra desde GitHub o el editor:

### 1. `Dim_Tiempo` (1,096 registros, 2025-2027)
| fecha_sk | fecha_completa | anio | mes | dia | nombre_mes | trimestre | dia_semana |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 20260108 | 2026-01-08 | 2026 | 1 | 8 | Enero | 1 | Jueves |
| 20260315 | 2026-03-15 | 2026 | 3 | 15 | Marzo | 1 | Domingo |
| 20260520 | 2026-05-20 | 2026 | 5 | 20 | Mayo | 2 | Miércoles |

### 2. `Dim_Showroom` (Puntos de venta físicos)
| showroom_sk | showroom_id_bk | nombre_showroom | ciudad | zona |
|:---:|:---:|:---|:---|:---:|
| 1 | 101 | Showroom San Pedro Luxury | San Pedro Garza García | Norte |
| 2 | 102 | Showroom Valle Oriente | Monterrey | Norte |
| 3 | 103 | Showroom Cumbres Lifestyle | Monterrey | Norte |
| 4 | 104 | Showroom Polanco Design | Ciudad de México | Centro |
| 5 | 105 | Showroom Santa Fe Living | Ciudad de México | Centro |
| 6 | 106 | Showroom Andares Prestige | Guadalajara | Occidente |
| 7 | 107 | Showroom Angelópolis Elite | Puebla | Sur |
| 8 | 108 | Showroom Juriquilla Modern | Querétaro | Bajío |

### 3. `Dim_Canal`
| canal_sk | nombre_canal |
|:---:|:---|
| 1 | Showroom Físico |
| 2 | E-commerce Web |
| 3 | Venta Telefónica / WhatsApp Concierge |
| 4 | Diseño por Proyecto / B2B |

### 4. `Dim_Asesor` (Comisiones del personal)
| asesor_sk | asesor_id_bk | nombre_asesor | porcentaje_comision |
|:---:|:---:|:---|:---:|
| 1 | 201 | Valeria Ríos González | 5.00% |
| 2 | 202 | Carlos Montemayor Benavides | 4.50% |
| 3 | 203 | Mariana Treviño Lozano | 5.50% |
| 4 | 204 | Rodrigo Garza Sada | 4.00% |
| 5 | 205 | Sofía Villarreal Cantú | 6.00% |

### 5. `Dim_Cliente` (Muestra de perfiles)
| cliente_sk | cliente_id_bk | nombre | tipo_cliente | ciudad | zona |
|:---:|:---:|:---|:---|:---|:---:|
| 1 | 301 | Alejandro Morales Gómez | Consumidor final | San Pedro Garza García | Norte |
| 2 | 302 | Studio Arq & Deco S.A. | Arquitecto | San Pedro Garza García | Norte |
| 4 | 304 | Interiores Sofía Domínguez | Diseñador | Monterrey | Norte |
| 6 | 306 | Hotel Boutique Valle Real | Corporativo | San Pedro Garza García | Norte |

### 6. `Dim_Producto` (Muestra del catálogo desnormalizado)
| producto_sk | variante_id_bk | producto_id_bk | nombre_producto | categoria | coleccion | tamano |
|:---:|:---:|:---:|:---|:---|:---|:---|
| 1 | 501 | 401 | Sofá Seccional Oslo | Salas y Sofás | Nórdica Elegance | 3 Cuerpos |
| 6 | 506 | 405 | Mesa de Comedor Kioto | Comedores | Minimalista Zen | 8 Sillas |
| 11 | 511 | 408 | Cama King Size Estocolmo | Recámaras | Nórdica Elegance | King Size |
| 15 | 515 | 411 | Escritorio Ejecutivo Berlín | Estudio y Oficina | Industrial Loft | Grande |

### 7. `Fact_Ventas` (Muestra de métricas prorrateadas y logísticas)
| fact_venta_id | orden_id | producto_sk | cantidad | monto_subtotal | monto_descuento_prorrateado | monto_venta_neta | ganancia_bruta | dias_para_entrega | retraso_dias |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | ORD-2025-001 | 1 | 1 | $28,500.00 | $1,328.67 | $27,171.33 | $12,921.33 | 4 | -1 (Anticipado) |
| 2 | ORD-2025-001 | 5 | 1 | $6,500.00 | $303.03 | $6,196.97 | $3,296.97 | 4 | -1 (Anticipado) |
| 4 | ORD-2025-002 | 6 | 1 | $29,800.00 | $784.21 | $29,015.79 | $13,515.79 | 28 | +5 (Demora) |

---

## ⌨️ Método 4: Consultas Rápidas desde la Terminal con Docker

Para quienes prefieran verificar rápidamente datos sin salir de la consola:

```bash
# Ver lista de tablas
docker exec -it casa_estilo_postgres psql -U postgres -d casa_estilo_bi -c "\dt"

# Ver resumen de registros por tabla
docker exec -it casa_estilo_postgres psql -U postgres -d casa_estilo_bi -c "
SELECT 'Dim_Tiempo' AS tabla, COUNT(*) FROM Dim_Tiempo
UNION ALL SELECT 'Dim_Cliente', COUNT(*) FROM Dim_Cliente
UNION ALL SELECT 'Dim_Producto', COUNT(*) FROM Dim_Producto
UNION ALL SELECT 'Fact_Ventas', COUNT(*) FROM Fact_Ventas;
"

# Consultar las 5 primeras líneas de venta
docker exec -it casa_estilo_postgres psql -U postgres -d casa_estilo_bi -c "
SELECT orden_id, producto_sk, cantidad, monto_subtotal, monto_venta_neta, ganancia_bruta, retraso_dias 
FROM Fact_Ventas 
LIMIT 5;
"
```
