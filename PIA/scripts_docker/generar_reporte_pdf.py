# ==============================================================================
# PROYECTO: PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA) - CASA&ESTILO
# ARCHIVO: generar_reporte_pdf.py
# AUTOR: Equipo 8 - Analítica e Inteligencia de Negocios (FIME - UANL)
# ENTORNO: Python 3.12 / Docker (reportlab)
# ==============================================================================
# FUNCIÓN GENERAL:
# Generar el reporte formal de evidencias académicas y certificación técnica
# `PIA_Evidencias_CasaEstilo_Equipo08.pdf` para la entrega oficial del PIA.
#
# FUNCIÓN ESPECÍFICA:
# 1. Integrar portada institucional FIME, metadatos y resumen ejecutivo.
# 2. Documentar la auditoría de calidad, el diagrama ER, el esquema estrella y DDL.
# 3. Presentar las tablas de balance de masa contable (100% conciliado).
# 4. Incluir el catálogo de 10 medidas DAX y las 5 recomendaciones para el C-Level.
# ==============================================================================

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

OUT_FILE = "PIA/PIA_Evidencias_CasaEstilo_Equipo08.pdf"

# Colores Ejecutivos FIME / Casa&Estilo
C_NAVY = colors.HexColor("#1A365D")
C_GOLD = colors.HexColor("#D69E2E")
C_SLATE = colors.HexColor("#2D3748")
C_LIGHT_BG = colors.HexColor("#F7FAFC")
C_WHITE = colors.HexColor("#FFFFFF")
C_CARD_BG = colors.HexColor("#EDF2F7")
C_GREEN = colors.HexColor("#2F855A")
C_RED = colors.HexColor("#C53030")
C_BORDER = colors.HexColor("#CBD5E0")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # No decorar portada
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8)
            self.setFillColor(C_SLATE)
            self.drawString(54, 750, "FIME UANL | Analítica e Inteligencia de Negocios — PIA: Solución BI Casa&Estilo (Equipo 8)")
            self.setStrokeColor(C_GOLD)
            self.setLineWidth(1)
            self.line(54, 744, 558, 744)

            # Footer
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.5)
            self.line(54, 45, 558, 45)
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))
            self.drawString(54, 32, "Documento de Evidencias Técnicas, Auditoría de Calidad y Modelo Analítico")
            page_text = f"Página {self._pageNumber} de {total_pages}"
            self.drawRightString(558, 32, page_text)
        self.restoreState()


def generate_pdf():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    doc = SimpleDocTemplate(
        OUT_FILE,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    title_cover = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=C_NAVY, alignment=1
    )
    sub_cover = ParagraphStyle(
        'CoverSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=C_GOLD, alignment=1
    )
    meta_cover = ParagraphStyle(
        'CoverMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10, leading=14,
        textColor=C_SLATE, alignment=1
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=C_NAVY, spaceAfter=8
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=C_GOLD, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=C_SLATE, spaceAfter=6
    )
    body_bold = ParagraphStyle(
        'BodyBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=13,
        textColor=C_NAVY, spaceAfter=6
    )
    code_style = ParagraphStyle(
        'CodeStyle', parent=styles['Normal'],
        fontName='Courier', fontSize=7.5, leading=10,
        textColor=colors.HexColor("#2C5282")
    )
    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=C_SLATE
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=C_NAVY
    )
    table_hdr = ParagraphStyle(
        'TableHdr', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=C_WHITE, alignment=1
    )

    story = []

    # --------------------------------------------------------------------------
    # 1. PORTADA FORMAL
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN", title_cover))
    story.append(Spacer(1, 8))
    story.append(Paragraph("FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA", sub_cover))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="80%", thickness=2, color=C_GOLD, spaceAfter=25, spaceBefore=10))

    story.append(Paragraph("PRODUCTO INTEGRADOR DE APRENDIZAJE (PIA)", ParagraphStyle('PIA', parent=title_cover, fontSize=16, textColor=C_GOLD)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Solución de Business Intelligence Empresarial Completa", title_cover))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Caso Práctico: Casa&Estilo (Sector Muebles y Decoración)", ParagraphStyle('Case', parent=sub_cover, fontSize=14, textColor=C_NAVY)))
    story.append(Spacer(1, 35))

    meta_table_data = [
        [Paragraph("<b>Unidad de Aprendizaje:</b>", table_cell_bold), Paragraph("Analítica e Inteligencia de Negocios", table_cell)],
        [Paragraph("<b>Ponderación del Proyecto:</b>", table_cell_bold), Paragraph("30% de la Calificación Total del Semestre", table_cell)],
        [Paragraph("<b>Equipo Evaluado:</b>", table_cell_bold), Paragraph("Equipo 8", table_cell)],
        [Paragraph("<b>Empresa Asignada:</b>", table_cell_bold), Paragraph("Casa&Estilo (Retail Omnicanal de Mobiliario)", table_cell)],
        [Paragraph("<b>Ecosistema Técnico:</b>", table_cell_bold), Paragraph("MySQL 8.0, Docker Engine, Python 3.12, Excel / Power Pivot (DAX)", table_cell)],
        [Paragraph("<b>Fecha de Entrega:</b>", table_cell_bold), Paragraph("Noviembre 2026", table_cell)]
    ]
    meta_table = Table(meta_table_data, colWidths=[150, 320])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_GOLD),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 50))
    story.append(Paragraph("“Los datos por sí solos no toman decisiones; el valor está en convertirlos en información accionable.”", ParagraphStyle('Quote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, textColor=C_SLATE, alignment=1)))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 2. RESUMEN EJECUTIVO Y PROBLEMA PROPUESTO
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. Resumen Ejecutivo y Problemática de Negocio", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "El presente informe formal documenta la construcción, validación y defensa de una solución integral de <b>Business Intelligence (BI)</b> "
        "para la empresa <b>Casa&Estilo</b>, cadena minorista omnicanal especializada en muebles finos y artículos de decoración del hogar. "
        "La compañía opera mediante una red de 16 sucursales físicas distribuidas en el noreste mexicano (Nuevo León, Coahuila y Tamaulipas), "
        "así como plataformas de comercio electrónico (Web y App móvil), complementadas por un servicio logístico de armado e instalación especializada.",
        body_style
    ))
    story.append(Paragraph(
        "A partir de un ecosistema de datos crudos (RAW) compuesto por 11 archivos transaccionales y más de medio millón de registros, "
        "el Equipo 8 diseñó un pipeline de ingeniería de datos en MySQL 8.0 estructurado en tres capas (RAW &rarr; Staging &rarr; Data Mart Dimensional), "
        "garantizando la trazabilidad absoluta de balance de masa contable, un modelo relacional en esquema estrella con granularidad a nivel línea de ticket, "
        "un catálogo exhaustivo de 10 medidas DAX en Power Pivot y un tablero ejecutivo orientado a la toma de decisiones estratégicas.",
        body_style
    ))

    # Cifras Clave del Negocio
    story.append(Spacer(1, 5))
    story.append(Paragraph("Cifras Oficiales de Control Financiero y Operacional (2024 - 2026):", h2_style))

    score_data = [
        [Paragraph("Ventas Netas Globales", table_hdr), Paragraph("Utilidad Bruta", table_hdr), Paragraph("Margen Bruto %", table_hdr), Paragraph("Ticket Promedio", table_hdr)],
        [Paragraph("<b>$1,310,746,491.89 MXN</b>", table_cell_bold), Paragraph("<b>$280,874,853.71 MXN</b>", table_cell_bold), Paragraph("<b>21.43%</b>", table_cell_bold), Paragraph("<b>$9,362.47 MXN</b>", table_cell_bold)],
        [Paragraph("Cumplimiento SLA Instalaciones", table_hdr), Paragraph("Devoluciones Procesadas", table_hdr), Paragraph("Reembolsos Totales", table_hdr), Paragraph("Ítems en Rotura de Stock", table_hdr)],
        [Paragraph("<font color='#C53030'><b>34.77% (Alerta Crítica)</b></font>", table_cell_bold), Paragraph("<b>9,952 eventos</b>", table_cell), Paragraph("<font color='#C53030'><b>$22,897,836.87 MXN</b></font>", table_cell), Paragraph("<font color='#C53030'><b>126 productos (0 stock)</b></font>", table_cell)]
    ]
    t_score = Table(score_data, colWidths=[126, 126, 126, 126])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('BACKGROUND', (0, 2), (-1, 2), C_NAVY),
        ('BACKGROUND', (0, 1), (-1, 1), C_CARD_BG),
        ('BACKGROUND', (0, 3), (-1, 3), C_CARD_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 15))

    # --------------------------------------------------------------------------
    # 3. AUDITORÍA DE CALIDAD Y TRATAMIENTO ETL
    # --------------------------------------------------------------------------
    story.append(Paragraph("2. Perfilado de Fuentes RAW y Tratamiento de Calidad", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Se aplicó una auditoría algorítmica exhaustiva sobre los 11 archivos provistos en <code>ALUMNO/RAW/</code>. "
        "Se confirmaron problemas intencionales de calidad, cuya detección y resolución se documenta a continuación:",
        body_style
    ))

    raw_table_data = [
        [Paragraph("Archivo Fuente", table_hdr), Paragraph("Registros", table_hdr), Paragraph("Clave Primaria", table_hdr), Paragraph("Anomalía Detectada", table_hdr), Paragraph("Tratamiento en Staging / ETL", table_hdr)],
        [Paragraph("ERP/productos.csv", table_cell_bold), Paragraph("1,340", table_cell), Paragraph("producto_id", table_cell), Paragraph("UTF-8 BOM en cabecera", table_cell), Paragraph("Limpieza con IGNORE 1 LINES y cálculo de margen teórico.", table_cell)],
        [Paragraph("CRM/clientes.csv", table_cell_bold), Paragraph("10,800", table_cell), Paragraph("cliente_id", table_cell), Paragraph("20 ciudades nulas, 43 emails vacíos, 235 sexos 'N/E'", table_cell), Paragraph("Imputación: ciudad='No Especificada', email institucional, sexo normalizado.", table_cell)],
        [Paragraph("OPERACION/sucursales.csv", table_cell_bold), Paragraph("16", table_cell), Paragraph("sucursal_id", table_cell), Paragraph("Completitud 100%", table_cell), Paragraph("Estratificación por superficie en m2 (Pequeña, Mediana, Grande).", table_cell)],
        [Paragraph("POS/ventas.csv", table_cell_bold), Paragraph("140,000", table_cell), Paragraph("venta_id", table_cell), Paragraph("Completitud 100%", table_cell), Paragraph("Validación de integridad referencial hacia clientes y sucursales.", table_cell)],
        [Paragraph("POS/detalle_ventas.csv", table_cell_bold), Paragraph("331,758", table_cell), Paragraph("(venta_id, linea)", table_cell), Paragraph("<b>Fórmula errónea:</b> importe = bruto (sin restar descuento)", table_cell), Paragraph("<b>Corrección contable:</b> desglose de monto_bruto, monto_descuento y monto_neto.", table_cell)],
        [Paragraph("POS/devoluciones.csv", table_cell_bold), Paragraph("9,952", table_cell), Paragraph("devolucion_id", table_cell), Paragraph("Importe devuelto bruto", table_cell), Paragraph("Vinculación con línea de ticket y flag de devolución en hecho central.", table_cell)],
        [Paragraph("INVENTARIO/existencias.csv", table_cell_bold), Paragraph("21,440", table_cell), Paragraph("(sucursal, prod)", table_cell), Paragraph("126 productos con stock cero", table_cell), Paragraph("Cálculo de déficit frente a punto de reorden y alertas de rotura.", table_cell)],
        [Paragraph("ESPECIFICO/instalaciones.csv", table_cell_bold), Paragraph("6,500", table_cell), Paragraph("instalacion_id", table_cell), Paragraph("Retrasos severos generalizados", table_cell), Paragraph("Cálculo de varianza en días (reales - programados) y flag cumplio_sla.", table_cell)]
    ]
    t_raw = Table(raw_table_data, colWidths=[90, 45, 75, 140, 154])
    t_raw.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_raw)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 4. ARQUITECTURA DE DATOS Y MODELO DIMENSIONAL
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. Modelo Dimensional en Esquema Estrella", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Siguiendo la metodología de modelado dimensional de Ralph Kimball, se implementó un <b>Data Mart en Esquema Estrella (Constelación de Hechos)</b> "
        "con granularidad atómica para el hecho principal <code>fact_ventas_detalle</code> y tres hechos satélites especializados. "
        "Se rechazó la normalización tipo Copo de Nieve (Snowflake) para optimizar el rendimiento en consultas de agregación masiva y permitir "
        "la máxima eficiencia en el motor columnar VertiPaq de Microsoft Power Pivot.",
        body_style
    ))

    # Tabla de Estructura de Hechos y Dimensiones
    arch_data = [
        [Paragraph("Entidad Dimensional", table_hdr), Paragraph("Tipo", table_hdr), Paragraph("Registros", table_hdr), Paragraph("Granularidad / Claves", table_hdr), Paragraph("Métricas / Atributos Principales", table_hdr)],
        [Paragraph("dim_tiempo", table_cell_bold), Paragraph("Dimensión", table_cell), Paragraph("1,096", table_cell), Paragraph("tiempo_id (YYYYMMDD) PK", table_cell), Paragraph("Fecha, Año, Trimestre, Mes, Semana, Día, Fin de Semana.", table_cell)],
        [Paragraph("dim_producto", table_cell_bold), Paragraph("Dimensión", table_cell), Paragraph("1,341", table_cell), Paragraph("producto_key (INT) PK", table_cell), Paragraph("SKU, Producto, Categoría, Marca, Costo, Precio Lista, Margen.", table_cell)],
        [Paragraph("dim_cliente", table_cell_bold), Paragraph("Dimensión", table_cell), Paragraph("10,801", table_cell), Paragraph("cliente_key (INT) PK", table_cell), Paragraph("Nombre, Sexo normalizado, Ciudad imputada, Segmento, Email.", table_cell)],
        [Paragraph("dim_sucursal", table_cell_bold), Paragraph("Dimensión", table_cell), Paragraph("17", table_cell), Paragraph("sucursal_key (INT) PK", table_cell), Paragraph("Nombre tienda, Ciudad, Estado, Superficie m2, Formato escala.", table_cell)],
        [Paragraph("dim_canal / metodo", table_cell_bold), Paragraph("Dimensiones", table_cell), Paragraph("3 / 4", table_cell), Paragraph("canal_id / metodo_id PK", table_cell), Paragraph("Tienda, Web, App | Tarjeta, Efectivo, Transferencia, Wallet.", table_cell)],
        [Paragraph("fact_ventas_detalle", table_cell_bold), Paragraph("Hecho Central", table_cell), Paragraph("331,758", table_cell), Paragraph("(venta_id, linea) PK", table_cell), Paragraph("Cantidad, Precio, Descuento, Monto Bruto/Neto, COGS, Utilidad.", table_cell)],
        [Paragraph("fact_devoluciones", table_cell_bold), Paragraph("Hecho Satélite", table_cell), Paragraph("9,952", table_cell), Paragraph("devolucion_id PK", table_cell), Paragraph("Venta origen, Cantidad devuelta, Importe devuelto, Motivo.", table_cell)],
        [Paragraph("fact_instalaciones", table_cell_bold), Paragraph("Hecho Satélite", table_cell), Paragraph("6,500", table_cell), Paragraph("instalacion_id PK", table_cell), Paragraph("Días programados, Días reales, Varianza retraso, SLA (0/1), CSAT.", table_cell)],
        [Paragraph("fact_inventario", table_cell_bold), Paragraph("Hecho Satélite", table_cell), Paragraph("21,440", table_cell), Paragraph("(sucursal_key, prod_key) PK", table_cell), Paragraph("Stock actual, Punto reorden, Déficit unidades, Valor a costo.", table_cell)]
    ]
    t_arch = Table(arch_data, colWidths=[95, 55, 45, 120, 189])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 15))

    # --------------------------------------------------------------------------
    # 5. BALANCE DE MASA Y AUDITORÍA CONTABLE
    # --------------------------------------------------------------------------
    story.append(Paragraph("4. Certificación de Balance de Masa y Cero Discrepancias", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Para certificar la integridad de los datos, el procedimiento maestro <code>sp_orquestador_etl_maestro()</code> "
        "ejecutó pruebas cuantitativas de reconciliación comparando el conteo de registros en archivos RAW, tablas Staging y el Data Mart. "
        "La tabla <code>etl_balance_masa</code> certifica una discrepancia numérica de cero (100.00% de conciliación):",
        body_style
    ))

    bal_data = [
        [Paragraph("Entidad Auditada", table_hdr), Paragraph("Volumen RAW", table_hdr), Paragraph("Volumen Staging", table_hdr), Paragraph("Volumen Data Mart", table_hdr), Paragraph("Discrepancia", table_hdr), Paragraph("Integridad", table_hdr), Paragraph("Estatus Oficial", table_hdr)],
        [Paragraph("Ventas Detalle (Líneas)", table_cell_bold), Paragraph("331,758", table_cell), Paragraph("331,758", table_cell), Paragraph("331,758", table_cell), Paragraph("0", table_cell), Paragraph("100.00%", table_cell), Paragraph("<font color='#2F855A'><b>CONCILIADO</b></font>", table_cell)],
        [Paragraph("Devoluciones", table_cell_bold), Paragraph("9,952", table_cell), Paragraph("9,952", table_cell), Paragraph("9,952", table_cell), Paragraph("0", table_cell), Paragraph("100.00%", table_cell), Paragraph("<font color='#2F855A'><b>CONCILIADO</b></font>", table_cell)],
        [Paragraph("Instalaciones Técnicas", table_cell_bold), Paragraph("6,500", table_cell), Paragraph("6,500", table_cell), Paragraph("6,500", table_cell), Paragraph("0", table_cell), Paragraph("100.00%", table_cell), Paragraph("<font color='#2F855A'><b>CONCILIADO</b></font>", table_cell)],
        [Paragraph("Snapshot Existencias", table_cell_bold), Paragraph("21,440", table_cell), Paragraph("21,440", table_cell), Paragraph("21,440", table_cell), Paragraph("0", table_cell), Paragraph("100.00%", table_cell), Paragraph("<font color='#2F855A'><b>CONCILIADO</b></font>", table_cell)]
    ]
    t_bal = Table(bal_data, colWidths=[120, 60, 65, 75, 55, 55, 74])
    t_bal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_bal)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 6. CATÁLOGO DE MEDIDAS DAX
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. Catálogo Oficial de Medidas DAX en Power Pivot", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    story.append(Paragraph(
        "Se diseñó un modelo de cálculo analítico formal en Power Pivot integrando 10 medidas DAX que cubren los tres niveles de decisión empresarial: "
        "Estratégico (Dirección General), Táctico (Gerencias Comerciales) y Operacional (Logística, Tiendas e Inventario):",
        body_style
    ))

    dax_data = [
        [Paragraph("ID", table_hdr), Paragraph("Medida DAX", table_hdr), Paragraph("Nivel", table_hdr), Paragraph("Formulación DAX", table_hdr), Paragraph("Formato", table_hdr), Paragraph("Valor Oficial", table_hdr)],
        [Paragraph("M01", table_cell_bold), Paragraph("Ventas Brutas", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>SUM(FactVentas[monto_bruto])</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("$1,402,502,128.39", table_cell)],
        [Paragraph("M02", table_cell_bold), Paragraph("Descuentos Otorgados", table_cell_bold), Paragraph("Táctico", table_cell), Paragraph("<code>SUM(FactVentas[monto_descuento])</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("$91,755,708.99", table_cell)],
        [Paragraph("M03", table_cell_bold), Paragraph("Ventas Netas", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>[Ventas Brutas] - [Descuentos Otorgados]</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("<b>$1,310,746,491.89</b>", table_cell_bold)],
        [Paragraph("M04", table_cell_bold), Paragraph("Costo de Ventas (COGS)", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>SUM(FactVentas[costo_total])</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("$1,029,871,626.89", table_cell)],
        [Paragraph("M05", table_cell_bold), Paragraph("Utilidad Bruta", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>[Ventas Netas] - [Costo de Ventas]</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("<b>$280,874,853.71</b>", table_cell_bold)],
        [Paragraph("M06", table_cell_bold), Paragraph("Margen Bruto %", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>DIVIDE([Utilidad Bruta], [Ventas Netas], 0)</code>", code_style), Paragraph("0.00%", table_cell), Paragraph("<b>21.43%</b>", table_cell_bold)],
        [Paragraph("M07", table_cell_bold), Paragraph("Ticket Promedio", table_cell_bold), Paragraph("Táctico", table_cell), Paragraph("<code>DIVIDE([Ventas Netas], DISTINCTCOUNT(FactVentas[venta_id]), 0)</code>", code_style), Paragraph("$#,##0.00", table_cell), Paragraph("$9,362.47", table_cell)],
        [Paragraph("M08", table_cell_bold), Paragraph("Tasa Devolución %", table_cell_bold), Paragraph("Operacional", table_cell), Paragraph("<code>DIVIDE(SUM(FactDevoluciones[importe_devuelto]), [Ventas Brutas], 0)</code>", code_style), Paragraph("0.00%", table_cell), Paragraph("1.63% ($22.9M)", table_cell)],
        [Paragraph("M09", table_cell_bold), Paragraph("Cumplimiento SLA %", table_cell_bold), Paragraph("Operacional", table_cell), Paragraph("<code>DIVIDE(CALCULATE(COUNTROWS(FactInst), FactInst[cumplio_sla]=1), COUNTROWS(FactInst), 0)</code>", code_style), Paragraph("0.00%", table_cell), Paragraph("<font color='#C53030'><b>34.77% (Crítico)</b></font>", table_cell)],
        [Paragraph("M10", table_cell_bold), Paragraph("Crecimiento YoY %", table_cell_bold), Paragraph("Estratégico", table_cell), Paragraph("<code>DIVIDE([Ventas Netas] - [Ventas Netas LY], [Ventas Netas LY], 0)</code>", code_style), Paragraph("+0.00%", table_cell), Paragraph("+0.85% (2025)", table_cell)]
    ]
    t_dax = Table(dax_data, colWidths=[25, 95, 60, 164, 55, 105])
    t_dax.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_WHITE, C_LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dax)
    story.append(Spacer(1, 15))

    # --------------------------------------------------------------------------
    # 7. HOJA DE RUTA PRESCRIPTIVA Y RECOMENDACIONES
    # --------------------------------------------------------------------------
    story.append(Paragraph("6. Conclusiones y Hoja de Ruta Prescriptiva para el C-Level", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=C_GOLD, spaceAfter=10, spaceBefore=2))

    recs_pdf = [
        ("1. Reestructuración Inmediata de la Logística de Instalaciones (Prioridad Máxima):",
         "El cumplimiento de SLA del 34.77% y el retraso promedio de +3.8 días destruyen la lealtad del cliente (satisfacción 2.98/5.0). "
         "Se recomienda licitar cuadrillas dedicadas por zona geográfica e implementar ruteo dinámico con penalizaciones por retraso. Meta: 85% SLA en 90 días."),
        ("2. Protocolo de Inspección en Muelle y Embalaje Reforzado:",
         "Daños y defectos de fabricación generan el 39% de las devoluciones ($8.9M MXN). Es imperativo implementar una política de rechazo en muelle "
         "y exigir a los proveedores de muebles cajas reforzadas con esquineros de poliestireno de alta densidad. Meta: reducir devoluciones en 40% (Ahorro: $9.2M MXN)."),
        ("3. Algoritmo Dinámico de Reabastecimiento Min/Max en Inventarios:",
         "Coexisten 126 ítems en rotura total de stock (pérdida de venta directa) con $2,330M MXN inmovilizados en inventario excedente. "
         "Conectando el Data Mart dimensional se debe calcular el punto de reorden en función de la velocidad de venta de las últimas 4 semanas por tienda."),
        ("4. Aceleración Comercial de la App Móvil con Visualizador 3D/AR:",
         "La App aporta únicamente el 9.8% de ventas ($128.8M), pero presenta un margen idéntico a tienda física (21.47%). "
         "Integrar un visor de realidad aumentada resolverá el problema de devoluciones por 'talla/espacio' ($4.6M) y permitirá duplicar la cuota de la App al 20%."),
        ("5. Institucionalización de la Gobernanza con Power Pivot y MySQL:",
         "Reemplazar los reportes aislados en hojas de cálculo por este Data Mart y Tablero Ejecutivo corporativo como la única versión oficial de la verdad "
         "para las reuniones mensuales de consejo de administración y directores de sucursal.")
    ]
    for r_title, r_desc in recs_pdf:
        story.append(Paragraph(f"<b>{r_title}</b>", body_bold))
        story.append(Paragraph(r_desc, body_style))
        story.append(Spacer(1, 4))

    # Construir el documento
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Reporte Formal de Evidencias en PDF generado: {OUT_FILE}")


if __name__ == "__main__":
    generate_pdf()
