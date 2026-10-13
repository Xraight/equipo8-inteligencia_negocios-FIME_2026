-- ==============================================================================
-- PROYECTO: DATA MART DE VENTAS - CASA&ESTILO
-- OBJETIVO: Población de Datos Simulados (>1,000 filas requeridas por la rúbrica)
-- EQUIPO 8: Arely Carrillo, Rafael Collazo, Sergio Jaziel Butzmann
-- FECHA: Septiembre / Octubre 2026
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 0. LIMPIEZA PREVIA (IDEMPOTENCIA PARA PRUEBAS REPETIBLES)
-- ------------------------------------------------------------------------------
TRUNCATE TABLE Fact_Ventas, Dim_Cliente, Dim_Producto, Dim_Showroom, Dim_Asesor, Dim_Canal, Dim_Tiempo RESTART IDENTITY CASCADE;

-- ------------------------------------------------------------------------------
-- 1. POBLACIÓN DE DIM_TIEMPO (AÑOS 2025 A 2027 - 1,096 DÍAS)
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Tiempo (fecha_sk, fecha_completa, anio, mes, dia, nombre_mes, trimestre, dia_semana)
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT AS fecha_sk,
    d::DATE AS fecha_completa,
    EXTRACT(YEAR FROM d)::INT AS anio,
    EXTRACT(MONTH FROM d)::INT AS mes,
    EXTRACT(DAY FROM d)::INT AS dia,
    CASE EXTRACT(MONTH FROM d)::INT
        WHEN 1 THEN 'Enero'
        WHEN 2 THEN 'Febrero'
        WHEN 3 THEN 'Marzo'
        WHEN 4 THEN 'Abril'
        WHEN 5 THEN 'Mayo'
        WHEN 6 THEN 'Junio'
        WHEN 7 THEN 'Julio'
        WHEN 8 THEN 'Agosto'
        WHEN 9 THEN 'Septiembre'
        WHEN 10 THEN 'Octubre'
        WHEN 11 THEN 'Noviembre'
        WHEN 12 THEN 'Diciembre'
    END AS nombre_mes,
    EXTRACT(QUARTER FROM d)::INT AS trimestre,
    CASE EXTRACT(ISODOW FROM d)::INT
        WHEN 1 THEN 'Lunes'
        WHEN 2 THEN 'Martes'
        WHEN 3 THEN 'Miércoles'
        WHEN 4 THEN 'Jueves'
        WHEN 5 THEN 'Viernes'
        WHEN 6 THEN 'Sábado'
        WHEN 7 THEN 'Domingo'
    END AS dia_semana
FROM generate_series('2025-01-01'::DATE, '2027-12-31'::DATE, '1 day'::INTERVAL) AS d
ON CONFLICT (fecha_sk) DO NOTHING;

-- ------------------------------------------------------------------------------
-- 2. POBLACIÓN DE DIM_CANAL
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Canal (canal_sk, nombre_canal) VALUES
(1, 'Showroom Físico'),
(2, 'E-commerce Web'),
(3, 'Venta Telefónica / WhatsApp Concierge'),
(4, 'Diseño por Proyecto / B2B');

-- ------------------------------------------------------------------------------
-- 3. POBLACIÓN DE DIM_SHOWROOM
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Showroom (showroom_sk, showroom_id_bk, nombre_showroom, ciudad, zona) VALUES
(1, 101, 'Showroom San Pedro Luxury', 'San Pedro Garza García', 'Norte'),
(2, 102, 'Showroom Valle Oriente', 'Monterrey', 'Norte'),
(3, 103, 'Showroom Cumbres Lifestyle', 'Monterrey', 'Norte'),
(4, 104, 'Showroom Polanco Design', 'Ciudad de México', 'Centro'),
(5, 105, 'Showroom Santa Fe Living', 'Ciudad de México', 'Centro'),
(6, 106, 'Showroom Andares Prestige', 'Guadalajara', 'Occidente'),
(7, 107, 'Showroom Angelópolis Elite', 'Puebla', 'Sur'),
(8, 108, 'Showroom Juriquilla Modern', 'Querétaro', 'Bajío');

-- ------------------------------------------------------------------------------
-- 4. POBLACIÓN DE DIM_ASESOR
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Asesor (asesor_sk, asesor_id_bk, nombre_asesor, porcentaje_comision) VALUES
(1, 201, 'Valeria Ríos González', 5.00),
(2, 202, 'Carlos Montemayor Benavides', 4.50),
(3, 203, 'Mariana Treviño Lozano', 5.50),
(4, 204, 'Rodrigo Garza Sada', 4.00),
(5, 205, 'Sofía Villarreal Cantú', 6.00),
(6, 206, 'Andrés Hinojosa Martínez', 3.50),
(7, 207, 'Daniela Morales Peña', 5.00),
(8, 208, 'Mauricio Elizondo Leal', 4.00);

-- ------------------------------------------------------------------------------
-- 5. POBLACIÓN DE DIM_CLIENTE
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Cliente (cliente_sk, cliente_id_bk, nombre, tipo_cliente, ciudad, zona) VALUES
(1, 301, 'Alejandro Morales Gómez', 'Consumidor final', 'San Pedro Garza García', 'Norte'),
(2, 302, 'Studio Arq & Deco S.A. de C.V.', 'Arquitecto', 'San Pedro Garza García', 'Norte'),
(3, 303, 'Claudia Marcela Garza', 'Consumidor final', 'Monterrey', 'Norte'),
(4, 304, 'Interiores Sofía Domínguez', 'Diseñador', 'Monterrey', 'Norte'),
(5, 305, 'Roberto Cantú Treviño', 'Consumidor final', 'Monterrey', 'Norte'),
(6, 306, 'Hotel Boutique Valle Real', 'Corporativo', 'San Pedro Garza García', 'Norte'),
(7, 307, 'Ana Patricia Ramos', 'Consumidor final', 'Ciudad de México', 'Centro'),
(8, 308, 'Despacho Legorreta & Asociados', 'Arquitecto', 'Ciudad de México', 'Centro'),
(9, 309, 'Fernando Zepeda Castro', 'Consumidor final', 'Ciudad de México', 'Centro'),
(10, 310, 'Luxe Interior Design CDMX', 'Diseñador', 'Ciudad de México', 'Centro'),
(11, 311, 'Corporativo Santa Fe Tower', 'Corporativo', 'Ciudad de México', 'Centro'),
(12, 312, 'María Fernanda Alatorre', 'Consumidor final', 'Guadalajara', 'Occidente'),
(13, 313, 'Héctor Covarrubias Silva', 'Consumidor final', 'Guadalajara', 'Occidente'),
(14, 314, 'Taller de Diseño Andares', 'Diseñador', 'Guadalajara', 'Occidente'),
(15, 315, 'Gabriela Fuentes Madero', 'Consumidor final', 'Puebla', 'Sur'),
(16, 316, 'Residencial Angelópolis Club', 'Corporativo', 'Puebla', 'Sur'),
(17, 317, 'Eduardo Palacios Junco', 'Consumidor final', 'Querétaro', 'Bajío'),
(18, 318, 'Arq. Guillermo Sada', 'Arquitecto', 'Querétaro', 'Bajío'),
(19, 319, 'Lucía Cárdenas Beltrán', 'Consumidor final', 'Monterrey', 'Norte'),
(20, 320, 'Espacios Corporativos Norte', 'Corporativo', 'San Pedro Garza García', 'Norte'),
(21, 321, 'Javier Lozano Elizondo', 'Consumidor final', 'San Pedro Garza García', 'Norte'),
(22, 322, 'Mariana de la Garza', 'Consumidor final', 'Ciudad de México', 'Centro'),
(23, 323, 'Diego Armando Santos', 'Consumidor final', 'Guadalajara', 'Occidente'),
(24, 324, 'Inmobiliaria Península & Hogar', 'Corporativo', 'Puebla', 'Sur'),
(25, 325, 'Beatriz Adriana Salgado', 'Consumidor final', 'Querétaro', 'Bajío');

-- ------------------------------------------------------------------------------
-- 6. POBLACIÓN DE DIM_PRODUCTO
-- ------------------------------------------------------------------------------
INSERT INTO Dim_Producto (producto_sk, variante_id_bk, producto_id_bk, nombre_producto, categoria, coleccion, marca, color, material, tamano) VALUES
(1, 501, 401, 'Sofá Seccional Oslo', 'Salas y Sofás', 'Nórdica Elegance', 'Casa&Estilo Signature', 'Gris Oxford', 'Lino Premium', '3 Cuerpos'),
(2, 502, 401, 'Sofá Seccional Oslo', 'Salas y Sofás', 'Nórdica Elegance', 'Casa&Estilo Signature', 'Beige Arena', 'Lino Premium', '3 Cuerpos'),
(3, 503, 402, 'Sofá Chaiselongue Malmö', 'Salas y Sofás', 'Nórdica Elegance', 'Nordic Living', 'Azul Marino', 'Terciopelo', '3 Cuerpos'),
(4, 504, 403, 'Sillón Ocasional Bergen', 'Salas y Sofás', 'Nórdica Elegance', 'Nordic Living', 'Caramelo', 'Cuero Sintético', 'Individual'),
(5, 505, 404, 'Mesa de Centro Manhattan', 'Salas y Sofás', 'Industrial Loft', 'Urban Wood', 'Negro Mate', 'Metal y Vidrio', 'Mediano'),
(6, 506, 405, 'Mesa de Comedor Kioto', 'Comedores', 'Minimalista Zen', 'Urban Wood', 'Nogal Natural', 'Madera de Roble', '8 Sillas'),
(7, 507, 405, 'Mesa de Comedor Kioto', 'Comedores', 'Minimalista Zen', 'Urban Wood', 'Roble Claro', 'Madera de Roble', '6 Sillas'),
(8, 508, 406, 'Silla de Comedor Copenhague', 'Comedores', 'Nórdica Elegance', 'Nordic Living', 'Gris Claro', 'Lino y Roble', 'Estándar'),
(9, 509, 406, 'Silla de Comedor Copenhague', 'Comedores', 'Nórdica Elegance', 'Nordic Living', 'Mostaza', 'Terciopelo y Roble', 'Estándar'),
(10, 510, 407, 'Credenza Buffet Milán', 'Comedores', 'Clásica Contemporánea', 'Luxe Deco', 'Nogal y Mármol', 'Madera y Mármol', 'Grande'),
(11, 511, 408, 'Cama King Size Estocolmo', 'Recámaras', 'Nórdica Elegance', 'Casa&Estilo Signature', 'Gris Perla', 'Madera y Tapiz', 'King Size'),
(12, 512, 408, 'Cama King Size Estocolmo', 'Recámaras', 'Nórdica Elegance', 'Casa&Estilo Signature', 'Arena', 'Madera y Tapiz', 'Queen Size'),
(13, 513, 409, 'Buró de Noche Nórdico', 'Recámaras', 'Nórdica Elegance', 'Nordic Living', 'Nogal Natural', 'Madera de Roble', 'Mediano'),
(14, 514, 410, 'Cómoda 6 Cajones Viena', 'Recámaras', 'Clásica Contemporánea', 'Luxe Deco', 'Blanco Puro', 'Madera Laqueada', 'Grande'),
(15, 515, 411, 'Escritorio Ejecutivo Berlín', 'Estudio y Oficina', 'Industrial Loft', 'Urban Wood', 'Nogal y Negro', 'Madera y Acero', 'Grande'),
(16, 516, 412, 'Silla Ergonómica Zurich', 'Estudio y Oficina', 'Industrial Loft', 'Urban Wood', 'Negro', 'Cuero Sintético', 'Ajustable'),
(17, 517, 413, 'Lámpara de Pie Ámsterdam', 'Iluminación', 'Art Déco Moderna', 'Luxe Deco', 'Dorado Latón', 'Metal y Vidrio', 'Alto'),
(18, 518, 414, 'Lámpara Colgante Vintage', 'Iluminación', 'Industrial Loft', 'Urban Wood', 'Cobre Mate', 'Metal', 'Mediano'),
(19, 519, 415, 'Tapete Geométrico Lyon', 'Decoración y Tapetes', 'Boho Chic', 'Artesan Home', 'Gris y Crema', 'Lana y Algodón', '2.5 x 3.0 m'),
(20, 520, 416, 'Espejo de Piso Verona', 'Decoración y Tapetes', 'Clásica Contemporánea', 'Luxe Deco', 'Negro Mate', 'Hierro y Cristal', '180 x 80 cm');

-- Sincronizar secuencias
SELECT setval(pg_get_serial_sequence('Dim_Canal', 'canal_sk'), COALESCE(MAX(canal_sk), 1)) FROM Dim_Canal;
SELECT setval(pg_get_serial_sequence('Dim_Showroom', 'showroom_sk'), COALESCE(MAX(showroom_sk), 1)) FROM Dim_Showroom;
SELECT setval(pg_get_serial_sequence('Dim_Asesor', 'asesor_sk'), COALESCE(MAX(asesor_sk), 1)) FROM Dim_Asesor;
SELECT setval(pg_get_serial_sequence('Dim_Cliente', 'cliente_sk'), COALESCE(MAX(cliente_sk), 1)) FROM Dim_Cliente;
SELECT setval(pg_get_serial_sequence('Dim_Producto', 'producto_sk'), COALESCE(MAX(producto_sk), 1)) FROM Dim_Producto;

-- ------------------------------------------------------------------------------
-- 7. POBLACIÓN DE FACT_VENTAS (1,250 REGISTROS CON FÓRMULAS DE PRORRATEO)
-- ------------------------------------------------------------------------------
INSERT INTO Fact_Ventas (
    fecha_orden_sk, fecha_prometida_sk, fecha_real_entrega_sk,
    cliente_sk, producto_sk, showroom_sk, asesor_sk, canal_sk,
    orden_id, tipo_surtido,
    cantidad, precio_unitario, costo_unitario,
    monto_subtotal, monto_costo_total,
    monto_descuento_prorrateado, monto_envio_prorrateado,
    monto_venta_neta, ganancia_bruta,
    dias_para_entrega, retraso_dias
)
WITH generador_lineas AS (
    SELECT
        s AS id,
        'ORD-2026-' || LPAD(((s / 3) + 1)::TEXT, 4, '0') AS orden_id,
        (DATE '2026-01-02' + ((s * 179) / 1250)::INT) AS fecha_orden_date,
        ((s * 7) % 25) + 1 AS cliente_sk,
        ((s * 11) % 20) + 1 AS producto_sk,
        ((s * 3) % 8) + 1 AS showroom_sk,
        ((s * 5) % 8) + 1 AS asesor_sk,
        ((s * 2) % 4) + 1 AS canal_sk,
        CASE WHEN (s % 10) < 7 THEN 'Stock' ELSE 'Sobre pedido' END AS tipo_surtido,
        CASE WHEN (s % 5) = 0 THEN 4 WHEN (s % 3) = 0 THEN 2 ELSE 1 END AS cantidad
    FROM generate_series(1, 1250) AS s
),
staging_lineas AS (
    SELECT
        g.orden_id,
        TO_CHAR(g.fecha_orden_date, 'YYYYMMDD')::INT AS fecha_orden_sk,
        TO_CHAR(
            CASE 
                WHEN g.tipo_surtido = 'Stock' THEN g.fecha_orden_date + (5 + (g.id % 4))
                ELSE g.fecha_orden_date + (25 + (g.id % 11))
            END, 'YYYYMMDD')::INT AS fecha_prometida_sk,
        TO_CHAR(
            CASE
                WHEN g.id % 45 = 0 THEN NULL
                WHEN g.tipo_surtido = 'Stock' THEN g.fecha_orden_date + (3 + (g.id % 4))
                WHEN (g.id % 4) = 0 THEN g.fecha_orden_date + (28 + (g.id % 12) + 5)
                ELSE g.fecha_orden_date + (22 + (g.id % 10))
            END, 'YYYYMMDD')::INT AS fecha_real_entrega_sk,
        g.cliente_sk,
        g.producto_sk,
        g.showroom_sk,
        g.asesor_sk,
        g.canal_sk,
        g.tipo_surtido,
        g.cantidad,
        p.precio_base AS precio_unitario,
        p.costo_base AS costo_unitario,
        CASE WHEN (g.id % 4) = 0 THEN 2500.00 WHEN (g.id % 3) = 0 THEN 1200.00 ELSE 0.00 END AS descuento_orden,
        CASE WHEN g.canal_sk = 2 THEN 650.00 WHEN (g.id % 2) = 0 THEN 850.00 ELSE 450.00 END AS envio_orden
    FROM generador_lineas g
    JOIN (
        VALUES
        (1, 28500.00, 14250.00), (2, 28500.00, 14250.00), (3, 34900.00, 18500.00), (4, 8900.00, 4200.00),
        (5, 6500.00, 2900.00),   (6, 29800.00, 15500.00), (7, 22500.00, 11800.00), (8, 3400.00, 1600.00),
        (9, 3600.00, 1750.00),   (10, 21900.00, 10500.00),(11, 32000.00, 16800.00),(12, 26500.00, 13900.00),
        (13, 4800.00, 2200.00),  (14, 18500.00, 9100.00), (15, 16800.00, 8200.00), (16, 7200.00, 3400.00),
        (17, 5400.00, 2400.00),  (18, 3200.00, 1350.00),  (19, 7900.00, 3600.00),   (20, 6200.00, 2700.00)
    ) AS p(prod_id, precio_base, costo_base) ON g.producto_sk = p.prod_id
),
ordenes_totales AS (
    SELECT
        orden_id,
        SUM(cantidad * precio_unitario) AS subtotal_orden
    FROM staging_lineas
    GROUP BY orden_id
)
SELECT
    l.fecha_orden_sk,
    l.fecha_prometida_sk,
    l.fecha_real_entrega_sk,
    l.cliente_sk,
    l.producto_sk,
    l.showroom_sk,
    l.asesor_sk,
    l.canal_sk,
    l.orden_id,
    l.tipo_surtido,
    l.cantidad,
    l.precio_unitario,
    l.costo_unitario,
    (l.cantidad * l.precio_unitario) AS monto_subtotal,
    (l.cantidad * l.costo_unitario) AS monto_costo_total,
    ROUND(((l.cantidad * l.precio_unitario) / ot.subtotal_orden) * l.descuento_orden, 2) AS monto_descuento_prorrateado,
    ROUND(((l.cantidad * l.precio_unitario) / ot.subtotal_orden) * l.envio_orden, 2) AS monto_envio_prorrateado,
    ((l.cantidad * l.precio_unitario) - ROUND(((l.cantidad * l.precio_unitario) / ot.subtotal_orden) * l.descuento_orden, 2)) AS monto_venta_neta,
    (((l.cantidad * l.precio_unitario) - ROUND(((l.cantidad * l.precio_unitario) / ot.subtotal_orden) * l.descuento_orden, 2)) - (l.cantidad * l.costo_unitario)) AS ganancia_bruta,
    CASE
        WHEN l.fecha_real_entrega_sk IS NOT NULL AND l.fecha_orden_sk IS NOT NULL THEN
            (TO_DATE(l.fecha_real_entrega_sk::TEXT, 'YYYYMMDD') - TO_DATE(l.fecha_orden_sk::TEXT, 'YYYYMMDD'))::INT
        ELSE NULL
    END AS dias_para_entrega,
    CASE
        WHEN l.fecha_real_entrega_sk IS NOT NULL AND l.fecha_prometida_sk IS NOT NULL THEN
            (TO_DATE(l.fecha_real_entrega_sk::TEXT, 'YYYYMMDD') - TO_DATE(l.fecha_prometida_sk::TEXT, 'YYYYMMDD'))::INT
        ELSE NULL
    END AS retraso_dias
FROM staging_lineas l
JOIN ordenes_totales ot ON l.orden_id = ot.orden_id;

-- ------------------------------------------------------------------------------
-- 8. CONSULTAS DE CONTROL DE CALIDAD
-- ------------------------------------------------------------------------------
SELECT 'Fact_Ventas' AS tabla, COUNT(*) AS total_registros FROM Fact_Ventas;
