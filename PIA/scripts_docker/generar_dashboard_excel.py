# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) — CASA&ESTILO
# ARCHIVO: generar_dashboard_excel.py
# AUTOR: Equipo 8 — Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Contenedor Docker (python:3.12-slim)
# ==============================================================================
# FUNCIÓN GENERAL:
# Genera los libros de trabajo oficiales `PIA_Dashboard_CasaEstilo_Equipo08.xlsx`
# y `PIA_Dashboard_CasaEstilo_Completo_v2.xlsx` con 3 pestañas ejecutivas
# (5 Pilares de Negocio), 11 Gráficos Nativos de Excel, 10 Tablas Oficiales
# `ListObjects` (Esquema Constelación completo sin distorsión temporal ni
# truncamientos) y la memoria técnica de las 21 medidas DAX.
#
# FUNCIÓN ESPECÍFICA:
# Orquesta la lectura nombrada de CSVs (`csv.DictReader`), maqueta tarjetas KPI,
# tablas formateadas, gráficos nativos (`openpyxl.chart`) y hojas dimensionales
# optimizadas para importación inmediata en Microsoft Power Pivot / VertiPaq.
# ==============================================================================

import csv
import os
import re
import shutil
import openpyxl
from openpyxl.chart import BarChart, DoughnutChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

DATA_DIR = "PIA/03_dashboard_excel/datos_exportados"
OUT_FILES = [
    "PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx",
    "PIA/PIA_Dashboard_CasaEstilo_Completo_v2.xlsx",
]
NUMERIC_RE = re.compile(r"^-?\d+(\.\d+)?$")

# Paleta Ejecutiva FIME / Casa&Estilo
C_NAVY = "1A365D"        # Azul Institucional FIME
C_GOLD = "D69E2E"        # Dorado Ejecutivo
C_SLATE = "2D3748"       # Gris Carbón
C_LIGHT_BG = "F7FAFC"    # Fondo suave zebra
C_WHITE = "FFFFFF"       # Blanco puro
C_ACCENT_BLUE = "2B6CB0" # Azul medio
C_GREEN = "2F855A"       # Verde éxito
C_RED = "C53030"         # Rojo alerta
C_CARD_BG = "EDF2F7"     # Fondo tarjetas

FONT_TITLE = Font(name="Calibri", size=15, bold=True, color=C_WHITE)
FONT_SUBTITLE = Font(name="Calibri", size=10.5, italic=True, color=C_GOLD)
FONT_SECTION = Font(name="Calibri", size=11.5, bold=True, color=C_NAVY)
FONT_HEADER = Font(name="Calibri", size=10, bold=True, color=C_WHITE)
FONT_BOLD = Font(name="Calibri", size=9.5, bold=True, color=C_SLATE)
FONT_REGULAR = Font(name="Calibri", size=9, color=C_SLATE)
FONT_KPI_LBL = Font(name="Calibri", size=8.5, bold=True, color="718096")
FONT_KPI_NOTE = Font(name="Calibri", size=8, italic=True, color="718096")
FONT_CODE = Font(name="Consolas", size=9, color="2C5282")

FILL_NAVY = PatternFill(start_color=C_NAVY, end_color=C_NAVY, fill_type="solid")
FILL_GOLD = PatternFill(start_color=C_GOLD, end_color=C_GOLD, fill_type="solid")
FILL_CARD = PatternFill(start_color=C_CARD_BG, end_color=C_CARD_BG, fill_type="solid")
FILL_ZEBRA = PatternFill(start_color=C_LIGHT_BG, end_color=C_LIGHT_BG, fill_type="solid")
FILL_RED = PatternFill(start_color="FFF5F5", end_color="FFF5F5", fill_type="solid")

BORDER_SIDE = Side(style="thin", color="CBD5E0")
BORDER_THIN = Border(left=BORDER_SIDE, right=BORDER_SIDE, top=BORDER_SIDE, bottom=BORDER_SIDE)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_LEFT = Alignment(horizontal="left", vertical="center")


def read_csv_dicts(filename):
    """Lee un archivo CSV UTF-8 usando encabezados por nombre (DictReader)."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_csv_raw(filename):
    """Lee encabezados y filas crudas de un CSV para volcados ListObject de alto volumen."""
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return next(reader), list(reader)


def parse_scalar(val):
    """Convierte strings numéricos exactos a int/float conservando códigos e IDs como texto."""
    if val is None or val == "":
        return val
    if NUMERIC_RE.match(val):
        return float(val) if "." in val else int(val)
    return val


def render_banner(ws, cell_range, title_text):
    """Dibuja el banner corporativo superior en una hoja de dashboard."""
    ws.merge_cells(cell_range)
    top_left = cell_range.split(":")[0]
    cell = ws[top_left]
    cell.value = title_text
    cell.font = FONT_TITLE
    cell.fill = FILL_NAVY
    cell.alignment = ALIGN_CENTER


def render_kpi_cards(ws, row_top, cards):
    """Renderiza una banda de tarjetas KPI con título, valor principal y nota contextual."""
    for title, val, note, color, c_start, c_end in cards:
        ws.merge_cells(f"{c_start}{row_top}:{c_end}{row_top}")
        c_lbl = ws[f"{c_start}{row_top}"]
        c_lbl.value = title
        c_lbl.font = FONT_KPI_LBL
        c_lbl.fill = FILL_CARD
        c_lbl.alignment = ALIGN_CENTER

        ws.merge_cells(f"{c_start}{row_top + 1}:{c_end}{row_top + 1}")
        c_val = ws[f"{c_start}{row_top + 1}"]
        c_val.value = val
        c_val.font = Font(name="Calibri", size=13.5, bold=True, color=color)
        c_val.fill = FILL_CARD
        c_val.alignment = ALIGN_CENTER

        ws.merge_cells(f"{c_start}{row_top + 2}:{c_end}{row_top + 2}")
        c_note = ws[f"{c_start}{row_top + 2}"]
        c_note.value = note
        c_note.font = FONT_KPI_NOTE
        c_note.fill = FILL_CARD
        c_note.alignment = ALIGN_CENTER


def render_table(ws, header_row, start_col, columns_spec, rows_data, total_formulas=None, zebra=True):
    """
    Renderiza encabezados, filas tipadas con formato numérico y fila opcional de totales.
    `columns_spec`: lista de tuplas `(header_title, extractor_fn, num_fmt, is_bold, align_opt)`.
    Retorna `(header_row, first_data_row, last_data_row, total_row)`.
    """
    n_cols = len(columns_spec)
    for offset, (hdr, _, _, _, _) in enumerate(columns_spec):
        cell = ws.cell(row=header_row, column=start_col + offset, value=hdr)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER
        cell.border = BORDER_THIN

    first_row = header_row + 1
    cur_row = first_row
    for item in rows_data:
        for offset, (_, extractor, num_fmt, is_bold, align_opt) in enumerate(columns_spec):
            col_idx = start_col + offset
            cell = ws.cell(row=cur_row, column=col_idx, value=extractor(item))
            if num_fmt:
                cell.number_format = num_fmt
            cell.font = FONT_BOLD if is_bold else FONT_REGULAR
            cell.border = BORDER_THIN
            if align_opt:
                cell.alignment = align_opt
            if zebra and cur_row % 2 == 1:
                cell.fill = FILL_ZEBRA
        cur_row += 1

    last_data_row = cur_row - 1
    total_row = None
    if total_formulas:
        total_row = cur_row
        for offset in range(n_cols):
            col_idx = start_col + offset
            spec = total_formulas.get(offset)
            val = spec[0](first_row, last_data_row, total_row) if (spec and callable(spec[0])) else (spec[0] if spec else None)
            cell = ws.cell(row=total_row, column=col_idx, value=val)
            if spec and spec[1]:
                cell.number_format = spec[1]
            cell.font = FONT_BOLD
            cell.fill = FILL_GOLD
            cell.border = BORDER_THIN
    return header_row, first_row, last_data_row, total_row


def add_bar_chart(ws, anchor, title, x_title, y_title, min_col, max_col, hdr_row, first_row, last_row,
                  cat_col, chart_type="col", grouping=None, style=10, width=16, height=9.5, show_legend=True):
    """Crea y posiciona un BarChart (barras/columnas/apilado) en la hoja indicada."""
    chart = BarChart()
    chart.type = chart_type
    if grouping:
        chart.grouping = grouping
        if grouping == "stacked":
            chart.overlap = 100
    chart.style = style
    chart.title = title
    chart.x_axis.title = x_title
    chart.y_axis.title = y_title
    data = Reference(ws, min_col=min_col, min_row=hdr_row, max_col=max_col, max_row=last_row)
    cats = Reference(ws, min_col=cat_col, min_row=first_row, max_row=last_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    if not show_legend:
        chart.legend = None
    chart.width = width
    chart.height = height
    ws.add_chart(chart, anchor)


def add_doughnut_chart(ws, anchor, title, val_col, hdr_row, first_row, last_row, cat_col,
                       style=2, width=16, height=9):
    """Crea y posiciona un DoughnutChart ejecutivo en la hoja indicada."""
    chart = DoughnutChart()
    chart.title = title
    chart.style = style
    data = Reference(ws, min_col=val_col, min_row=hdr_row, max_row=last_row)
    cats = Reference(ws, min_col=cat_col, min_row=first_row, max_row=last_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width = width
    chart.height = height
    ws.add_chart(chart, anchor)


def add_line_chart(ws, anchor, title, x_title, y_title, min_col, max_col, hdr_row, first_row, last_row,
                   cat_col, style=13, width=22, height=14):
    """Crea y posiciona un LineChart de tendencia temporal en la hoja indicada."""
    chart = LineChart()
    chart.title = title
    chart.style = style
    chart.x_axis.title = x_title
    chart.y_axis.title = y_title
    data = Reference(ws, min_col=min_col, min_row=hdr_row, max_col=max_col, max_row=last_row)
    cats = Reference(ws, min_col=cat_col, min_row=first_row, max_row=last_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.width = width
    chart.height = height
    ws.add_chart(chart, anchor)


def build_portada(wb):
    """Construye la hoja institucional PORTADA con mapa de navegación v2."""
    ws = wb.create_sheet(title="PORTADA", index=0)
    ws.views.sheetView[0].showGridLines = False

    render_banner(ws, "B2:J3", "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN — FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA")
    ws.merge_cells("B4:J4")
    sub = ws["B4"]
    sub.value = "Analítica e Inteligencia de Negocios · Producto Integrador de Aprendizaje (PIA) · Solución Completa v2"
    sub.font = FONT_SUBTITLE
    sub.fill = FILL_NAVY
    sub.alignment = ALIGN_CENTER

    meta = [
        ("Empresa Evaluada:", "Casa&Estilo S.A. de C.V. (Retail Omnicanal de Mobiliario y Decoración)"),
        ("Equipo de Trabajo:", "Equipo 8 — FIME UANL"),
        ("Data Mart Dimensional:", "MySQL 8.0 (ce_bi) — 331,758 líneas de venta detalladas conciliadas al $0.00"),
        ("Arquitectura Analítica:", "Constelación Kimball (4 Tablas de Hechos + 6 Dimensiones Conformes)"),
        ("Catálogo Tabular:", "21 Medidas DAX Oficiales agrupadas en 5 Pilares de Negocio"),
        ("Periodo Cubierto:", "2024-01-01 a 2026-09-30 (33 meses operativos; DimTiempo 2024–2026 completa)"),
        ("Fecha de Entrega:", "Noviembre 2026"),
    ]
    r = 6
    for lbl, val in meta:
        ws.cell(row=r, column=2, value=lbl).font = FONT_BOLD
        ws.cell(row=r, column=4, value=val).font = FONT_REGULAR
        r += 1

    r += 1
    ws.cell(row=r, column=2, value="MAPA DEL LIBRO DE TRABAJO (3 VISTAS EJECUTIVAS + 10 TABLAS POWER PIVOT)").font = FONT_SECTION
    r += 1
    menu = [
        ("GUIA_POWERPIVOT", "Instrucciones paso a paso para modelar las 10 tablas en Power Pivot y crear segmentadores"),
        ("DASHBOARD_EJECUTIVO", "Vista 1 (C-Level): 6 KPIs maestros, Categorías, Omnicanalidad, Métodos de Pago, Anual y Tendencia 33 Meses"),
        ("COMERCIAL_Y_CLIENTES", "Vista 2 (Comercial y CRM): Ranking 16 Sucursales, $/m2, Segmentos CRM, Descuentos y Top 15 SKUs"),
        ("OPERACIONES_Y_STOCK", "Vista 3 (Riesgo Operativo): Devoluciones (9,952), SLA Instalaciones (36.91% / CSAT 2.99) e Inventario ($2,373.7M)"),
        ("DICCIONARIO_DAX", "Memoria técnica copiable con las 21 fórmulas DAX oficiales (M01 a M21)"),
        ("FACT_VENTAS_MODELO", "TablaFactVentas completa (331,758 líneas atómicas, sin distorsión temporal)"),
        ("FACT_DEVOLUCIONES", "TablaFactDevoluciones completa (9,952 devoluciones auditadas)"),
        ("FACT_INSTALACIONES", "TablaFactInstalaciones completa (6,500 órdenes técnicas y SLA)"),
        ("FACT_INVENTARIO", "TablaFactInventario completa (21,440 combinaciones tienda-producto)"),
        ("DIM_PRODUCTO / SUCURSAL / CANAL / TIEMPO / CLIENTE / METODO_PAGO", "Las 6 Dimensiones Conformes completas en ListObject"),
    ]
    for tab, desc in menu:
        c = ws.cell(row=r, column=3, value=f"▶ {tab}")
        c.font = Font(name="Calibri", size=9.5, bold=True, color=C_ACCENT_BLUE, underline="single")
        ws.cell(row=r, column=5, value=desc).font = FONT_REGULAR
        r += 1


def build_guia_powerpivot(wb):
    """Construye la hoja GUIA_POWERPIVOT con instrucciones del modelo Constelación de 10 tablas."""
    ws = wb.create_sheet(title="GUIA_POWERPIVOT")
    ws.views.sheetView[0].showGridLines = False
    render_banner(ws, "B2:J3", "GUÍA DE CONSTRUCCIÓN MANUAL, POWER PIVOT Y DEFENSA ANTE EL PROFESOR")

    sections = [
        ("1. CONTENIDO INTEGRAL DE ESTE LIBRO (SIN TRUNCAMIENTOS NI DISTORSIÓN TEMPORAL)",
         "Este libro contiene 3 pestañas ejecutivas con 11 gráficos nativos y las 10 tablas del Esquema Constelación en formato oficial ListObject:\n"
         "• TablaFactVentas (331,758 filas atómicas con venta_id, tiempo_id, producto_key, cliente_key, sucursal_key, canal_id y metodo_pago_id)\n"
         "• TablaFactDevoluciones (9,952 filas completas), TablaFactInstalaciones (6,500 filas) y TablaFactInventario (21,440 filas)\n"
         "• 6 Dimensiones Conformes: TablaDimTiempo, TablaDimProducto, TablaDimSucursal, TablaDimCanal, TablaDimCliente y TablaDimMetodoPago."),
        ("2. CONEXIONES EN LA VISTA DE DIAGRAMA DE POWER PIVOT (15 RELACIONES 1:N)",
         "Agrega cada ListObject al Modelo (Power Pivot -> Agregar a modelo de datos), abre Vista de Diagrama y arrastra:\n"
         "• A TablaFactVentas: desde DimTiempo[tiempo_id], DimProducto[producto_key], DimSucursal[sucursal_key], DimCanal[canal_id], DimCliente[cliente_key], DimMetodoPago[metodo_pago_id].\n"
         "• A TablaFactDevoluciones: desde DimTiempo[tiempo_id], DimProducto[producto_key], DimSucursal[sucursal_key], DimCliente[cliente_key].\n"
         "• A TablaFactInstalaciones: desde DimTiempo[tiempo_id], DimSucursal[sucursal_key], DimCliente[cliente_key].\n"
         "• A TablaFactInventario: desde DimSucursal[sucursal_key] y DimProducto[producto_key].\n"
         "IMPORTANTE: Marca TablaDimTiempo como Tabla de Fechas (Diseño -> Marcar como tabla de fechas -> fecha) para habilitar [Crecimiento YoY %]."),
        ("3. REGLA DE ORO KIMBALL PARA TABLAS DE HECHOS",
         "Las tablas de hechos (Ventas, Devoluciones, Instalaciones e Inventario) NUNCA se conectan directo entre sí. Se comunican mediante Dimensiones Conformes (Producto, Sucursal, Tiempo, Cliente), evitando conteos duplicados y permitiendo cruzar tasas de devolución, SLA por sucursal y margen bruto en una misma Tabla Dinámica."),
        ("4. CREACIÓN DE SEGMENTADORES SINCRONIZADOS ENTRE LAS 3 PESTAÑAS",
         "1) Crea Tablas Dinámicas desde el Modelo en una hoja auxiliar (AUX_DINAMICAS).\n"
         "2) Inserta Segmentadores (Año, Trimestre, Canal, Ciudad, Categoría, Segmento Cliente).\n"
         "3) Clic derecho en cada segmentador -> 'Conexiones de informes...' -> marca TODAS las Tablas Dinámicas del libro."),
    ]
    r = 5
    for stitle, sdesc in sections:
        ws.merge_cells(f"B{r}:J{r}")
        c_st = ws[f"B{r}"]
        c_st.value = stitle
        c_st.font = FONT_SECTION
        c_st.fill = FILL_CARD
        r += 1
        ws.merge_cells(f"B{r}:J{r+3}")
        c_sd = ws[f"B{r}"]
        c_sd.value = sdesc
        c_sd.font = FONT_REGULAR
        c_sd.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        r += 5


def build_dashboard_ejecutivo(wb):
    """Vista 1: DASHBOARD_EJECUTIVO con 6 tarjetas C-Level, 5 tablas y 4 gráficos nativos."""
    ws = wb.create_sheet(title="DASHBOARD_EJECUTIVO")
    render_banner(ws, "B2:S3", "CASA&ESTILO — VISTA 1: TABLERO DE CONTROL EJECUTIVO (VISIÓN C-LEVEL)")

    kpis = [
        ("VENTAS NETAS", "$1,310,746,491.89", "Brutas $1,402.50M | 140k tickets", C_NAVY, "B", "D"),
        ("UTILIDAD BRUTA", "$280,874,853.71", "Beneficio comercial real", C_GREEN, "E", "G"),
        ("MARGEN BRUTO %", "21.43%", "COGS: $1,029.87M (78.57%)", C_GOLD, "H", "J"),
        ("CRECIMIENTO YoY", "+0.86%", "2025 $479.8M vs 2024 $475.7M", C_ACCENT_BLUE, "K", "M"),
        ("TICKET PROMEDIO", "$9,362.47", "UPT: 5.94 piezas/ticket", C_SLATE, "N", "P"),
        ("SLA INSTALACIÓN", "36.91%", "Alerta: 63.1% retraso | CSAT 2.99", C_RED, "Q", "S"),
    ]
    render_kpi_cards(ws, 5, kpis)

    # 1. Desempeño por Categoría
    ws.cell(row=9, column=2, value="1. DESEMPEÑO COMERCIAL POR CATEGORÍA DE PRODUCTO").font = font_section_ref()
    cats = read_csv_dicts("kpi_categorias.csv")
    cat_cols = [
        ("Categoría", lambda r: r["categoria"], None, True, ALIGN_LEFT),
        ("SKUs", lambda r: int(r["skus_activos"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades_vendidas"]), "#,##0", False, None),
        ("Venta Neta ($ MXN)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Utilidad ($ MXN)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
        ("Devoluciones ($)", lambda r: float(r["monto_devuelto"]), "$#,##0.00", False, None),
        ("Tasa Dev %", lambda r: float(r["tasa_devolucion_pct"]) / 100.0, "0.00%", False, None),
    ]
    cat_totals = {
        0: ("TOTAL GENERAL", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "$#,##0.00"),
        5: (lambda f, l, t: f"=F{t}/E{t}", "0.00%"),
        6: (lambda f, l, _: f"=SUM(H{f}:H{l})", "$#,##0.00"),
        7: (lambda f, l, t: f"=H{t}/E{t}", "0.00%"),
    }
    hdr_c, f_c, l_c, tot_c = render_table(ws, 11, 2, cat_cols, cats, cat_totals)
    add_bar_chart(ws, "L9", "Ventas Netas y Utilidad Bruta por Categoría ($ MXN)", "Categoría", "Monto ($ MXN)",
                  5, 6, hdr_c, f_c, l_c, 2, width=16, height=9.5)

    # 2. Omnicanalidad
    r_om = tot_c + 2
    ws.cell(row=r_om, column=2, value="2. DESEMPEÑO OMNICANAL (TIENDA VS WEB VS APP)").font = FONT_SECTION
    chans = read_csv_dicts("kpi_omnicanalidad.csv")
    chan_cols = [
        ("Canal Comercial", lambda r: r["canal"], None, True, ALIGN_LEFT),
        ("Transacciones", lambda r: int(r["transacciones"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades_vendidas"]), "#,##0", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Ticket Promedio", lambda r: float(r["ticket_promedio"]), "$#,##0.00", False, None),
        ("Utilidad ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
    ]
    chan_totals = {
        0: ("TOTAL OMNICANAL", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, t: f"=E{t}/C{t}", "$#,##0.00"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "$#,##0.00"),
        6: (lambda f, l, t: f"=G{t}/E{t}", "0.00%"),
    }
    hdr_ch, f_ch, l_ch, tot_ch = render_table(ws, r_om + 2, 2, chan_cols, chans, chan_totals, zebra=False)
    add_doughnut_chart(ws, "L21", "Participación de Ventas por Canal Comercial", 5, hdr_ch, f_ch, l_ch, 2, height=8.5)

    # 3. Mix de Métodos de Pago
    r_mp = tot_ch + 2
    ws.cell(row=r_mp, column=2, value="3. MIX DE MÉTODOS DE PAGO (DIM_METODO_PAGO)").font = FONT_SECTION
    m_pagos = read_csv_dicts("kpi_metodos_pago.csv")
    mp_cols = [
        ("Método de Pago", lambda r: r["metodo_nombre"], None, True, ALIGN_LEFT),
        ("Tickets", lambda r: int(r["tickets"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades"]), "#,##0", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Ticket Promedio", lambda r: float(r["ticket_promedio"]), "$#,##0.00", False, None),
        ("Utilidad ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
    ]
    mp_totals = {
        0: ("TOTAL MÉTODOS PAGO", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, t: f"=E{t}/C{t}", "$#,##0.00"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "$#,##0.00"),
    }
    hdr_mp, f_mp, l_mp, tot_mp = render_table(ws, r_mp + 2, 2, mp_cols, m_pagos, mp_totals)
    add_doughnut_chart(ws, "L32", "Distribución de Ventas por Método de Pago", 5, hdr_mp, f_mp, l_mp, 2, style=4, height=8.5)

    # 4. Comparativo Anual 2024–2026
    r_yr = tot_mp + 2
    ws.cell(row=r_yr, column=2, value="4. DESEMPEÑO ANUAL COMPARATIVO (2024 – 2026 ENE-SEP)").font = FONT_SECTION
    anual = read_csv_dicts("kpi_resumen_anual.csv")
    yr_cols = [
        ("Año", lambda r: int(r["anio"]), "0", True, ALIGN_CENTER),
        ("Tickets", lambda r: int(r["transacciones"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades_vendidas"]), "#,##0", False, None),
        ("Venta Bruta ($)", lambda r: float(r["venta_bruta"]), "$#,##0.00", False, None),
        ("Descuentos ($)", lambda r: float(r["descuentos_otorgados"]), "$#,##0.00", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Utilidad Bruta ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_bruto_pct"]) / 100.0, "0.00%", False, None),
    ]
    yr_totals = {
        0: ("TOTAL HISTÓRICO", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "$#,##0.00"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "$#,##0.00"),
        6: (lambda f, l, _: f"=SUM(H{f}:H{l})", "$#,##0.00"),
        7: (lambda f, l, t: f"=H{t}/G{t}", "0.00%"),
    }
    _, _, _, tot_yr = render_table(ws, r_yr + 2, 2, yr_cols, anual, yr_totals)

    # 5. Evolución Mensual Exacta (33 Meses: 2024-01 a 2026-09)
    r_tr = tot_yr + 2
    ws.cell(row=r_tr, column=2, value="5. EVOLUCIÓN HISTÓRICA MENSUAL (33 MESES: ENE 2024 – SEP 2026)").font = FONT_SECTION
    mensual = read_csv_dicts("kpi_resumen_mensual.csv")
    tr_cols = [
        ("Periodo (Año-Mes)", lambda r: r["mes_anio"], None, True, ALIGN_CENTER),
        ("Tickets", lambda r: int(r["transacciones"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades_vendidas"]), "#,##0", False, None),
        ("Venta Neta ($ MXN)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Utilidad Bruta ($ MXN)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_bruto_pct"]) / 100.0, "0.00%", False, None),
    ]
    hdr_tr, f_tr, l_tr, _ = render_table(ws, r_tr + 2, 2, tr_cols, mensual, total_formulas=None)
    add_line_chart(ws, f"I{r_tr + 2}", "Evolución Mensual de Ventas Netas y Utilidad Bruta (2024 – 2026)",
                   "Periodo Mensual", "Monto ($ MXN)", 5, 6, hdr_tr, f_tr, l_tr, 2)


def build_comercial_clientes(wb):
    """Vista 2: COMERCIAL_Y_CLIENTES con 6 tarjetas comerciales, 4 tablas y 4 gráficos."""
    ws = wb.create_sheet(title="COMERCIAL_Y_CLIENTES")
    render_banner(ws, "B2:S3", "CASA&ESTILO — VISTA 2: PRODUCTIVIDAD DE SUCURSALES, SEGMENTACIÓN CRM Y TOP SKUs")

    kpis = [
        ("TOTAL TICKETS", "140,000", "331,758 líneas de venta", C_NAVY, "B", "D"),
        ("UNIDADES VENDIDAS", "831,382", "Piezas de catálogo vendidas", C_ACCENT_BLUE, "E", "G"),
        ("UNIDADES / TICKET (UPT)", "5.94", "Promedio artículos/ticket", C_GOLD, "H", "J"),
        ("CLIENTES ACTIVOS CRM", "10,800", "4,870 Frecuentes | 1,214 Premium", C_GREEN, "K", "M"),
        ("VENTA / M² GLOBAL", "$58,226.93", "22,511 m² en 16 sucursales", C_SLATE, "N", "P"),
        ("TASA DESCUENTO %", "6.54%", "$91,755,708.99 promocionados", C_RED, "Q", "S"),
    ]
    render_kpi_cards(ws, 5, kpis)

    # 1. Ranking 16 Sucursales
    ws.cell(row=9, column=2, value="1. RANKING Y PRODUCTIVIDAD POR SUCURSAL FÍSICA (16 TIENDAS)").font = FONT_SECTION
    sucs = read_csv_dicts("kpi_sucursales.csv")
    suc_cols = [
        ("ID", lambda r: r["sucursal_id"], None, False, ALIGN_CENTER),
        ("Sucursal", lambda r: r["sucursal"], None, True, ALIGN_LEFT),
        ("Ciudad", lambda r: r["ciudad"], None, False, None),
        ("Estado", lambda r: r["estado"], None, False, None),
        ("Superficie (m²)", lambda r: int(r["m2"]), "#,##0", False, None),
        ("Formato", lambda r: r["categoria_tamano"], None, False, None),
        ("Tickets", lambda r: int(r["transacciones"]), "#,##0", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Venta / m² ($)", lambda r: float(r["venta_por_m2"]), "$#,##0.00", False, None),
        ("Utilidad ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
    ]
    suc_totals = {
        0: ("TOTAL", None),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "#,##0"),
        6: (lambda f, l, _: f"=SUM(H{f}:H{l})", "#,##0"),
        7: (lambda f, l, _: f"=SUM(I{f}:I{l})", "$#,##0.00"),
        8: (lambda f, l, t: f"=I{t}/F{t}", "$#,##0.00"),
        9: (lambda f, l, _: f"=SUM(K{f}:K{l})", "$#,##0.00"),
        10: (lambda f, l, t: f"=K{t}/I{t}", "0.00%"),
    }
    hdr_s, f_s, l_s, tot_s = render_table(ws, 11, 2, suc_cols, sucs, suc_totals)
    add_bar_chart(ws, "N9", "Ranking de Sucursales por Venta Neta ($ MXN)", "Venta Neta ($ MXN)", "Sucursal",
                  9, 9, hdr_s, f_s, l_s, 3, chart_type="bar", style=10, width=17, height=11, show_legend=False)
    add_bar_chart(ws, "N32", "Productividad Comercial por Metro Cuadrado ($ / m²)", "Sucursal", "Venta por m² ($ MXN)",
                  10, 10, hdr_s, f_s, l_s, 3, chart_type="col", style=11, width=17, height=10, show_legend=False)

    # 2. Segmentación CRM
    r_seg = tot_s + 2
    ws.cell(row=r_seg, column=2, value="2. DESEMPEÑO POR SEGMENTO DE CLIENTE (CRM — DIM_CLIENTE)").font = FONT_SECTION
    segs = read_csv_dicts("kpi_clientes_segmentos.csv")
    seg_cols = [
        ("Segmento CRM", lambda r: r["segmento"], None, True, ALIGN_LEFT),
        ("Clientes Únicos", lambda r: int(r["clientes"]), "#,##0", False, None),
        ("Tickets", lambda r: int(r["tickets"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades"]), "#,##0", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Descuentos ($)", lambda r: float(r["descuentos_mxn"]), "$#,##0.00", False, None),
        ("Utilidad ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
    ]
    seg_totals = {
        0: ("TOTAL CRM", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "#,##0"),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "$#,##0.00"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "$#,##0.00"),
        6: (lambda f, l, _: f"=SUM(H{f}:H{l})", "$#,##0.00"),
        7: (lambda f, l, t: f"=H{t}/F{t}", "0.00%"),
    }
    hdr_sg, f_sg, l_sg, tot_sg = render_table(ws, r_seg + 2, 2, seg_cols, segs, seg_totals)
    add_bar_chart(ws, "N53", "Ventas Netas por Segmento CRM ($ MXN)", "Segmento", "Venta Neta ($ MXN)",
                  6, 6, hdr_sg, f_sg, l_sg, 2, chart_type="col", style=10, width=17, height=9.5, show_legend=False)

    # 3. Impacto de Descuentos vs Margen por Categoría
    r_dsc = tot_sg + 2
    ws.cell(row=r_dsc, column=2, value="3. MATRIZ DE TASA DE DESCUENTO % VS MARGEN BRUTO % POR CATEGORÍA").font = FONT_SECTION
    descs = read_csv_dicts("kpi_descuentos_categorias.csv")
    dsc_cols = [
        ("Categoría", lambda r: r["categoria"], None, True, ALIGN_LEFT),
        ("Unidades", lambda r: int(r["unidades"]), "#,##0", False, None),
        ("Venta Bruta ($)", lambda r: float(r["venta_bruta"]), "$#,##0.00", False, None),
        ("Descuentos ($)", lambda r: float(r["descuentos_mxn"]), "$#,##0.00", False, None),
        ("Tasa Desc %", lambda r: float(r["tasa_descuento_pct"]) / 100.0, "0.00%", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Margen Bruto %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
    ]
    dsc_totals = {
        0: ("TOTAL GENERAL", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "$#,##0.00"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, t: f"=E{t}/D{t}", "0.00%"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "$#,##0.00"),
    }
    hdr_ds, f_ds, l_ds, tot_ds = render_table(ws, r_dsc + 2, 2, dsc_cols, descs, dsc_totals)
    add_bar_chart(ws, "N73", "Comparativo Descuento Otorgado ($) vs Categoría", "Categoría", "Descuento ($ MXN)",
                  5, 5, hdr_ds, f_ds, l_ds, 2, chart_type="col", style=12, width=17, height=9.5, show_legend=False)

    # 4. Top 15 Productos por Venta Neta
    r_top = tot_ds + 2
    ws.cell(row=r_top, column=2, value="4. TOP 15 PRODUCTOS LÍDERES POR INGRESO NETO Y MARGEN").font = FONT_SECTION
    tops = read_csv_dicts("kpi_productos_top.csv")
    top_cols = [
        ("Producto ID", lambda r: r["producto_id"], None, False, ALIGN_CENTER),
        ("SKU", lambda r: r["sku"], None, False, ALIGN_CENTER),
        ("Nombre Producto", lambda r: r["producto"], None, True, ALIGN_LEFT),
        ("Categoría", lambda r: r["categoria"], None, False, None),
        ("Marca", lambda r: r["marca"], None, False, None),
        ("Req. Inst.", lambda r: r["requiere_instalacion"], None, False, ALIGN_CENTER),
        ("Tickets", lambda r: int(r["tickets"]), "#,##0", False, None),
        ("Unidades", lambda r: int(r["unidades"]), "#,##0", False, None),
        ("Venta Neta ($)", lambda r: float(r["venta_neta"]), "$#,##0.00", False, None),
        ("Utilidad ($)", lambda r: float(r["utilidad_bruta"]), "$#,##0.00", False, None),
        ("Margen %", lambda r: float(r["margen_pct"]) / 100.0, "0.00%", False, None),
    ]
    render_table(ws, r_top + 2, 2, top_cols, tops, total_formulas=None)


def build_operaciones_stock(wb):
    """Vista 3: OPERACIONES_Y_STOCK con 6 tarjetas operacionales, 4 tablas y 3 gráficos."""
    ws = wb.create_sheet(title="OPERACIONES_Y_STOCK")
    render_banner(ws, "B2:S3", "CASA&ESTILO — VISTA 3: CALIDAD, DEVOLUCIONES, SLA LOGÍSTICO Y SALUD DE INVENTARIOS")

    kpis = [
        ("MONTO DEVUELTO", "$22,897,836.87", "9,952 eventos | 13,712 piezas", C_RED, "B", "D"),
        ("TASA DEVOLUCIÓN %", "1.63%", "Respecto a Venta Bruta", C_GOLD, "E", "G"),
        ("CUMPLIMIENTO SLA %", "36.91%", "2,399 a tiempo de 6,500", C_RED, "H", "J"),
        ("RETRASO PROMEDIO", "+3.41 días", "10.93 reales vs 7.52 pactados", C_RED, "K", "M"),
        ("SATISFACCIÓN CSAT", "2.99 / 5.0", "Mínimo: Apodaca 2 (2.86)", C_GOLD, "N", "P"),
        ("INVENTARIO (COSTO)", "$2,373.72M", "126 roturas | 2,566 alertas", C_NAVY, "Q", "S"),
    ]
    render_kpi_cards(ws, 5, kpis)

    # 1. Motivos de Devolución (9,952 eventos completos)
    ws.cell(row=9, column=2, value="1. ANÁLISIS DE CAUSA RAÍZ DE DEVOLUCIONES (9,952 EVENTOS COMPLETOS)").font = FONT_SECTION
    devs = read_csv_dicts("kpi_devoluciones_motivos.csv")
    dev_total_row = 12 + len(devs)
    dev_cols = [
        ("Motivo de Devolución", lambda r: r["motivo"], None, True, ALIGN_LEFT),
        ("Eventos", lambda r: int(r["eventos"]), "#,##0", False, None),
        ("Piezas Devueltas", lambda r: int(r["piezas"]), "#,##0", False, None),
        ("Importe Reembolsado ($)", lambda r: float(r["total_reembolsado"]), "$#,##0.00", False, None),
        ("Participación %", lambda _: None, "0.00%", False, None),
    ]
    dev_totals = {
        0: ("TOTAL DEVOLUCIONES", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "$#,##0.00"),
        4: (lambda f, l, t: f"=E{t}/E{t}", "0.00%"),
    }
    hdr_d, f_d, l_d, tot_d = render_table(ws, 11, 2, dev_cols, devs, dev_totals, zebra=False)
    for row_idx in range(f_d, l_d + 1):
        ws.cell(row=row_idx, column=6, value=f"=E{row_idx}/E{dev_total_row}")
    add_doughnut_chart(ws, "H9", "Distribución del Costo de Devoluciones por Motivo", 5, hdr_d, f_d, l_d, 2, width=15, height=9)

    # 2. SLA Instalaciones por Sucursal
    r_sla_sec = tot_d + 2
    ws.cell(row=r_sla_sec, column=2, value="2. DESEMPEÑO LOGÍSTICO Y SLA DE INSTALACIONES POR SUCURSAL (6,500 SERVICIOS)").font = FONT_SECTION
    slas = read_csv_dicts("kpi_instalaciones_sla.csv")
    sla_cols = [
        ("Sucursal", lambda r: r["sucursal"], None, True, ALIGN_LEFT),
        ("Servicios Totales", lambda r: int(r["total_servicios"]), "#,##0", False, None),
        ("A Tiempo", lambda r: int(r["servicios_a_tiempo"]), "#,##0", False, None),
        ("Con Retraso", lambda r: int(r["servicios_con_retraso"]), "#,##0", False, None),
        ("Cumplimiento SLA %", lambda r: float(r["cumplimiento_sla_pct"]) / 100.0, "0.00%", True, None),
        ("Días Reales", lambda r: float(r["dias_reales_promedio"]), "0.00", False, None),
        ("Días Retraso", lambda r: float(r["dias_retraso_promedio"]), "+0.00", False, None),
        ("CSAT (1-5)", lambda r: float(r["satisfaccion_promedio"]), "0.00", False, None),
    ]
    sla_totals = {
        0: ("GLOBAL CASA&ESTILO", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "#,##0"),
        4: (lambda f, l, t: f"=D{t}/C{t}", "0.00%"),
        5: (lambda f, l, _: f"=AVERAGE(G{f}:G{l})", "0.00"),
        6: (lambda f, l, _: f"=AVERAGE(H{f}:H{l})", "+0.00"),
        7: (lambda f, l, _: f"=AVERAGE(I{f}:I{l})", "0.00"),
    }
    hdr_sl, f_sl, l_sl, tot_sl = render_table(ws, r_sla_sec + 2, 2, sla_cols, slas, sla_totals)
    for r_idx in range(f_sl, l_sl + 1):
        c_val = ws.cell(row=r_idx, column=6)
        if float(c_val.value) < 0.35:
            c_val.fill = FILL_RED
    add_bar_chart(ws, f"K{r_sla_sec}", "Cumplimiento SLA de Instalaciones por Sucursal (%)", "Sucursal",
                  "% Entregas a Tiempo", 6, 6, hdr_sl, f_sl, l_sl, 2, style=12, width=17, height=11, show_legend=False)

    # 3. Resumen Global de Inventario
    r_inv_sec = tot_sl + 2
    ws.cell(row=r_inv_sec, column=2, value="3. ESTATUS GLOBAL DE SALUD DE INVENTARIO (21,440 PUNTOS TIENDA-SKU)").font = FONT_SECTION
    inv_res = read_csv_dicts("kpi_inventario_resumen.csv")
    inv_res_cols = [
        ("Estatus Stock", lambda r: r["estatus_stock"], None, True, ALIGN_LEFT),
        ("Ítems Tienda-SKU", lambda r: int(r["items"]), "#,##0", False, None),
        ("Piezas en Stock", lambda r: int(r["piezas_stock"]), "#,##0", False, None),
        ("Déficit vs Reorden", lambda r: int(r["deficit_piezas"]), "#,##0", False, None),
        ("Valor al Costo ($ MXN)", lambda r: float(r["valor_inventario"]), "$#,##0.00", False, None),
    ]
    inv_res_totals = {
        0: ("TOTAL INVENTARIO", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "#,##0"),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "$#,##0.00"),
    }
    _, _, _, tot_ir = render_table(ws, r_inv_sec + 2, 2, inv_res_cols, inv_res, inv_res_totals)

    # 4. Salud de Inventario por Categoría
    r_icat = tot_ir + 2
    ws.cell(row=r_icat, column=2, value="4. RIESGO DE ABASTO Y CAPITAL INMOVILIZADO POR CATEGORÍA").font = FONT_SECTION
    inv_cats = read_csv_dicts("kpi_inventario_categorias.csv")
    icat_cols = [
        ("Categoría", lambda r: r["categoria"], None, True, ALIGN_LEFT),
        ("Puntos Tienda-SKU", lambda r: int(r["skus_sucursal"]), "#,##0", False, None),
        ("SKUs Distintos", lambda r: int(r["skus"]), "#,##0", False, None),
        ("Stock Actual", lambda r: int(r["stock_actual"]), "#,##0", False, None),
        ("Déficit (pzas)", lambda r: int(r["deficit_unidades"]), "#,##0", False, None),
        ("Rotura Stock", lambda r: int(r["roturas"]), "#,##0", True, None),
        ("Alerta Reorden", lambda r: int(r["alertas"]), "#,##0", False, None),
        ("Valor Costo ($ MXN)", lambda r: float(r["valor_costo"]), "$#,##0.00", False, None),
    ]
    icat_totals = {
        0: ("TOTAL RED", None),
        1: (lambda f, l, _: f"=SUM(C{f}:C{l})", "#,##0"),
        2: (lambda f, l, _: f"=SUM(D{f}:D{l})", "#,##0"),
        3: (lambda f, l, _: f"=SUM(E{f}:E{l})", "#,##0"),
        4: (lambda f, l, _: f"=SUM(F{f}:F{l})", "#,##0"),
        5: (lambda f, l, _: f"=SUM(G{f}:G{l})", "#,##0"),
        6: (lambda f, l, _: f"=SUM(H{f}:H{l})", "#,##0"),
        7: (lambda f, l, _: f"=SUM(I{f}:I{l})", "$#,##0.00"),
    }
    hdr_ic, f_ic, l_ic, _ = render_table(ws, r_icat + 2, 2, icat_cols, inv_cats, icat_totals)
    add_bar_chart(ws, f"K{r_inv_sec + 2}", "Incidencias Críticas de Stock por Categoría (Roturas + Alertas)",
                  "Categoría", "Ítems en Riesgo", 7, 8, hdr_ic, f_ic, l_ic, 2,
                  chart_type="col", grouping="stacked", style=10, width=17, height=11)


def add_table_sheet(wb, sheet_title, table_name, csv_filename, style_name="TableStyleMedium9"):
    """Escribe un CSV completo en una hoja con formato oficial ListObject optimizada para volumen."""
    ws = wb.create_sheet(title=sheet_title)
    headers, rows = read_csv_raw(csv_filename)

    for c_idx, hdr in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=c_idx, value=hdr)
        cell.font = FONT_HEADER
        cell.fill = FILL_NAVY
        cell.alignment = ALIGN_CENTER

    # Para tablas grandes (>3,000 filas) omitimos estilo Font por celda para evitar inflado XML
    apply_row_font = len(rows) <= 3000
    for r_idx, row in enumerate(rows, start=2):
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=parse_scalar(val))
            if apply_row_font:
                cell.font = FONT_REGULAR

    last_col = get_column_letter(len(headers))
    last_row = len(rows) + 1
    excel_tab = Table(displayName=table_name, ref=f"A1:{last_col}{last_row}")
    excel_tab.tableStyleInfo = TableStyleInfo(
        name=style_name, showFirstColumn=False, showLastColumn=False,
        showRowStripes=True, showColumnStripes=False
    )
    ws.add_table(excel_tab)
    return ws, len(rows)


def build_diccionario_dax(wb):
    """Construye DICCIONARIO_DAX con el catálogo completo de 21 medidas oficiales."""
    ws = wb.create_sheet(title="DICCIONARIO_DAX")
    render_banner(ws, "B2:I3", "CASA&ESTILO — CATÁLOGO OFICIAL DE 21 MEDIDAS DAX EN POWER PIVOT (5 PILARES)")

    dax_specs = [
        ("M01", "Ventas Brutas", "Financiero", "Estratégico", "Aditiva", "SUM(TablaFactVentas[monto_bruto])", "$#,##0.00", "$1,402,502,128.39"),
        ("M02", "Descuentos Totales", "Financiero", "Táctico", "Aditiva", "SUM(TablaFactVentas[monto_descuento])", "$#,##0.00", "$91,755,708.99"),
        ("M03", "Ventas Netas", "Financiero", "Estratégico", "Derivada", "[Ventas Brutas] - [Descuentos Totales]", "$#,##0.00", "$1,310,746,491.89"),
        ("M04", "Costo de Ventas (COGS)", "Financiero", "Estratégico", "Aditiva", "SUM(TablaFactVentas[costo_total])", "$#,##0.00", "$1,029,871,626.89"),
        ("M05", "Utilidad Bruta", "Financiero", "Estratégico", "Derivada", "[Ventas Netas] - [Costo de Ventas (COGS)]", "$#,##0.00", "$280,874,853.71"),
        ("M06", "Margen Bruto %", "Financiero", "Estratégico", "Ratio", "DIVIDE([Utilidad Bruta], [Ventas Netas], 0)", "0.00%", "21.43%"),
        ("M07", "Tasa de Descuento %", "Financiero", "Táctico", "Ratio", "DIVIDE([Descuentos Totales], [Ventas Brutas], 0)", "0.00%", "6.54%"),
        ("M08", "Crecimiento YoY %", "Financiero", "Estratégico", "Time Intel", "DIVIDE([Ventas Netas] - CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), CALCULATE([Ventas Netas], SAMEPERIODLASTYEAR(TablaDimTiempo[fecha])), 0)", "+0.00%;-0.00%;0.00%", "+0.86% (2025 vs 2024)"),
        ("M09", "Total Tickets", "Comercial", "Táctico", "Distinct", "DISTINCTCOUNT(TablaFactVentas[venta_id])", "#,##0", "140,000"),
        ("M10", "Unidades Vendidas", "Comercial", "Táctico", "Aditiva", "SUM(TablaFactVentas[cantidad])", "#,##0", "831,382"),
        ("M11", "Ticket Promedio", "Comercial", "Táctico", "Ratio", "DIVIDE([Ventas Netas], [Total Tickets], 0)", "$#,##0.00", "$9,362.47"),
        ("M12", "Unidades por Ticket (UPT)", "Comercial", "Táctico", "Ratio", "DIVIDE([Unidades Vendidas], [Total Tickets], 0)", "0.00", "5.94"),
        ("M13", "Venta por m2", "Comercial", "Táctico", "Ratio", "DIVIDE([Ventas Netas], SUM(TablaDimSucursal[m2]), 0)", "$#,##0.00", "$58,226.93 / m²"),
        ("M14", "Clientes Activos", "Comercial", "Táctico", "Distinct", "DISTINCTCOUNT(TablaFactVentas[cliente_key])", "#,##0", "10,800"),
        ("M15", "Monto Devuelto", "Calidad", "Operacional", "Aditiva", "SUM(TablaFactDevoluciones[importe_devuelto])", "$#,##0.00", "$22,897,836.87"),
        ("M16", "Tasa de Devolucion %", "Calidad", "Operacional", "Ratio", "DIVIDE([Monto Devuelto], [Ventas Brutas], 0)", "0.00%", "1.63%"),
        ("M17", "Cumplimiento SLA %", "Logística", "Operacional", "Ratio", "DIVIDE(CALCULATE(COUNTROWS(TablaFactInstalaciones), TablaFactInstalaciones[cumplio_sla]=1), COUNTROWS(TablaFactInstalaciones), 0)", "0.00%", "36.91% (2,399 / 6,500)"),
        ("M18", "Dias Promedio Retraso", "Logística", "Operacional", "Promedio", "AVERAGE(TablaFactInstalaciones[dias_desviacion])", "+0.00;-0.00;0.00", "+3.41 días"),
        ("M19", "Satisfaccion CSAT", "Logística", "Operacional", "Promedio", "AVERAGE(TablaFactInstalaciones[satisfaccion])", "0.00", "2.99 / 5.0"),
        ("M20", "Valor Inventario (Costo)", "Inventario", "Operacional", "Snapshot", "SUM(TablaFactInventario[valor_inventario_costo])", "$#,##0.00", "$2,373,716,477.50"),
        ("M21", "SKUs en Rotura Stock", "Inventario", "Operacional", "Conteo", "CALCULATE(COUNTROWS(TablaFactInventario), TablaFactInventario[estatus_stock]=\"Rotura Stock\")", "#,##0", "126 combinaciones (2,738 u.)"),
    ]
    cols = [
        ("ID", lambda item: item[0], None, True, ALIGN_CENTER),
        ("Medida DAX", lambda item: item[1], None, True, ALIGN_LEFT),
        ("Pilar", lambda item: item[2], None, False, ALIGN_CENTER),
        ("Nivel", lambda item: item[3], None, False, ALIGN_CENTER),
        ("Tipo", lambda item: item[4], None, False, ALIGN_CENTER),
        ("Fórmula DAX Oficial", lambda item: item[5], None, False, ALIGN_LEFT),
        ("Formato", lambda item: item[6], None, False, ALIGN_CENTER),
        ("Valor Certificado", lambda item: item[7], None, True, ALIGN_RIGHT_OPT),
    ]
    hdr_row, f_row, l_row, _ = render_table(ws, 5, 2, cols, dax_specs)
    for r_idx in range(f_row, l_row + 1):
        ws.cell(row=r_idx, column=7).font = FONT_CODE


ALIGN_RIGHT_OPT = Alignment(horizontal="right", vertical="center")


def font_section_ref():
    """Retorna la fuente institucional para títulos de sección."""
    return FONT_SECTION


def autofit_columns_fast(wb, max_sample_rows=35):
    """Ajusta anchos de columna muestreando únicamente las primeras filas (O(1) en tablas de 331k filas)."""
    for ws in wb.worksheets:
        max_col = ws.max_column
        sample_limit = min(ws.max_row, max_sample_rows)
        lengths = [0] * max_col
        for row in ws.iter_rows(min_row=1, max_row=sample_limit, max_col=max_col, values_only=True):
            for idx, val in enumerate(row):
                s = str(val or "")
                if len(s) < 65 and len(s) > lengths[idx]:
                    lengths[idx] = len(s)
        for idx, max_len in enumerate(lengths, start=1):
            ws.column_dimensions[get_column_letter(idx)].width = max(max_len + 3, 11)


def create_workbook():
    """Genera el libro Excel completo con 3 vistas ejecutivas, 11 gráficos, 10 ListObjects y 21 DAX."""
    wb = openpyxl.Workbook()
    default_sheet = wb.active

    build_portada(wb)
    build_guia_powerpivot(wb)
    build_dashboard_ejecutivo(wb)
    build_comercial_clientes(wb)
    build_operaciones_stock(wb)
    build_diccionario_dax(wb)

    tables_spec = [
        ("FACT_VENTAS_MODELO", "TablaFactVentas", "fact_ventas_detalle.csv", "TableStyleMedium2"),
        ("FACT_DEVOLUCIONES", "TablaFactDevoluciones", "fact_devoluciones_completo.csv", "TableStyleMedium2"),
        ("FACT_INSTALACIONES", "TablaFactInstalaciones", "fact_instalaciones_completo.csv", "TableStyleMedium2"),
        ("FACT_INVENTARIO", "TablaFactInventario", "fact_inventario_snapshot.csv", "TableStyleMedium2"),
        ("DIM_PRODUCTO", "TablaDimProducto", "dim_producto.csv", "TableStyleMedium9"),
        ("DIM_SUCURSAL", "TablaDimSucursal", "dim_sucursal.csv", "TableStyleMedium9"),
        ("DIM_CANAL", "TablaDimCanal", "dim_canal.csv", "TableStyleMedium9"),
        ("DIM_TIEMPO", "TablaDimTiempo", "dim_tiempo.csv", "TableStyleMedium9"),
        ("DIM_CLIENTE", "TablaDimCliente", "dim_cliente.csv", "TableStyleMedium9"),
        ("DIM_METODO_PAGO", "TablaDimMetodoPago", "dim_metodo_pago.csv", "TableStyleMedium9"),
    ]
    for sheet_title, tbl_name, csv_file, style in tables_spec:
        _, count = add_table_sheet(wb, sheet_title, tbl_name, csv_file, style)
        print(f"  + {sheet_title} ({tbl_name}): {count:,} filas")

    autofit_columns_fast(wb)
    wb.remove(default_sheet)

    primary_out = OUT_FILES[0]
    os.makedirs(os.path.dirname(primary_out), exist_ok=True)
    wb.save(primary_out)
    for copy_out in OUT_FILES[1:]:
        shutil.copy2(primary_out, copy_out)

    size_mb = os.path.getsize(primary_out) / (1024 * 1024)
    print(f"✅ Libros Excel generados (11 Gráficos Nativos, 10 ListObjects, 21 DAX, {size_mb:.2f} MB):")
    for path in OUT_FILES:
        print(f"   - {path}")


if __name__ == "__main__":
    create_workbook()
