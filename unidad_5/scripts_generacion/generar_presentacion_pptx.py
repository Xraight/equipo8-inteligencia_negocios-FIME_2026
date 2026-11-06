#!/usr/bin/env python3
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
# SCRIPT: GENERADOR DE PRESENTACIÓN EJECUTIVA PARA EL COMITÉ DIRECTIVO (PPTX)
# ARCHIVO DE SALIDA: U5_Comite_Equipo08.pptx
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def crear_presentacion_comite():
    base_dir = Path(__file__).resolve().parent.parent
    output_file = base_dir / "U5_Comite_Equipo08.pptx"

    print("==============================================================================")
    print("🖥️ GENERANDO PRESENTACIÓN PPTX: U5_Comite_Equipo08.pptx")
    print("==============================================================================")

    prs = Presentation()
    # Configurar formato panorámico 16:9 (13.33 x 7.5 pulgadas)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Paleta de Colores Corporativa
    COLOR_NAVY = RGBColor(31, 73, 125)        # #1F497D (Primario)
    COLOR_BLUE_LIGHT = RGBColor(220, 230, 241) # #DCE6F1 (Fondos tarjetas)
    COLOR_BLUE_ACCENT = RGBColor(46, 117, 182) # #2E75B6 (Secundario)
    COLOR_DARK = RGBColor(38, 38, 38)          # #262626 (Texto principal)
    COLOR_GRAY = RGBColor(89, 89, 89)          # #595959 (Texto secundario)
    COLOR_WHITE = RGBColor(255, 255, 255)      # Blanco
    COLOR_GOLD = RGBColor(197, 90, 17)         # #C55A11 (Acento)
    COLOR_BG_CARD = RGBColor(245, 247, 250)    # Gris suave fondo tarjetas

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="INFORME EJECUTIVO · BI"):
        # Barra superior decorativa
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = COLOR_NAVY
        bar.line.fill.background()

        # Categoría pequeña
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_BLUE_LIGHT

        # Título de diapositiva
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.3))
        tf_foot = footer_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Empresa Comercial · Equipo 8 (Inteligencia de Negocios · FIME UANL 2026) | Confidencial para Comité Directivo"
        p_foot.font.size = Pt(9)
        p_foot.font.color.rgb = COLOR_GRAY

    # ==========================================================================
    # SLIDE 1: PORTADA EJECUTIVA
    # ==========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    # Caja de texto principal portada
    p_box = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(3.8))
    tf1 = p_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "📊 EMPRESA COMERCIAL · REPORTE EJECUTIVO AL COMITÉ DIRECTIVO"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_GOLD

    p1 = tf1.add_paragraph()
    p1.text = "Del Data Mart al Dashboard Ejecutivo y Decisiones Estratégicas"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_before = Pt(15)

    p2 = tf1.add_paragraph()
    p2.text = "Análisis Multidimensional de Ventas, Rentabilidad y Mix Comercial (2025 - 2026)"
    p2.font.size = Pt(16)
    p2.font.color.rgb = COLOR_BLUE_LIGHT
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Equipo 8 · Inteligencia de Negocios · FIME UANL\nIntegrantes: Arely Carrillo Sustaita (2226630) | Rafael Jesús Collazo Hernández (2169304) | Sergio Jaziel Butzmann Martinez (2163239)\nFecha: Noviembre 2026 · Modalidad: Modelo de Datos en Esquema Estrella y Medidas DAX"
    p3.font.size = Pt(11)
    p3.font.color.rgb = RGBColor(200, 210, 225)
    p3.space_before = Pt(25)

    slide1.notes_slide.notes_text_frame.text = (
        "Minuto 0:00 a 1:30. Buenos días miembros del Comité Directivo. "
        "A nombre del Equipo 8, presentamos el análisis integral de ventas y rentabilidad 2025-2026 "
        "construido sobre un Data Mart dimensional riguroso y validado al 100%."
    )

    # ==========================================================================
    # SLIDE 2: CIFRAS GLOBALES Y KPIS VALIDADOS
    # ==========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Desempeño Financiero y Operativo Global (KPIs Validados)", "Contexto y Cifras de Control")

    # 4 Tarjetas Superiores
    cards_data = [
        ("VENTAS TOTALES", "$2,416,376.00", "MXN Facturados (1,200 tx)", COLOR_NAVY),
        ("MARGEN BRUTO", "$712,195.62", "Utilidad Bruta Directa", COLOR_BLUE_ACCENT),
        ("MARGEN %", "29.5%", "Rentabilidad s/ Venta (29.47%)", COLOR_GOLD),
        ("TICKET PROMEDIO", "$2,013.65", "Gasto medio por operación", COLOR_NAVY)
    ]

    card_w = Inches(2.7)
    card_h = Inches(1.6)
    card_y = Inches(1.5)

    for idx, (title, num, sub, col) in enumerate(cards_data):
        x = Inches(0.8 + idx * 2.95)
        shape = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, card_y, card_w, card_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_BG_CARD
        shape.line.color.rgb = COLOR_BLUE_ACCENT
        shape.line.width = Pt(1)

        tf = shape.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_GRAY
        p_t.alignment = PP_ALIGN.CENTER

        p_n = tf.add_paragraph()
        p_n.text = num
        p_n.font.size = Pt(20)
        p_n.font.bold = True
        p_n.font.color.rgb = col
        p_n.alignment = PP_ALIGN.CENTER
        p_n.space_before = Pt(4)

        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = COLOR_DARK
        p_s.alignment = PP_ALIGN.CENTER

    # Tabla Comparativa Anual (2025 vs 2026)
    t_shape = slide2.shapes.add_table(4, 7, Inches(0.8), Inches(3.4), Inches(11.7), Inches(2.0))
    table = t_shape.table

    table_data = [
        ["Período Fiscal", "Transacciones", "Unidades", "Ventas (MXN)", "Costo (MXN)", "Margen Bruto (MXN)", "Margen %"],
        ["Año 2025", "603", "1,841", "$1,214,067.00", "$855,921.74", "$358,145.26", "29.50%"],
        ["Año 2026", "597", "1,781", "$1,202,309.00", "$848,258.64", "$354,050.36", "29.45%"],
        ["Variación / Total", "1,200", "3,622", "$2,416,376.00", "$1,704,180.38", "$712,195.62", "29.47% (YoY: -0.97%)"]
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY
            elif r_idx == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_NAVY
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_BLUE_LIGHT
            else:
                p.font.color.rgb = COLOR_DARK
            p.alignment = PP_ALIGN.CENTER

    # Nota al pie de slide 2
    msg_box = slide2.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2))
    tf_msg = msg_box.text_frame
    tf_msg.word_wrap = True
    p_m1 = tf_msg.paragraphs[0]
    p_m1.text = "💡 Hallazgo Estratégico Clave: Alta Estabilidad Comercial con Alerta de Meseta"
    p_m1.font.size = Pt(11)
    p_m1.font.bold = True
    p_m1.font.color.rgb = COLOR_NAVY

    p_m2 = tf_msg.add_paragraph()
    p_m2.text = (
        "• Todas las cifras concilian al 100.00% con los controles institucionales (Discrepancia $0.00).\n"
        "• El volumen anual exhibe estabilidad estructural (-0.97% YoY: -$11,758 MXN), manteniendo un margen bruto intacto de 29.5%.\n"
        "• El negocio sostiene rentabilidad pero requiere una palanca de crecimiento para evitar la erosión inflacionaria."
    )
    p_m2.font.size = Pt(10)
    p_m2.font.color.rgb = COLOR_DARK

    slide2.notes_slide.notes_text_frame.text = (
        "Minuto 1:30 a 4:00. Resaltar la coincidencia exacta de los $2,416,376 pesos y 1,200 transacciones. "
        "Explicar que no hay pérdida estructural de clientes pero sí una meseta que exige decisiones."
    )

    # ==========================================================================
    # SLIDE 3: RADIOGRAFÍA REGIONAL Y DE CATEGORÍAS
    # ==========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Radiografía Dimensional: Concentración Regional y Mix por Categoría", "Análisis Descriptivo y Diagnóstico")

    # Tabla Izquierda: Regiones
    t_reg = slide3.shapes.add_table(6, 4, Inches(0.8), Inches(1.5), Inches(5.7), Inches(3.0)).table
    reg_rows = [
        ["Región Geográfica", "Transacciones", "Ventas (MXN)", "Margen %"],
        ["Occidente (Líder)", "327 (27.3%)", "$677,408.00 (28.0%)", "29.11%"],
        ["Centro", "324 (27.0%)", "$655,677.00 (27.1%)", "29.31%"],
        ["Sur (Mayor Margen)", "298 (24.8%)", "$608,288.00 (25.2%)", "30.39% ⭐"],
        ["Norte (Rezago)", "251 (20.9%)", "$475,003.00 (19.7%)", "29.05% ⚠️"],
        ["Total Consolidado", "1,200", "$2,416,376.00", "29.47%"]
    ]
    for r_idx, row in enumerate(reg_rows):
        for c_idx, val in enumerate(row):
            cell = t_reg.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY
            elif r_idx == 5:
                p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_BLUE_LIGHT
            else:
                p.font.color.rgb = COLOR_DARK
            p.alignment = PP_ALIGN.CENTER

    # Tabla Derecha: Categorías
    t_cat = slide3.shapes.add_table(5, 4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(2.6)).table
    cat_rows = [
        ["Categoría Comercial", "Transacciones", "Ventas (MXN)", "Margen %"],
        ["Tecnología (Motor)", "407 (33.9%)", "$889,916.00 (36.8%)", "30.13% ⭐"],
        ["Oficina", "401 (33.4%)", "$801,265.00 (33.2%)", "28.62%"],
        ["Hogar", "392 (32.7%)", "$725,195.00 (30.0%)", "29.61%"],
        ["Total Consolidado", "1,200", "$2,416,376.00", "29.47%"]
    ]
    for r_idx, row in enumerate(cat_rows):
        for c_idx, val in enumerate(row):
            cell = t_cat.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_BLUE_ACCENT
            elif r_idx == 4:
                p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_BLUE_LIGHT
            else:
                p.font.color.rgb = COLOR_DARK
            p.alignment = PP_ALIGN.CENTER

    # Conclusiones abajo
    box_sub = slide3.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(11.7), Inches(2.0))
    tf_sub = box_sub.text_frame
    tf_sub.word_wrap = True
    p_s1 = tf_sub.paragraphs[0]
    p_s1.text = "🎯 Hallazgos Diagnósticos Clave:"
    p_s1.font.size = Pt(11)
    p_s1.font.bold = True
    p_s1.font.color.rgb = COLOR_NAVY

    p_s2 = tf_sub.add_paragraph()
    p_s2.text = (
        "1. Polarización Territorial: Occidente y Centro concentran el 55.16% de los ingresos ($1.33M MXN).\n"
        "2. El Cuello de Botella del Norte: Factura $202k menos que Occidente (-29.9%) pese a contar con el mismo número de clientes registrados (20 clientes por región).\n"
        "3. Efectividad del Sur: Con menor facturación ($608k), alcanza el mayor margen porcentual (30.39%), confirmando una excelente mezcla de productos.\n"
        "4. Dominio Tecnológico: Tecnología aporta más de 1 de cada 3 pesos vendidos con el margen relativo más elevado."
    )
    p_s2.font.size = Pt(10)
    p_s2.font.color.rgb = COLOR_DARK

    slide3.notes_slide.notes_text_frame.text = (
        "Minuto 4:00 a 6:30. Explicar el contraste: el Norte tiene 20 clientes igual que Occidente, "
        "pero 76 transacciones menos. En cambio el Sur destaca por rentabilidad unitaria."
    )

    # ==========================================================================
    # SLIDE 4: MOTOR DE MARGEN Y TOP PRODUCTOS
    # ==========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Motor de Margen: Ranking de Productos Estrella (Top 5)", "Portafolio y Concentración de Valor")

    # Tabla Top 5
    t_top = slide4.shapes.add_table(6, 6, Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.0)).table
    top_rows = [
        ["Ranking", "Producto", "Categoría", "Ventas (MXN)", "Margen Bruto (MXN)", "Margen %"],
        ["#1 Estrella", "Producto 12", "Tecnología", "$346,902.00", "$111,004.30", "32.00% ⭐"],
        ["#2 Pilar", "Producto 10", "Hogar", "$285,698.00", "$84,661.20", "29.63%"],
        ["#3 Volumen", "Producto 11", "Oficina", "$285,677.00", "$80,171.08", "28.06%"],
        ["#4 Soporte", "Producto 09", "Tecnología", "$245,429.00", "$70,910.65", "28.89%"],
        ["#5 Soporte", "Producto 08", "Oficina", "$233,984.00", "$67,314.65", "28.77%"]
    ]
    for r_idx, row in enumerate(top_rows):
        for c_idx, val in enumerate(row):
            cell = t_top.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY
            elif r_idx == 1:
                p.font.bold = True
                p.font.color.rgb = COLOR_GOLD
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(254, 243, 230)
            else:
                p.font.color.rgb = COLOR_DARK
            p.alignment = PP_ALIGN.CENTER

    # Resumen de Concentración
    box_top_msg = slide4.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(11.7), Inches(2.0))
    tf_tm = box_top_msg.text_frame
    tf_tm.word_wrap = True
    p_tm1 = tf_tm.paragraphs[0]
    p_tm1.text = "⚠️ Diagnóstico de Portafolio: Alta Dependencia en Productos Clave"
    p_tm1.font.size = Pt(11)
    p_tm1.font.bold = True
    p_tm1.font.color.rgb = COLOR_GOLD

    p_tm2 = tf_tm.add_paragraph()
    p_tm2.text = (
        "• El Producto 12 es el líder indiscutible: 14.4% de la facturación total y 15.6% de la utilidad bruta con el margen más alto (32.0%).\n"
        "• Los dos productos líderes (Prod 12 y Prod 10) concentran el 27.5% de las ventas y el 44.8% del margen bruto de la empresa.\n"
        "• Oportunidad de Cross-Selling: Apalancar la alta demanda de Producto 12 para arrastrar productos de oficina como el Producto 11 mediante paquetes comerciales."
    )
    p_tm2.font.size = Pt(10)
    p_tm2.font.color.rgb = COLOR_DARK

    slide4.notes_slide.notes_text_frame.text = (
        "Minuto 6:30 a 8:30. Enfatizar la fortaleza del Producto 12 pero alertar sobre el riesgo "
        "de concentración: el 45% del margen depende de solo 2 artículos. Necesitamos diversificar."
    )

    # ==========================================================================
    # SLIDE 5: DIAGNÓSTICO E HIPÓTESIS
    # ==========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Diagnóstico Analítico y Formulación de Hipótesis", "Rigor Metodológico y Límites del Dataset")

    # Tarjeta Izquierda: Hipótesis 1
    h1_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(3.2))
    h1_shape.fill.solid()
    h1_shape.fill.fore_color.rgb = COLOR_BG_CARD
    h1_shape.line.color.rgb = COLOR_BLUE_ACCENT

    tf_h1 = h1_shape.text_frame
    tf_h1.word_wrap = True
    ph1 = tf_h1.paragraphs[0]
    ph1.text = "🧪 HIPÓTESIS H1: DESFASE COMERCIAL ESTACIONAL"
    ph1.font.size = Pt(11)
    ph1.font.bold = True
    ph1.font.color.rgb = COLOR_NAVY

    ph1_b = tf_h1.add_paragraph()
    ph1_b.text = (
        "\n• Observación en Datos: Noviembre 2026 cayó -25.0% YoY ($104k vs $139k), pero Diciembre 2026 repuntó +34.8% YoY ($114k vs $84k).\n\n"
        "• Hipótesis: No se trató de pérdida de clientes, sino de un desplazamiento temporal en las decisiones de compra corporativa de fin de año o retrasos de facturación hacia el último mes.\n\n"
        "• Validación requerida: Cruzar con fechas de órdenes de compra del ERP."
    )
    ph1_b.font.size = Pt(9.5)
    ph1_b.font.color.rgb = COLOR_DARK

    # Tarjeta Derecha: Hipótesis 2
    h2_shape = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(3.2))
    h2_shape.fill.solid()
    h2_shape.fill.fore_color.rgb = COLOR_BG_CARD
    h2_shape.line.color.rgb = COLOR_GOLD

    tf_h2 = h2_shape.text_frame
    tf_h2.word_wrap = True
    ph2 = tf_h2.paragraphs[0]
    ph2.text = "🧪 HIPÓTESIS H2: FRICCIÓN DE FRECUENCIA EN EL NORTE"
    ph2.font.size = Pt(11)
    ph2.font.bold = True
    ph2.font.color.rgb = COLOR_GOLD

    ph2_b = tf_h2.add_paragraph()
    ph2_b.text = (
        "\n• Observación en Datos: El Norte tiene exactamente 20 clientes al igual que Occidente, pero registró 76 transacciones menos (251 vs 327).\n\n"
        "• Hipótesis: La brecha comercial no se debe a rechazo de precios (margen del 29.05% es sano), sino a una menor frecuencia de contacto de la fuerza de ventas o mayores tiempos de entrega logística.\n\n"
        "• Validación requerida: Auditoría de visitas y nivel de servicio en plazas del Norte."
    )
    ph2_b.font.size = Pt(9.5)
    ph2_b.font.color.rgb = COLOR_DARK

    # Aviso metodológico abajo
    box_warn = slide5.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8))
    tf_w = box_warn.text_frame
    tf_w.word_wrap = True
    pw1 = tf_w.paragraphs[0]
    pw1.text = "🛡️ Declaración de Integridad Metodológica (Antigravity Standard):"
    pw1.font.size = Pt(10.5)
    pw1.font.bold = True
    pw1.font.color.rgb = RGBColor(180, 40, 40)

    pw2 = tf_w.add_paragraph()
    pw2.text = (
        "El Data Mart analizado no contiene datos de existencias en almacén, quiebres de inventario, presupuestos de marketing ni tráfico web.\n"
        "Por tanto, afirmamos con responsabilidad que las anteriores son HIPÓTESIS DE NEGOCIO y no verdades absolutas. Ninguna decisión debe sustentarse en suposiciones no auditadas."
    )
    pw2.font.size = Pt(9.5)
    pw2.font.color.rgb = COLOR_DARK

    slide5.notes_slide.notes_text_frame.text = (
        "Minuto 8:30 a 10:00. Destacar el rigor profesional: no especular sobre faltantes de stock "
        "porque el dataset no mide inventario. Presentar H1 y H2 como hipótesis a comprobar."
    )

    # ==========================================================================
    # SLIDE 6: RECOMENDACIONES ESTRATÉGICAS Y PLAN PRESCRIPTIVO
    # ==========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Recomendaciones Estratégicas y Plan Prescriptivo", "Propuesta de Acción para Aprobación")

    # Tabla Prescriptiva
    t_pre = slide6.shapes.add_table(5, 4, Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.2)).table
    pre_rows = [
        ["Línea de Acción Estratégica", "Responsable Directo", "Plazo de Ejecución", "KPI y Meta de Control"],
        [
            "1. Reactivación Comercial Región Norte\nPlan de fidelización y visitas dedicadas a los 20 clientes corporativos para elevar frecuencia de pedido.",
            "Dirección de Ventas\n(Gerencia Comercial Norte)",
            "Meses 1 a 6\n(Semestre 1)",
            "• Crecimiento Ventas Norte: +15% ($275,000 MXN)\n• Transacciones: Incrementar de 125 a 155 semestrales"
        ],
        [
            "2. Estrategia de Bundling Producto 12 + 11\nEmpaquetamiento comercial de Tecnología (Prod 12, margen 32%) con Oficina (Prod 11, margen 28%).",
            "Dirección de Mercadotecnia\ny Pricing",
            "Meses 2 a 5",
            "• Margen % Oficina: Elevar de 28.6% a 29.5%\n• Ticket Promedio Global: Sostener > $2,100 MXN"
        ],
        [
            "3. Auditoría de Tiempos y Fricción Logística\nRevisión de tiempos de despacho hacia el Norte para descartar demoras como causa de baja recompra.",
            "Dirección de Operaciones\ny Logística",
            "Meses 1 a 3\n(Diagnóstico rápido)",
            "• Nivel de Servicio (OTIF): > 95% en plazas Norte\n• Tiempo de Entrega: Reducir a < 72 hrs"
        ],
        [
            "4. Monitoreo Quincenal en Dashboard Power Pivot\nSesiones quincenales de seguimiento directivo utilizando el tablero y segmentadores dinámicos.",
            "Equipo de BI\n(Equipo 8)",
            "Permanente\n(Quincenal)",
            "• Conciliación 100% de datos en tiempo real\n• Detección temprana de desviaciones por región"
        ]
    ]

    for r_idx, row in enumerate(pre_rows):
        for c_idx, val in enumerate(row):
            cell = t_pre.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_NAVY
            else:
                p.font.color.rgb = COLOR_DARK
                if c_idx == 0:
                    p.font.bold = True
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 or c_idx == 3 else PP_ALIGN.CENTER

    # Impacto Económico Estimado
    box_roi = slide6.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.8))
    tf_roi = box_roi.text_frame
    tf_roi.word_wrap = True
    pr1 = tf_roi.paragraphs[0]
    pr1.text = "💰 Impacto Económico Estimado para la Empresa Comercial:"
    pr1.font.size = Pt(11)
    pr1.font.bold = True
    pr1.font.color.rgb = COLOR_GOLD

    pr2 = tf_roi.add_paragraph()
    pr2.text = (
        "• Un incremento del +15% en las ventas de la región Norte aportará aproximadamente +$71,000 MXN en facturación semestral adicional.\n"
        "• La optimización del mix de oficina vía bundles aportará cerca de +$15,000 MXN directos a la utilidad bruta, cerrando la brecha regional."
    )
    pr2.font.size = Pt(10)
    pr2.font.color.rgb = COLOR_DARK

    slide6.notes_slide.notes_text_frame.text = (
        "Minuto 10:00 a 11:30. Presentar las 4 acciones con responsables, plazos y métricas exactas. "
        "Enfatizar que cerrar la brecha del Norte genera más de $70k pesos de ingreso incremental inmediato."
    )

    # ==========================================================================
    # SLIDE 7: HOJA DE RUTA Y PRÓXIMOS PASOS
    # ==========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Hoja de Ruta de Implementación y Gobernanza de Datos", "Próximos Pasos y Cierre")

    # 3 Columnas de Fases Bimestrales
    fases = [
        ("FASE 1: DIAGNÓSTICO Y OFERTA", "Meses 1 y 2", [
            "• Acercamiento comercial a los 20 clientes del Norte.",
            "• Definición de paquetes promocionales Prod 12 + 11.",
            "• Auditoría de servicio logístico hacia plazas norteñas.",
            "• Aprobación formal de metas en Comité."
        ], COLOR_NAVY),
        ("FASE 2: DESPLIEGUE Y OPERACIÓN", "Meses 3 y 4", [
            "• Lanzamiento de la campaña comercial dirigida.",
            "• Colocación de bundles en clientes corporativos.",
            "• Monitoreo semanal en el Dashboard de Excel.",
            "• Ajustes de inventario según demanda observada."
        ], COLOR_BLUE_ACCENT),
        ("FASE 3: EVALUACIÓN Y ESCALA", "Meses 5 y 6", [
            "• Medición final contra los KPIs comprometidos (+15%).",
            "• Evaluación del margen consolidado en Oficina y Norte.",
            "• Presentación de resultados y balance al Comité.",
            "• Institucionalización de buenas prácticas al resto del país."
        ], COLOR_GOLD)
    ]

    for idx, (f_title, f_sub, f_items, f_col) in enumerate(fases):
        x = Inches(0.8 + idx * 4.0)
        shape = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(3.7), Inches(4.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLOR_BG_CARD
        shape.line.color.rgb = f_col
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f_title
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = f_col
        p1.alignment = PP_ALIGN.CENTER

        p2 = tf.add_paragraph()
        p2.text = f_sub
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_GRAY
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(4)

        for item in f_items:
            pi = tf.add_paragraph()
            pi.text = item
            pi.font.size = Pt(9.5)
            pi.font.color.rgb = COLOR_DARK
            pi.space_before = Pt(8)

    # Cierre abajo
    box_close = slide7.shapes.add_textbox(Inches(0.8), Inches(6.2), Inches(11.7), Inches(0.8))
    tf_c = box_close.text_frame
    tf_c.word_wrap = True
    pc = tf_c.paragraphs[0]
    pc.text = "🤝 Sesión de Preguntas y Respuestas (Q&A): El Equipo 8 queda a disposición del Comité Directivo para consultas y demostración en vivo del Dashboard."
    pc.font.size = Pt(10.5)
    pc.font.bold = True
    pc.font.color.rgb = COLOR_NAVY
    pc.alignment = PP_ALIGN.CENTER

    slide7.notes_slide.notes_text_frame.text = (
        "Minuto 11:30 a 15:00. Abrir el micrófono a preguntas. "
        "Tener listo el archivo de Excel U5_Dashboard_Equipo08.xlsx para aplicar segmentadores en vivo si el Comité lo solicita."
    )

    # Guardar presentación
    prs.save(output_file)
    print(f"✅ Presentación PPTX generada exitosamente: {output_file}")
    print(f"📦 Tamaño: {output_file.stat().st_size:,} bytes | Diapositivas: {len(prs.slides)}")
    print("==============================================================================")
    return True

if __name__ == "__main__":
    crear_presentacion_comite()
