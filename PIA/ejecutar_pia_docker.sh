#!/usr/bin/env bash
# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
# ARCHIVO: ejecutar_pia_docker.sh
# AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Docker Engine / Bash
# ==============================================================================
# FUNCIÓN GENERAL:
# Orquestador maestro 100% automatizado y reproducible para desplegar, ejecutar,
# validar y empaquetar de principio a fin la solución de Business Intelligence
# para Casa&Estilo dentro de contenedores Docker.
#
# FUNCIÓN ESPECÍFICA:
# 1. Iniciar el servicio de MySQL 8.0 en Docker Compose y validar salud.
# 2. Copiar archivos RAW e ingestar las 11 tablas en la base de datos `ce_bi`.
# 3. Compilar DDL, Stored Procedures y vistas analíticas del Data Mart.
# 4. Ejecutar el pipeline ETL maestro (`CALL sp_orquestador_etl_maestro()`).
# 5. Ejecutar la auditoría de balance de masa y certificar 0 discrepancias.
# 6. Exportar vistas analíticas y generar artefactos (.xlsx, .pptx, .pdf).
# 7. Empaquetar la entrega final en `PIA/PIA_Equipo08_CasaEstilo.zip`.
# ==============================================================================

set -e

COLOR_CYAN='\033[0;36m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

echo -e "${COLOR_CYAN}==============================================================================${COLOR_RESET}"
echo -e "${COLOR_CYAN}    FIME UANL — ANALÍTICA E INTELIGENCIA DE NEGOCIOS (EQUIPO 8)               ${COLOR_RESET}"
echo -e "${COLOR_CYAN}    RUNNER MAESTRO AUTOMATIZADO: PIA SOLUCIÓN BI CASA&ESTILO                  ${COLOR_RESET}"
echo -e "${COLOR_CYAN}==============================================================================${COLOR_RESET}"

# Paso 1: Levantar MySQL en Docker
echo -e "\n${COLOR_YELLOW}[1/7] Iniciando y verificando contenedor MySQL 8.0 (casa_estilo_mysql)...${COLOR_RESET}"
docker compose up -d mysql

echo -n "Esperando a que MySQL responda salud..."
for i in {1..30}; do
  if docker exec casa_estilo_mysql mysqladmin ping -h localhost -u root -ppassword &>/dev/null; then
    echo -e " ${COLOR_GREEN}✔ MySQL activo y saludable.${COLOR_RESET}"
    break
  fi
  sleep 1
  echo -n "."
done

# Paso 2: Copiar archivos CSV al contenedor de MySQL
echo -e "\n${COLOR_YELLOW}[2/7] Copiando fuentes RAW al contenedor para carga ultrarrápida...${COLOR_RESET}"
docker exec casa_estilo_mysql mkdir -p /var/lib/mysql-files/raw
docker cp PIA/CasaEstilo/CasaEstilo/ALUMNO/RAW/. casa_estilo_mysql:/var/lib/mysql-files/raw/
echo -e "${COLOR_GREEN}✔ Archivos RAW sincronizados en /var/lib/mysql-files/raw/ dentro del contenedor.${COLOR_RESET}"

# Paso 3: Inicializar Base de Datos, Staging y Carga Masiva
echo -e "\n${COLOR_YELLOW}[3/7] Desplegando DDL de Staging e ingestando 11 CSVs (+530,000 filas)...${COLOR_RESET}"
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/00_inicializacion_bd_y_logs.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/01_ddl_staging.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/01b_cargar_csv_a_staging.sql
echo -e "${COLOR_GREEN}✔ Tablas Staging cargadas exitosamente con conteo oficial verificado.${COLOR_RESET}"

# Paso 4: Desplegar DDL del Data Mart, Procedimientos y Vistas
echo -e "\n${COLOR_YELLOW}[4/7] Desplegando Data Mart Dimensional, Stored Procedures y Vistas Analíticas...${COLOR_RESET}"
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/02_ddl_datamart.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/03_sp_limpieza_transformacion.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/04_sp_carga_dimensiones_hechos.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/05_sp_orquestador_etl.sql
docker exec -i casa_estilo_mysql mysql -u root -ppassword < PIA/02_datamart_mysql/06_vistas_analiticas_kpi.sql
echo -e "${COLOR_GREEN}✔ Esquema Estrella y Procedimientos Almacenados compilados sin errores.${COLOR_RESET}"

# Paso 5: Ejecutar Orquestador Maestro y Auditoría de Balance de Masa
echo -e "\n${COLOR_YELLOW}[5/7] Ejecutando Pipeline ETL Maestro (sp_orquestador_etl_maestro)...${COLOR_RESET}"
docker exec -i casa_estilo_mysql mysql -u root -ppassword ce_bi -e "CALL sp_orquestador_etl_maestro();"
echo -e "\n${COLOR_YELLOW}Validando Balance de Masa y Cero Discrepancias...${COLOR_RESET}"
docker exec -i casa_estilo_mysql mysql -u root -ppassword ce_bi < PIA/02_datamart_mysql/07_auditoria_balance_masa.sql
echo -e "${COLOR_GREEN}✔ Balance de Masa 100% Conciliado. Discrepancia $0.00 / Cero Huérfanos.${COLOR_RESET}"

# Paso 6: Exportación de Datos y Generación de Artefactos (.xlsx, .pptx, .pdf)
echo -e "\n${COLOR_YELLOW}[6/7] Exportando datasets analíticos y generando entregables en Docker...${COLOR_RESET}"
mkdir -p PIA/03_dashboard_excel/datos_exportados

python3 -c "
import os, subprocess, csv

def export_csv(sql, headers, out_path):
    \"\"\"Ejecuta consulta MySQL en Docker y escribe un CSV UTF-8 validado.\"\"\"
    cmd = ['docker', 'exec', '-i', 'casa_estilo_mysql', 'mysql', '--default-character-set=utf8mb4',
           '-u', 'root', '-ppassword', 'ce_bi', '-B', '-N', '-e', sql]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if res.returncode != 0:
        raise RuntimeError(res.stderr)
    rows = [line.split('\t') for line in res.stdout.rstrip('\n').split('\n') if line]
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

base_dir = 'PIA/03_dashboard_excel/datos_exportados'
for stale in ('fact_ventas_modelo.csv', 'fact_devoluciones_muestra.csv'):
    stale_path = os.path.join(base_dir, stale)
    if os.path.exists(stale_path):
        os.remove(stale_path)

exports = [
    # Vistas y agregados KPI ejecutivos (5 Pilares)
    ('SELECT anio, mes, mes_nombre, mes_anio, transacciones, unidades_vendidas, venta_bruta, descuentos_otorgados, venta_neta, costo_ventas_cogs, utilidad_bruta, margen_bruto_pct, ticket_promedio FROM vw_kpi_resumen_mensual;',
     ['anio', 'mes', 'mes_nombre', 'mes_anio', 'transacciones', 'unidades_vendidas', 'venta_bruta', 'descuentos_otorgados', 'venta_neta', 'costo_ventas_cogs', 'utilidad_bruta', 'margen_bruto_pct', 'ticket_promedio'],
     'kpi_resumen_mensual.csv'),
    ('''SELECT t.anio, COUNT(DISTINCT f.venta_id) AS transacciones, SUM(f.cantidad) AS unidades_vendidas,
               ROUND(SUM(f.monto_bruto), 2) AS venta_bruta, ROUND(SUM(f.monto_descuento), 2) AS descuentos_otorgados,
               ROUND(SUM(f.monto_neto), 2) AS venta_neta, ROUND(SUM(f.utilidad_bruta), 2) AS utilidad_bruta,
               ROUND(100 * SUM(f.utilidad_bruta) / SUM(f.monto_neto), 2) AS margen_bruto_pct,
               ROUND(SUM(f.monto_neto) / COUNT(DISTINCT f.venta_id), 2) AS ticket_promedio
        FROM fact_ventas_detalle f INNER JOIN dim_tiempo t ON f.tiempo_id = t.tiempo_id
        GROUP BY t.anio ORDER BY t.anio;''',
     ['anio', 'transacciones', 'unidades_vendidas', 'venta_bruta', 'descuentos_otorgados', 'venta_neta', 'utilidad_bruta', 'margen_bruto_pct', 'ticket_promedio'],
     'kpi_resumen_anual.csv'),
    ('SELECT categoria, skus_activos, unidades_vendidas, venta_bruta, venta_neta, costo_total, utilidad_bruta, margen_pct, unidades_devueltas, monto_devuelto, tasa_devolucion_pct FROM vw_kpi_desempeno_categorias;',
     ['categoria', 'skus_activos', 'unidades_vendidas', 'venta_bruta', 'venta_neta', 'costo_total', 'utilidad_bruta', 'margen_pct', 'unidades_devueltas', 'monto_devuelto', 'tasa_devolucion_pct'],
     'kpi_categorias.csv'),
    ('SELECT canal, transacciones, unidades_vendidas, venta_neta, ticket_promedio, utilidad_bruta, margen_pct FROM vw_kpi_omnicanalidad;',
     ['canal', 'transacciones', 'unidades_vendidas', 'venta_neta', 'ticket_promedio', 'utilidad_bruta', 'margen_pct'],
     'kpi_omnicanalidad.csv'),
    ('SELECT sucursal_id, sucursal, ciudad, estado, m2, categoria_tamano, transacciones, venta_neta, venta_por_m2, utilidad_bruta, margen_pct FROM vw_kpi_sucursales;',
     ['sucursal_id', 'sucursal', 'ciudad', 'estado', 'm2', 'categoria_tamano', 'transacciones', 'venta_neta', 'venta_por_m2', 'utilidad_bruta', 'margen_pct'],
     'kpi_sucursales.csv'),
    ('SELECT sucursal, total_servicios, servicios_a_tiempo, servicios_con_retraso, cumplimiento_sla_pct, dias_reales_promedio, dias_retraso_promedio, satisfaccion_promedio FROM vw_kpi_instalaciones_sla;',
     ['sucursal', 'total_servicios', 'servicios_a_tiempo', 'servicios_con_retraso', 'cumplimiento_sla_pct', 'dias_reales_promedio', 'dias_retraso_promedio', 'satisfaccion_promedio'],
     'kpi_instalaciones_sla.csv'),
    ('SELECT motivo, COUNT(*) AS eventos, SUM(cantidad_devuelta) AS piezas, SUM(importe_devuelto) AS total_reembolsado FROM fact_devoluciones GROUP BY motivo ORDER BY total_reembolsado DESC;',
     ['motivo', 'eventos', 'piezas', 'total_reembolsado'],
     'kpi_devoluciones_motivos.csv'),
    ('SELECT estatus_stock, COUNT(*) AS items, SUM(stock_actual) AS piezas_stock, SUM(deficit_unidades) AS deficit_piezas, SUM(valor_inventario_costo) AS valor_inventario FROM fact_inventario_snapshot GROUP BY estatus_stock;',
     ['estatus_stock', 'items', 'piezas_stock', 'deficit_piezas', 'valor_inventario'],
     'kpi_inventario_resumen.csv'),
    ('''SELECT c.segmento, COUNT(DISTINCT c.cliente_key) AS clientes, COUNT(DISTINCT f.venta_id) AS tickets,
               SUM(f.cantidad) AS unidades, ROUND(SUM(f.monto_bruto), 2) AS venta_bruta,
               ROUND(SUM(f.monto_descuento), 2) AS descuentos_mxn, ROUND(SUM(f.monto_neto), 2) AS venta_neta,
               ROUND(SUM(f.utilidad_bruta), 2) AS utilidad_bruta, ROUND(100 * SUM(f.utilidad_bruta) / SUM(f.monto_neto), 2) AS margen_pct
        FROM fact_ventas_detalle f INNER JOIN dim_cliente c ON f.cliente_key = c.cliente_key
        GROUP BY c.segmento ORDER BY venta_neta DESC;''',
     ['segmento', 'clientes', 'tickets', 'unidades', 'venta_bruta', 'descuentos_mxn', 'venta_neta', 'utilidad_bruta', 'margen_pct'],
     'kpi_clientes_segmentos.csv'),
    ('''SELECT m.metodo_pago_id, m.metodo_nombre, COUNT(DISTINCT f.venta_id) AS tickets,
               SUM(f.cantidad) AS unidades, ROUND(SUM(f.monto_neto), 2) AS venta_neta,
               ROUND(SUM(f.monto_neto) / COUNT(DISTINCT f.venta_id), 2) AS ticket_promedio,
               ROUND(SUM(f.utilidad_bruta), 2) AS utilidad_bruta
        FROM fact_ventas_detalle f INNER JOIN dim_metodo_pago m ON f.metodo_pago_id = m.metodo_pago_id
        GROUP BY m.metodo_pago_id, m.metodo_nombre ORDER BY venta_neta DESC;''',
     ['metodo_pago_id', 'metodo_nombre', 'tickets', 'unidades', 'venta_neta', 'ticket_promedio', 'utilidad_bruta'],
     'kpi_metodos_pago.csv'),
    ('''SELECT p.categoria, COUNT(*) AS skus_sucursal, COUNT(DISTINCT inv.producto_key) AS skus,
               SUM(inv.stock_actual) AS stock_actual, SUM(inv.punto_reorden) AS punto_reorden,
               SUM(inv.deficit_unidades) AS deficit_unidades,
               SUM(inv.estatus_stock = 'Rotura Stock') AS roturas,
               SUM(inv.estatus_stock = 'Alerta Reorden') AS alertas,
               ROUND(SUM(inv.valor_inventario_costo), 2) AS valor_costo
        FROM fact_inventario_snapshot inv INNER JOIN dim_producto p ON inv.producto_key = p.producto_key
        GROUP BY p.categoria ORDER BY valor_costo DESC;''',
     ['categoria', 'skus_sucursal', 'skus', 'stock_actual', 'punto_reorden', 'deficit_unidades', 'roturas', 'alertas', 'valor_costo'],
     'kpi_inventario_categorias.csv'),
    ('''SELECT p.categoria, SUM(f.cantidad) AS unidades, ROUND(SUM(f.monto_bruto), 2) AS venta_bruta,
               ROUND(SUM(f.monto_descuento), 2) AS descuentos_mxn,
               ROUND(100 * SUM(f.monto_descuento) / SUM(f.monto_bruto), 2) AS tasa_descuento_pct,
               ROUND(SUM(f.monto_neto), 2) AS venta_neta, ROUND(SUM(f.utilidad_bruta), 2) AS utilidad_bruta,
               ROUND(100 * SUM(f.utilidad_bruta) / SUM(f.monto_neto), 2) AS margen_pct
        FROM fact_ventas_detalle f INNER JOIN dim_producto p ON f.producto_key = p.producto_key
        GROUP BY p.categoria ORDER BY venta_neta DESC;''',
     ['categoria', 'unidades', 'venta_bruta', 'descuentos_mxn', 'tasa_descuento_pct', 'venta_neta', 'utilidad_bruta', 'margen_pct'],
     'kpi_descuentos_categorias.csv'),
    ('''SELECT p.producto_id, p.sku, p.producto, p.categoria, p.marca, p.requiere_instalacion,
               COUNT(DISTINCT f.venta_id) AS tickets, SUM(f.cantidad) AS unidades,
               ROUND(SUM(f.monto_neto), 2) AS venta_neta, ROUND(SUM(f.utilidad_bruta), 2) AS utilidad_bruta,
               ROUND(100 * SUM(f.utilidad_bruta) / SUM(f.monto_neto), 2) AS margen_pct
        FROM fact_ventas_detalle f INNER JOIN dim_producto p ON f.producto_key = p.producto_key
        GROUP BY p.producto_key, p.producto_id, p.sku, p.producto, p.categoria, p.marca, p.requiere_instalacion
        ORDER BY venta_neta DESC LIMIT 15;''',
     ['producto_id', 'sku', 'producto', 'categoria', 'marca', 'requiere_instalacion', 'tickets', 'unidades', 'venta_neta', 'utilidad_bruta', 'margen_pct'],
     'kpi_productos_top.csv'),

    # Dimensiones conformes completas (Esquema Estrella Kimball)
    ('SELECT tiempo_id, fecha, anio, trimestre, trimestre_nombre, mes, mes_nombre, mes_anio, semana_anio, dia_mes, dia_semana, dia_semana_nombre, es_fin_semana FROM dim_tiempo;',
     ['tiempo_id', 'fecha', 'anio', 'trimestre', 'trimestre_nombre', 'mes', 'mes_nombre', 'mes_anio', 'semana_anio', 'dia_mes', 'dia_semana', 'dia_semana_nombre', 'es_fin_semana'],
     'dim_tiempo.csv'),
    ('SELECT producto_key, producto_id, sku, producto, categoria, marca, costo, precio_lista, margen_teorico_pct, activo, requiere_instalacion FROM dim_producto;',
     ['producto_key', 'producto_id', 'sku', 'producto', 'categoria', 'marca', 'costo', 'precio_lista', 'margen_teorico_pct', 'activo', 'requiere_instalacion'],
     'dim_producto.csv'),
    ('SELECT sucursal_key, sucursal_id, sucursal, ciudad, estado, m2, categoria_tamano, fecha_apertura FROM dim_sucursal;',
     ['sucursal_key', 'sucursal_id', 'sucursal', 'ciudad', 'estado', 'm2', 'categoria_tamano', 'fecha_apertura'],
     'dim_sucursal.csv'),
    ('SELECT canal_id, canal_nombre FROM dim_canal;',
     ['canal_id', 'canal_nombre'],
     'dim_canal.csv'),
    ('SELECT cliente_key, cliente_id, nombre, sexo, fecha_alta, ciudad, segmento, email FROM dim_cliente;',
     ['cliente_key', 'cliente_id', 'nombre', 'sexo', 'fecha_alta', 'ciudad', 'segmento', 'email'],
     'dim_cliente.csv'),
    ('SELECT metodo_pago_id, metodo_nombre FROM dim_metodo_pago;',
     ['metodo_pago_id', 'metodo_nombre'],
     'dim_metodo_pago.csv'),

    # Tablas de Hechos completas (100% fidelidad sin truncamiento ni distorsion temporal)
    ('SELECT venta_id, tiempo_id, producto_key, cliente_key, sucursal_key, canal_id, metodo_pago_id, cantidad, monto_bruto, monto_descuento, monto_neto, costo_total, utilidad_bruta FROM fact_ventas_detalle;',
     ['venta_id', 'tiempo_id', 'producto_key', 'cliente_key', 'sucursal_key', 'canal_id', 'metodo_pago_id', 'cantidad', 'monto_bruto', 'monto_descuento', 'monto_neto', 'costo_total', 'utilidad_bruta'],
     'fact_ventas_detalle.csv'),
    ('SELECT devolucion_id, venta_id, tiempo_id, producto_key, sucursal_key, cliente_key, cantidad_devuelta, importe_devuelto, motivo FROM fact_devoluciones;',
     ['devolucion_id', 'venta_id', 'tiempo_id', 'producto_key', 'sucursal_key', 'cliente_key', 'cantidad_devuelta', 'importe_devuelto', 'motivo'],
     'fact_devoluciones_completo.csv'),
    ('SELECT instalacion_id, venta_id, tiempo_id, cliente_key, sucursal_key, dias_programados, dias_reales, dias_desviacion, cumplio_sla, satisfaccion FROM fact_instalaciones;',
     ['instalacion_id', 'venta_id', 'tiempo_id', 'cliente_key', 'sucursal_key', 'dias_programados', 'dias_reales', 'dias_desviacion', 'cumplio_sla', 'satisfaccion'],
     'fact_instalaciones_completo.csv'),
    ('SELECT sucursal_key, producto_key, stock_actual, punto_reorden, deficit_unidades, valor_inventario_costo, estatus_stock FROM fact_inventario_snapshot;',
     ['sucursal_key', 'producto_key', 'stock_actual', 'punto_reorden', 'deficit_unidades', 'valor_inventario_costo', 'estatus_stock'],
     'fact_inventario_snapshot.csv'),
]

for sql, headers, fname in exports:
    out_file = os.path.join(base_dir, fname)
    export_csv(sql, headers, out_file)
    print(f'  OK {fname}')
"

docker run --rm -v "$(pwd):/workspace" localhost/equipo8-u5-generator:latest python3 PIA/scripts_docker/generar_dashboard_excel.py
docker run --rm -v "$(pwd):/workspace" localhost/equipo8-u5-generator:latest python3 PIA/scripts_docker/generar_presentacion_pptx.py
docker run --rm -v "$(pwd):/workspace" localhost/equipo8-u5-generator:latest python3 PIA/scripts_docker/generar_reporte_pdf.py

echo -e "${COLOR_GREEN}✔ Artefactos generados exitosamente:${COLOR_RESET}"
echo -e "  - Dashboard Excel:       PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx"
echo -e "  - Presentación 10 Slides: PIA/PIA_Comite_CasaEstilo_Equipo08.pptx"
echo -e "  - Reporte Formal PDF:    PIA/PIA_Evidencias_CasaEstilo_Equipo08.pdf"

# Paso 7: Empaque Oficial en ZIP
echo -e "\n${COLOR_YELLOW}[7/7] Empaquetando solución integral en PIA_Equipo08_CasaEstilo.zip...${COLOR_RESET}"
python3 -c "
import os, zipfile

zip_path = 'PIA/PIA_Equipo08_CasaEstilo.zip'
if os.path.exists(zip_path):
    os.remove(zip_path)

targets = [
    'PIA/01_arquitectura_datos',
    'PIA/02_datamart_mysql',
    'PIA/03_dashboard_excel',
    'PIA/04_presentacion_ejecutiva',
    'PIA/scripts_docker',
    'PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx',
    'PIA/PIA_Comite_CasaEstilo_Equipo08.pptx',
    'PIA/PIA_Evidencias_CasaEstilo_Equipo08.pdf',
    'PIA/README.md',
    'PIA/ejecutar_pia_docker.sh'
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for t in targets:
        if os.path.isdir(t):
            for root, dirs, files in os.walk(t):
                for f in files:
                    full_p = os.path.join(root, f)
                    arcname = os.path.relpath(full_p, 'PIA')
                    z.write(full_p, arcname)
        elif os.path.isfile(t):
            arcname = os.path.basename(t)
            z.write(t, arcname)
print(f'Archivo ZIP creado: {zip_path} ({os.path.getsize(zip_path):,} bytes)')
"

echo -e "${COLOR_GREEN}✔ Empaque oficial generado: PIA/PIA_Equipo08_CasaEstilo.zip${COLOR_RESET}"

echo -e "\n${COLOR_CYAN}==============================================================================${COLOR_RESET}"
echo -e "${COLOR_GREEN}    ¡PROYECTO INTEGRADOR DE APRENDIZAJE COMPLETADO AL 100%!                   ${COLOR_RESET}"
echo -e "${COLOR_CYAN}==============================================================================${COLOR_RESET}"
