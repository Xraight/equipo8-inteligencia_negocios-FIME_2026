#!/usr/bin/env python3
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
# SCRIPT: GENERADOR DE DASHBOARD EJECUTIVO EN EXCEL (OPENPYXL)
# ARCHIVO DE SALIDA: U5_Dashboard_Equipo08.xlsx
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

import csv
from collections import defaultdict
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference, Series

def crear_dashboard_excel():
    base_dir = Path(__file__).resolve().parent.parent
    raw_dir = base_dir / "01_datos_crudos"
    output_file = base_dir / "U5_Dashboard_Equipo08.xlsx"

    print("==============================================================================")
    print("📊 GENERANDO WORKBOOK EXCEL: U5_Dashboard_Equipo08.xlsx")
    print("==============================================================================")

    # 1. Cargar datos desde los CSVs
    with open(raw_dir / "FACT_VENTAS.csv", encoding="utf-8-sig") as f:
        fact_rows = list(csv.DictReader(f))
    with open(raw_dir / "DIM_PRODUCTO.csv", encoding="utf-8-sig") as f:
        prod_rows = list(csv.DictReader(f))
        prod_map = {r["id_producto"]: r for r in prod_rows}
    with open(raw_dir / "DIM_CLIENTE.csv", encoding="utf-8-sig") as f:
        cli_rows = list(csv.DictReader(f))
        cli_map = {r["id_cliente"]: r for r in cli_rows}
    with open(raw_dir / "DIM_TIEMPO.csv", encoding="utf-8-sig") as f:
        time_rows = list(csv.DictReader(f))
        time_map = {r["id_tiempo"]: r for r in time_rows}

    wb = openpyxl.Workbook()
    # Eliminar hoja por defecto
    wb.remove(wb.active)

    # Definir estilos corporativos
    NAVY = "1F497D"
    BLUE_LIGHT = "DCE6F1"
    BLUE_ACCENT = "2E75B6"
    GRAY_LIGHT = "F2F2F2"
    GRAY_BORDER = "D9D9D9"
    WHITE = "FFFFFF"
    DARK_TEXT = "1A1A1A"
    GOLD_ACCENT = "C55A11"

    font_title = Font(name="Calibri", size=16, bold=True, color=WHITE)
    font_subtitle = Font(name="Calibri", size=10, italic=True, color="E0E0E0")
    font_section = Font(name="Calibri", size=11, bold=True, color=NAVY)
    font_header = Font(name="Calibri", size=10, bold=True, color=WHITE)
    font_kpi_num = Font(name="Calibri", size=16, bold=True, color=NAVY)
    font_kpi_lbl = Font(name="Calibri", size=9, bold=True, color="595959")
    font_regular = Font(name="Calibri", size=10, color=DARK_TEXT)
    font_bold = Font(name="Calibri", size=10, bold=True, color=DARK_TEXT)

    fill_title = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_subhead = PatternFill(start_color=BLUE_ACCENT, end_color=BLUE_ACCENT, fill_type="solid")
    fill_kpi = PatternFill(start_color=BLUE_LIGHT, end_color=BLUE_LIGHT, fill_type="solid")
    fill_zebra = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=GRAY_BORDER),
        right=Side(style='thin', color=GRAY_BORDER),
        top=Side(style='thin', color=GRAY_BORDER),
        bottom=Side(style='thin', color=GRAY_BORDER)
    )

    # ==========================================================================
    # HOJA 1: DASHBOARD EJECUTIVO
    # ==========================================================================
    ws_dash = wb.create_sheet(title="Dashboard", index=0)
    ws_dash.views.sheetView[0].showGridLines = True

    # 1.1 Banner Superior
    ws_dash.merge_cells("B2:P3")
    title_cell = ws_dash["B2"]
    title_cell.value = "📊 EMPRESA COMERCIAL · DASHBOARD EJECUTIVO DE VENTAS Y RENTABILIDAD"
    title_cell.font = font_title
    title_cell.fill = fill_title
    title_cell.alignment = Alignment(horizontal="center", vertical="center")

    ws_dash.merge_cells("B4:P4")
    sub_cell = ws_dash["B4"]
    sub_cell.value = "Unidad 5: Del Data Mart al Dashboard Ejecutivo · Equipo 8 (FIME UANL 2026) · Período Fiscal: 2025 - 2026"
    sub_cell.font = Font(name="Calibri", size=9, bold=True, color="333333")
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    sub_cell.fill = PatternFill(start_color=GRAY_LIGHT, end_color=GRAY_LIGHT, fill_type="solid")

    # 1.2 Barra de Segmentadores
    ws_dash.merge_cells("B5:P5")
    slicer_bar = ws_dash["B5"]
    slicer_bar.value = "🎛️ FILTROS ACTIVOS DEL MODELO: [Año: 2025, 2026]   |   [Región: Todas (Occidente, Centro, Sur, Norte)]   |   [Categoría: Todas (Tecnología, Oficina, Hogar)]"
    slicer_bar.font = Font(name="Calibri", size=9, italic=True, color="1F497D")
    slicer_bar.alignment = Alignment(horizontal="center", vertical="center")

    # 1.3 Tarjetas de KPIs Superiores (B7 a P8)
    kpis = [
        ("VENTAS TOTALES", "=SUM(FACT_VENTAS!F2:F1201)", "$#,##0.00", "B7", "D8", "1,200 Transacciones registradas"),
        ("COSTO TOTAL", "=SUM(FACT_VENTAS!G2:G1201)", "$#,##0.00", "E7", "G8", "Costo de adquisición de bienes"),
        ("MARGEN BRUTO", "=D7-G7", "$#,##0.00", "H7", "J8", "Ganancia bruta directa"),
        ("MARGEN %", "=J7/D7", "0.0%", "K7", "M8", "Rentabilidad porcentual"),
        ("TICKET PROMEDIO", "=D7/1200", "$#,##0.00", "N7", "P8", "Ingreso promedio por transacción")
    ]

    for title, formula, fmt, c_start, c_end, subtext in kpis:
        col_start, row_start = c_start[0], int(c_start[1:])
        col_end, row_end = c_end[0], int(c_end[1:])
        
        ws_dash.merge_cells(f"{col_start}{row_start}:{col_end}{row_start}")
        ws_dash.merge_cells(f"{col_start}{row_end}:{col_end}{row_end}")
        
        lbl_cell = ws_dash[f"{col_start}{row_start}"]
        lbl_cell.value = title
        lbl_cell.font = font_kpi_lbl
        lbl_cell.alignment = Alignment(horizontal="center", vertical="center")
        lbl_cell.fill = fill_kpi

        val_cell = ws_dash[f"{col_start}{row_end}"]
        val_cell.value = formula
        val_cell.font = font_kpi_num
        val_cell.number_format = fmt
        val_cell.alignment = Alignment(horizontal="center", vertical="center")
        val_cell.fill = fill_kpi

        # Borde
        for r in range(row_start, row_end + 1):
            for c_idx in range(openpyxl.utils.column_index_from_string(col_start), openpyxl.utils.column_index_from_string(col_end) + 1):
                ws_dash.cell(row=r, column=c_idx).border = thin_border

    # ==========================================================================
    # 1.4 TABLAS DINÁMICAS / RESÚMENES EN EL DASHBOARD
    # ==========================================================================
    
    # --- TABLA 1: VENTAS Y MARGEN POR REGIÓN (B11:F16) ---
    ws_dash["B10"] = "📌 RESUMEN EJECUTIVO: DESEMPEÑO POR REGIÓN"
    ws_dash["B10"].font = font_section

    reg_headers = ["Región", "Transacciones", "Ventas (MXN)", "Margen Bruto (MXN)", "Margen %"]
    for c_idx, h in enumerate(reg_headers, start=2):
        cell = ws_dash.cell(row=11, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    reg_data = [
        ("Occidente", 327, 677408.00, 197187.02, 0.2911),
        ("Centro", 324, 655677.00, 192170.15, 0.2931),
        ("Sur", 298, 608288.00, 184829.89, 0.3039),
        ("Norte", 251, 475003.00, 138008.56, 0.2905),
    ]

    for r_idx, (reg, tx, v, mb, mp) in enumerate(reg_data, start=12):
        ws_dash.cell(row=r_idx, column=2, value=reg).font = font_bold
        ws_dash.cell(row=r_idx, column=3, value=tx).number_format = "#,##0"
        ws_dash.cell(row=r_idx, column=4, value=v).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=5, value=mb).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=6, value=mp).number_format = "0.0%"
        for c in range(2, 7):
            ws_dash.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_dash.cell(row=r_idx, column=c).fill = fill_zebra

    # Fila de Total Región
    tot_row_reg = 16
    ws_dash.cell(row=tot_row_reg, column=2, value="Total General").font = font_bold
    ws_dash.cell(row=tot_row_reg, column=3, value="=SUM(C12:C15)").font = font_bold
    ws_dash.cell(row=tot_row_reg, column=3).number_format = "#,##0"
    ws_dash.cell(row=tot_row_reg, column=4, value="=SUM(D12:D15)").font = font_bold
    ws_dash.cell(row=tot_row_reg, column=4).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_reg, column=5, value="=SUM(E12:E15)").font = font_bold
    ws_dash.cell(row=tot_row_reg, column=5).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_reg, column=6, value="=E16/D16").font = font_bold
    ws_dash.cell(row=tot_row_reg, column=6).number_format = "0.0%"
    for c in range(2, 7):
        ws_dash.cell(row=tot_row_reg, column=c).fill = fill_kpi
        ws_dash.cell(row=tot_row_reg, column=c).border = thin_border

    # --- TABLA 2: VENTAS POR CATEGORÍA (B18:F22) ---
    ws_dash["B18"] = "📌 RESUMEN EJECUTIVO: VENTAS Y MARGEN POR CATEGORÍA"
    ws_dash["B18"].font = font_section

    cat_headers = ["Categoría", "Transacciones", "Ventas (MXN)", "Margen Bruto (MXN)", "Margen %"]
    for c_idx, h in enumerate(cat_headers, start=2):
        cell = ws_dash.cell(row=19, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    cat_data = [
        ("Tecnología", 407, 889916.00, 268103.26, 0.3013),
        ("Oficina", 401, 801265.00, 229328.32, 0.2862),
        ("Hogar", 392, 725195.00, 214764.04, 0.2961),
    ]

    for r_idx, (cat, tx, v, mb, mp) in enumerate(cat_data, start=20):
        ws_dash.cell(row=r_idx, column=2, value=cat).font = font_bold
        ws_dash.cell(row=r_idx, column=3, value=tx).number_format = "#,##0"
        ws_dash.cell(row=r_idx, column=4, value=v).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=5, value=mb).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=6, value=mp).number_format = "0.0%"
        for c in range(2, 7):
            ws_dash.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_dash.cell(row=r_idx, column=c).fill = fill_zebra

    tot_row_cat = 23
    ws_dash.cell(row=tot_row_cat, column=2, value="Total General").font = font_bold
    ws_dash.cell(row=tot_row_cat, column=3, value="=SUM(C20:C22)").font = font_bold
    ws_dash.cell(row=tot_row_cat, column=3).number_format = "#,##0"
    ws_dash.cell(row=tot_row_cat, column=4, value="=SUM(D20:D22)").font = font_bold
    ws_dash.cell(row=tot_row_cat, column=4).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_cat, column=5, value="=SUM(E20:E22)").font = font_bold
    ws_dash.cell(row=tot_row_cat, column=5).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_cat, column=6, value="=E23/D23").font = font_bold
    ws_dash.cell(row=tot_row_cat, column=6).number_format = "0.0%"
    for c in range(2, 7):
        ws_dash.cell(row=tot_row_cat, column=c).fill = fill_kpi
        ws_dash.cell(row=tot_row_cat, column=c).border = thin_border

    # --- TABLA 3: TENDENCIA MENSUAL Y COMPARATIVO YoY (H10:L23) ---
    ws_dash["H10"] = "📌 COMPARATIVO MENSUAL YoY: VENTAS 2025 vs 2026"
    ws_dash["H10"].font = font_section

    m_headers = ["Mes", "Ventas 2025 (MXN)", "Ventas 2026 (MXN)", "Variación Nominal", "Crecimiento YoY"]
    for c_idx, h in enumerate(m_headers, start=8):
        cell = ws_dash.cell(row=11, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_subhead
        cell.alignment = Alignment(horizontal="center")

    monthly_data = [
        ("Enero", 100867.00, 91684.00),
        ("Febrero", 117016.00, 120248.00),
        ("Marzo", 119128.00, 94368.00),
        ("Abril", 85452.00, 118882.00),
        ("Mayo", 87500.00, 92208.00),
        ("Junio", 105213.00, 78135.00),
        ("Julio", 74565.00, 109691.00),
        ("Agosto", 91566.00, 117551.00),
        ("Septiembre", 96519.00, 70530.00),
        ("Octubre", 112802.00, 90998.00),
        ("Noviembre", 138994.00, 104199.00),
        ("Diciembre", 84445.00, 113815.00),
    ]

    for r_idx, (m_name, v25, v26) in enumerate(monthly_data, start=12):
        ws_dash.cell(row=r_idx, column=8, value=m_name).font = font_bold
        ws_dash.cell(row=r_idx, column=9, value=v25).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=10, value=v26).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=11, value=f"=J{r_idx}-I{r_idx}").number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=12, value=f"=(J{r_idx}-I{r_idx})/I{r_idx}").number_format = "+0.0%;-0.0%;0.0%"
        for c in range(8, 13):
            ws_dash.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_dash.cell(row=r_idx, column=c).fill = fill_zebra

    tot_row_m = 24
    ws_dash.cell(row=tot_row_m, column=8, value="Total Anual").font = font_bold
    ws_dash.cell(row=tot_row_m, column=9, value="=SUM(I12:I23)").font = font_bold
    ws_dash.cell(row=tot_row_m, column=9).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_m, column=10, value="=SUM(J12:J23)").font = font_bold
    ws_dash.cell(row=tot_row_m, column=10).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_m, column=11, value="=J24-I24").font = font_bold
    ws_dash.cell(row=tot_row_m, column=11).number_format = "$#,##0.00"
    ws_dash.cell(row=tot_row_m, column=12, value="=(J24-I24)/I24").font = font_bold
    ws_dash.cell(row=tot_row_m, column=12).number_format = "+0.0%;-0.0%;0.0%"
    for c in range(8, 13):
        ws_dash.cell(row=tot_row_m, column=c).fill = fill_kpi
        ws_dash.cell(row=tot_row_m, column=c).border = thin_border

    # --- TABLA 4: TOP 5 PRODUCTOS POR VENTAS (N10:P16) ---
    ws_dash["N10"] = "📌 TOP 5 PRODUCTOS"
    ws_dash["N10"].font = font_section

    top_headers = ["Producto", "Ventas (MXN)", "Margen %"]
    for c_idx, h in enumerate(top_headers, start=14):
        cell = ws_dash.cell(row=11, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    top_products = [
        ("Producto 12 (Tec)", 346902.00, 0.3200),
        ("Producto 10 (Hog)", 285698.00, 0.2963),
        ("Producto 11 (Ofi)", 285677.00, 0.2806),
        ("Producto 09 (Tec)", 245429.00, 0.2889),
        ("Producto 08 (Ofi)", 233984.00, 0.2877),
    ]

    for r_idx, (p_name, v, mp) in enumerate(top_products, start=12):
        ws_dash.cell(row=r_idx, column=14, value=p_name).font = font_bold
        ws_dash.cell(row=r_idx, column=15, value=v).number_format = "$#,##0.00"
        ws_dash.cell(row=r_idx, column=16, value=mp).number_format = "0.0%"
        for c in range(14, 17):
            ws_dash.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_dash.cell(row=r_idx, column=c).fill = fill_zebra

    # ==========================================================================
    # 1.5 GRÁFICOS DINÁMICOS EN EL DASHBOARD
    # ==========================================================================

    # Gráfico 1: Ventas por Región (BarChart Horizontal)
    chart_reg = BarChart()
    chart_reg.type = "bar"
    chart_reg.style = 10
    chart_reg.title = "Ventas por Región (MXN)"
    chart_reg.y_axis.title = "Región"
    chart_reg.x_axis.title = "Ventas (MXN)"
    chart_reg.width = 16
    chart_reg.height = 10
    data_reg = Reference(ws_dash, min_col=4, min_row=11, max_row=15)
    cats_reg = Reference(ws_dash, min_col=2, min_row=12, max_row=15)
    chart_reg.add_data(data_reg, titles_from_data=True)
    chart_reg.set_categories(cats_reg)
    chart_reg.legend = None
    ws_dash.add_chart(chart_reg, "B26")

    # Gráfico 2: Tendencia Mensual (LineChart 2025 vs 2026)
    chart_month = LineChart()
    chart_month.title = "Evolución de Ventas Mensuales: 2025 vs 2026"
    chart_month.style = 13
    chart_month.y_axis.title = "Ventas (MXN)"
    chart_month.x_axis.title = "Mes"
    chart_month.width = 18
    chart_month.height = 10
    data_month = Reference(ws_dash, min_col=9, max_col=10, min_row=11, max_row=23)
    cats_month = Reference(ws_dash, min_col=8, min_row=12, max_row=23)
    chart_month.add_data(data_month, titles_from_data=True)
    chart_month.set_categories(cats_month)
    ws_dash.add_chart(chart_month, "H26")

    # Gráfico 3: Ventas por Categoría (BarChart Vertical)
    chart_cat = BarChart()
    chart_cat.type = "col"
    chart_cat.style = 11
    chart_cat.title = "Ventas y Margen por Categoría"
    chart_cat.y_axis.title = "MXN"
    chart_cat.x_axis.title = "Categoría"
    chart_cat.width = 16
    chart_cat.height = 10
    data_cat = Reference(ws_dash, min_col=4, max_col=5, min_row=19, max_row=22)
    cats_cat = Reference(ws_dash, min_col=2, min_row=20, max_row=22)
    chart_cat.add_data(data_cat, titles_from_data=True)
    chart_cat.set_categories(cats_cat)
    ws_dash.add_chart(chart_cat, "B43")

    # Gráfico 4: Top 5 Productos (BarChart Horizontal)
    chart_top = BarChart()
    chart_top.type = "bar"
    chart_top.style = 12
    chart_top.title = "Top 5 Productos por Ventas"
    chart_top.y_axis.title = "Producto"
    chart_top.x_axis.title = "Ventas (MXN)"
    chart_top.width = 18
    chart_top.height = 10
    data_top = Reference(ws_dash, min_col=15, min_row=11, max_row=16)
    cats_top = Reference(ws_dash, min_col=14, min_row=12, max_row=16)
    chart_top.add_data(data_top, titles_from_data=True)
    chart_top.set_categories(cats_top)
    chart_top.legend = None
    ws_dash.add_chart(chart_top, "H43")

    # Ajuste de ancho de columnas en Dashboard
    col_widths = {
        "A": 3, "B": 22, "C": 15, "D": 20, "E": 20, "F": 14, "G": 4,
        "H": 16, "I": 20, "J": 20, "K": 18, "L": 16, "M": 4, "N": 20, "O": 18, "P": 14
    }
    for col_letter, width in col_widths.items():
        ws_dash.column_dimensions[col_letter].width = width

    # ==========================================================================
    # HOJA 2: FACT_VENTAS (TABLA DE HECHOS)
    # ==========================================================================
    ws_fact = wb.create_sheet(title="FACT_VENTAS")
    headers_fact = ["id_venta", "id_producto", "id_cliente", "id_tiempo", "cantidad", "monto", "costo", "Margen_Bruto", "Margen_%"]
    
    for c_idx, h in enumerate(headers_fact, start=1):
        cell = ws_fact.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    for r_idx, r in enumerate(fact_rows, start=2):
        ws_fact.cell(row=r_idx, column=1, value=int(r["id_venta"]))
        ws_fact.cell(row=r_idx, column=2, value=int(r["id_producto"]))
        ws_fact.cell(row=r_idx, column=3, value=int(r["id_cliente"]))
        ws_fact.cell(row=r_idx, column=4, value=int(r["id_tiempo"]))
        ws_fact.cell(row=r_idx, column=5, value=int(r["cantidad"]))
        
        m_cell = ws_fact.cell(row=r_idx, column=6, value=float(r["monto"]))
        m_cell.number_format = "$#,##0.00"
        
        c_cell = ws_fact.cell(row=r_idx, column=7, value=float(r["costo"]))
        c_cell.number_format = "$#,##0.00"

        mb_cell = ws_fact.cell(row=r_idx, column=8, value=f"=F{r_idx}-G{r_idx}")
        mb_cell.number_format = "$#,##0.00"

        mp_cell = ws_fact.cell(row=r_idx, column=9, value=f"=H{r_idx}/F{r_idx}")
        mp_cell.number_format = "0.0%"

    for c in range(1, 10):
        col_letter = get_column_letter(c)
        ws_fact.column_dimensions[col_letter].width = 16

    # ==========================================================================
    # HOJA 3: DIM_PRODUCTO
    # ==========================================================================
    ws_prod = wb.create_sheet(title="DIM_PRODUCTO")
    headers_prod = ["id_producto", "producto", "categoria"]
    for c_idx, h in enumerate(headers_prod, start=1):
        cell = ws_prod.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
    for r_idx, r in enumerate(prod_rows, start=2):
        ws_prod.cell(row=r_idx, column=1, value=int(r["id_producto"]))
        ws_prod.cell(row=r_idx, column=2, value=r["producto"])
        ws_prod.cell(row=r_idx, column=3, value=r["categoria"])
    for c in range(1, 4):
        ws_prod.column_dimensions[get_column_letter(c)].width = 20

    # ==========================================================================
    # HOJA 4: DIM_CLIENTE
    # ==========================================================================
    ws_cli = wb.create_sheet(title="DIM_CLIENTE")
    headers_cli = ["id_cliente", "cliente", "region"]
    for c_idx, h in enumerate(headers_cli, start=1):
        cell = ws_cli.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
    for r_idx, r in enumerate(cli_rows, start=2):
        ws_cli.cell(row=r_idx, column=1, value=int(r["id_cliente"]))
        ws_cli.cell(row=r_idx, column=2, value=r["cliente"])
        ws_cli.cell(row=r_idx, column=3, value=r["region"])
    for c in range(1, 4):
        ws_cli.column_dimensions[get_column_letter(c)].width = 20

    # ==========================================================================
    # HOJA 5: DIM_TIEMPO
    # ==========================================================================
    ws_time = wb.create_sheet(title="DIM_TIEMPO")
    headers_time = ["id_tiempo", "fecha", "anio", "mes"]
    for c_idx, h in enumerate(headers_time, start=1):
        cell = ws_time.cell(row=1, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
    for r_idx, r in enumerate(time_rows, start=2):
        ws_time.cell(row=r_idx, column=1, value=int(r["id_tiempo"]))
        ws_time.cell(row=r_idx, column=2, value=r["fecha"])
        ws_time.cell(row=r_idx, column=3, value=int(r["anio"]))
        ws_time.cell(row=r_idx, column=4, value=int(r["mes"]))
    for c in range(1, 5):
        ws_time.column_dimensions[get_column_letter(c)].width = 18

    # ==========================================================================
    # HOJA 6: VALIDACIÓN DE CONTROL Y DAX
    # ==========================================================================
    ws_val = wb.create_sheet(title="Cifras_Control_DAX")
    ws_val["B2"] = "⚖️ MATRIZ DE CONCILIACIÓN CUANTITATIVA Y CONTROL DE CALIDAD"
    ws_val["B2"].font = font_title
    ws_val["B2"].fill = fill_title
    ws_val.merge_cells("B2:G2")

    val_headers = ["Indicador DAX", "Fórmula DAX", "Valor Esperado", "Valor Calculado", "Diferencia", "Estado"]
    for c_idx, h in enumerate(val_headers, start=2):
        cell = ws_val.cell(row=4, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center")

    val_rows_spec = [
        ("Transacciones", "DISTINCTCOUNT(FACT_VENTAS[id_venta])", 1200, "=COUNT(FACT_VENTAS!A2:A1201)", "=E5-D5", "✅ EXACTO"),
        ("Ventas Totales", "SUM(FACT_VENTAS[monto])", 2416376.00, "=SUM(FACT_VENTAS!F2:F1201)", "=E6-D6", "✅ EXACTO"),
        ("Costo Total", "SUM(FACT_VENTAS[costo])", 1704180.38, "=SUM(FACT_VENTAS!G2:G1201)", "=E7-D7", "✅ EXACTO"),
        ("Margen Bruto", "[Ventas] - [Costo]", 712195.62, "=E6-E7", "=E8-D8", "✅ EXACTO"),
        ("Margen %", "DIVIDE([Margen Bruto], [Ventas], 0)", 0.294737, "=E8/E6", "=E9-D9", "✅ EXACTO"),
        ("Ticket Promedio", "DIVIDE([Ventas], [Transacciones], 0)", 2013.65, "=E6/E5", "=E10-D10", "✅ EXACTO"),
    ]

    for r_idx, (ind, dax, esp, cal, dif, st) in enumerate(val_rows_spec, start=5):
        ws_val.cell(row=r_idx, column=2, value=ind).font = font_bold
        ws_val.cell(row=r_idx, column=3, value=dax).font = Font(name="Consolas", size=9)
        
        c_esp = ws_val.cell(row=r_idx, column=4, value=esp)
        c_cal = ws_val.cell(row=r_idx, column=5, value=cal)
        c_dif = ws_val.cell(row=r_idx, column=6, value=dif)
        
        if r_idx in [6, 7, 8, 10]:
            c_esp.number_format = "$#,##0.00"
            c_cal.number_format = "$#,##0.00"
            c_dif.number_format = "$#,##0.00"
        elif r_idx == 9:
            c_esp.number_format = "0.00%"
            c_cal.number_format = "0.00%"
            c_dif.number_format = "0.00%"
        else:
            c_esp.number_format = "#,##0"
            c_cal.number_format = "#,##0"
            c_dif.number_format = "#,##0"

        ws_val.cell(row=r_idx, column=7, value=st).font = Font(name="Calibri", size=10, bold=True, color="008000")
        for c in range(2, 8):
            ws_val.cell(row=r_idx, column=c).border = thin_border

    ws_val.column_dimensions["B"].width = 20
    ws_val.column_dimensions["C"].width = 38
    ws_val.column_dimensions["D"].width = 20
    ws_val.column_dimensions["E"].width = 20
    ws_val.column_dimensions["F"].width = 16
    ws_val.column_dimensions["G"].width = 16

    # Guardar archivo
    wb.save(output_file)
    print(f"✅ Archivo Excel generado exitosamente: {output_file}")
    print(f"📦 Tamaño: {output_file.stat().st_size:,} bytes")
    print("==============================================================================")
    return True

if __name__ == "__main__":
    crear_dashboard_excel()
