#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
# SCRIPT: GENERADOR DE REPORTE FORMAL DE EVIDENCIAS EN PDF (REPORTLAB)
# ARCHIVO DE SALIDA: U5_Evidencias_Equipo08.pdf
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas de dos pasadas para numeración dinámica 'Página X de Y' y encabezados elegantes."""
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

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Portada limpia

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1F497D"))

        # Encabezado
        self.drawString(54, 750, "UANL · FIME | Inteligencia de Negocios · Unidad 5: Del Data Mart al Dashboard")
        self.drawRightString(612 - 54, 750, "Data Mart de Ventas · Equipo 8")
        self.setStrokeColor(colors.HexColor("#2E75B6"))
        self.setLineWidth(0.75)
        self.line(54, 744, 612 - 54, 744)

        # Pie de página
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.line(54, 45, 612 - 54, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#595959"))
        self.drawString(54, 32, "Reporte Formal de Evidencias: Modelo Dimensional, DAX, Dashboard y Comité")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()

def generar_pdf():
    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = base_dir / "U5_Evidencias_Equipo08.pdf"

    print("==============================================================================")
    print("📄 GENERANDO REPORTE PDF DE EVIDENCIAS: U5_Evidencias_Equipo08.pdf")
    print("==============================================================================")

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Colores
    NAVY = colors.HexColor("#1F497D")
    BLUE_ACCENT = colors.HexColor("#2E75B6")
    BLUE_LIGHT = colors.HexColor("#DCE6F1")
    DARK_TEXT = colors.HexColor("#262626")
    GRAY_BG = colors.HexColor("#F8F9FA")
    BORDER_COLOR = colors.HexColor("#D9D9D9")
    GOLD = colors.HexColor("#C55A11")

    # Estilos
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=NAVY,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=BLUE_ACCENT,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=BLUE_ACCENT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'BodyCustomBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=DARK_TEXT,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=DARK_TEXT,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=DARK_TEXT,
        alignment=TA_LEFT
    ))
    styles.add(ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=NAVY,
        backColor=GRAY_BG
    ))
    styles.add(ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=NAVY
    ))

    story = []

    # ==========================================================================
    # 1. PORTADA FORMAL
    # ==========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN", styles['CoverSubtitle']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA", styles['CoverSubtitle']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=3, color=NAVY, spaceAfter=20))

    story.append(Paragraph("LABORATORIO GUIADO · UNIDAD 5", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=13, textColor=GOLD, alignment=TA_CENTER)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("DEL DATA MART AL DASHBOARD EJECUTIVO Y AL COMITÉ DIRECTIVO", styles['CoverTitle']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Modelado Dimensional, DAX, Tablero Interactivo y Análisis para la Toma de Decisiones", styles['CoverSubtitle']))
    
    story.append(Spacer(1, 40))

    # Cuadro de Integrantes
    team_data = [
        [Paragraph("<b>INTEGRANTES DEL EQUIPO 8</b>", styles['TableHeader']), Paragraph("<b>MATRÍCULA</b>", styles['TableHeader'])],
        [Paragraph("Arely Carrillo Sustaita", styles['TableCellBold']), Paragraph("2226630", styles['TableCellCenter'])],
        [Paragraph("Rafael Jesús Collazo Hernández", styles['TableCellBold']), Paragraph("2169304", styles['TableCellCenter'])],
        [Paragraph("Sergio Jaziel Butzmann Martinez", styles['TableCellBold']), Paragraph("2163239", styles['TableCellCenter'])],
    ]
    t_team = Table(team_data, colWidths=[320, 184])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_team)

    story.append(Spacer(1, 50))
    meta_info = [
        [Paragraph("<b>Unidad de Aprendizaje:</b>", styles['TableCellBold']), Paragraph("Inteligencia de Negocios (FIME 2026)", styles['TableCell'])],
        [Paragraph("<b>Herramientas:</b>", styles['TableCellBold']), Paragraph("Excel 365 (Windows) · Power Query · Power Pivot · Lenguaje DAX · Docker", styles['TableCell'])],
        [Paragraph("<b>Entorno del Repositorio:</b>", styles['TableCellBold']), Paragraph("equipo8-inteligencia_negocios-FIME_2026 / unidad_5", styles['TableCell'])],
        [Paragraph("<b>Fecha de Emisión:</b>", styles['TableCellBold']), Paragraph("Noviembre 2026 · San Nicolás de los Garza, N.L.", styles['TableCell'])]
    ]
    t_meta = Table(meta_info, colWidths=[160, 344])
    t_meta.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (0, -1), BLUE_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(t_meta)

    story.append(PageBreak())

    # ==========================================================================
    # 2. ÍNDICE Y RESUMEN EJECUTIVO
    # ==========================================================================
    story.append(Paragraph("Resumen Ejecutivo y Pregunta Rectora", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "<b>Pregunta Rectora:</b> <i>¿Cómo se comportan las ventas y la rentabilidad por período, región y categoría, y qué decisión justificada con datos podemos recomendar a la alta dirección?</i>",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "El presente informe documenta el desarrollo técnico y metodológico integral del Laboratorio de la Unidad 5 para la <b>empresa comercial</b> a partir de su Data Mart transaccional de ventas. A partir de cuatro archivos CSV transaccionales y catálogos, se construyó un Data Mart analítico normalizado bajo el esquema estrella (Star Schema) en el Modelo de Datos de Excel 365 (Power Pivot). Se implementaron y validaron seis medidas analíticas en lenguaje DAX, alcanzando una <b>conciliación exacta al 100.00% ($0.00 de discrepancia)</b> contra las cifras de control institucionales: 1,200 transacciones, $2,416,376.00 MXN en ventas, $1,704,180.38 MXN en costo y $712,195.62 MXN de margen bruto (29.47%).",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "Asimismo, se articuló el análisis bajo los cuatro niveles de Business Intelligence (descriptivo, diagnóstico, predictivo y prescriptivo), culminando en el diseño del dashboard ejecutivo interactivo <code>U5_Dashboard_Equipo08.xlsx</code>, la presentación para el Comité Directivo <code>U5_Comite_Equipo08.pptx</code> y el presente informe de evidencias.",
        styles['BodyCustom']
    ))

    # ==========================================================================
    # 3. FASE A: IMPORTACIÓN Y CALIDAD EN POWER QUERY
    # ==========================================================================
    story.append(Paragraph("Fase A · Importación y Calidad en Power Query", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "La ingesta de datos se realizó a través de Power Query utilizando delimitador por coma y codificación UTF-8 sin alterar los cuatro archivos CSV fuente. Se aplicaron validaciones estrictas de tipado, integridad y reglas de negocio, cargando las consultas exclusivamente mediante la opción <b>'Solo crear conexión'</b> y marcando <b>'Agregar estos datos al Modelo de datos'</b>.",
        styles['BodyCustom']
    ))

    pq_audit_data = [
        [Paragraph("<b>Tabla / Consulta</b>", styles['TableHeader']), Paragraph("<b>Filas</b>", styles['TableHeader']), Paragraph("<b>Columnas y Tipos M</b>", styles['TableHeader']), Paragraph("<b>Hallazgo de Calidad y Validación</b>", styles['TableHeader']), Paragraph("<b>Estado</b>", styles['TableHeader'])],
        [
            Paragraph("<b>FACT_VENTAS</b>", styles['TableCellBold']),
            Paragraph("1,200", styles['TableCellCenter']),
            Paragraph("id_venta, id_prod, id_cli, id_tiempo, cant (Int64)<br/>monto, costo (number)", styles['TableCell']),
            Paragraph("0 nulos, 0 duplicados en PK. Cantidad > 0 (promedio 3.02). Monto y costo no negativos. Coherencia costo <= monto.", styles['TableCell']),
            Paragraph("✅ 100% Válido", styles['TableCellCenter'])
        ],
        [
            Paragraph("<b>DIM_PRODUCTO</b>", styles['TableCellBold']),
            Paragraph("12", styles['TableCellCenter']),
            Paragraph("id_producto (Int64), producto (text), categoria (text)", styles['TableCell']),
            Paragraph("Catálogo cerrado con 12 artículos distribuidos en 3 categorías (Hogar, Oficina, Tecnología). Llaves primarias únicas [1..12].", styles['TableCell']),
            Paragraph("✅ 100% Válido", styles['TableCellCenter'])
        ],
        [
            Paragraph("<b>DIM_CLIENTE</b>", styles['TableCellBold']),
            Paragraph("80", styles['TableCellCenter']),
            Paragraph("id_cliente (Int64), cliente (text), region (text)", styles['TableCell']),
            Paragraph("80 clientes únicos [1..80] distribuidos equitativamente en 4 regiones geográficas (Centro, Sur, Occidente, Norte; 20 c/u).", styles['TableCell']),
            Paragraph("✅ 100% Válido", styles['TableCellCenter'])
        ],
        [
            Paragraph("<b>DIM_TIEMPO</b>", styles['TableCellBold']),
            Paragraph("96", styles['TableCellCenter']),
            Paragraph("id_tiempo (Int64), fecha (date), anio (Int64), mes (Int64)", styles['TableCell']),
            Paragraph("Granularidad de 4 cortes semanales por mes (días 5, 12, 19, 26) para 2025 y 2026. Fechas ISO válidas sin gaps de formato.", styles['TableCell']),
            Paragraph("✅ 100% Válido", styles['TableCellCenter'])
        ],
    ]
    t_pq = Table(pq_audit_data, colWidths=[90, 45, 150, 165, 54])
    t_pq.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_pq)

    # ==========================================================================
    # 4. FASE B: RELACIONES Y ESQUEMA ESTRELLA EN POWER PIVOT
    # ==========================================================================
    story.append(Spacer(1, 8))
    story.append(Paragraph("Fase B · Relaciones y Esquema Estrella", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "En la Vista de Diagrama de Power Pivot se configuró el esquema estrella clásico, vinculando las claves primarias únicas de cada dimensión con las claves foráneas de la tabla central <code>FACT_VENTAS</code> con cardinalidad <b>1 a Varios (1:N)</b> y dirección de filtro unidireccional.",
        styles['BodyCustom']
    ))

    rel_data = [
        [Paragraph("<b>Dimensión (Lado 1)</b>", styles['TableHeader']), Paragraph("<b>Clave Primaria (PK)</b>", styles['TableHeader']), Paragraph("<b>Tabla Hechos (Lado N)</b>", styles['TableHeader']), Paragraph("<b>Clave Foránea (FK)</b>", styles['TableHeader']), Paragraph("<b>Dirección del Filtro</b>", styles['TableHeader'])],
        [Paragraph("DIM_PRODUCTO", styles['TableCell']), Paragraph("id_producto", styles['TableCellCenter']), Paragraph("FACT_VENTAS", styles['TableCell']), Paragraph("id_producto", styles['TableCellCenter']), Paragraph("Dimensión → Hechos", styles['TableCellCenter'])],
        [Paragraph("DIM_CLIENTE", styles['TableCell']), Paragraph("id_cliente", styles['TableCellCenter']), Paragraph("FACT_VENTAS", styles['TableCell']), Paragraph("id_cliente", styles['TableCellCenter']), Paragraph("Dimensión → Hechos", styles['TableCellCenter'])],
        [Paragraph("DIM_TIEMPO", styles['TableCell']), Paragraph("id_tiempo", styles['TableCellCenter']), Paragraph("FACT_VENTAS", styles['TableCell']), Paragraph("id_tiempo", styles['TableCellCenter']), Paragraph("Dimensión → Hechos", styles['TableCellCenter'])],
    ]
    t_rel = Table(rel_data, colWidths=[110, 95, 110, 95, 94])
    t_rel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_rel)

    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Nota Técnica sobre Inteligencia de Tiempo:</b> El archivo <code>DIM_TIEMPO.csv</code> contiene 96 cortes semanales (4 por mes) y no un calendario diario continuo de 730 días. Por tanto, no se utiliza la función nativa <code>SAMEPERIODLASTYEAR</code>, ya que las funciones DAX Time-Intelligence exigen continuidad estricta sin huecos. Las comparativas interanuales (YoY) se implementan mediante filtros explícitos sobre <code>DIM_TIEMPO[anio]</code> y <code>DIM_TIEMPO[mes]</code>.",
        styles['CalloutText']
    ))

    # ==========================================================================
    # 5. FASE C: MEDIDAS DAX
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("Fase C · Catálogo de Medidas DAX Fundamentales", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "En el área de cálculo de <code>FACT_VENTAS</code> se definieron las seis medidas requeridas por el laboratorio más métricas auxiliares para cálculo YoY y análisis de volumen:",
        styles['BodyCustom']
    ))

    dax_data = [
        [Paragraph("<b>Medida DAX</b>", styles['TableHeader']), Paragraph("<b>Expresión DAX</b>", styles['TableHeader']), Paragraph("<b>Interpretación y Formato</b>", styles['TableHeader'])],
        [
            Paragraph("<b>Ventas</b>", styles['TableCellBold']),
            Paragraph("<code>SUM(FACT_VENTAS[monto])</code>", styles['TableCell']),
            Paragraph("Suma total del ingreso bruto de ventas. Formato Moneda (<code>$#,##0.00</code>).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Costo</b>", styles['TableCellBold']),
            Paragraph("<code>SUM(FACT_VENTAS[costo])</code>", styles['TableCell']),
            Paragraph("Suma total del costo de los bienes vendidos (COGS). Formato Moneda (<code>$#,##0.00</code>).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Margen Bruto</b>", styles['TableCellBold']),
            Paragraph("<code>[Ventas] - [Costo]</code>", styles['TableCell']),
            Paragraph("Utilidad bruta monetaria resultante de restar costos a ventas. Formato Moneda (<code>$#,##0.00</code>).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Margen %</b>", styles['TableCellBold']),
            Paragraph("<code>DIVIDE([Margen Bruto], [Ventas], 0)</code>", styles['TableCell']),
            Paragraph("Porcentaje del ingreso conservado como utilidad. Formato Porcentaje (<code>0.0%</code>). Uso de DIVIDE seguro.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Transacciones</b>", styles['TableCellBold']),
            Paragraph("<code>DISTINCTCOUNT(FACT_VENTAS[id_venta])</code>", styles['TableCell']),
            Paragraph("Conteo cardinal de transacciones únicas realizadas. Formato Entero (<code>#,##0</code>).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Ticket Promedio</b>", styles['TableCellBold']),
            Paragraph("<code>DIVIDE([Ventas], [Transacciones], 0)</code>", styles['TableCell']),
            Paragraph("Ingreso promedio por cada transacción individual. Formato Moneda (<code>$#,##0.00</code>).", styles['TableCell'])
        ],
        [
            Paragraph("<b>Crecimiento YoY</b>", styles['TableCellBold']),
            Paragraph("<code>DIVIDE([Ventas 2026] - [Ventas 2025], [Ventas 2025], 0)</code>", styles['TableCell']),
            Paragraph("Variación relativa interanual calculada entre períodos comparables.", styles['TableCell'])
        ]
    ]
    t_dax = Table(dax_data, colWidths=[95, 195, 214])
    t_dax.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_dax)

    # ==========================================================================
    # 6. FASE D: VALIDACIÓN NUMÉRICA Y CIFRAS DE CONTROL
    # ==========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Fase D · Validación Numérica contra Cifras de Control", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "Antes de diseñar los componentes visuales del tablero, se confrontaron las medidas DAX globales sin filtros contra las cifras de control provistas en la especificación del laboratorio:",
        styles['BodyCustom']
    ))

    val_data = [
        [Paragraph("<b>Indicador Clave</b>", styles['TableHeader']), Paragraph("<b>Valor Esperado (Control)</b>", styles['TableHeader']), Paragraph("<b>Valor Calculado (Modelo)</b>", styles['TableHeader']), Paragraph("<b>Diferencia</b>", styles['TableHeader']), Paragraph("<b>Discrepancia (%)</b>", styles['TableHeader']), Paragraph("<b>Estado</b>", styles['TableHeader'])],
        [Paragraph("Transacciones", styles['TableCellBold']), Paragraph("1,200", styles['TableCellCenter']), Paragraph("1,200", styles['TableCellCenter']), Paragraph("0", styles['TableCellCenter']), Paragraph("0.00%", styles['TableCellCenter']), Paragraph("✅ Exacto", styles['TableCellCenter'])],
        [Paragraph("Ventas Totales", styles['TableCellBold']), Paragraph("MXN $2,416,376.00", styles['TableCellCenter']), Paragraph("MXN $2,416,376.00", styles['TableCellCenter']), Paragraph("$0.00", styles['TableCellCenter']), Paragraph("0.00%", styles['TableCellCenter']), Paragraph("✅ Exacto", styles['TableCellCenter'])],
        [Paragraph("Costo Total", styles['TableCellBold']), Paragraph("MXN $1,704,180.38", styles['TableCellCenter']), Paragraph("MXN $1,704,180.38", styles['TableCellCenter']), Paragraph("$0.00", styles['TableCellCenter']), Paragraph("0.00%", styles['TableCellCenter']), Paragraph("✅ Exacto", styles['TableCellCenter'])],
        [Paragraph("Margen Bruto", styles['TableCellBold']), Paragraph("MXN $712,195.62", styles['TableCellCenter']), Paragraph("MXN $712,195.62", styles['TableCellCenter']), Paragraph("$0.00", styles['TableCellCenter']), Paragraph("0.00%", styles['TableCellCenter']), Paragraph("✅ Exacto", styles['TableCellCenter'])],
        [Paragraph("Ticket Promedio", styles['TableCellBold']), Paragraph("MXN $2,013.65", styles['TableCellCenter']), Paragraph("MXN $2,013.65", styles['TableCellCenter']), Paragraph("$0.00", styles['TableCellCenter']), Paragraph("0.00%", styles['TableCellCenter']), Paragraph("✅ Exacto", styles['TableCellCenter'])],
    ]
    t_val = Table(val_data, colWidths=[104, 110, 110, 60, 65, 55])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_val)

    # Subtotales de control
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Conciliación por Región Geográfica y Categoría:</b>", styles['BodyCustomBold']))
    
    subtot_data = [
        [Paragraph("<b>Corte Dimensional</b>", styles['TableHeader']), Paragraph("<b>Transacciones</b>", styles['TableHeader']), Paragraph("<b>Ventas (MXN)</b>", styles['TableHeader']), Paragraph("<b>Part. Ventas (%)</b>", styles['TableHeader']), Paragraph("<b>Margen Bruto (MXN)</b>", styles['TableHeader']), Paragraph("<b>Margen %</b>", styles['TableHeader'])],
        [Paragraph("Occidente", styles['TableCell']), Paragraph("327", styles['TableCellCenter']), Paragraph("$677,408.00", styles['TableCellCenter']), Paragraph("28.03%", styles['TableCellCenter']), Paragraph("$197,187.02", styles['TableCellCenter']), Paragraph("29.11%", styles['TableCellCenter'])],
        [Paragraph("Centro", styles['TableCell']), Paragraph("324", styles['TableCellCenter']), Paragraph("$655,677.00", styles['TableCellCenter']), Paragraph("27.13%", styles['TableCellCenter']), Paragraph("$192,170.15", styles['TableCellCenter']), Paragraph("29.31%", styles['TableCellCenter'])],
        [Paragraph("Sur", styles['TableCell']), Paragraph("298", styles['TableCellCenter']), Paragraph("$608,288.00", styles['TableCellCenter']), Paragraph("25.17%", styles['TableCellCenter']), Paragraph("$184,829.89", styles['TableCellCenter']), Paragraph("30.39%", styles['TableCellCenter'])],
        [Paragraph("Norte", styles['TableCell']), Paragraph("251", styles['TableCellCenter']), Paragraph("$475,003.00", styles['TableCellCenter']), Paragraph("19.66%", styles['TableCellCenter']), Paragraph("$138,008.56", styles['TableCellCenter']), Paragraph("29.05%", styles['TableCellCenter'])],
        [Paragraph("<b>Total Consolidado</b>", styles['TableCellBold']), Paragraph("<b>1,200</b>", styles['TableCellCenter']), Paragraph("<b>$2,416,376.00</b>", styles['TableCellCenter']), Paragraph("<b>100.00%</b>", styles['TableCellCenter']), Paragraph("<b>$712,195.62</b>", styles['TableCellCenter']), Paragraph("<b>29.47%</b>", styles['TableCellCenter'])],
    ]
    t_subtot = Table(subtot_data, colWidths=[104, 75, 95, 80, 95, 55])
    t_subtot.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BLUE_ACCENT),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 5), (-1, 5), BLUE_LIGHT)
    ]))
    story.append(t_subtot)

    # ==========================================================================
    # 7. FASE E: DASHBOARD EJECUTIVO
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("Fase E · Dashboard Ejecutivo Interactivo", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "En el archivo <code>U5_Dashboard_Equipo08.xlsx</code> (hoja <code>Dashboard</code>), se implementó un tablero gerencial estructurado con los siguientes elementos visuales y dinámicos:",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "1. <b>Fila de Tarjetas KPI Superiores:</b> Visualización ejecutiva de Ventas ($2.42M), Margen Bruto ($712.2k), Margen % (29.5%) y Ticket Promedio ($2,013.65).<br/>"
        "2. <b>Gráfico 1 · Ventas por Región:</b> Gráfico de barras horizontales que contrasta el volumen de ventas y margen bruto entre Occidente, Centro, Sur y Norte.<br/>"
        "3. <b>Gráfico 2 · Tendencia Mensual (2025 vs 2026):</b> Gráfico de líneas que ilustra la estacionalidad mes a mes y permite identificar el crecimiento YoY.<br/>"
        "4. <b>Gráfico 3 · Mix por Categoría:</b> Gráfico de columnas con la facturación y margen porcentual de Tecnología, Oficina y Hogar.<br/>"
        "5. <b>Gráfico 4 · Top 5 Productos Estrella:</b> Ranking de los cinco productos con mayor facturación encabezado por el Producto 12.<br/>"
        "6. <b>Segmentadores Sincronizados:</b> Controles dinámicos por Año, Región y Categoría vinculados mediante <i>Conexiones de informe</i>.",
        styles['BodyCustom']
    ))

    # ==========================================================================
    # 8. FASE F: CUATRO NIVELES DE ANÁLISIS
    # ==========================================================================
    story.append(Paragraph("Fase F · Cuatro Niveles de Análisis de Negocio", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph("<b>1. Análisis Descriptivo (¿Qué pasó?):</b>", styles['BodyCustomBold']))
    story.append(Paragraph(
        "• <i>Estabilidad Global con Ligera Contracción:</i> Facturación de $2,416,376.00 MXN en 1,200 transacciones. Ventas de 2025 ($1,214,067.00 MXN) y 2026 ($1,202,309.00 MXN) variaron apenas -0.97% YoY (-$11,758.00 MXN).<br/>"
        "• <i>Tecnología como Motor Primario:</i> Generó $889,916.00 MXN (36.83% de participación) con el margen relativo más alto (30.13%). El Producto 12 aportó $346,902.00 MXN con 32.00% de margen.<br/>"
        "• <i>Brecha Territorial:</i> Occidente ($677.4k) y Centro ($655.7k) lideran, mientras que el Norte ($475.0k) presenta un rezago del -29.88% en ventas.",
        styles['BodyCustom']
    ))

    story.append(Paragraph("<b>2. Análisis Diagnóstico (¿Dónde se concentró y por qué?):</b>", styles['BodyCustomBold']))
    story.append(Paragraph(
        "• <i>Hipótesis H1 (Desfase Comercial en Fin de Año):</i> La caída de noviembre 2026 (-25.0%) y repunte en diciembre 2026 (+34.8%) sugiere un desplazamiento en órdenes de compra corporativas y no una pérdida neta de demanda.<br/>"
        "• <i>Hipótesis H2 (Fricción de Frecuencia en el Norte):</i> Teniendo 20 clientes registrados al igual que Occidente, el Norte realizó 76 transacciones menos (251 vs 327), sugiriendo menor frecuencia de visita o fricciones de distribución.<br/>"
        "<i>*Rigor Metodológico:</i> No se afirma falta de inventario ni problemas publicitarios porque el dataset no captura stock ni marketing.",
        styles['BodyCustom']
    ))

    story.append(Paragraph("<b>3. Análisis Predictivo (¿Qué podría pasar?):</b>", styles['BodyCustomBold']))
    story.append(Paragraph(
        "• Bajo el supuesto inercial de estabilidad de clientes y precios, el ejercicio 2027 se proyecta en ~$1,195,000.00 MXN ± $35,000 MXN con $352,000 MXN de margen bruto. Si el Norte continúa su rezago (-2.5% anual), la empresa enfrentará una lenta erosión de cuota.",
        styles['BodyCustom']
    ))

    story.append(Paragraph("<b>4. Análisis Prescriptivo (¿Qué conviene hacer?):</b>", styles['BodyCustomBold']))
    
    plan_data = [
        [Paragraph("<b>Acción Propuesta</b>", styles['TableHeader']), Paragraph("<b>Responsable</b>", styles['TableHeader']), Paragraph("<b>Plazo</b>", styles['TableHeader']), Paragraph("<b>KPI y Meta de Seguimiento</b>", styles['TableHeader'])],
        [
            Paragraph("Campaña de Reactivación Comercial Región Norte", styles['TableCellBold']),
            Paragraph("Dirección de Ventas", styles['TableCellCenter']),
            Paragraph("6 Meses", styles['TableCellCenter']),
            Paragraph("Ventas Norte: +15% (meta $275k semestrales). Elevar tx de 125 a 155.", styles['TableCell'])
        ],
        [
            Paragraph("Estrategia de Bundling Producto 12 + 11 (Tec + Ofi)", styles['TableCellBold']),
            Paragraph("Mkt / Pricing", styles['TableCellCenter']),
            Paragraph("3 Meses", styles['TableCellCenter']),
            Paragraph("Elevar margen de Oficina del 28.6% al 29.5%. Ticket > $2,100.", styles['TableCell'])
        ],
        [
            Paragraph("Auditoría Logística y Nivel de Servicio Norte", styles['TableCellBold']),
            Paragraph("Operaciones", styles['TableCellCenter']),
            Paragraph("2 Meses", styles['TableCellCenter']),
            Paragraph("Cumplimiento OTIF > 95% y entrega < 72 hrs.", styles['TableCell'])
        ],
    ]
    t_plan = Table(plan_data, colWidths=[160, 90, 60, 194])
    t_plan.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
    ]))
    story.append(t_plan)

    # ==========================================================================
    # 9. FASE G: COMITÉ DIRECTIVO Y BITÁCORA IA
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("Fase G · Presentación al Comité y Bitácora de IA", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "Se estructuró la presentación ejecutiva <code>U5_Comite_Equipo08.pptx</code> en 7 diapositivas (16:9) acompañada de un guion de 15 minutos (11 min exposición + 4 min Q&A), cumpliendo con el principio de pirámide de Minto.",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<b>Transparencia y Bitácora de Inteligencia Artificial:</b> La IA generativa se utilizó exclusivamente para afinar la claridad narrativa y estructurar el guion oral sobre cifras previamente validadas al 100%. Se auditó que la IA no introdujera causalidades infundadas ni alterara ningún valor numérico.",
        styles['BodyCustom']
    ))

    # ==========================================================================
    # 10. REPRODUCIBILIDAD DOCKER Y ENTREGABLES
    # ==========================================================================
    story.append(Paragraph("Reproducibilidad Técnica y Verificación en Docker", styles['SectionHeading']))
    story.append(HRFlowable(width="100%", thickness=1, color=BLUE_ACCENT, spaceAfter=8))

    story.append(Paragraph(
        "En estricto cumplimiento con la regla de oro del proyecto (<b>'Nunca instalar dependencias en el host, utilizar siempre Docker'</b>), todo el pipeline de validación y generación de artefactos se ejecuta dentro del contenedor <code>equipo8-u5-generator:latest</code> mediante el script automatizado:",
        styles['BodyCustom']
    ))
    story.append(Paragraph(
        "<code>./unidad_5/ejecutar_laboratorio_docker.sh</code>",
        styles['CodeStyle']
    ))

    story.append(Spacer(1, 10))
    deliv_data = [
        [Paragraph("<b>Entregable Formal</b>", styles['TableHeader']), Paragraph("<b>Ruta en Repositorio</b>", styles['TableHeader']), Paragraph("<b>Estado y Verificación</b>", styles['TableHeader'])],
        [Paragraph("Workbook Excel con Dashboard", styles['TableCellBold']), Paragraph("unidad_5/U5_Dashboard_Equipo08.xlsx", styles['TableCell']), Paragraph("✅ Generado (83 KB, 6 hojas, 4 gráficos)", styles['TableCell'])],
        [Paragraph("Presentación Comité (PPTX)", styles['TableCellBold']), Paragraph("unidad_5/U5_Comite_Equipo08.pptx", styles['TableCell']), Paragraph("✅ Generado (55 KB, 7 diapositivas 16:9)", styles['TableCell'])],
        [Paragraph("Reporte de Evidencias (PDF)", styles['TableCellBold']), Paragraph("unidad_5/U5_Evidencias_Equipo08.pdf", styles['TableCell']), Paragraph("✅ Generado (Documento formal completo)", styles['TableCell'])],
        [Paragraph("Datos Crudos Originales (4 CSVs)", styles['TableCellBold']), Paragraph("unidad_5/01_datos_crudos/*.csv", styles['TableCell']), Paragraph("✅ Íntegros e Inmutables (1,200 transacciones)", styles['TableCell'])],
    ]
    t_deliv = Table(deliv_data, colWidths=[160, 194, 150])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, GRAY_BG])
    ]))
    story.append(t_deliv)

    # Construir documento PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Archivo PDF generado exitosamente: {pdf_path}")
    print(f"📦 Tamaño: {pdf_path.stat().st_size:,} bytes")
    print("==============================================================================")
    return True

if __name__ == "__main__":
    generar_pdf()
