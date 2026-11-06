# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
# ARCHIVO: generar_dashboard_excel.py
# AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Python 3.12 / Docker (openpyxl)
# ==============================================================================
# FUNCIÓN GENERAL:
# Generar el libro de trabajo corporativo oficial `PIA_Dashboard_CasaEstilo_Equipo08.xlsx`
# con el modelo dimensional, catálogo de medidas DAX y Dashboard Ejecutivo interactivo.
#
# FUNCIÓN ESPECÍFICA:
# 1. Crear las pestañas: PORTADA, DASHBOARD_EJECUTIVO, ANALISIS_COMERCIAL,
#    OPERACIONES_Y_CALIDAD, DATA_MODEL_MENSUAL, DATA_CATEGORIAS,
#    DATA_SUCURSALES, DATA_CANALES y DICCIONARIO_DAX.
# 2. Aplicar diseño institucional (Deep Blue #1A365D, Gold #D69E2E, Slate Grey #2D3748).
# 3. Formatear tarjetas KPI, tablas ejecutivas y fórmulas de conciliación cuantitativa.
# ==============================================================================

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DATA_DIR = "PIA/03_dashboard_excel/datos_exportados"
OUT_FILE = "PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx"

# Paleta Ejecutiva FIME / Casa&Estilo
C_NAVY = "1A365D"       # Azul Institucional FIME
C_GOLD = "D69E2E"       # Dorado Ejecutivo
C_SLATE = "2D3748"      # Gris Carbón
C_LIGHT_BG = "F7FAFC"   # Fondo suave
C_WHITE = "FFFFFF"      # Blanco puro
C_ACCENT_BLUE = "2B6CB0"# Azul medio
C_GREEN = "2F855A"      # Verde éxito
C_RED = "C53030"        # Rojo alerta
C_CARD_BG = "EDF2F7"    # Fondo tarjetas

font_title = Font(name="Calibri", size=18, bold=True, color=C_WHITE)
font_subtitle = Font(name="Calibri", size=11, italic=True, color=C_GOLD)
font_section = Font(name="Calibri", size=13, bold=True, color=C_NAVY)
font_header = Font(name="Calibri", size=10, bold=True, color=C_WHITE)
font_bold = Font(name="Calibri", size=10, bold=True, color=C_SLATE)
font_regular = Font(name="Calibri", size=10, color=C_SLATE)
font_kpi_val = Font(name="Calibri", size=16, bold=True, color=C_NAVY)
font_kpi_lbl = Font(name="Calibri", size=9, bold=True, color="718096")

fill_navy = PatternFill(start_color=C_NAVY, end_color=C_NAVY, fill_type="solid")
fill_gold = PatternFill(start_color=C_GOLD, end_color=C_GOLD, fill_type="solid")
fill_card = PatternFill(start_color=C_CARD_BG, end_color=C_CARD_BG, fill_type="solid")
fill_zebra = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
fill_green = PatternFill(start_color="E6FFFA", end_color="E6FFFA", fill_type="solid")
fill_red = PatternFill(start_color="FFF5F5", end_color="FFF5F5", fill_type="solid")

thin_border_side = Side(style='thin', color="CBD5E0")
border_thin = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_card = Border(
    left=Side(style='medium', color=C_NAVY),
    right=thin_border_side,
    top=thin_border_side,
    bottom=thin_border_side
)

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")


def read_csv_data(filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    return headers, rows


def create_workbook():
    wb = openpyxl.Workbook()
    # Eliminar hoja default
    default_sheet = wb.active

    # --------------------------------------------------------------------------
    # 1. HOJA PORTADA
    # --------------------------------------------------------------------------
    ws_portada = wb.create_sheet(title="PORTADA")
    ws_portada.views.sheetView[0].showGridLines = False

    # Banner Institucional
    ws_portada.merge_cells("B2:J3")
    top_cell = ws_portada["B2"]
    top_cell.value = "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN | FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA"
    top_cell.font = Font(name="Calibri", size=13, bold=True, color=C_GOLD)
    top_cell.fill = fill_navy
    top_cell.alignment = align_center

    ws_portada.merge_cells("B4:J5")
    title_cell = ws_portada["B4"]
    title_cell.value = "PRODUCTO INTEGRADOR DE APRENDIZAJE — SOLUCIÓN BI EMPRESARIAL"
    title_cell.font = Font(name="Calibri", size=16, bold=True, color=C_WHITE)
    title_cell.fill = fill_navy
    title_cell.alignment = align_center

    ws_portada.merge_cells("B6:J6")
    sub_cell = ws_portada["B6"]
    sub_cell.value = "Caso de Negocio: Casa&Estilo (Sector Muebles y Decoración) | Noviembre 2026"
    sub_cell.font = Font(name="Calibri", size=11, bold=True, color=C_GOLD)
    sub_cell.fill = fill_navy
    sub_cell.alignment = align_center

    # Tarjeta de Datos del Equipo
    datos_meta = [
        ("Unidad de Aprendizaje:", "Analítica e Inteligencia de Negocios"),
        ("Ponderación Académica:", "30% de la Calificación Total del Curso"),
        ("Equipo Asignado:", "Equipo 8"),
        ("Empresa Asignada:", "Casa&Estilo (Código: CE)"),
        ("Motor Data Mart:", "MySQL 8.0+ Contenerizado en Docker"),
        ("Herramienta Visual:", "Microsoft Excel 365 (Power Pivot & Modelo DAX)"),
        ("Auditoría de Registros:", "140,000 Ventas | 331,758 Líneas Detalle (100% Conciliado)"),
        ("Fecha de Entrega:", "Noviembre 2026")
    ]
    r = 8
    for label, val in datos_meta:
        ws_portada.cell(row=r, column=3, value=label).font = font_bold
        ws_portada.cell(row=r, column=3).alignment = align_left
        ws_portada.cell(row=r, column=5, value=val).font = font_regular
        ws_portada.cell(row=r, column=5).alignment = align_left
        r += 1

    # Índice de Navegación del Libro
    r = 17
    ws_portada.cell(row=r, column=3, value="MAPA DE NAVEGACIÓN DEL LIBRO ANALÍTICO:").font = font_section
    r += 2
    menu = [
        ("DASHBOARD_EJECUTIVO", "Tablero de mando principal con Scorecard de KPIs, tendencias y Pareto"),
        ("ANALISIS_COMERCIAL", "Desglose de márgenes, ventas brutas vs netas y canales de venta"),
        ("OPERACIONES_Y_CALIDAD", "Diagnóstico de devoluciones, SLA de instalaciones y alertas de inventario"),
        ("DICCIONARIO_DAX", "Memoria técnica de formulaciones, medidas DAX y lógica de cálculo"),
        ("DATA_MODEL_MENSUAL", "Tabla de hechos mensual agregada para alimentación analítica"),
        ("DATA_CATEGORIAS", "Dimensión y métricas de desempeño por categoría de producto"),
        ("DATA_SUCURSALES", "Desempeño y ventas por metro cuadrado de las 16 sucursales"),
        ("DATA_CANALES", "Matriz omnicanal (Tienda física, Web y App móvil)")
    ]
    for pestana, desc in menu:
        c1 = ws_portada.cell(row=r, column=3, value=f"▶ {pestana}")
        c1.font = Font(name="Calibri", size=10, bold=True, color=C_ACCENT_BLUE, underline="single")
        ws_portada.cell(row=r, column=5, value=desc).font = font_regular
        r += 1

    # --------------------------------------------------------------------------
    # 2. HOJA DASHBOARD_EJECUTIVO
    # --------------------------------------------------------------------------
    ws_dash = wb.create_sheet(title="DASHBOARD_EJECUTIVO")
    ws_dash.views.sheetView[0].showGridLines = True

    # Encabezado
    ws_dash.merge_cells("B2:K3")
    h_cell = ws_dash["B2"]
    h_cell.value = "CASA&ESTILO — TABLERO DE CONTROL EJECUTIVO Y SCORECARD ESTRATÉGICO"
    h_cell.font = font_title
    h_cell.fill = fill_navy
    h_cell.alignment = align_center

    # Tarjetas KPI (Fila 5 a 7)
    kpis = [
        ("VENTAS NETAS", "$1,310,746,491.89", "Ingreso real de caja", C_NAVY, "B", "C"),
        ("UTILIDAD BRUTA", "$280,874,853.71", "Beneficio comercial", C_GREEN, "D", "E"),
        ("MARGEN BRUTO", "21.43%", "Rentabilidad s/venta", C_GOLD, "F", "G"),
        ("TICKET PROMEDIO", "$9,362.47", "Gasto medio cliente", C_SLATE, "H", "I"),
        ("SLA INSTALACIÓN", "34.77%", "Alerta: 65.2% retraso", C_RED, "J", "K")
    ]

    for title, val, note, color, c_start, c_end in kpis:
        # Título KPI
        ws_dash.merge_cells(f"{c_start}5:{c_end}5")
        cell_t = ws_dash[f"{c_start}5"]
        cell_t.value = title
        cell_t.font = font_kpi_lbl
        cell_t.fill = fill_card
        cell_t.alignment = align_center
        # Valor KPI
        ws_dash.merge_cells(f"{c_start}6:{c_end}6")
        cell_v = ws_dash[f"{c_start}6"]
        cell_v.value = val
        cell_v.font = Font(name="Calibri", size=15, bold=True, color=color)
        cell_v.fill = fill_card
        cell_v.alignment = align_center
        # Nota
        ws_dash.merge_cells(f"{c_start}7:{c_end}7")
        cell_n = ws_dash[f"{c_start}7"]
        cell_n.value = note
        cell_n.font = Font(name="Calibri", size=8, italic=True, color="718096")
        cell_n.fill = fill_card
        cell_n.alignment = align_center

    # Sección 1: Resumen de Desempeño por Categoría
    ws_dash.cell(row=9, column=2, value="1. DESEMPEÑO COMERCIAL POR CATEGORÍA DE PRODUCTO").font = font_section

    cat_headers, cat_rows = read_csv_data("kpi_categorias.csv")
    headers_display = ["Categoría", "SKUs", "Unidades", "Venta Neta ($ MXN)", "Utilidad ($ MXN)", "Margen %", "Devoluciones ($)", "Tasa Dev %"]
    for col_idx, h_name in enumerate(headers_display, start=2):
        cell = ws_dash.cell(row=11, column=col_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_cat = 12
    for r_data in cat_rows:
        ws_dash.cell(row=r_cat, column=2, value=r_data[0]).font = font_bold        # Categoria
        ws_dash.cell(row=r_cat, column=3, value=int(r_data[1])).font = font_regular # SKUs
        ws_dash.cell(row=r_cat, column=3).number_format = "#,##0"
        ws_dash.cell(row=r_cat, column=4, value=int(r_data[2])).font = font_regular # Unidades
        ws_dash.cell(row=r_cat, column=4).number_format = "#,##0"

        c_vn = ws_dash.cell(row=r_cat, column=5, value=float(r_data[4]))           # Venta Neta
        c_vn.font = font_regular
        c_vn.number_format = "$#,##0.00"

        c_ub = ws_dash.cell(row=r_cat, column=6, value=float(r_data[6]))           # Utilidad
        c_ub.font = font_regular
        c_ub.number_format = "$#,##0.00"

        c_mg = ws_dash.cell(row=r_cat, column=7, value=float(r_data[7])/100.0)      # Margen
        c_mg.font = font_bold
        c_mg.number_format = "0.00%"

        c_dev = ws_dash.cell(row=r_cat, column=8, value=float(r_data[9]))          # Monto devuelto
        c_dev.font = font_regular
        c_dev.number_format = "$#,##0.00"

        c_td = ws_dash.cell(row=r_cat, column=9, value=float(r_data[10])/100.0)    # Tasa dev
        c_td.font = font_regular
        c_td.number_format = "0.00%"

        for c_idx in range(2, 10):
            ws_dash.cell(row=r_cat, column=c_idx).border = border_thin
            if r_cat % 2 == 1:
                ws_dash.cell(row=r_cat, column=c_idx).fill = fill_zebra
        r_cat += 1

    # Fila de Totales de Categoría
    ws_dash.cell(row=r_cat, column=2, value="TOTAL GENERAL").font = font_bold
    ws_dash.cell(row=r_cat, column=2).fill = fill_gold
    ws_dash.cell(row=r_cat, column=3, value="=SUM(C12:C18)").number_format = "#,##0"
    ws_dash.cell(row=r_cat, column=4, value="=SUM(D12:D18)").number_format = "#,##0"
    ws_dash.cell(row=r_cat, column=5, value="=SUM(E12:E18)").number_format = "$#,##0.00"
    ws_dash.cell(row=r_cat, column=6, value="=SUM(F12:F18)").number_format = "$#,##0.00"
    ws_dash.cell(row=r_cat, column=7, value="=F19/E19").number_format = "0.00%"
    ws_dash.cell(row=r_cat, column=8, value="=SUM(H12:H18)").number_format = "$#,##0.00"
    ws_dash.cell(row=r_cat, column=9, value="=H19/E19").number_format = "0.00%"
    for c_idx in range(2, 10):
        c = ws_dash.cell(row=r_cat, column=c_idx)
        c.font = font_bold
        c.fill = fill_gold
        c.border = border_thin

    # Sección 2: Matriz Omnicanal (Tienda vs Web vs App)
    r_chan_title = r_cat + 3
    ws_dash.cell(row=r_chan_title, column=2, value="2. DESEMPEÑO OMNICANAL (TIENDA VS WEB VS APP)").font = font_section

    chan_headers, chan_rows = read_csv_data("kpi_omnicanalidad.csv")
    chan_cols = ["Canal Comercial", "Transacciones", "Unidades", "Venta Neta ($)", "Ticket Promedio", "Utilidad ($)", "Margen %"]
    for col_idx, h_name in enumerate(chan_cols, start=2):
        cell = ws_dash.cell(row=r_chan_title+2, column=col_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_ch = r_chan_title + 3
    for r_data in chan_rows:
        ws_dash.cell(row=r_ch, column=2, value=r_data[0]).font = font_bold
        ws_dash.cell(row=r_ch, column=3, value=int(r_data[1])).number_format = "#,##0"
        ws_dash.cell(row=r_ch, column=4, value=int(r_data[2])).number_format = "#,##0"
        ws_dash.cell(row=r_ch, column=5, value=float(r_data[3])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_ch, column=6, value=float(r_data[4])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_ch, column=7, value=float(r_data[5])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_ch, column=8, value=float(r_data[6])/100.0).number_format = "0.00%"
        for c_idx in range(2, 9):
            ws_dash.cell(row=r_ch, column=c_idx).border = border_thin
            ws_dash.cell(row=r_ch, column=c_idx).font = font_regular
        r_ch += 1

    # Totales Canal
    ws_dash.cell(row=r_ch, column=2, value="TOTAL OMNICANAL").font = font_bold
    ws_dash.cell(row=r_ch, column=2).fill = fill_gold
    ws_dash.cell(row=r_ch, column=3, value=f"=SUM(C{r_chan_title+3}:C{r_ch-1})").number_format = "#,##0"
    ws_dash.cell(row=r_ch, column=4, value=f"=SUM(D{r_chan_title+3}:D{r_ch-1})").number_format = "#,##0"
    ws_dash.cell(row=r_ch, column=5, value=f"=SUM(E{r_chan_title+3}:E{r_ch-1})").number_format = "$#,##0.00"
    ws_dash.cell(row=r_ch, column=6, value=f"=E{r_ch}/C{r_ch}").number_format = "$#,##0.00"
    ws_dash.cell(row=r_ch, column=7, value=f"=SUM(G{r_chan_title+3}:G{r_ch-1})").number_format = "$#,##0.00"
    ws_dash.cell(row=r_ch, column=8, value=f"=G{r_ch}/E{r_ch}").number_format = "0.00%"
    for c_idx in range(2, 9):
        c = ws_dash.cell(row=r_ch, column=c_idx)
        c.font = font_bold
        c.fill = fill_gold
        c.border = border_thin

    # --------------------------------------------------------------------------
    # 3. HOJA ANALISIS_COMERCIAL
    # --------------------------------------------------------------------------
    ws_com = wb.create_sheet(title="ANALISIS_COMERCIAL")
    ws_com.views.sheetView[0].showGridLines = True

    ws_com.merge_cells("B2:J3")
    c_hdr = ws_com["B2"]
    c_hdr.value = "CASA&ESTILO — ANÁLISIS DE RENTABILIDAD, DESCUENTOS Y SUCURSALES"
    c_hdr.font = font_title
    c_hdr.fill = fill_navy
    c_hdr.alignment = align_center

    ws_com.cell(row=5, column=2, value="PRODUCTIVIDAD Y RENTABILIDAD POR SUCURSAL FÍSICA (16 TIENDAS)").font = font_section

    suc_headers, suc_rows = read_csv_data("kpi_sucursales.csv")
    s_cols = ["ID", "Sucursal", "Ciudad", "Estado", "Superficie (m2)", "Formato", "Tickets", "Venta Neta ($)", "Venta / m2 ($)", "Utilidad ($)", "Margen %"]
    for c_idx, h_name in enumerate(s_cols, start=2):
        cell = ws_com.cell(row=7, column=c_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_s = 8
    for r_data in suc_rows:
        ws_com.cell(row=r_s, column=2, value=r_data[0]).alignment = align_center # ID
        ws_com.cell(row=r_s, column=3, value=r_data[1]).font = font_bold         # Nombre
        ws_com.cell(row=r_s, column=4, value=r_data[2])                          # Ciudad
        ws_com.cell(row=r_s, column=5, value=r_data[3])                          # Estado
        ws_com.cell(row=r_s, column=6, value=int(r_data[4])).number_format = "#,##0" # m2
        ws_com.cell(row=r_s, column=7, value=r_data[5])                          # Formato
        ws_com.cell(row=r_s, column=8, value=int(r_data[6])).number_format = "#,##0" # Tickets
        ws_com.cell(row=r_s, column=9, value=float(r_data[7])).number_format = "$#,##0.00" # Venta
        ws_com.cell(row=r_s, column=10, value=float(r_data[8])).number_format = "$#,##0.00" # Venta/m2
        ws_com.cell(row=r_s, column=11, value=float(r_data[9])).number_format = "$#,##0.00" # Utilidad
        ws_com.cell(row=r_s, column=12, value=float(r_data[10])/100.0).number_format = "0.00%" # Margen
        for col_idx in range(2, 13):
            ws_com.cell(row=r_s, column=col_idx).border = border_thin
            ws_com.cell(row=r_s, column=col_idx).font = font_regular
            if r_s % 2 == 1:
                ws_com.cell(row=r_s, column=col_idx).fill = fill_zebra
        r_s += 1

    # Total Sucursales
    ws_com.cell(row=r_s, column=2, value="TOTAL").font = font_bold
    ws_com.cell(row=r_s, column=2).fill = fill_gold
    ws_com.cell(row=r_s, column=6, value=f"=SUM(F8:F{r_s-1})").number_format = "#,##0"
    ws_com.cell(row=r_s, column=8, value=f"=SUM(H8:H{r_s-1})").number_format = "#,##0"
    ws_com.cell(row=r_s, column=9, value=f"=SUM(I8:I{r_s-1})").number_format = "$#,##0.00"
    ws_com.cell(row=r_s, column=10, value=f"=I{r_s}/F{r_s}").number_format = "$#,##0.00"
    ws_com.cell(row=r_s, column=11, value=f"=SUM(K8:K{r_s-1})").number_format = "$#,##0.00"
    ws_com.cell(row=r_s, column=12, value=f"=K{r_s}/I{r_s}").number_format = "0.00%"
    for col_idx in range(2, 13):
        c = ws_com.cell(row=r_s, column=col_idx)
        c.font = font_bold
        c.fill = fill_gold
        c.border = border_thin

    # --------------------------------------------------------------------------
    # 4. HOJA OPERACIONES_Y_CALIDAD
    # --------------------------------------------------------------------------
    ws_ops = wb.create_sheet(title="OPERACIONES_Y_CALIDAD")
    ws_ops.views.sheetView[0].showGridLines = True

    ws_ops.merge_cells("B2:J3")
    o_hdr = ws_ops["B2"]
    o_hdr.value = "CASA&ESTILO — CALIDAD, DEVOLUCIONES Y NIVEL DE SERVICIO LOGÍSTICO"
    o_hdr.font = font_title
    o_hdr.fill = fill_navy
    o_hdr.alignment = align_center

    # Tabla 1: Devoluciones por Motivo
    ws_ops.cell(row=5, column=2, value="1. ANÁLISIS DE CAUSA RAÍZ DE DEVOLUCIONES (COSTO DE NO CALIDAD)").font = font_section

    dev_headers, dev_rows = read_csv_data("kpi_devoluciones_motivos.csv")
    d_cols = ["Motivo de Devolución", "Eventos", "Piezas Devueltas", "Importe Reembolsado ($ MXN)", "Participación %"]
    for c_idx, h_name in enumerate(d_cols, start=2):
        cell = ws_ops.cell(row=7, column=c_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_d = 8
    for r_data in dev_rows:
        ws_ops.cell(row=r_d, column=2, value=r_data[0]).font = font_bold
        ws_ops.cell(row=r_d, column=3, value=int(r_data[1])).number_format = "#,##0"
        ws_ops.cell(row=r_d, column=4, value=int(r_data[2])).number_format = "#,##0"
        ws_ops.cell(row=r_d, column=5, value=float(r_data[3])).number_format = "$#,##0.00"
        ws_ops.cell(row=r_d, column=6, value=f"=E{r_d}/E13").number_format = "0.00%"
        for col_idx in range(2, 7):
            ws_ops.cell(row=r_d, column=col_idx).border = border_thin
            ws_ops.cell(row=r_d, column=col_idx).font = font_regular
        r_d += 1

    # Total Devoluciones
    ws_ops.cell(row=r_d, column=2, value="TOTAL DEVOLUCIONES").font = font_bold
    ws_ops.cell(row=r_d, column=2).fill = fill_gold
    ws_ops.cell(row=r_d, column=3, value="=SUM(C8:C12)").number_format = "#,##0"
    ws_ops.cell(row=r_d, column=4, value="=SUM(D8:D12)").number_format = "#,##0"
    ws_ops.cell(row=r_d, column=5, value="=SUM(E8:E12)").number_format = "$#,##0.00"
    ws_ops.cell(row=r_d, column=6, value="100.00%").number_format = "0.00%"
    for col_idx in range(2, 7):
        c = ws_ops.cell(row=r_d, column=col_idx)
        c.font = font_bold
        c.fill = fill_gold
        c.border = border_thin

    # Tabla 2: Cumplimiento de SLA en Instalaciones por Sucursal
    ws_ops.cell(row=15, column=2, value="2. DESEMPEÑO LOGÍSTICO Y SLA DE INSTALACIONES (6,500 SERVICIOS)").font = font_section

    sla_headers, sla_rows = read_csv_data("kpi_instalaciones_sla.csv")
    sla_cols = ["Sucursal", "Servicios Totales", "A Tiempo", "Con Retraso", "Cumplimiento SLA %", "Días Reales", "Días Retraso", "Satisfacción (1-5)"]
    for c_idx, h_name in enumerate(sla_cols, start=2):
        cell = ws_ops.cell(row=17, column=c_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_sla = 18
    for r_data in sla_rows:
        ws_ops.cell(row=r_sla, column=2, value=r_data[0]).font = font_bold
        ws_ops.cell(row=r_sla, column=3, value=int(r_data[1])).number_format = "#,##0"
        ws_ops.cell(row=r_sla, column=4, value=int(r_data[2])).number_format = "#,##0"
        ws_ops.cell(row=r_sla, column=5, value=int(r_data[3])).number_format = "#,##0"

        c_sla = ws_ops.cell(row=r_sla, column=6, value=float(r_data[4])/100.0)
        c_sla.number_format = "0.00%"
        c_sla.font = font_bold
        if float(r_data[4]) < 35.0:
            c_sla.fill = fill_red

        ws_ops.cell(row=r_sla, column=7, value=float(r_data[5])).number_format = "0.0"
        ws_ops.cell(row=r_sla, column=8, value=float(r_data[6])).number_format = "0.0"
        ws_ops.cell(row=r_sla, column=9, value=float(r_data[7])).number_format = "0.00"

        for col_idx in range(2, 10):
            ws_ops.cell(row=r_sla, column=col_idx).border = border_thin
            if r_sla % 2 == 1 and col_idx != 6:
                ws_ops.cell(row=r_sla, column=col_idx).fill = fill_zebra
        r_sla += 1

    # --------------------------------------------------------------------------
    # 5. HOJAS DE DATOS ALIMENTADORES DEL MODELO
    # --------------------------------------------------------------------------
    tablas_data = [
        ("DATA_MODEL_MENSUAL", "kpi_resumen_mensual.csv"),
        ("DATA_CATEGORIAS", "kpi_categorias.csv"),
        ("DATA_SUCURSALES", "kpi_sucursales.csv"),
        ("DATA_CANALES", "kpi_omnicanalidad.csv")
    ]
    for sheet_title, csv_file in tablas_data:
        ws_data = wb.create_sheet(title=sheet_title)
        headers, rows = read_csv_data(csv_file)
        # Encabezado
        for c_idx, h in enumerate(headers, start=1):
            cell = ws_data.cell(row=1, column=c_idx, value=h)
            cell.font = font_header
            cell.fill = fill_navy
            cell.alignment = align_center
            cell.border = border_thin
        # Filas
        for r_idx, row in enumerate(rows, start=2):
            for c_idx, val in enumerate(row, start=1):
                cell = ws_data.cell(row=r_idx, column=c_idx)
                # Intentar convertir numéricos
                try:
                    if "." in val:
                        cell.value = float(val)
                    else:
                        cell.value = int(val)
                except ValueError:
                    cell.value = val
                cell.font = font_regular
                cell.border = border_thin
                if r_idx % 2 == 1:
                    cell.fill = fill_zebra

    # --------------------------------------------------------------------------
    # 6. HOJA DICCIONARIO_DAX
    # --------------------------------------------------------------------------
    ws_dax = wb.create_sheet(title="DICCIONARIO_DAX")
    ws_dax.views.sheetView[0].showGridLines = True

    ws_dax.merge_cells("B2:H3")
    d_hdr = ws_dax["B2"]
    d_hdr.value = "CASA&ESTILO — CATÁLOGO OFICIAL DE MEDIDAS DAX EN POWER PIVOT"
    d_hdr.font = font_title
    d_hdr.fill = fill_navy
    d_hdr.alignment = align_center

    dax_headers = ["ID", "Medida DAX", "Nivel", "Tipo", "Fórmula DAX", "Formato", "Valor Global Registrado"]
    for c_idx, h_name in enumerate(dax_headers, start=2):
        cell = ws_dax.cell(row=5, column=c_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    dax_specs = [
        ("M01", "Ventas Brutas", "Estratégico", "Aditiva", "SUM(FactVentasDetalle[monto_bruto])", "$#,##0.00", "$1,402,502,128.39"),
        ("M02", "Descuentos Totales", "Táctico", "Aditiva", "SUM(FactVentasDetalle[monto_descuento])", "$#,##0.00", "$91,755,708.99"),
        ("M03", "Ventas Netas", "Estratégico", "Aditiva", "[Ventas Brutas] - [Descuentos Totales]", "$#,##0.00", "$1,310,746,491.89"),
        ("M04", "Costo de Ventas (COGS)", "Estratégico", "Aditiva", "SUM(FactVentasDetalle[costo_total])", "$#,##0.00", "$1,029,871,626.89"),
        ("M05", "Utilidad Bruta", "Estratégico", "Aditiva", "[Ventas Netas] - [Costo de Ventas (COGS)]", "$#,##0.00", "$280,874,853.71"),
        ("M06", "Margen Bruto %", "Estratégico", "Ratio", "DIVIDE([Utilidad Bruta], [Ventas Netas], 0)", "0.00%", "21.43%"),
        ("M07", "Ticket Promedio", "Táctico", "Ratio", "DIVIDE([Ventas Netas], DISTINCTCOUNT(FactVentasDetalle[venta_id]), 0)", "$#,##0.00", "$9,362.47"),
        ("M08", "Tasa de Devolución %", "Operacional", "Ratio", "DIVIDE(SUM(FactDevoluciones[importe_devuelto]), [Ventas Brutas], 0)", "0.00%", "1.63%"),
        ("M09", "Cumplimiento SLA %", "Operacional", "Ratio", "DIVIDE(CALCULATE(COUNTROWS(FactInstalaciones), FactInstalaciones[cumplio_sla]=1), COUNTROWS(FactInstalaciones), 0)", "0.00%", "34.77%"),
        ("M10", "Crecimiento YoY %", "Estratégico", "Time Intel", "DIVIDE([Ventas Netas] - CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(DimTiempo[fecha])), CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(DimTiempo[fecha])), 0)", "+0.00%", "+0.85% (2025 vs 2024)")
    ]

    r_dx = 6
    for item in dax_specs:
        ws_dax.cell(row=r_dx, column=2, value=item[0]).alignment = align_center
        ws_dax.cell(row=r_dx, column=3, value=item[1]).font = font_bold
        ws_dax.cell(row=r_dx, column=4, value=item[2]).alignment = align_center
        ws_dax.cell(row=r_dx, column=5, value=item[3]).alignment = align_center
        ws_dax.cell(row=r_dx, column=6, value=item[4]).font = Font(name="Consolas", size=9, color="2C5282")
        ws_dax.cell(row=r_dx, column=7, value=item[5]).alignment = align_center
        ws_dax.cell(row=r_dx, column=8, value=item[6]).font = font_bold
        for c_idx in range(2, 9):
            ws_dax.cell(row=r_dx, column=c_idx).border = border_thin
            if r_dx % 2 == 1:
                ws_dax.cell(row=r_dx, column=c_idx).fill = fill_zebra
        r_dx += 1

    # Ajustar ancho de columnas en todas las hojas
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val = str(cell.value or '')
                if len(val) > max_len and len(val) < 60:
                    max_len = len(val)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # Eliminar hoja default
    wb.remove(default_sheet)

    # Guardar
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    wb.save(OUT_FILE)
    print(f"✅ Libro Excel generado exitosamente: {OUT_FILE}")


if __name__ == "__main__":
    create_workbook()
