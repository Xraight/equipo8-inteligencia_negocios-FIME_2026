# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
# ARCHIVO: generar_presentacion_pptx.py
# AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Python 3.12 / Docker (python-pptx)
# ==============================================================================
# FUNCIÓN GENERAL:
# Generar el deck ejecutivo corporativo oficial `PIA_Comite_CasaEstilo_Equipo08.pptx`
# de exactamente 10 diapositivas panorámicas (16:9) para el Comité Directivo.
#
# FUNCIÓN ESPECÍFICA:
# 1. Configurar dimensiones panorámicas 16:9 (13.333 x 7.5 pulgadas).
# 2. Diseñar 10 diapositivas con maquetación ejecutiva, banners, tarjetas de KPI,
#    tablas comparativas, diagnóstico de riesgos y hoja de ruta prescriptiva.
# 3. Aplicar paleta corporativa: Deep Navy (0x1A, 0x36, 0x5D), Gold (0xD6, 0x9E, 0x2E),
#    Slate (0x2D, 0x37, 0x48) y White (0xFF, 0xFF, 0xFF).
# ==============================================================================

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUT_FILE = "PIA/PIA_Comite_CasaEstilo_Equipo08.pptx"

# Paleta Ejecutiva FIME / Casa&Estilo
COLOR_NAVY = RGBColor(0x1A, 0x36, 0x5D)
COLOR_GOLD = RGBColor(0xD6, 0x9E, 0x2E)
COLOR_SLATE = RGBColor(0x2D, 0x37, 0x48)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_LIGHT_BG = RGBColor(0xF7, 0xFA, 0xFC)
COLOR_CARD = RGBColor(0xED, 0xF2, 0xF7)
COLOR_RED = RGBColor(0xC5, 0x30, 0x30)
COLOR_GREEN = RGBColor(0x2F, 0x85, 0x5A)
COLOR_BLUE = RGBColor(0x2B, 0x6C, 0xB0)
COLOR_MUTED = RGBColor(0x71, 0x80, 0x96)


def add_header(slide, title_text, category_text="PRODUCTO INTEGRADOR DE APRENDIZAJE | CASA&ESTILO"):
    # Header Banner Background
    header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = COLOR_NAVY
    header_box.line.color.rgb = COLOR_NAVY

    # Gold Accent Stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = COLOR_GOLD
    stripe.line.color.rgb = COLOR_GOLD

    # Category / Breadcrumb
    tf_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3)).text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_GOLD

    # Title
    tf_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65)).text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_WHITE


def add_footer(slide, slide_num):
    # Footer Line
    footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.02))
    footer_line.fill.solid()
    footer_line.fill.fore_color.rgb = RGBColor(0xCB, 0xD5, 0xE0)
    footer_line.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)

    # Footer Text
    tf_footer = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(9.0), Inches(0.4)).text_frame
    p_f = tf_footer.paragraphs[0]
    p_f.text = "FIME UANL — Analítica e Inteligencia de Negocios | Equipo 8 — Solución BI Casa&Estilo"
    p_f.font.size = Pt(8.5)
    p_f.font.color.rgb = COLOR_MUTED

    # Slide Number
    tf_num = slide.shapes.add_textbox(Inches(11.5), Inches(6.95), Inches(1.0), Inches(0.4)).text_frame
    p_num = tf_num.paragraphs[0]
    p_num.text = f"{slide_num} / 10"
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.font.size = Pt(9)
    p_num.font.bold = True
    p_num.font.color.rgb = COLOR_NAVY


def add_card(slide, left, top, width, height, title, value, subtitle="", border_color=COLOR_NAVY):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12)

    p0 = tf.paragraphs[0]
    p0.text = title.upper()
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_MUTED
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = value
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = border_color
    p1.alignment = PP_ALIGN.CENTER

    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(8.5)
        p2.font.italic = True
        p2.font.color.rgb = COLOR_MUTED
        p2.alignment = PP_ALIGN.CENTER


def generate_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: PORTADA
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.color.rgb = COLOR_NAVY

    # Decorative Stripe
    gold_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.0), Inches(0.15), Inches(5.5))
    gold_bar.fill.solid()
    gold_bar.fill.fore_color.rgb = COLOR_GOLD
    gold_bar.line.color.rgb = COLOR_GOLD

    tf_p1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(4.5)).text_frame
    tf_p1.word_wrap = True

    p = tf_p1.paragraphs[0]
    p.text = "UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN | FIME"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    p = tf_p1.add_paragraph()
    p.text = "Solución Integral de Business Intelligence"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE

    p = tf_p1.add_paragraph()
    p.text = "Caso de Negocio: Casa&Estilo (Sector Muebles y Decoración)"
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(0xEB, 0xF8, 0xFF)

    p = tf_p1.add_paragraph()
    p.text = "\nProducto Integrador de Aprendizaje (30% de la Calificación Total)\nDefensa ante Comité Directivo — Noviembre 2026"
    p.font.size = Pt(13)
    p.font.italic = True
    p.font.color.rgb = RGBColor(0xA0, 0xAE, 0xC0)

    p = tf_p1.add_paragraph()
    p.text = "\nEquipo 8 | Analítica e Inteligencia de Negocios"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    # Cita de pie
    tf_quote = s1.shapes.add_textbox(Inches(1.2), Inches(6.3), Inches(11.0), Inches(0.6)).text_frame
    p_q = tf_quote.paragraphs[0]
    p_q.text = "“Los datos por sí solos no toman decisiones; el valor está en convertirlos en información accionable.”"
    p_q.font.size = Pt(11)
    p_q.font.italic = True
    p_q.font.color.rgb = COLOR_WHITE

    # ==========================================================================
    # SLIDE 2: CONTEXTO Y FUENTES RAW
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Contexto Empresarial y Diagnóstico del Ecosistema RAW")
    add_footer(s2, 2)

    # 4 Cards resumen de volumen
    add_card(s2, Inches(0.8), Inches(1.4), Inches(2.7), Inches(1.3), "Transacciones POS", "140,000", "Ventas de cabecera", COLOR_NAVY)
    add_card(s2, Inches(3.7), Inches(1.4), Inches(2.7), Inches(1.3), "Líneas de Detalle", "331,758", "Granularidad atómica", COLOR_BLUE)
    add_card(s2, Inches(6.6), Inches(1.4), Inches(2.7), Inches(1.3), "Clientes CRM", "10,800", "Cartera registrada", COLOR_GREEN)
    add_card(s2, Inches(9.5), Inches(1.4), Inches(2.7), Inches(1.3), "Red de Distribución", "16 Tiendas", "Omnicanal (+Web +App)", COLOR_GOLD)

    # Bloque de hallazgos
    box2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.9), Inches(11.733), Inches(3.8))
    box2.fill.solid()
    box2.fill.fore_color.rgb = COLOR_LIGHT_BG
    box2.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)

    tf2 = box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.3)
    tf2.margin_top = Inches(0.25)

    p = tf2.paragraphs[0]
    p.text = "DIAGNÓSTICO CRÍTICO DE LA PROBLEMÁTICA EMPRESARIAL:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    items_s2 = [
        ("Dispersión de Fuentes:", "11 archivos CSV desarticulados entre sistemas POS, ERP, CRM, Almacén y Logística de Armado."),
        ("Hallazgo Crítico en POS:", "La columna 'importe' en el RAW contenía el subtotal bruto sin descontar el 'descuento_pct', generando una sobreestimación artificial de $91.7M MXN."),
        ("Anomalías Controladas en CRM:", "20 registros con ciudad vacía, 43 correos nulos y 235 sexos 'N/E' que requerían reglas formales de saneamiento."),
        ("Ceguera en la Última Milla:", "Falta de trazabilidad entre los servicios técnicos de armado/instalación, el retraso en días y el índice de satisfacción del cliente."),
        ("Mandato de Trabajo:", "No modificar los archivos RAW originales; diseñar una solución limpia, trazable y reproducible en MySQL 8.0 y Docker.")
    ]
    for bold_prefix, text in items_s2:
        p = tf2.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {bold_prefix} "
        run1.font.bold = True
        run1.font.color.rgb = COLOR_NAVY
        run1.font.size = Pt(11)

        run2 = p.add_run()
        run2.text = text
        run2.font.color.rgb = COLOR_SLATE
        run2.font.size = Pt(11)

    # ==========================================================================
    # SLIDE 3: ARQUITECTURA TECNOLÓGICA Y ETL
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Arquitectura Tecnológica y Pipeline ETL Automatizado")
    add_footer(s3, 3)

    # 3 Cajas de Arquitectura (RAW -> Staging -> Data Mart)
    capas = [
        (Inches(0.8), "CAPA 1: FUENTES RAW", "11 Archivos CSV Inmutables",
         ["• Extracción directa sin alterar archivos", "• Contención de anomalías y BOM", "• +530,000 registros procesados"], COLOR_MUTED),
        (Inches(4.8), "CAPA 2: STAGING (stg_ce_*)", "Área de Ingesta y Limpieza",
         ["• Ingesta masiva con LOAD DATA INFILE", "• Saneamiento de textos e imputaciones", "• Cálculo de importes brutos vs netos"], COLOR_BLUE),
        (Inches(8.8), "CAPA 3: DATA MART (ce_bi)", "Modelo Analítico Dimensional",
         ["• Esquema Estrella / Constelación", "• Dimensiones Conformes + Surrogate Keys", "• 100% Conciliado en etl_balance_masa"], COLOR_GREEN)
    ]
    for left, title, sub, bullets, color in capas:
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.4), Inches(3.7), Inches(3.4))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_LIGHT_BG
        box.line.color.rgb = color
        box.line.width = Pt(2)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_top = Inches(0.2)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(9.5)
        p.font.italic = True
        p.font.color.rgb = COLOR_SLATE

        for b in bullets:
            p = tf.add_paragraph()
            p.text = b
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_SLATE

    # Tabla de Certificación de Balance de Masa
    box_audit = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.7))
    box_audit.fill.solid()
    box_audit.fill.fore_color.rgb = COLOR_CARD
    box_audit.line.color.rgb = COLOR_GOLD

    tf_a = box_audit.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = Inches(0.25)
    tf_a.margin_top = Inches(0.15)

    p = tf_a.paragraphs[0]
    p.text = "CERTIFICACIÓN DE BALANCE DE MASA Y AUDITORÍA (DISCREPANCIA CERO):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    audits = [
        "✔ Ventas Detalle: 331,758 filas RAW = 331,758 Data Mart (100.00% CONCILIADO)",
        "✔ Devoluciones: 9,952 filas RAW = 9,952 Data Mart (100.00% CONCILIADO)",
        "✔ Instalaciones: 6,500 órdenes = 6,500 Data Mart (100.00% CONCILIADO)",
        "✔ Existencias: 21,440 pares sucursal-producto = 21,440 Data Mart (100.00% CONCILIADO)",
        "✔ Integridad Referencial: CERO claves foráneas huérfanas o nulas en todo el Data Mart."
    ]
    for a in audits:
        p = tf_a.add_paragraph()
        p.text = a
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 4: MODELO DIMENSIONAL EN ESQUEMA ESTRELLA
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Diseño Dimensional: Esquema Estrella y Justificación")
    add_footer(s4, 4)

    # Columna Izquierda: Arquitectura del Esquema Estrella
    box4_l = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.3))
    box4_l.fill.solid()
    box4_l.fill.fore_color.rgb = COLOR_LIGHT_BG
    box4_l.line.color.rgb = COLOR_NAVY

    tf4_l = box4_l.text_frame
    tf4_l.word_wrap = True
    tf4_l.margin_left = Inches(0.25)
    tf4_l.margin_top = Inches(0.2)

    p = tf4_l.paragraphs[0]
    p.text = "ESTRUCTURA DEL MODELO EN ESQUEMA ESTRELLA:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    dims = [
        ("Tabla de Hechos Central:", "fact_ventas_detalle (331,758 filas a nivel línea de ticket)."),
        ("Hechos Satélites:", "fact_devoluciones (9,952) | fact_instalaciones (6,500) | fact_inventario (21,440)."),
        ("dim_tiempo:", "1,096 días continuos (2024 a 2026) con jerarquías Año, Q, Mes, Semana, Día."),
        ("dim_producto:", "1,340 SKUs en 7 categorías, costo, precio lista y margen teórico."),
        ("dim_cliente:", "10,800 clientes con género, ciudad y segmento de valor."),
        ("dim_sucursal:", "16 tiendas físicas con superficie (m2) y fecha de apertura."),
        ("dim_canal / metodo:", "Desacopladas (Tienda/Web/App y Tarjeta/Efectivo/Transferencia/Wallet).")
    ]
    for b_title, b_desc in dims:
        p = tf4_l.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {b_title} "
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_NAVY

        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_SLATE

    # Columna Derecha: Justificación de Decisiones
    box4_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.3))
    box4_r.fill.solid()
    box4_r.fill.fore_color.rgb = COLOR_LIGHT_BG
    box4_r.line.color.rgb = COLOR_GOLD

    tf4_r = box4_r.text_frame
    tf4_r.word_wrap = True
    tf4_r.margin_left = Inches(0.25)
    tf4_r.margin_top = Inches(0.2)

    p = tf4_r.paragraphs[0]
    p.text = "DEFENSA DE DECISIONES DE DISEÑO (KIMBALL):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    justs = [
        ("¿Por qué Estrella y no Snowflake?:", "Minimiza saltos relacionales en consultas OLAP. Optimiza la compresión en memoria del motor columnar VertiPaq en Power Pivot."),
        ("Granularidad Atómica:", "Al modelar a nivel línea de ticket, permitimos análisis cruzado de rentabilidad por producto sin pérdida de varianza."),
        ("Surrogate Keys Enteras (INT):", "Reducen en 60% el peso de índices en comparación con VARCHAR y aíslan el Data Mart de cambios en el ERP."),
        ("Registro Comodín (Key = 1 / -1):", "Garantiza que transacciones con atributos ausentes no generen rechazos ni descuadren el balance contable."),
        ("Fórmula de Margen Saneada:", "Monto Neto = Bruto - Descuento. Utilidad = Neto - COGS.")
    ]
    for j_title, j_desc in justs:
        p = tf4_r.add_paragraph()
        run1 = p.add_run()
        run1.text = f"✔ {j_title} "
        run1.font.bold = True
        run1.font.size = Pt(9.5)
        run1.font.color.rgb = COLOR_NAVY

        run2 = p.add_run()
        run2.text = j_desc
        run2.font.size = Pt(9.5)
        run2.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 5: DIAGNÓSTICO COMERCIAL GLOBAL
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Desempeño Comercial y Rentabilidad Global (2024 - 2026)")
    add_footer(s5, 5)

    # 4 Scorecards Financieros Principales
    add_card(s5, Inches(0.8), Inches(1.4), Inches(2.7), Inches(1.4), "Venta Neta Total", "$1,310.75M", "Facturación efectiva", COLOR_NAVY)
    add_card(s5, Inches(3.7), Inches(1.4), Inches(2.7), Inches(1.4), "Costo de Ventas (COGS)", "$1,029.87M", "78.57% s/Venta Neta", COLOR_SLATE)
    add_card(s5, Inches(6.6), Inches(1.4), Inches(2.7), Inches(1.4), "Utilidad Bruta", "$280.87M", "Beneficio comercial", COLOR_GREEN)
    add_card(s5, Inches(9.5), Inches(1.4), Inches(2.7), Inches(1.4), "Margen Bruto Real", "21.43%", "Ticket Med: $9,362.47", COLOR_GOLD)

    # Tabla de Evolución Anual
    table_shape = s5.shapes.add_table(4, 6, Inches(0.8), Inches(3.1), Inches(11.733), Inches(1.8))
    table = table_shape.table

    headers_s5 = ["Año", "Transacciones", "Venta Neta ($ MXN)", "Costo COGS ($ MXN)", "Utilidad Bruta ($ MXN)", "Margen Bruto %"]
    for col_idx, h in enumerate(headers_s5):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    rows_s5 = [
        ("2024", "50,852", "$475,742,846.03", "$373,806,439.75", "$101,936,406.28", "21.43%"),
        ("2025", "51,055", "$479,812,870.85", "$377,062,390.86", "$102,750,479.99", "21.41%"),
        ("2026 (9m)", "38,093", "$355,190,775.01", "$279,002,796.28", "$76,187,967.44", "21.45%")
    ]
    for r_idx, r_data in enumerate(rows_s5, start=1):
        for c_idx, val in enumerate(r_data):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_SLATE
            p.alignment = PP_ALIGN.CENTER if c_idx in (0, 1, 5) else PP_ALIGN.RIGHT

    # Cuadro de Hallazgo Estratégico
    box5_callout = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.733), Inches(1.6))
    box5_callout.fill.solid()
    box5_callout.fill.fore_color.rgb = COLOR_LIGHT_BG
    box5_callout.line.color.rgb = COLOR_GREEN

    tf5_c = box5_callout.text_frame
    tf5_c.word_wrap = True
    tf5_c.margin_left = Inches(0.25)
    tf5_c.margin_top = Inches(0.15)

    p = tf5_c.paragraphs[0]
    p.text = "IMPACTO DE LA CORRECCIÓN DE CALIDAD DE DATOS EN EL ESTADO FINANCIERO:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    p = tf5_c.add_paragraph()
    p.text = "• En los datos crudos, la Venta Bruta facturada fue de $1,402.50M. Si no se hubieran auditado los descuentos comerciales ($91.75M), el Comité Directivo habría sobreestimado los ingresos reales en un 7.0%."
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_SLATE

    p = tf5_c.add_paragraph()
    p.text = "• El margen bruto se mantiene notablemente estable en torno al 21.43% anual, demostrando una disciplina de precios consistente pero dejando margen para optimizar costos de adquisición."
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 6: ANÁLISIS DE CATEGORÍAS Y OMNICANALIDAD
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Análisis de Cartera: Categorías y Desempeño Omnicanal")
    add_footer(s6, 6)

    # Lado Izquierdo: Tabla Categorías
    t_cat_shape = s6.shapes.add_table(8, 5, Inches(0.8), Inches(1.4), Inches(6.8), Inches(5.3))
    t_cat = t_cat_shape.table

    h_cat = ["Categoría", "Venta Neta ($)", "Margen %", "Devueltos ($)", "Tasa Dev %"]
    for c_idx, h in enumerate(h_cat):
        cell = t_cat.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    cat_display = [
        ("Recámara", "$221,409,378.34", "21.14%", "$3,710,510.42", "1.63%"),
        ("Comedor", "$194,527,306.68", "21.07%", "$3,317,624.50", "1.66%"),
        ("Exterior", "$186,060,615.84", "21.72%", "$3,039,871.20", "1.59%"),
        ("Oficina", "$184,793,466.90", "21.41%", "$3,169,450.80", "1.67%"),
        ("Iluminación", "$183,836,018.89", "21.22%", "$2,976,512.10", "1.58%"),
        ("Sala", "$173,698,543.15", "21.98%", "$2,878,940.35", "1.62%"),
        ("Decoración", "$166,421,162.09", "21.58%", "$2,804,927.50", "1.69%")
    ]
    for r_idx, r_data in enumerate(cat_display, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_cat.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(8.5)
            p.font.color.rgb = COLOR_SLATE
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else (PP_ALIGN.CENTER if c_idx in (2, 4) else PP_ALIGN.RIGHT)

    # Lado Derecho: Omnicanalidad
    box6_r = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.4), Inches(4.733), Inches(5.3))
    box6_r.fill.solid()
    box6_r.fill.fore_color.rgb = COLOR_LIGHT_BG
    box6_r.line.color.rgb = COLOR_BLUE

    tf6_r = box6_r.text_frame
    tf6_r.word_wrap = True
    tf6_r.margin_left = Inches(0.25)
    tf6_r.margin_top = Inches(0.2)

    p = tf6_r.paragraphs[0]
    p.text = "PARTICIPACIÓN Y COMPORTAMIENTO OMNICANAL:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    channels = [
        ("Tienda Física (68.0%):", "$891.76M | 95,152 tickets | Ticket: $9,372.00 | Margen: 21.43%"),
        ("Portal Web (22.1%):", "$290.22M | 30,970 tickets | Ticket: $9,371.08 | Margen: 21.39%"),
        ("App Móvil (9.8%):", "$128.76M | 13,878 tickets | Ticket: $9,277.96 | Margen: 21.47%")
    ]
    for c_title, c_stats in channels:
        p = tf6_r.add_paragraph()
        run1 = p.add_run()
        run1.text = f"\n• {c_title} "
        run1.font.bold = True
        run1.font.size = Pt(10)
        run1.font.color.rgb = COLOR_NAVY

        run2 = p.add_run()
        run2.text = f"\n  {c_stats}"
        run2.font.size = Pt(9)
        run2.font.color.rgb = COLOR_SLATE

    p = tf6_r.add_paragraph()
    p.text = "\n💡 INSIGHT DE OMNICANALIDAD:\nEl ticket promedio y el margen son homogéneos en todos los canales (~$9,370 MXN). El cliente digital tiene el mismo valor transaccional; la oportunidad estratégica es acelerar la App para ganar cuota digital."
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN

    # ==========================================================================
    # SLIDE 7: CALIDAD Y COSTO DE DEVOLUCIONES
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Diagnóstico de Calidad: Fuga de Recursos en Devoluciones")
    add_footer(s7, 7)

    # 3 Cards de Devoluciones
    add_card(s7, Inches(0.8), Inches(1.4), Inches(3.7), Inches(1.3), "Eventos de Devolución", "9,952", "Reembolsos procesados", COLOR_RED)
    add_card(s7, Inches(4.8), Inches(1.4), Inches(3.7), Inches(1.3), "Monto Total Devuelto", "$22,897,836.87", "Costo directo de no calidad", COLOR_RED)
    add_card(s7, Inches(8.8), Inches(1.4), Inches(3.7), Inches(1.3), "Tasa de Devolución", "1.63%", "Sobre venta bruta total", COLOR_GOLD)

    # Tabla de Motivos
    t_dev_shape = s7.shapes.add_table(6, 4, Inches(0.8), Inches(2.9), Inches(11.733), Inches(2.2))
    t_dev = t_dev_shape.table

    h_dev = ["Motivo de Devolución", "Eventos", "Piezas Retornadas", "Importe Reembolsado ($ MXN)"]
    for c_idx, h in enumerate(h_dev):
        cell = t_dev.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    dev_data = [
        ("Otro Motivo / No Especificado", "2,020", "2,795", "$4,729,914.86"),
        ("Talla / Compatibilidad de Espacio", "2,008", "2,753", "$4,665,625.86"),
        ("No era lo esperado (diferencia foto/realidad)", "2,027", "2,807", "$4,580,798.65"),
        ("Daño Físico en Transporte", "1,983", "2,706", "$4,499,455.27"),
        ("Defecto de Fabricación", "1,914", "2,651", "$4,422,042.23")
    ]
    for r_idx, r_data in enumerate(dev_data, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_dev.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_SLATE
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else (PP_ALIGN.CENTER if c_idx in (1, 2) else PP_ALIGN.RIGHT)

    # Llamado de Atención
    box7_callout = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.4))
    box7_callout.fill.solid()
    box7_callout.fill.fore_color.rgb = COLOR_LIGHT_BG
    box7_callout.line.color.rgb = COLOR_RED

    tf7_c = box7_callout.text_frame
    tf7_c.word_wrap = True
    tf7_c.margin_left = Inches(0.25)
    tf7_c.margin_top = Inches(0.12)

    p = tf7_c.paragraphs[0]
    p.text = "ALERTA OPERACIONAL — IMPACTO EN CADENA LOGÍSTICA:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p = tf7_c.add_paragraph()
    p.text = "• Daños y Defectos suman casi $9.0M MXN (39.0% del total): Falla directa atribuible a embalaje y manipulación de transportistas."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_SLATE

    p = tf7_c.add_paragraph()
    p.text = "• Devoluciones por 'Talla' y 'No era lo esperado' ($9.2M MXN): Indican falta de visualización precisa y dimensiones claras en la tienda web y app."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 8: LOGÍSTICA DE INSTALACIONES Y SLA
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Experiencia de Cliente: Cuello de Botella en Instalaciones")
    add_footer(s8, 8)

    # 4 Cards SLA
    add_card(s8, Inches(0.8), Inches(1.4), Inches(2.7), Inches(1.3), "Servicios Auditados", "6,500", "Órdenes de instalación", COLOR_NAVY)
    add_card(s8, Inches(3.7), Inches(1.4), Inches(2.7), Inches(1.3), "Cumplimiento SLA", "34.77%", "¡ALERTA CRÍTICA!", COLOR_RED)
    add_card(s8, Inches(6.6), Inches(1.4), Inches(2.7), Inches(1.3), "Retraso Promedio", "+3.8 Días", "Varianza real vs pactada", COLOR_RED)
    add_card(s8, Inches(9.5), Inches(1.4), Inches(2.7), Inches(1.3), "Satisfacción Promedio", "2.98 / 5.0", "CSAT severamente dañado", COLOR_GOLD)

    # Tabla Top 5 Sucursales con Peor SLA
    t_sla_shape = s8.shapes.add_table(6, 5, Inches(0.8), Inches(2.9), Inches(11.733), Inches(2.2))
    t_sla = t_sla_shape.table

    h_sla = ["Sucursal Crítica", "Servicios Totales", "Cumplimiento SLA %", "Días Retraso Promedio", "Satisfacción (1-5)"]
    for c_idx, h in enumerate(h_sla):
        cell = t_sla.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    sla_top5 = [
        ("Sucursal Monterrey 11", "408", "29.66%", "4.2 días", "3.05"),
        ("Sucursal Santa Catarina 6", "392", "34.18%", "3.6 días", "2.94"),
        ("Sucursal Escobedo 5", "408", "34.31%", "3.8 días", "3.04"),
        ("Sucursal Apodaca 2", "432", "34.72%", "3.7 días", "2.86"),
        ("Sucursal Guadalupe 4", "431", "35.03%", "3.8 días", "2.98")
    ]
    for r_idx, r_data in enumerate(sla_top5, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_sla.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_RED if c_idx == 2 else COLOR_SLATE
            p.font.bold = True if c_idx in (0, 2) else False
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER

    # Llamado
    box8_callout = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.4))
    box8_callout.fill.solid()
    box8_callout.fill.fore_color.rgb = COLOR_LIGHT_BG
    box8_callout.line.color.rgb = COLOR_RED

    tf8_c = box8_callout.text_frame
    tf8_c.word_wrap = True
    tf8_c.margin_left = Inches(0.25)
    tf8_c.margin_top = Inches(0.12)

    p = tf8_c.paragraphs[0]
    p.text = "CORRELACIÓN DIRECTA ENTRE RETRASO LOGÍSTICO Y PÉRDIDA DE CLIENTES:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED

    p = tf8_c.add_paragraph()
    p.text = "• El 65.23% de las instalaciones no se entregan en la fecha pactada, generando fricción inmediata post-venta."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_SLATE

    p = tf8_c.add_paragraph()
    p.text = "• En sucursales con retrasos superiores a 4 días, la satisfacción cae por debajo de 3 estrellas, detonando cancelaciones y daño reputacional."
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 9: CADENA DE SUMINISTRO E INVENTARIOS
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Cadena de Suministro: Roturas de Stock vs Capital Inmovilizado")
    add_footer(s9, 9)

    # 3 Cards Inventario
    add_card(s9, Inches(0.8), Inches(1.4), Inches(3.7), Inches(1.3), "Rotura Total de Stock", "126 Ítems (Stock = 0)", "2,738 piezas en déficit", COLOR_RED)
    add_card(s9, Inches(4.8), Inches(1.4), Inches(3.7), Inches(1.3), "En Alerta de Reorden", "2,566 Ítems", "$43.4M MXN en riesgo", COLOR_GOLD)
    add_card(s9, Inches(8.8), Inches(1.4), Inches(3.7), Inches(1.3), "Inventario Excedente", "$2,330 Millones", "Capital inmovilizado", COLOR_BLUE)

    # Tabla Comparativa de Estatus de Inventario
    t_inv_shape = s9.shapes.add_table(4, 5, Inches(0.8), Inches(2.9), Inches(11.733), Inches(1.8))
    t_inv = t_inv_shape.table

    h_inv = ["Estatus de Stock", "Registros", "Piezas en Almacén", "Déficit frente a Umbral", "Valoración a Costo ($ MXN)"]
    for c_idx, h in enumerate(h_inv):
        cell = t_inv.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

    inv_display = [
        ("Rotura de Stock", "126", "0", "2,738 piezas", "$0.00 (Venta Perdida)"),
        ("Alerta de Reorden", "2,566", "34,668", "33,908 piezas", "$43,416,695.15"),
        ("Óptimo / Sobreinventario", "18,748", "1,878,247", "0 piezas", "$2,330,299,782.35")
    ]
    for r_idx, r_data in enumerate(inv_display, start=1):
        for c_idx, val in enumerate(r_data):
            cell = t_inv.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else COLOR_CARD
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9)
            p.font.color.rgb = COLOR_SLATE
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else (PP_ALIGN.CENTER if c_idx in (1, 3) else PP_ALIGN.RIGHT)

    # Diagnóstico de Compras
    box9_callout = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.9), Inches(11.733), Inches(1.8))
    box9_callout.fill.solid()
    box9_callout.fill.fore_color.rgb = COLOR_LIGHT_BG
    box9_callout.line.color.rgb = COLOR_GOLD

    tf9_c = box9_callout.text_frame
    tf9_c.word_wrap = True
    tf9_c.margin_left = Inches(0.25)
    tf9_c.margin_top = Inches(0.15)

    p = tf9_c.paragraphs[0]
    p.text = "DIAGNÓSTICO DE COMPRAS Y DESEMPEÑO DE PROVEEDORES:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY

    p = tf9_c.add_paragraph()
    p.text = "• 1,348 órdenes de compra en estatus 'Pendiente' con lead times de hasta 28 días estrangulan el abasto de muebles en tiendas de alto tráfico."
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_SLATE

    p = tf9_c.add_paragraph()
    p.text = "• Existe una severa asimetría: capital atrapado en $2,330M de inventario de baja rotación mientras 126 productos esenciales sufren rotura de stock."
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_SLATE

    # ==========================================================================
    # SLIDE 10: CONCLUSIONES Y RECOMENDACIONES (HOJA DE RUTA)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Hoja de Ruta Estratégica: 5 Recomendaciones Accionables")
    add_footer(s10, 10)

    recs = [
        ("1. Rediseño Operativo del SLA de Instalaciones", "Contratar cuadrillas logísticas regionales dedicadas y optimizar rutas. Meta: pasar de 34.7% a 85% de cumplimiento en 90 días (+1.5 pts CSAT).", COLOR_RED),
        ("2. Protocolo de Inspección en Muelle y Embalaje Reforzado", "Certificar empaques con proveedores y penalizar defectos. Meta: reducir en 40% las devoluciones por daño/defecto (Ahorro: ~$9.2M MXN anuales).", COLOR_GOLD),
        ("3. Algoritmo Dinámico de Reorden y Rebalanceo de Stock", "Conectar el Data Mart para calcular puntos de reorden según velocidad de venta semanal por tienda. Eliminar las 126 roturas de stock y liberar capital.", COLOR_BLUE),
        ("4. Aceleración Comercial de la App Móvil con AR/3D", "Incorporar visor de muebles en realidad aumentada en la App para resolver el motivo 'talla/espacio' ($4.6M devueltos) y duplicar cuota digital al 20%.", COLOR_GREEN),
        ("5. Gobernanza Analítica Continua con Power Pivot / DAX", "Institucionalizar las reuniones de Comité Directivo basadas en este Data Mart de MySQL y el Tablero Excel como única fuente auditada de la verdad.", COLOR_NAVY)
    ]

    top_r = 1.4
    for title, desc, col in recs:
        r_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top_r), Inches(11.733), Inches(0.95))
        r_box.fill.solid()
        r_box.fill.fore_color.rgb = COLOR_CARD
        r_box.line.color.rgb = col
        r_box.line.width = Pt(1.5)

        tf_r = r_box.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = Inches(0.2)
        tf_r.margin_top = Inches(0.1)

        p = tf_r.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf_r.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = COLOR_SLATE

        top_r += 1.05

    # Guardar
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    prs.save(OUT_FILE)
    print(f"✅ Presentación Ejecutiva generada exitosamente (10 slides): {OUT_FILE}")


if __name__ == "__main__":
    generate_deck()
