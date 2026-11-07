# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) — CASA&ESTILO
# ARCHIVO: generar_dashboard_excel.py
# AUTOR: Equipo 8 — Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Contenedor Docker (python:3.12-slim)
# ==============================================================================
# FUNCIÓN GENERAL:
# Genera el libro de trabajo oficial `PIA_Dashboard_CasaEstilo_Equipo08.xlsx`
# integrando un Tablero de Control Ejecutivo con 7 Gráficos Nativos de Excel
# (Barras, Columnas, Anillos y Líneas de Tendencia), Tablas Oficiales
# ListObjects para Power Pivot, y la memoria técnica de medidas DAX.
# ==============================================================================

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import BarChart, LineChart, DoughnutChart, Reference

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

font_title = Font(name="Calibri", size=16, bold=True, color=C_WHITE)
font_subtitle = Font(name="Calibri", size=10.5, italic=True, color=C_GOLD)
font_section = Font(name="Calibri", size=11.5, bold=True, color=C_NAVY)
font_header = Font(name="Calibri", size=10, bold=True, color=C_WHITE)
font_bold = Font(name="Calibri", size=9.5, bold=True, color=C_SLATE)
font_regular = Font(name="Calibri", size=9, color=C_SLATE)
font_kpi_val = Font(name="Calibri", size=14, bold=True, color=C_NAVY)
font_kpi_lbl = Font(name="Calibri", size=8.5, bold=True, color="718096")

fill_navy = PatternFill(start_color=C_NAVY, end_color=C_NAVY, fill_type="solid")
fill_gold = PatternFill(start_color=C_GOLD, end_color=C_GOLD, fill_type="solid")
fill_card = PatternFill(start_color=C_CARD_BG, end_color=C_CARD_BG, fill_type="solid")
fill_zebra = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")
fill_green = PatternFill(start_color="E6FFFA", end_color="E6FFFA", fill_type="solid")
fill_red = PatternFill(start_color="FFF5F5", end_color="FFF5F5", fill_type="solid")

thin_border_side = Side(style='thin', color="CBD5E0")
border_thin = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

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
    default_sheet = wb.active

    # ==========================================================================
    # 1. HOJA PORTADA
    # ==========================================================================
    ws_portada = wb.create_sheet(title="PORTADA", index=0)
    ws_portada.views.sheetView[0].showGridLines = False

    # Encabezado Institucional
    ws_portada.merge_cells("B2:I3")
    title_cell = ws_portada["B2"]
    title_cell.value = "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN — FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA"
    title_cell.font = font_title
    title_cell.fill = fill_navy
    title_cell.alignment = align_center

    ws_portada.merge_cells("B4:I4")
    sub_cell = ws_portada["B4"]
    sub_cell.value = "Analítica e Inteligencia de Negocios · Producto Integrador de Aprendizaje (PIA) · Enero - Junio 2026"
    sub_cell.font = font_subtitle
    sub_cell.fill = fill_navy
    sub_cell.alignment = align_center

    # Metadatos del Proyecto
    meta = [
        ("Empresa Evaluada:", "Casa&Estilo S.A. de C.V. (Retail Omnicanal de Mobiliario y Decoración)"),
        ("Equipo de Trabajo:", "Equipo 8"),
        ("Integrantes:", "Ángel Butzmann (Líder BI), Analistas de Datos y Modeladores Dimensionales"),
        ("Data Mart Dimensional:", "MySQL 8.0 (ce_bi) — 331,758 transacciones de detalle conciliadas al $0.00"),
        ("Tecnología Tabular:", "Microsoft Power Pivot / VertiPaq & Catálogo de 10 Medidas DAX"),
        ("Fecha de Entrega:", "Noviembre 2026"),
        ("Ponderación Académica:", "30% de la Calificación Final del Curso")
    ]
    r = 6
    for label, val in meta:
        ws_portada.cell(row=r, column=2, value=label).font = font_bold
        ws_portada.cell(row=r, column=4, value=val).font = font_regular
        r += 1

    # Índice de Navegación del Libro
    r += 1
    ws_portada.cell(row=r, column=2, value="MAPA DEL LIBRO Y GUÍA DE NAVEGACIÓN").font = font_section
    r += 1

    menu = [
        ("GUIA_POWERPIVOT", "Instrucciones de activación en 1 clic y defensa del Esquema Estrella ante el profesor"),
        ("DASHBOARD_EJECUTIVO", "Tablero de mando C-Level con Scorecard, Gráfico de Categorías, Anillo Omnicanal y Tendencia 36 Meses"),
        ("ANALISIS_COMERCIAL", "Ranking de 16 Sucursales por Venta Neta ($) y Productividad por metro cuadrado ($/m2)"),
        ("OPERACIONES_Y_CALIDAD", "Diagnóstico de Devoluciones por Causa Raíz y Cumplimiento de SLA Logístico de Instalaciones"),
        ("DICCIONARIO_DAX", "Memoria técnica de las 10 medidas DAX oficiales y formulaciones analíticas"),
        ("FACT_VENTAS_MODELO", "Tabla de hechos de ventas con claves foráneas para Power Pivot (11,086 filas)"),
        ("DIM_PRODUCTO", "Catálogo dimensional de 1,340 productos con costos y precios"),
        ("DIM_SUCURSAL", "Dimensión de las 16 sucursales físicas con superficie en m2 y formatos"),
        ("DIM_CANAL", "Dimensión de canales de venta (Tienda Física, Web, App Móvil)"),
        ("DIM_TIEMPO", "Calendario continuo 2022-2024 (1,096 días)")
    ]
    for pestana, desc in menu:
        c1 = ws_portada.cell(row=r, column=3, value=f"▶ {pestana}")
        c1.font = Font(name="Calibri", size=9.5, bold=True, color=C_ACCENT_BLUE, underline="single")
        ws_portada.cell(row=r, column=5, value=desc).font = font_regular
        r += 1

    # ==========================================================================
    # 2. HOJA GUIA_POWERPIVOT (DEFENSA Y ACTIVACIÓN EN VIVO)
    # ==========================================================================
    ws_guia = wb.create_sheet(title="GUIA_POWERPIVOT")
    ws_guia.views.sheetView[0].showGridLines = False

    ws_guia.merge_cells("B2:J3")
    g_hdr = ws_guia["B2"]
    g_hdr.value = "GUÍA DE DEMOSTRACIÓN Y DEFENSA DE POWER PIVOT ANTE EL PROFESOR"
    g_hdr.font = font_title
    g_hdr.fill = fill_navy
    g_hdr.alignment = align_center

    instrucciones = [
        ("1. ¿QUÉ CONTIENE ESTE LIBRO DE TRABAJO?",
         "Este archivo incluye un Tablero de Control Ejecutivo 100% interactivo con 7 gráficos nativos en las pestañas 'DASHBOARD_EJECUTIVO', 'ANALISIS_COMERCIAL' y 'OPERACIONES_Y_CALIDAD'. Además, todas las hojas de datos están estructuradas como Tablas Oficiales de Excel (ListObjects) listas para integrarse en el Modelo de Datos de Power Pivot."),
        ("2. CÓMO MOSTRAR EL ESQUEMA ESTRELLA EN VIVO (2 MINUTOS)",
         "Paso 1: Ve a la pestaña 'FACT_VENTAS_MODELO', haz clic dentro de la tabla y en la pestaña superior 'Power Pivot', pulsa 'Agregar a modelo de datos'.\n"
         "Paso 2: Repite el mismo paso para 'DIM_PRODUCTO', 'DIM_SUCURSAL', 'DIM_CANAL' y 'DIM_TIEMPO'.\n"
         "Paso 3: En la ventana de Power Pivot, haz clic en 'Vista de diagrama' (Diagram View).\n"
         "Paso 4: Arrastra las llaves con el cursor para unir las tablas:\n"
         "  • sucursal_key de TablaDimSucursal -> sucursal_key de TablaFactVentas\n"
         "  • canal_id de TablaDimCanal -> canal_id de TablaFactVentas\n"
         "  • tiempo_id de TablaDimTiempo -> tiempo_id de TablaFactVentas\n"
         "✔ ¡Excel dibujará de inmediato las líneas de relación 1 a Varios (1:*) del Esquema Estrella!"),
        ("3. CÓMO CREAR UN GRÁFICO DINÁMICO EN 10 SEGUNDOS",
         "En la misma ventana de Power Pivot, en la pestaña Inicio, haz clic en 'Tabla dinámica' -> 'Gráfico dinámico' -> 'Nueva hoja'. Arrastra 'categoria' a Eje y 'monto_neto' a Valores. ¡Listo! Habrás demostrado la conexión directa con el cubo tabular VertiPaq frente al sínodo."),
        ("4. ARGUMENTACIÓN TÉCNICA ANTE EL SÍNODO (RÚBRICA 25%)",
         "'Profesor, nuestro modelo dimensional en estrella conecta la tabla de hechos FactVentas con 4 dimensiones conformes. El cálculo de margen se realiza mediante la medida DAX [Margen Bruto %] = DIVIDE([Utilidad Bruta], [Ventas Netas], 0), evitando promedios simples y garantizando rigor financiero en las 16 sucursales y 3 canales.'")
    ]

    r_g = 5
    for sec_title, sec_desc in instrucciones:
        ws_guia.merge_cells(f"B{r_g}:J{r_g}")
        c_st = ws_guia[f"B{r_g}"]
        c_st.value = sec_title
        c_st.font = font_section
        c_st.fill = fill_card
        r_g += 1

        ws_guia.merge_cells(f"B{r_g}:J{r_g+2}")
        c_sd = ws_guia[f"B{r_g}"]
        c_sd.value = sec_desc
        c_sd.font = font_regular
        c_sd.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        r_g += 4

    # ==========================================================================
    # 3. HOJA DASHBOARD_EJECUTIVO (SCORECARD + 3 GRÁFICOS NATIVOS)
    # ==========================================================================
    ws_dash = wb.create_sheet(title="DASHBOARD_EJECUTIVO")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.merge_cells("B2:P3")
    h_cell = ws_dash["B2"]
    h_cell.value = "CASA&ESTILO — TABLERO DE CONTROL EJECUTIVO Y SCORECARD ESTRATÉGICO"
    h_cell.font = font_title
    h_cell.fill = fill_navy
    h_cell.alignment = align_center

    # Scorecard de KPIs
    kpis = [
        ("VENTAS NETAS", "$1,310,746,491.89", "Ingreso real de caja", C_NAVY, "B", "C"),
        ("UTILIDAD BRUTA", "$280,874,853.71", "Beneficio comercial", C_GREEN, "D", "E"),
        ("MARGEN BRUTO", "21.43%", "Rentabilidad s/venta", C_GOLD, "F", "G"),
        ("TICKET PROMEDIO", "$9,362.47", "Gasto medio cliente", C_SLATE, "H", "I"),
        ("SLA INSTALACIÓN", "34.77%", "Alerta: 65.2% retraso", C_RED, "J", "K")
    ]
    for title, val, note, color, c_start, c_end in kpis:
        ws_dash.merge_cells(f"{c_start}5:{c_end}5")
        cell_t = ws_dash[f"{c_start}5"]
        cell_t.value = title
        cell_t.font = font_kpi_lbl
        cell_t.fill = fill_card
        cell_t.alignment = align_center

        ws_dash.merge_cells(f"{c_start}6:{c_end}6")
        cell_v = ws_dash[f"{c_start}6"]
        cell_v.value = val
        cell_v.font = Font(name="Calibri", size=14, bold=True, color=color)
        cell_v.fill = fill_card
        cell_v.alignment = align_center

        ws_dash.merge_cells(f"{c_start}7:{c_end}7")
        cell_n = ws_dash[f"{c_start}7"]
        cell_n.value = note
        cell_n.font = Font(name="Calibri", size=8, italic=True, color="718096")
        cell_n.fill = fill_card
        cell_n.alignment = align_center

    # 1. Desempeño por Categoría
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
        ws_dash.cell(row=r_cat, column=2, value=r_data[0]).font = font_bold
        ws_dash.cell(row=r_cat, column=3, value=int(r_data[1])).number_format = "#,##0"
        ws_dash.cell(row=r_cat, column=4, value=int(r_data[2])).number_format = "#,##0"
        ws_dash.cell(row=r_cat, column=5, value=float(r_data[4])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_cat, column=6, value=float(r_data[6])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_cat, column=7, value=float(r_data[7])/100.0).number_format = "0.00%"
        ws_dash.cell(row=r_cat, column=8, value=float(r_data[9])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_cat, column=9, value=float(r_data[10])/100.0).number_format = "0.00%"
        for c_idx in range(2, 10):
            ws_dash.cell(row=r_cat, column=c_idx).border = border_thin
            if r_cat % 2 == 1:
                ws_dash.cell(row=r_cat, column=c_idx).fill = fill_zebra
        r_cat += 1

    # Total Categoría
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

    # Gráfico 1: Columnas de Ventas Netas y Utilidad por Categoría
    chart_cat = BarChart()
    chart_cat.type = "col"
    chart_cat.style = 10
    chart_cat.title = "Ventas Netas y Utilidad Bruta por Categoría ($ MXN)"
    chart_cat.y_axis.title = "Monto ($ MXN)"
    chart_cat.x_axis.title = "Categoría"
    data_cat = Reference(ws_dash, min_col=5, min_row=11, max_col=6, max_row=18)
    cats_cat = Reference(ws_dash, min_col=2, min_row=12, max_row=18)
    chart_cat.add_data(data_cat, titles_from_data=True)
    chart_cat.set_categories(cats_cat)
    chart_cat.width = 16
    chart_cat.height = 10
    ws_dash.add_chart(chart_cat, "L9")

    # 2. Desempeño Omnicanal
    r_chan_title = r_cat + 2
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

    # Gráfico 2: Anillo de Participación de Ventas por Canal
    chart_chan = DoughnutChart()
    chart_chan.title = "Participación de Ventas por Canal Comercial"
    chart_chan.style = 2
    data_chan = Reference(ws_dash, min_col=5, min_row=r_chan_title+2, max_row=r_ch-1)
    cats_chan = Reference(ws_dash, min_col=2, min_row=r_chan_title+3, max_row=r_ch-1)
    chart_chan.add_data(data_chan, titles_from_data=True)
    chart_chan.set_categories(cats_chan)
    chart_chan.width = 16
    chart_chan.height = 9.5
    ws_dash.add_chart(chart_chan, "L21")

    # 3. Tendencia Histórica Mensual (2022-2024)
    r_trend_title = r_ch + 2
    ws_dash.cell(row=r_trend_title, column=2, value="3. EVOLUCIÓN HISTÓRICA MENSUAL (36 MESES 2022-2024)").font = font_section

    trend_headers, trend_rows = read_csv_data("kpi_resumen_mensual.csv")
    trend_cols = ["Mes / Año", "Transacciones", "Venta Neta ($ MXN)", "Utilidad Bruta ($ MXN)"]
    for c_idx, h_name in enumerate(trend_cols, start=2):
        cell = ws_dash.cell(row=r_trend_title+2, column=c_idx, value=h_name)
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = align_center
        cell.border = border_thin

    r_tr = r_trend_title + 3
    for r_data in trend_rows:
        ws_dash.cell(row=r_tr, column=2, value=r_data[0]).alignment = align_center
        ws_dash.cell(row=r_tr, column=3, value=int(r_data[1])).number_format = "#,##0"
        ws_dash.cell(row=r_tr, column=4, value=float(r_data[5])).number_format = "$#,##0.00"
        ws_dash.cell(row=r_tr, column=5, value=float(r_data[7])).number_format = "$#,##0.00"
        for c_idx in range(2, 6):
            ws_dash.cell(row=r_tr, column=c_idx).border = border_thin
            ws_dash.cell(row=r_tr, column=c_idx).font = font_regular
            if r_tr % 2 == 1:
                ws_dash.cell(row=r_tr, column=c_idx).fill = fill_zebra
        r_tr += 1

    # Gráfico 3: Línea de Tendencia Mensual de Ventas y Utilidad
    chart_trend = LineChart()
    chart_trend.title = "Evolución Histórica de Ventas Netas y Utilidad Bruta (2022 - 2024)"
    chart_trend.style = 13
    chart_trend.y_axis.title = "Monto ($ MXN)"
    chart_trend.x_axis.title = "Periodo Mensual"
    data_tr = Reference(ws_dash, min_col=4, min_row=r_trend_title+2, max_col=5, max_row=r_tr-1)
    cats_tr = Reference(ws_dash, min_col=2, min_row=r_trend_title+3, max_row=r_tr-1)
    chart_trend.add_data(data_tr, titles_from_data=True)
    chart_trend.set_categories(cats_tr)
    chart_trend.width = 22
    chart_trend.height = 14
    ws_dash.add_chart(chart_trend, "G" + str(r_trend_title+2))

    # ==========================================================================
    # 4. HOJA ANALISIS_COMERCIAL (RANKING SUCURSALES + 2 GRÁFICOS)
    # ==========================================================================
    ws_com = wb.create_sheet(title="ANALISIS_COMERCIAL")
    ws_com.views.sheetView[0].showGridLines = True

    ws_com.merge_cells("B2:U3")
    c_hdr = ws_com["B2"]
    c_hdr.value = "CASA&ESTILO — ANÁLISIS DE PRODUCTIVIDAD Y RENTABILIDAD POR SUCURSAL"
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
        ws_com.cell(row=r_s, column=2, value=r_data[0]).alignment = align_center
        ws_com.cell(row=r_s, column=3, value=r_data[1]).font = font_bold
        ws_com.cell(row=r_s, column=4, value=r_data[2])
        ws_com.cell(row=r_s, column=5, value=r_data[3])
        ws_com.cell(row=r_s, column=6, value=int(r_data[4])).number_format = "#,##0"
        ws_com.cell(row=r_s, column=7, value=r_data[5])
        ws_com.cell(row=r_s, column=8, value=int(r_data[6])).number_format = "#,##0"
        ws_com.cell(row=r_s, column=9, value=float(r_data[7])).number_format = "$#,##0.00"
        ws_com.cell(row=r_s, column=10, value=float(r_data[8])).number_format = "$#,##0.00"
        ws_com.cell(row=r_s, column=11, value=float(r_data[9])).number_format = "$#,##0.00"
        ws_com.cell(row=r_s, column=12, value=float(r_data[10])/100.0).number_format = "0.00%"
        for col_idx in range(2, 13):
            ws_com.cell(row=r_s, column=col_idx).border = border_thin
            ws_com.cell(row=r_s, column=col_idx).font = font_regular
            if r_s % 2 == 1:
                ws_com.cell(row=r_s, column=col_idx).fill = fill_zebra
        r_s += 1

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

    # Gráfico 4: Ranking de Sucursales por Venta Neta (Barras Horizontales)
    chart_suc = BarChart()
    chart_suc.type = "bar"
    chart_suc.style = 10
    chart_suc.title = "Ranking de Sucursales por Venta Neta ($ MXN)"
    chart_suc.x_axis.title = "Venta Neta ($ MXN)"
    chart_suc.y_axis.title = "Sucursal"
    data_suc = Reference(ws_com, min_col=9, min_row=7, max_row=23)
    cats_suc = Reference(ws_com, min_col=3, min_row=8, max_row=23)
    chart_suc.add_data(data_suc, titles_from_data=True)
    chart_suc.set_categories(cats_suc)
    chart_suc.legend = None
    chart_suc.width = 17
    chart_suc.height = 15
    ws_com.add_chart(chart_suc, "N5")

    # Gráfico 5: Productividad Comercial por Metro Cuadrado ($/m2)
    chart_m2 = BarChart()
    chart_m2.type = "col"
    chart_m2.style = 11
    chart_m2.title = "Productividad Comercial por Metro Cuadrado ($ / m²)"
    chart_m2.y_axis.title = "Venta por m² ($ MXN)"
    chart_m2.x_axis.title = "Sucursal"
    data_m2 = Reference(ws_com, min_col=10, min_row=7, max_row=23)
    chart_m2.add_data(data_m2, titles_from_data=True)
    chart_m2.set_categories(cats_suc)
    chart_m2.legend = None
    chart_m2.width = 17
    chart_m2.height = 11
    ws_com.add_chart(chart_m2, "N22")

    # ==========================================================================
    # 5. HOJA OPERACIONES_Y_CALIDAD (DEVOLUCIONES + SLA INSTALACIONES + 2 GRÁFICOS)
    # ==========================================================================
    ws_ops = wb.create_sheet(title="OPERACIONES_Y_CALIDAD")
    ws_ops.views.sheetView[0].showGridLines = True

    ws_ops.merge_cells("B2:R3")
    o_hdr = ws_ops["B2"]
    o_hdr.value = "CASA&ESTILO — CALIDAD, DEVOLUCIONES Y NIVEL DE SERVICIO LOGÍSTICO"
    o_hdr.font = font_title
    o_hdr.fill = fill_navy
    o_hdr.alignment = align_center

    # 1. Motivos de Devolución
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

    # Gráfico 6: Anillo de Motivos de Devolución
    chart_dev = DoughnutChart()
    chart_dev.title = "Distribución del Costo de Devoluciones por Motivo"
    chart_dev.style = 2
    data_dev = Reference(ws_ops, min_col=5, min_row=7, max_row=12)
    cats_dev = Reference(ws_ops, min_col=2, min_row=8, max_row=12)
    chart_dev.add_data(data_dev, titles_from_data=True)
    chart_dev.set_categories(cats_dev)
    chart_dev.width = 15
    chart_dev.height = 9.5
    ws_ops.add_chart(chart_dev, "H5")

    # 2. SLA de Instalaciones
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

    # Gráfico 7: Cumplimiento de SLA por Sucursal
    chart_sla = BarChart()
    chart_sla.type = "col"
    chart_sla.style = 12
    chart_sla.title = "Cumplimiento de SLA de Instalaciones por Sucursal (%)"
    chart_sla.y_axis.title = "% Entregas a Tiempo"
    chart_sla.x_axis.title = "Sucursal"
    data_sla = Reference(ws_ops, min_col=6, min_row=17, max_row=33)
    cats_sla = Reference(ws_ops, min_col=2, min_row=18, max_row=33)
    chart_sla.add_data(data_sla, titles_from_data=True)
    chart_sla.set_categories(cats_sla)
    chart_sla.legend = None
    chart_sla.width = 17
    chart_sla.height = 13
    ws_ops.add_chart(chart_sla, "K16")

    # ==========================================================================
    # 6. HOJAS DIMENSIONALES CON TABLAS OFICIALES ListObjects
    # ==========================================================================
    def add_table_sheet(sheet_title, table_name, csv_filename, style_name="TableStyleMedium9"):
        ws = wb.create_sheet(title=sheet_title)
        headers, rows = read_csv_data(csv_filename)

        for c_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=1, column=c_idx, value=h)
            cell.font = font_header
            cell.fill = fill_navy
            cell.alignment = align_center

        for r_idx, row in enumerate(rows, start=2):
            for c_idx, val in enumerate(row, start=1):
                cell = ws.cell(row=r_idx, column=c_idx)
                try:
                    if "." in val:
                        cell.value = float(val)
                    else:
                        cell.value = int(val)
                except ValueError:
                    cell.value = val
                cell.font = font_regular

        last_col = get_column_letter(len(headers))
        last_row = len(rows) + 1
        tab_range = f"A1:{last_col}{last_row}"

        excel_tab = Table(displayName=table_name, ref=tab_range)
        excel_tab.tableStyleInfo = TableStyleInfo(
            name=style_name,
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )
        ws.add_table(excel_tab)
        return ws

    add_table_sheet("FACT_VENTAS_MODELO", "TablaFactVentas", "fact_ventas_modelo.csv", "TableStyleMedium2")
    add_table_sheet("DIM_PRODUCTO", "TablaDimProducto", "dim_producto.csv", "TableStyleMedium9")
    add_table_sheet("DIM_SUCURSAL", "TablaDimSucursal", "dim_sucursal.csv", "TableStyleMedium9")
    add_table_sheet("DIM_CANAL", "TablaDimCanal", "dim_canal.csv", "TableStyleMedium9")
    add_table_sheet("DIM_TIEMPO", "TablaDimTiempo", "dim_tiempo.csv", "TableStyleMedium9")
    add_table_sheet("FACT_DEVOLUCIONES", "TablaFactDevoluciones", "fact_devoluciones_muestra.csv", "TableStyleMedium2")
    add_table_sheet("FACT_INSTALACIONES", "TablaFactInstalaciones", "fact_instalaciones_completo.csv", "TableStyleMedium2")

    # ==========================================================================
    # 7. HOJA DICCIONARIO_DAX
    # ==========================================================================
    ws_dax = wb.create_sheet(title="DICCIONARIO_DAX")
    ws_dax.views.sheetView[0].showGridLines = True

    ws_dax.merge_cells("B2:H3")
    d_hdr = ws_dax["B2"]
    d_hdr.value = "CASA&ESTILO — CATÁLOGO OFICIAL DE 10 MEDIDAS DAX EN POWER PIVOT"
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
        ("M01", "Ventas Brutas", "Estratégico", "Aditiva", "SUM(TablaFactVentas[monto_bruto])", "$#,##0.00", "$1,402,502,128.39"),
        ("M02", "Descuentos Totales", "Táctico", "Aditiva", "SUM(TablaFactVentas[monto_descuento])", "$#,##0.00", "$91,755,708.99"),
        ("M03", "Ventas Netas", "Estratégico", "Aditiva", "[Ventas Brutas] - [Descuentos Totales]", "$#,##0.00", "$1,310,746,491.89"),
        ("M04", "Costo de Ventas (COGS)", "Estratégico", "Aditiva", "SUM(TablaFactVentas[costo_total])", "$#,##0.00", "$1,029,871,626.89"),
        ("M05", "Utilidad Bruta", "Estratégico", "Aditiva", "[Ventas Netas] - [Costo de Ventas (COGS)]", "$#,##0.00", "$280,874,853.71"),
        ("M06", "Margen Bruto %", "Estratégico", "Ratio", "DIVIDE([Utilidad Bruta], [Ventas Netas], 0)", "0.00%", "21.43%"),
        ("M07", "Ticket Promedio", "Táctico", "Ratio", "DIVIDE([Ventas Netas], SUM(TablaFactVentas[transacciones]), 0)", "$#,##0.00", "$9,362.47"),
        ("M08", "Tasa de Devolución %", "Operacional", "Ratio", "DIVIDE(SUM(TablaFactDevoluciones[importe_devuelto]), [Ventas Brutas], 0)", "0.00%", "1.63%"),
        ("M09", "Cumplimiento SLA %", "Operacional", "Ratio", "DIVIDE(CALCULATE(COUNTROWS(TablaFactInstalaciones), TablaFactInstalaciones[cumplio_sla]=1), COUNTROWS(TablaFactInstalaciones), 0)", "0.00%", "34.77%"),
        ("M10", "Crecimiento YoY %", "Estratégico", "Time Intel", "DIVIDE([Ventas Netas] - CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), 0)", "+0.00%", "+0.85% (2025 vs 2024)")
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

    # Ajustar ancho de columnas
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in list(col)[:50]:
                val = str(cell.value or '')
                if len(val) > max_len and len(val) < 60:
                    max_len = len(val)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

    wb.remove(default_sheet)
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    wb.save(OUT_FILE)
    print(f"✅ Libro Excel generado exitosamente con 7 Gráficos Nativos y Tablas Oficiales: {OUT_FILE}")


if __name__ == "__main__":
    create_workbook()
