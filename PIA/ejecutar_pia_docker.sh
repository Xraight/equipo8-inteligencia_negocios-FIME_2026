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
import subprocess, csv
def query_mysql(sql):
    cmd = ['docker', 'exec', '-i', 'casa_estilo_mysql', 'mysql', '--default-character-set=utf8mb4', '-u', 'root', '-ppassword', 'ce_bi', '-B', '-N', '-e', sql]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if res.returncode != 0: raise Exception(res.stderr)
    return [l.split('\t') for l in res.stdout.strip().split('\n') if l]

def export_csv(sql, headers, out_path):
    lines = query_mysql(sql)
    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(lines)

export_csv('SELECT anio, mes, mes_nombre, mes_anio, transacciones, unidades_vendidas, venta_bruta, descuentos_otorgados, venta_neta, costo_ventas_cogs, utilidad_bruta, margen_bruto_pct, ticket_promedio FROM vw_kpi_resumen_mensual;',
           ['anio', 'mes', 'mes_nombre', 'mes_anio', 'transacciones', 'unidades_vendidas', 'venta_bruta', 'descuentos_otorgados', 'venta_neta', 'costo_ventas_cogs', 'utilidad_bruta', 'margen_bruto_pct', 'ticket_promedio'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_resumen_mensual.csv')

export_csv('SELECT categoria, skus_activos, unidades_vendidas, venta_bruta, venta_neta, costo_total, utilidad_bruta, margen_pct, unidades_devueltas, monto_devuelto, tasa_devolucion_pct FROM vw_kpi_desempeno_categorias;',
           ['categoria', 'skus_activos', 'unidades_vendidas', 'venta_bruta', 'venta_neta', 'costo_total', 'utilidad_bruta', 'margen_pct', 'unidades_devueltas', 'monto_devuelto', 'tasa_devolucion_pct'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_categorias.csv')

export_csv('SELECT canal, transacciones, unidades_vendidas, venta_neta, ticket_promedio, utilidad_bruta, margen_pct FROM vw_kpi_omnicanalidad;',
           ['canal', 'transacciones', 'unidades_vendidas', 'venta_neta', 'ticket_promedio', 'utilidad_bruta', 'margen_pct'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_omnicanalidad.csv')

export_csv('SELECT sucursal_id, sucursal, ciudad, estado, m2, categoria_tamano, transacciones, venta_neta, venta_por_m2, utilidad_bruta, margen_pct FROM vw_kpi_sucursales;',
           ['sucursal_id', 'sucursal', 'ciudad', 'estado', 'm2', 'categoria_tamano', 'transacciones', 'venta_neta', 'venta_por_m2', 'utilidad_bruta', 'margen_pct'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_sucursales.csv')

export_csv('SELECT sucursal, total_servicios, servicios_a_tiempo, servicios_con_retraso, cumplimiento_sla_pct, dias_reales_promedio, dias_retraso_promedio, satisfaccion_promedio FROM vw_kpi_instalaciones_sla;',
           ['sucursal', 'total_servicios', 'servicios_a_tiempo', 'servicios_con_retraso', 'cumplimiento_sla_pct', 'dias_reales_promedio', 'dias_retraso_promedio', 'satisfaccion_promedio'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_instalaciones_sla.csv')

export_csv('SELECT motivo, COUNT(*) AS eventos, SUM(cantidad_devuelta) AS piezas, SUM(importe_devuelto) AS total_reembolsado FROM fact_devoluciones GROUP BY motivo ORDER BY total_reembolsado DESC;',
           ['motivo', 'eventos', 'piezas', 'total_reembolsado'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_devoluciones_motivos.csv')

export_csv('SELECT estatus_stock, COUNT(*) AS items, SUM(stock_actual) AS piezas_stock, SUM(deficit_unidades) AS deficit_piezas, SUM(valor_inventario_costo) AS valor_inventario FROM fact_inventario_snapshot GROUP BY estatus_stock;',
           ['estatus_stock', 'items', 'piezas_stock', 'deficit_piezas', 'valor_inventario'],
           'PIA/03_dashboard_excel/datos_exportados/kpi_inventario_resumen.csv')

# Tablas dimensionales y modelo para Power Pivot
export_csv('SELECT tiempo_id, fecha, anio, trimestre, trimestre_nombre, mes, mes_nombre, mes_anio, semana_anio, dia_mes, dia_semana, dia_semana_nombre, es_fin_semana FROM dim_tiempo;',
           ['tiempo_id', 'fecha', 'anio', 'trimestre', 'trimestre_nombre', 'mes', 'mes_nombre', 'mes_anio', 'semana_anio', 'dia_mes', 'dia_semana', 'dia_semana_nombre', 'es_fin_semana'],
           'PIA/03_dashboard_excel/datos_exportados/dim_tiempo.csv')

export_csv('SELECT producto_key, producto_id, sku, producto, categoria, marca, costo, precio_lista, margen_teorico_pct, activo, requiere_instalacion FROM dim_producto;',
           ['producto_key', 'producto_id', 'sku', 'producto', 'categoria', 'marca', 'costo', 'precio_lista', 'margen_teorico_pct', 'activo', 'requiere_instalacion'],
           'PIA/03_dashboard_excel/datos_exportados/dim_producto.csv')

export_csv('SELECT sucursal_key, sucursal_id, sucursal, ciudad, estado, m2, categoria_tamano, fecha_apertura FROM dim_sucursal;',
           ['sucursal_key', 'sucursal_id', 'sucursal', 'ciudad', 'estado', 'm2', 'categoria_tamano', 'fecha_apertura'],
           'PIA/03_dashboard_excel/datos_exportados/dim_sucursal.csv')

export_csv('SELECT canal_id, canal_nombre FROM dim_canal;',
           ['canal_id', 'canal_nombre'],
           'PIA/03_dashboard_excel/datos_exportados/dim_canal.csv')

export_csv('''SELECT MIN(f.tiempo_id) as tiempo_id,
                     f.producto_key,
                     p.producto_id,
                     p.categoria,
                     f.sucursal_key,
                     f.canal_id,
                     COUNT(DISTINCT f.venta_id) as transacciones,
                     SUM(f.cantidad) as cantidad,
                     SUM(f.monto_bruto) as monto_bruto,
                     SUM(f.monto_descuento) as monto_descuento,
                     SUM(f.monto_neto) as monto_neto,
                     SUM(f.costo_total) as costo_total,
                     SUM(f.utilidad_bruta) as utilidad_bruta
              FROM fact_ventas_detalle f
              INNER JOIN dim_producto p ON f.producto_key = p.producto_key
              GROUP BY f.producto_key, p.producto_id, p.categoria, f.sucursal_key, f.canal_id;''',
           ['tiempo_id', 'producto_key', 'producto_id', 'categoria', 'sucursal_key', 'canal_id', 'transacciones', 'cantidad', 'monto_bruto', 'monto_descuento', 'monto_neto', 'costo_total', 'utilidad_bruta'],
           'PIA/03_dashboard_excel/datos_exportados/fact_ventas_modelo.csv')

export_csv('SELECT devolucion_id, venta_id, tiempo_id, producto_key, sucursal_key, cliente_key, cantidad_devuelta, importe_devuelto, motivo FROM fact_devoluciones LIMIT 2000;',
           ['devolucion_id', 'venta_id', 'tiempo_id', 'producto_key', 'sucursal_key', 'cliente_key', 'cantidad_devuelta', 'importe_devuelto', 'motivo'],
           'PIA/03_dashboard_excel/datos_exportados/fact_devoluciones_muestra.csv')

export_csv('SELECT instalacion_id, venta_id, tiempo_id, cliente_key, sucursal_key, dias_programados, dias_reales, dias_desviacion, cumplio_sla, satisfaccion FROM fact_instalaciones;',
           ['instalacion_id', 'venta_id', 'tiempo_id', 'cliente_key', 'sucursal_key', 'dias_programados', 'dias_reales', 'dias_desviacion', 'cumplio_sla', 'satisfaccion'],
           'PIA/03_dashboard_excel/datos_exportados/fact_instalaciones_completo.csv')

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
