-- ==============================================================================
-- PROYECTO: LABORATORIO ETL - DEL ARCHIVO CRUDO AL DATA MART
-- UNIDAD 4: 01_datos_crudos / 02_carga_datos_iniciales.sql
-- MOTOR: MySQL 8.0+
-- OBJETIVO: Carga reproducible de catalogo_estados y raw_clientes
--           (Equivalente automatizado al Table Data Import Wizard de Workbench)
-- EQUIPO: Equipo 8 (Inteligencia de Negocios - FIME 2026)
-- ==============================================================================

USE tienda_bi;

-- Limpieza preventiva
TRUNCATE TABLE catalogo_estados;
TRUNCATE TABLE raw_clientes;

-- 1. Población de catalogo_estados
INSERT INTO catalogo_estados (estado_canonico, nombre_oficial, alias) VALUES
('NL', 'Nuevo León', 'NL,N.L.,Nuevo Leon,NUEVO LEON,NL.,Nuevo León'),
('CDMX', 'Ciudad de México', 'CDMX,C.D.M.X.,Ciudad de Mexico,DF,D.F.,Distrito Federal,D.F,CDMX.'),
('JAL', 'Jalisco', 'JAL,Jal.,Jalisco,JALISCO,Jal'),
('COAH', 'Coahuila', 'COAH,Coah.,Coahuila de Zaragoza,Coahuila,COAHUILA'),
('TAM', 'Tamaulipas', 'TAM,Tamps.,Tamaulipas,TAMPS,TAM'),
('PUE', 'Puebla', 'PUE,Pue.,Puebla,PUEBLA'),
('QRO', 'Querétaro', 'QRO,Qro.,Queretaro,Querétaro,QUERETARO'),
('YUC', 'Yucatán', 'YUC,Yuc.,Yucatan,Yucatán,YUCATAN'),
('VER', 'Veracruz', 'VER,Ver.,Veracruz,Veracruz de Ignacio de la Llave'),
('GTO', 'Guanajuato', 'GTO,Gto.,Guanajuato,GUANAJUATO');

-- 2. Población de raw_clientes (mapeando las 5 columnas, fila_id autogenerado)
INSERT INTO raw_clientes (id_cliente, nombre, email, estado, fecha_registro) VALUES
('CLI-001', 'Carlos Mendoza', 'carlos.mendoza@email.com', 'Nuevo Leon', '2026-01-15'),
('CLI-002', 'Ana Sofia Garza', 'ana.garza@email.com', 'N.L.', '14/02/2026'),
('CLI-003', 'Roberto Martinez', 'roberto.mtz@email.com', 'CDMX', '2026-01-20'),
('CLI-004', 'Mariana Sanchez', 'mariana.snz@email.com', 'D.F.', '05/02/2026'),
('CLI-005', 'Eduardo Trevino', 'eduardo.trv@email.com', 'Jalisco', '2026-01-10'),
('CLI-005', 'Eduardo Trevino', 'eduardo.trv@email.com', 'JAL', '12/01/2026'), -- Duplicado con variante de estado
('CLI-006', 'Lucia Hernandez', 'lucia.hdz@email.com', 'Jal.', '2026-02-01'),
('CLI-007', 'Fernando Castillo', 'fernando.c@email.com', 'Coahuila', '2026-01-25'),
('CLI-008', 'Valeria Ramos', 'valeria.ramos@email.com', 'COAH', '18/02/2026'),
('CLI-009', 'Jorge Morales', 'jorge.morales@email.com', 'TAMPS', '2026-01-30'),
('CLI-010', 'Patricia Flores', 'patricia.fl@email.com', 'Puebla', '2026-02-10'),
('CLI-011', 'Diego Villarreal', 'diego.v@email.com', 'PUE', '22/02/2026'),
('CLI-012', 'Daniela Ortiz', 'daniela.ortiz@email.com', 'Yucatan', '2026-02-15'),
('CLI-013', 'Alejandro Gomez', 'alejandro.g@email.com', 'YUC', '2026-02-18'),
('CLI-014', 'Gabriela Rios', 'gabriela.r@email.com', 'Queretaro', '2026-02-20'),
('CLI-015', 'Mauricio Benitez', 'mauricio.b@email.com', 'QRO', '25/02/2026'),
('CLI-016', 'Laura Cavazos', 'laura.c@email.com', 'Veracruz', '2026-02-28'),
('CLI-017', 'Esteban Luna', 'esteban.luna@email.com', 'GTO', '2026-03-01'),
('CLI-018', 'Karla Navarro', 'karla.navarro@email.com', '', '2026-03-02'),         -- Estado vacío
('CLI-019', 'Hector Salinas', 'hector.salinas@email.com', 'DESCONOCIDO', '2026-03-05'), -- Estado no mapeable
('CLI-020', 'Beatriz Delgado', 'beatriz.delgado@email.com', 'NL', '');              -- Fecha vacía
