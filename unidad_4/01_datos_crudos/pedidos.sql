-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 01_datos_crudos / pedidos.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Carga de pedidos crudos en raw_pedidos con errores deliberados
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- Limpieza preventiva de pedidos crudos para evitar duplicaciones por recarga
TRUNCATE TABLE raw_pedidos;

INSERT INTO raw_pedidos (id_pedido, id_cliente, fecha_pedido, importe, estado_pedido, estado_envio) VALUES
-- Bloque 1: Pedidos válidos con estados oficiales y alias diversos
('PED-1001', 'CLI-001', '2026-03-01', '1250.00', 'Entregado', 'NL'),
('PED-1002', 'CLI-002', '02/03/2026', '840.50',  'Entregado', 'Nuevo Leon'),
('PED-1003', 'CLI-003', '2026-03-03', '2100.00', 'Entregado', 'CDMX'),
('PED-1004', 'CLI-004', '04/03/2026', '1450.00', 'Entregado', 'D.F.'),
('PED-1005', 'CLI-005', '2026-03-05', '3200.00', 'Entregado', 'JAL'),
('PED-1006', 'CLI-006', '2026-03-06', '750.00',  'Entregado', 'Jalisco'),
('PED-1007', 'CLI-007', '2026-03-07', '1890.00', 'Entregado', 'Coahuila'),
('PED-1008', 'CLI-008', '08/03/2026', '920.00',  'Entregado', 'COAH'),
('PED-1009', 'CLI-009', '2026-03-09', '1100.00', 'Entregado', 'TAMPS'),
('PED-1010', 'CLI-010', '2026-03-10', '2650.00', 'Entregado', 'Puebla'),
('PED-1011', 'CLI-011', '11/03/2026', '1350.00', 'Entregado', 'PUE'),
('PED-1012', 'CLI-012', '2026-03-12', '1780.00', 'Entregado', 'YUC'),
('PED-1013', 'CLI-013', '2026-03-13', '2900.00', 'Entregado', 'Yucatan'),
('PED-1014', 'CLI-014', '2026-03-14', '1560.00', 'Entregado', 'Queretaro'),
('PED-1015', 'CLI-015', '2026-03-15', '890.00',  'Entregado', 'QRO'),
('PED-1016', 'CLI-016', '2026-03-16', '3400.00', 'Entregado', 'Veracruz'),
('PED-1017', 'CLI-017', '2026-03-17', '1200.00', 'Entregado', 'GTO'),

-- Bloque 2: Pedidos válidos con otros estatus de negocio
('PED-1018', 'CLI-001', '2026-03-18', '950.00',  'En tránsito', 'NL'),
('PED-1019', 'CLI-003', '2026-03-19', '1800.00', 'Cancelado',   'CDMX'),
('PED-1020', 'CLI-005', '2026-03-20', '650.00',  'Pendiente',   'JAL'),

-- Bloque 3: Errores deliberados - Importes no positivos (negativo y cero)
('PED-1021', 'CLI-002', '2026-03-21', '-350.00', 'Entregado',   'NL'),
('PED-1022', 'CLI-004', '2026-03-22', '0.00',    'Entregado',   'CDMX'),

-- Bloque 4: Error deliberado - Cliente inexistente (huérfano)
('PED-1023', 'CLI-999', '2026-03-23', '1500.00', 'Entregado',   'NL'),

-- Bloque 5: Errores deliberados - Fechas vacías o corruptas
('PED-1024', 'CLI-007', '',           '1200.00', 'Entregado',   'COAH'),
('PED-1025', 'CLI-008', 'FECHA_ROTA', '980.00',  'Entregado',   'COAH'),

-- Bloque 6: Error deliberado - Estado federativo no reconocido en catálogo
('PED-1026', 'CLI-009', '2026-03-25', '1400.00', 'Entregado',   'ESTADO_INEXISTENTE'),

-- Bloque 7: Errores deliberados - Duplicados por id_pedido
('PED-1001', 'CLI-001', '2026-03-01', '1250.00', 'Entregado',   'NL'),
('PED-1010', 'CLI-010', '2026-03-10', '2650.00', 'Entregado',   'Puebla'),

-- Bloque 8: Pedidos adicionales entregados para mayor riqueza analítica
('PED-1027', 'CLI-010', '2026-03-26', '2100.00', 'Entregado',   'PUE'),
('PED-1028', 'CLI-012', '27/03/2026', '1650.00', 'Entregado',   'YUC'),
('PED-1029', 'CLI-014', '2026-03-28', '1950.00', 'Entregado',   'QRO'),
('PED-1030', 'CLI-017', '2026-03-29', '880.00',  'Entregado',   'GTO');
