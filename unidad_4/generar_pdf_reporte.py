#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Reporte PDF Ejecutivo - Laboratorio ETL Unidad 4
Inteligencia de Negocios - FIME 2026 - Equipo 8
"""

import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

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

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Portada sin encabezado ni pie
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Encabezado
        self.drawString(54, 750, "UANL · FIME | Inteligencia de Negocios · Unidad 4: Laboratorio ETL")
        self.drawRightString(612 - 54, 750, "Casa&Estilo · Equipo 8")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(54, 744, 612 - 54, 744)

        # Pie de página
        self.line(54, 45, 612 - 54, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Reporte Oficial de Práctica: Del Archivo Crudo al Data Mart")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()


def create_report(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Colores corporativos FIME / Casa&Estilo
    c_primary = colors.HexColor("#1A365D")   # Azul marino profundo
    c_secondary = colors.HexColor("#2B6CB0") # Azul institucional
    c_dark = colors.HexColor("#2D3748")      # Texto oscuro
    c_light = colors.HexColor("#F7FAFC")     # Fondo tablas
    c_border = colors.HexColor("#E2E8F0")    # Bordes sutiles
    c_accent = colors.HexColor("#C53030")    # Rojo alertas
    c_green = colors.HexColor("#276749")     # Verde éxito
    c_amber = colors.HexColor("#D69E2E")     # Amarillo advertencia

    # Estilos tipográficos
    style_cover_univ = ParagraphStyle(
        'CoverUniv',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=TA_CENTER
    )

    style_cover_fac = ParagraphStyle(
        'CoverFac',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_dark,
        alignment=TA_CENTER
    )

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=TA_CENTER
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_secondary,
        alignment=TA_CENTER
    )

    style_cover_body = ParagraphStyle(
        'CoverBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=c_dark,
        alignment=TA_CENTER
    )

    style_h1 = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )

    style_body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=style_body,
        fontName='Helvetica-Bold'
    )

    style_callout = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2C5282")
    )

    style_th = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    style_td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_dark,
        alignment=TA_LEFT
    )

    style_td_center = ParagraphStyle(
        'TDCenter',
        parent=style_td,
        alignment=TA_CENTER
    )

    style_td_bold = ParagraphStyle(
        'TDBold',
        parent=style_td,
        fontName='Helvetica-Bold'
    )

    style_td_mono = ParagraphStyle(
        'TDMono',
        parent=style_td,
        fontName='Courier',
        fontSize=7,
        leading=8.5
    )

    story = []

    # =========================================================================
    # PÁGINA 1: PORTADA INSTITUCIONAL
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("UNIVERSIDAD AUTÓNOMA DE NUEVO LEÓN", style_cover_univ))
    story.append(Paragraph("FACULTAD DE INGENIERÍA MECÁNICA Y ELÉCTRICA", style_cover_fac))
    story.append(Paragraph("COORDINACIÓN DE TECNOLOGÍAS DE INFORMACIÓN", style_cover_fac))
    story.append(Spacer(1, 35))

    story.append(HRFlowable(width="80%", thickness=2, color=c_secondary, spaceAfter=25, spaceBefore=0))
    story.append(Paragraph("ACTIVIDAD PRÁCTICA · UNIDAD 4", style_cover_sub))
    story.append(Spacer(1, 10))
    story.append(Paragraph("LABORATORIO ETL:<br/>DEL ARCHIVO CRUDO AL DATA MART", style_cover_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Arquitectura de Capas, Normalización Canónica, Mesa de Rechazos,<br/>Idempotencia (UPSERT), Conciliación y Analítica de Negocio en MySQL 8.0", style_cover_sub))
    story.append(HRFlowable(width="80%", thickness=2, color=c_secondary, spaceAfter=35, spaceBefore=25))

    story.append(Paragraph("<b>Unidad de Aprendizaje:</b> Inteligencia de Negocios (BI)", style_cover_body))
    story.append(Paragraph("<b>Empresa Asignada:</b> Casa&Estilo (Retail E-commerce)", style_cover_body))
    story.append(Paragraph("<b>Entorno Tecnológico:</b> MySQL Server 8.0 · Docker · Workbench", style_cover_body))
    story.append(Spacer(1, 30))

    # Tabla de integrantes
    equipo_data = [
        [Paragraph("<b>Miembro del Equipo 8</b>", style_th), Paragraph("<b>Matrícula</b>", style_th), Paragraph("<b>Carrera / Plan</b>", style_th)],
        [Paragraph("Sergio Jaziel Butzmann Martinez", style_td), Paragraph("2163239", style_td_center), Paragraph("Ingeniería en Tecnologías de Software (ITS)", style_td)],
        [Paragraph("Arely Carrillo Sustaita", style_td), Paragraph("2226630", style_td_center), Paragraph("Ingeniería en Tecnologías de Software (ITS)", style_td)],
        [Paragraph("Rafael Jesús Collazo Hernández", style_td), Paragraph("2169304", style_td_center), Paragraph("Ingeniería en Tecnologías de Software (ITS)", style_td)],
    ]
    t_equipo = Table(equipo_data, colWidths=[200, 80, 220])
    t_equipo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_equipo)

    story.append(Spacer(1, 35))
    story.append(Paragraph("<b>Semestre:</b> Agosto - Diciembre 2026", style_cover_body))
    story.append(Paragraph("San Nicolás de los Garza, Nuevo León, México", style_cover_body))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2: INTRODUCCIÓN, ARQUITECTURA Y ENTREGABLES
    # =========================================================================
    story.append(Paragraph("1. Propósito, Escenario y Entregables del Laboratorio", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "El presente laboratorio técnico tiene como propósito simular un escenario real de ingeniería de datos para la empresa "
        "de retail y comercio electrónico <b>Casa&Estilo</b>. La organización recibe flujos periódicos de datos provenientes de "
        "diferentes canales transaccionales (archivos planos <code>clientes.csv</code>, transacciones <code>pedidos.sql</code> y un "
        "catálogo de entidades federativas <code>catalogo_estados.csv</code>). Los datos crudos presentan defectos e inconsistencias "
        "deliberadas: registros duplicados, fechas con formatos mixtos, importes nulos o negativos, clientes inexistentes y alias de estados no homologados.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Regla Fundamental de Calidad:</b> Bajo ninguna circunstancia se deben corregir manualmente los archivos de origen. "
        "Todo el saneamiento, tipado y validación debe ser ejecutado de forma programática, automatizada y reproducible a través de un "
        "pipeline SQL implementado en <b>MySQL Server 8.0</b>.",
        style_body
    ))

    # Callout de entregables
    entregables_data = [[
        Paragraph(
            "<b>Entregables Oficiales de la Práctica:</b><br/>"
            "1. <b>Script SQL Maestro y Scripts Modulares:</b> Código DDL/DML determinista e idempotente.<br/>"
            "2. <b>Reporte de Diagnóstico y Cuarentena:</b> Evidencia de volumetrías, perfilado y las 8 transacciones rechazadas.<br/>"
            "3. <b>Prueba de Idempotencia:</b> Demostración matemática del mecanismo UPSERT sin duplicación de hechos.<br/>"
            "4. <b>Conciliación Cuantitativa y Financiera:</b> Registro formal en <code>etl_auditoria</code> (Balance de Masa = 0).<br/>"
            "5. <b>Consulta Final de Indicadores de Negocio:</b> Reporte de ventas netas y órdenes entregadas por estado y fecha.<br/>"
            "6. <b>Reflexión Crítica:</b> Justificación técnica sobre decisiones de limpieza, detección de pedidos tardíos y devoluciones.",
            style_callout
        )
    ]]
    t_callout = Table(entregables_data, colWidths=[504])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Arquitectura de Datos por Capas (Multi-Tier Pipeline)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    arch_data = [
        [Paragraph("<b>Capa</b>", style_th), Paragraph("<b>Tablas Físicas</b>", style_th), Paragraph("<b>Rol y Principio de Gobierno</b>", style_th)],
        [
            Paragraph("<b>Raw Zone</b><br/>(Aterrizaje)", style_td),
            Paragraph("<code>raw_clientes</code><br/><code>raw_pedidos</code><br/><code>catalogo_estados</code>", style_td_mono),
            Paragraph("<b>Inmutable y de sólo inserción.</b> Almacena la verdad fáctica recibida tal como ingresó de las fuentes. Permite reprocesar el pipeline ante cualquier cambio de regla.", style_td)
        ],
        [
            Paragraph("<b>Staging</b><br/>(Refinamiento)", style_td),
            Paragraph("<code>stg_clientes</code><br/><code>stg_pedidos</code><br/><code>stg_pedidos_limpios</code>", style_td_mono),
            Paragraph("<b>Transformación y tipado fuerte.</b> Convierte textos a <code>DATE</code> y <code>DECIMAL</code>, deduplica clientes mediante <code>ROW_NUMBER()</code> y homologa claves estatales canónicas.", style_td)
        ],
        [
            Paragraph("<b>Cuarentena</b><br/>(Error Mart)", style_td),
            Paragraph("<code>pedidos_rechazados</code>", style_td_mono),
            Paragraph("<b>Mesa de rechazos auditable.</b> Aísla registros con violaciones de reglas de calidad sin interrumpir la ejecución ni borrar datos.", style_td)
        ],
        [
            Paragraph("<b>Data Mart</b><br/>(Esquema Estrella)", style_td),
            Paragraph("<code>dim_estado</code><br/><code>dim_cliente</code><br/><code>fact_ordenes</code>", style_td_mono),
            Paragraph("<b>Modelo dimensional analítico.</b> Carga incremental con <code>INSERT ... ON DUPLICATE KEY UPDATE</code> (UPSERT) garantizando idempotencia estricta.", style_td)
        ],
        [
            Paragraph("<b>Gobierno</b><br/>(Auditoría)", style_td),
            Paragraph("<code>observaciones_perfilado</code><br/><code>etl_auditoria</code>", style_td_mono),
            Paragraph("<b>Balance de masa y conciliación.</b> Cuadra matemáticamente: <i>Total Raw = Total Limpios + Total Rechazados</i> (Discrepancia = 0).", style_td)
        ],
    ]
    t_arch = Table(arch_data, colWidths=[90, 140, 274])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_arch)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 3: PASO 1 (PERFILADO) Y PASOS 2-3 (STAGING Y NORMALIZACIÓN)
    # =========================================================================
    story.append(Paragraph("3. Paso 1: Perfilado de Datos y Diagnóstico de Calidad", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "El diagnóstico de calidad ejecutado por el script <code>01_perfilado_datos.sql</code> detectó 11 observaciones críticas, "
        "las cuales fueron guardadas formalmente en la tabla <code>observaciones_perfilado</code>:",
        style_body
    ))

    perfilado_data = [
        [Paragraph("<b>Tabla Origen</b>", style_th), Paragraph("<b>Métrica / Regla</b>", style_th), Paragraph("<b>Afectados</b>", style_th), Paragraph("<b>Severidad</b>", style_th), Paragraph("<b>Detalle del Hallazgo</b>", style_th)],
        [Paragraph("raw_clientes", style_td), Paragraph("VOLUMETRIA_TOTAL", style_td), Paragraph("21", style_td_center), Paragraph("<font color='#276749'>INFO</font>", style_td_center), Paragraph("Total de registros ingresados desde clientes.csv", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("VOLUMETRIA_TOTAL", style_td), Paragraph("32", style_td_center), Paragraph("<font color='#276749'>INFO</font>", style_td_center), Paragraph("Total de transacciones ingresadas desde pedidos.sql", style_td)],
        [Paragraph("catalogo_estados", style_td), Paragraph("VOLUMETRIA_TOTAL", style_td), Paragraph("10", style_td_center), Paragraph("<font color='#276749'>INFO</font>", style_td_center), Paragraph("Entidades federativas canónicas registradas", style_td)],
        [Paragraph("raw_clientes", style_td), Paragraph("DUPLICADOS_ID_CLIENTE", style_td), Paragraph("1", style_td_center), Paragraph("<font color='#C53030'>ALTA</font>", style_td_center), Paragraph("Cliente CLI-005 repetido con estados distintos (Jalisco / JAL)", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("DUPLICADOS_ID_PEDIDO", style_td), Paragraph("2", style_td_center), Paragraph("<font color='#C53030'>ALTA</font>", style_td_center), Paragraph("Transacciones duplicadas en clave natural: PED-1001 y PED-1010", style_td)],
        [Paragraph("raw_clientes", style_td), Paragraph("ESTADOS_NO_ESTANDARIZADOS", style_td), Paragraph("13", style_td_center), Paragraph("<font color='#D69E2E'>MEDIA</font>", style_td_center), Paragraph("Uso de alias ('N.L.', 'D.F.', 'Nuevo Leon'), vacíos y no identificados", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("ESTADOS_ENVIO_NO_CANONICOS", style_td), Paragraph("11", style_td_center), Paragraph("<font color='#D69E2E'>MEDIA</font>", style_td_center), Paragraph("Estados de envío con alias tipográficos o 'ESTADO_INEXISTENTE'", style_td)],
        [Paragraph("raw_clientes", style_td), Paragraph("FECHAS_CLIENTE_NO_ISO", style_td), Paragraph("7", style_td_center), Paragraph("<font color='#D69E2E'>MEDIA</font>", style_td_center), Paragraph("Formatos DD/MM/AAAA ('14/02/2026') y cliente CLI-020 con fecha vacía", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("FECHAS_PEDIDO_INVALIDAS", style_td), Paragraph("7", style_td_center), Paragraph("<font color='#C53030'>ALTA</font>", style_td_center), Paragraph("Formatos DD/MM/AAAA, fecha vacía (PED-1024) y cadena 'FECHA_ROTA' (PED-1025)", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("MONTOS_NO_POSITIVOS", style_td), Paragraph("2", style_td_center), Paragraph("<font color='#C53030'>ALTA</font>", style_td_center), Paragraph("Importe negativo '-$350.00' (PED-1021) e importe cero '$0.00' (PED-1022)", style_td)],
        [Paragraph("raw_pedidos", style_td), Paragraph("CLIENTES_HUERFANOS", style_td), Paragraph("1", style_td_center), Paragraph("<font color='#C53030'>ALTA</font>", style_td_center), Paragraph("Pedido PED-1023 referencia al cliente inexistente CLI-999", style_td)],
    ]
    t_perf = Table(perfilado_data, colWidths=[70, 110, 45, 45, 234])
    t_perf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_perf)
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Pasos 2 y 3: Staging, Inmutabilidad y Normalización", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "<b>Fundamento de Inmutabilidad de la Capa Raw:</b> Modificar los datos en la zona de aterrizaje cruda destruiría la "
        "trazabilidad legal y forense de las transacciones recibidas e impediría reprocesar el pipeline ante ajustes en las "
        "reglas comerciales. Por ello, la capa <code>stg_*</code> actúa como el laboratorio de estandarización sin alterar el origen.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Mapeo y Normalización Geográfica:</b> Se cruzaron los textos libres contra el catálogo de entidades oficiales "
        "mediante la búsqueda por nombre oficial, clave directa o lista de alias: <code>FIND_IN_SET(TRIM(estado), REPLACE(ce.alias, ', ', ',')) > 0</code>. "
        "De este modo, variantes como <i>'Nuevo Leon'</i>, <i>'N.L.'</i> y <i>'NL.'</i> convergen a la clave canónica única <b>'NL'</b>; "
        "<i>'D.F.'</i> y <i>'Distrito Federal'</i> a <b>'CDMX'</b>; y <i>'Jal.'</i> a <b>'JAL'</b>. "
        "A los clientes sin estado asignado se les imputó el valor centinela <b>'NE'</b> (<i>No Especificado</i>).",
        style_body
    ))
    story.append(Paragraph(
        "<b>Parsing Robusto de Fechas:</b> Para evitar fallos por modo estricto en MySQL (Error 1411), se implementó una estructura "
        "condicional con expresiones regulares (<code>CASE WHEN fecha REGEXP ...</code>) que reconoce tanto el estándar ISO (<code>%Y-%m-%d</code>) "
        "como el formato tradicional (<code>%d/%m/%Y</code>), convirtiéndolos al tipo nativo <code>DATE</code> y asignando <code>NULL</code> seguro "
        "a cadenas corruptas o vacías para su posterior cuarentena.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 4: PASO 4 (VALIDACIÓN Y RECHAZOS) Y PASO 5 (IDEMPOTENCIA)
    # =========================================================================
    story.append(Paragraph("5. Paso 4: Validación y Aislamiento de Rechazos (Cuarentena)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "Para proteger la integridad referencial y financiera del Data Mart sin perder visibilidad operativa de los errores, "
        "se creó la tabla de cuarentena <code>pedidos_rechazados</code>. De las 32 órdenes crudas, exactamente "
        "<b>8 transacciones fueron descalificadas</b> con documentación de causa raíz, y <b>24 transacciones limpias</b> pasaron a <code>stg_pedidos_limpios</code>:",
        style_body
    ))

    rechazos_data = [
        [Paragraph("<b>ID Rechazo</b>", style_th), Paragraph("<b>Fila Raw</b>", style_th), Paragraph("<b>ID Pedido</b>", style_th), Paragraph("<b>ID Cliente</b>", style_th), Paragraph("<b>Monto Raw</b>", style_th), Paragraph("<b>Motivo de Rechazo</b>", style_th), Paragraph("<b>Detalle Técnico del Error</b>", style_th)],
        [Paragraph("1", style_td_center), Paragraph("27", style_td_center), Paragraph("PED-1001", style_td), Paragraph("CLI-001", style_td), Paragraph("$1,250.00", style_td_center), Paragraph("<b>ID_PEDIDO_DUPLICADO</b>", style_td), Paragraph("Segunda aparición en lote; ya existe una transacción previa con esta clave.", style_td)],
        [Paragraph("2", style_td_center), Paragraph("28", style_td_center), Paragraph("PED-1010", style_td), Paragraph("CLI-010", style_td), Paragraph("$2,650.00", style_td_center), Paragraph("<b>ID_PEDIDO_DUPLICADO</b>", style_td), Paragraph("Transacción repetida en lote crudo.", style_td)],
        [Paragraph("3", style_td_center), Paragraph("23", style_td_center), Paragraph("PED-1023", style_td), Paragraph("CLI-999", style_td), Paragraph("$1,500.00", style_td_center), Paragraph("<b>CLIENTE_INEXISTENTE</b>", style_td), Paragraph("Cliente huérfano; no existe en la dimensión de clientes.", style_td)],
        [Paragraph("4", style_td_center), Paragraph("24", style_td_center), Paragraph("PED-1024", style_td), Paragraph("CLI-007", style_td), Paragraph("$1,200.00", style_td_center), Paragraph("<b>FECHA_INVALIDA</b>", style_td), Paragraph("Cadena de fecha vacía ([VACIO]).", style_td)],
        [Paragraph("5", style_td_center), Paragraph("25", style_td_center), Paragraph("PED-1025", style_td), Paragraph("CLI-008", style_td), Paragraph("$980.00", style_td_center), Paragraph("<b>FECHA_INVALIDA</b>", style_td), Paragraph("Valor corrupto no convertible a DATE ('FECHA_ROTA').", style_td)],
        [Paragraph("6", style_td_center), Paragraph("21", style_td_center), Paragraph("PED-1021", style_td), Paragraph("CLI-002", style_td), Paragraph("-$350.00", style_td_center), Paragraph("<b>IMPORTE_NO_POSITIVO</b>", style_td), Paragraph("Importe negativo que distorsiona la facturación de venta.", style_td)],
        [Paragraph("7", style_td_center), Paragraph("22", style_td_center), Paragraph("PED-1022", style_td), Paragraph("CLI-004", style_td), Paragraph("$0.00", style_td_center), Paragraph("<b>IMPORTE_NO_POSITIVO</b>", style_td), Paragraph("Importe en cero sin intercambio económico.", style_td)],
        [Paragraph("8", style_td_center), Paragraph("26", style_td_center), Paragraph("PED-1026", style_td), Paragraph("CLI-009", style_td), Paragraph("$1,400.00", style_td_center), Paragraph("<b>ESTADO_NO_RECONOCIDO</b>", style_td), Paragraph("Destino 'ESTADO_INEXISTENTE' sin coincidencia en catálogo estatal.", style_td)],
    ]
    t_rech = Table(rechazos_data, colWidths=[40, 35, 50, 45, 50, 95, 189])
    t_rech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_rech)
    story.append(Spacer(1, 10))

    story.append(Paragraph("6. Paso 5: Carga Incremental al Data Mart y Demostración de Idempotencia", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "<b>Fundamento de Idempotencia:</b> Un pipeline de datos es idempotente si su ejecución repetida sobre el mismo conjunto "
        "de datos produce exactamente el mismo estado final en el destino: <i>f(f(x)) = f(x)</i>. "
        "Esto se logra definiendo <b>claves primarias naturales estables</b> (<code>id_cliente</code> en la dimensión y <code>id_pedido</code> en los hechos) "
        "e implementando la instrucción <code>INSERT ... ON DUPLICATE KEY UPDATE</code> (UPSERT). "
        "Si el motor detecta que la clave ya existe en el índice primario B-Tree, ejecuta una actualización en sitio en lugar de crear un registro duplicado.",
        style_body
    ))

    idemp_data = [
        [Paragraph("<b>Concepto de Evaluación</b>", style_th), Paragraph("<b>Corrida Inicial (1)</b>", style_th), Paragraph("<b>Re-ejecución Idéntica (2)</b>", style_th), Paragraph("<b>Diferencial (Δ)</b>", style_th), Paragraph("<b>Veredicto Técnico</b>", style_th)],
        [Paragraph("Filas en <code>fact_ordenes</code>", style_td), Paragraph("24 registros", style_td_center), Paragraph("24 registros", style_td_center), Paragraph("0 filas", style_td_center), Paragraph("<font color='#276749'><b>IDEMPOTENTE (ÉXITO)</b></font>", style_td_center)],
        [Paragraph("Monto Total Facturado", style_td), Paragraph("$39,210.50", style_td_center), Paragraph("$39,210.50", style_td_center), Paragraph("$0.00", style_td_center), Paragraph("<font color='#276749'><b>INTEGRO (SIN DESVÍO)</b></font>", style_td_center)],
        [Paragraph("Filas en <code>dim_cliente</code>", style_td), Paragraph("20 clientes", style_td_center), Paragraph("20 clientes", style_td_center), Paragraph("0 filas", style_td_center), Paragraph("<font color='#276749'><b>ESTABLE</b></font>", style_td_center)],
    ]
    t_idemp = Table(idemp_data, colWidths=[140, 90, 100, 70, 104])
    t_idemp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_idemp)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 5: PASO 6 (CONCILIACIÓN) Y PASO 7 (INDICADORES)
    # =========================================================================
    story.append(Paragraph("7. Paso 6: Conciliación Cuantitativa y Balance de Masa", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "El principio de <b>balance de masa</b> garantiza que no existe pérdida ni creación inexplicable de registros a lo largo del flujo ETL: "
        "<i>Total Recibido (Raw) = Aceptados Únicos (Staging) + Rechazados (Cuarentena)</i>. "
        "Dicha conciliación se registró automáticamente en la tabla <code>etl_auditoria</code>:",
        style_body
    ))

    concil_data = [
        [Paragraph("<b>Métrica Cuantitativa</b>", style_th), Paragraph("<b>Valor</b>", style_th), Paragraph("<b>Métrica Financiera</b>", style_th), Paragraph("<b>Valor Monetario</b>", style_th)],
        [Paragraph("Total Recibido en <code>raw_pedidos</code>", style_td), Paragraph("32 filas", style_td_center), Paragraph("Monto Bruto Total Recibido", style_td), Paragraph("$47,840.50", style_td_center)],
        [Paragraph("Total Aceptado en <code>stg_pedidos_limpios</code>", style_td), Paragraph("24 filas", style_td_center), Paragraph("Monto Descartado en Cuarentena", style_td), Paragraph("$8,630.00", style_td_center)],
        [Paragraph("Total Aislado en <code>pedidos_rechazados</code>", style_td), Paragraph("8 filas", style_td_center), Paragraph("Monto Válido en Staging Limpio", style_td), Paragraph("$39,210.50", style_td_center)],
        [Paragraph("Total Justificado (24 + 8)", style_td), Paragraph("32 filas", style_td_center), Paragraph("Monto Persistido en <code>fact_ordenes</code>", style_td), Paragraph("$39,210.50", style_td_center)],
        [Paragraph("<b>Discrepancia Matemática</b>", style_td_bold), Paragraph("<b>0 filas</b>", style_td_center), Paragraph("<b>Desvío Financiero Staging vs Hechos</b>", style_td_bold), Paragraph("<b>$0.00</b>", style_td_center)],
        [Paragraph("<b>Balance de Masa Cuadrado</b>", style_td_bold), Paragraph("<font color='#276749'><b>SI (PERFECTO)</b></font>", style_td_center), Paragraph("<b>Estatus Global de Auditoría</b>", style_td_bold), Paragraph("<font color='#276749'><b>EXITOSO</b></font>", style_td_center)],
    ]
    t_concil = Table(concil_data, colWidths=[150, 85, 180, 89])
    t_concil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_concil)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>¿Por qué el total bruto difiere del total válido?</b><br/>"
        "El monto bruto ($47,840.50) representa el tráfico transaccional crudo que incluye anomalías económicas "
        "(importes negativos de -$350.00, órdenes de $0.00, transacciones a clientes inexistentes de $1,500.00, órdenes sin fecha válida de $2,180.00 "
        "y compras duplicadas por reintentos de red de $3,900.00). El total válido consolidado ($39,210.50) refleja la "
        "<b>verdad transaccional gobernada</b> apta para la toma de decisiones ejecutivas.",
        style_body
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Paso 7: Indicadores Analíticos de Negocio", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph(
        "<b>Supuesto Metodológico del Laboratorio:</b> Para fines analíticos de este ejercicio, la métrica <b>Ventas Netas</b> "
        "se define estrictamente como la suma de importes de las órdenes en estatus <code>'Entregado'</code>. "
        "No se modelaron deducciones fiscales (IVA), fletes ni notas de crédito por devoluciones.<br/>"
        "De las 24 órdenes válidas, <b>21 fueron entregadas</b> ($35,810.50). Las 3 órdenes restantes corresponden a compras en proceso "
        "(1 en tránsito por $950.00, 1 pendiente por $650.00 y 1 cancelada por $1,800.00).",
        style_body
    ))

    kpi_data = [
        [Paragraph("<b>Clave</b>", style_th), Paragraph("<b>Entidad Federativa</b>", style_th), Paragraph("<b>Pedidos Entregados</b>", style_th), Paragraph("<b>Ventas Netas</b>", style_th), Paragraph("<b>% Participación</b>", style_th), Paragraph("<b>Ticket Promedio</b>", style_th)],
        [Paragraph("YUC", style_td_center), Paragraph("Yucatán", style_td), Paragraph("3", style_td_center), Paragraph("$6,330.00", style_td_center), Paragraph("17.68%", style_td_center), Paragraph("$2,110.00", style_td_center)],
        [Paragraph("PUE", style_td_center), Paragraph("Puebla", style_td), Paragraph("3", style_td_center), Paragraph("$6,100.00", style_td_center), Paragraph("17.03%", style_td_center), Paragraph("$2,033.33", style_td_center)],
        [Paragraph("QRO", style_td_center), Paragraph("Querétaro", style_td), Paragraph("3", style_td_center), Paragraph("$4,400.00", style_td_center), Paragraph("12.29%", style_td_center), Paragraph("$1,466.67", style_td_center)],
        [Paragraph("JAL", style_td_center), Paragraph("Jalisco", style_td), Paragraph("2", style_td_center), Paragraph("$3,950.00", style_td_center), Paragraph("11.03%", style_td_center), Paragraph("$1,975.00", style_td_center)],
        [Paragraph("CDMX", style_td_center), Paragraph("Ciudad de México", style_td), Paragraph("2", style_td_center), Paragraph("$3,550.00", style_td_center), Paragraph("9.91%", style_td_center), Paragraph("$1,775.00", style_td_center)],
        [Paragraph("VER", style_td_center), Paragraph("Veracruz", style_td), Paragraph("1", style_td_center), Paragraph("$3,400.00", style_td_center), Paragraph("9.49%", style_td_center), Paragraph("$3,400.00", style_td_center)],
        [Paragraph("COAH", style_td_center), Paragraph("Coahuila", style_td), Paragraph("2", style_td_center), Paragraph("$2,810.00", style_td_center), Paragraph("7.85%", style_td_center), Paragraph("$1,405.00", style_td_center)],
        [Paragraph("NL", style_td_center), Paragraph("Nuevo León", style_td), Paragraph("2", style_td_center), Paragraph("$2,090.50", style_td_center), Paragraph("5.84%", style_td_center), Paragraph("$1,045.25", style_td_center)],
        [Paragraph("GTO", style_td_center), Paragraph("Guanajuato", style_td), Paragraph("2", style_td_center), Paragraph("$2,080.00", style_td_center), Paragraph("5.81%", style_td_center), Paragraph("$1,040.00", style_td_center)],
        [Paragraph("TAM", style_td_center), Paragraph("Tamaulipas", style_td), Paragraph("1", style_td_center), Paragraph("$1,100.00", style_td_center), Paragraph("3.07%", style_td_center), Paragraph("$1,100.00", style_td_center)],
        [Paragraph("<b>TOTAL</b>", style_td_center), Paragraph("<b>Consolidado General</b>", style_td_bold), Paragraph("<b>21 órdenes</b>", style_td_center), Paragraph("<b>$35,810.50</b>", style_td_center), Paragraph("<b>100.00%</b>", style_td_center), Paragraph("<b>$1,705.26</b>", style_td_center)],
    ]
    t_kpi = Table(kpi_data, colWidths=[40, 120, 85, 85, 84, 90])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-2,-1), [colors.white, c_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_kpi)
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 6: REFLEXIÓN CRÍTICA (PREGUNTAS 1 Y 2)
    # =========================================================================
    story.append(Paragraph("9. Respuestas Argumentadas a las Preguntas de Reflexión (Parte I)", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=10, spaceBefore=0))

    # Pregunta 1
    story.append(Paragraph("<b>Pregunta 1: ¿Qué ocurre si un cliente tiene estado vacío? ¿Se rechaza el cliente o se agrupa como no identificado?</b>", style_h2))
    story.append(Paragraph(
        "<b>Decisión de Diseño Adoptada:</b> Se agrupa como no identificado bajo la clave centinela <code>'NE'</code> (<i>No Especificado</i>) en <code>dim_cliente</code>.<br/>"
        "<b>Fundamentación Técnica:</b> En comercio electrónico, un usuario suele registrarse proporcionando únicamente nombre y correo electrónico, "
        "completando su domicilio fiscal o de entrega al realizar una compra posterior. Si el pipeline rechazara al cliente en la ingesta, "
        "cualquier orden futura generada por este usuario provocaría un fallo de integridad referencial (cliente inexistente / huérfano). "
        "Conforme a las mejores prácticas dimensionales de Ralph Kimball, la creación de registros centinela permite mantener intacto el árbol relacional, "
        "al tiempo que expone a los clientes incompletos para que el equipo de CRM detone campañas de actualización.<br/>"
        "<i>Diferencia con el Pedido:</i> Si un <u>pedido</u> reporta un estado de destino vacío o desconocido, la orden <b>sí debe rechazarse</b>, "
        "ya que el centro de distribución no puede despachar físicamente un paquete sin destino geográfico válido.",
        style_body
    ))
    story.append(Spacer(1, 10))

    # Pregunta 2
    story.append(Paragraph("<b>Pregunta 2: ¿Cómo detectarías pedidos que llegaron tarde?</b>", style_h2))
    story.append(Paragraph(
        "<b>Diagnóstico y Propuesta de Extensión:</b> El modelo actual únicamente captura <code>fecha_pedido</code>, lo cual impide medir la puntualidad de despacho. "
        "Para monitorear el cumplimiento de los acuerdos de nivel de servicio (SLA), se deben incorporar dos campos temporales en el sistema origen y en <code>fact_ordenes</code>:<br/>"
        "• <code>fecha_prometida_entrega DATE</code>: Plazo límite pactado con el cliente al momento de la compra.<br/>"
        "• <code>fecha_entrega_real DATE</code>: Marca de tiempo reportada por la empresa de paquetería al entregar el paquete.<br/>"
        "<b>Lógica de Detección en SQL:</b> La condición <code>DATEDIFF(fecha_entrega_real, fecha_prometida_entrega) > 0</code> clasifica la orden "
        "como tardía. A partir de esto se construye el indicador clave <b>OTIF (On-Time In-Full)</b>, permitiendo identificar qué transportistas o zonas "
        "presentan mayores cuellos de botella logísticos.",
        style_body
    ))
    story.append(Spacer(1, 10))

    # Matriz comparativa de decisiones de limpieza
    story.append(Paragraph("<b>Matriz Sintética de Decisiones de Limpieza y Calidad</b>", style_h2))
    matriz_data = [
        [Paragraph("<b>Defecto Detectado</b>", style_th), Paragraph("<b>Capa de Tratamiento</b>", style_th), Paragraph("<b>Estrategia Técnica</b>", style_th), Paragraph("<b>Justificación de Negocio</b>", style_th)],
        [Paragraph("Alias estatales ('N.L.', 'D.F.')", style_td), Paragraph("Staging", style_td_center), Paragraph("Cruce con catalogo_estados", style_td), Paragraph("Unifica segmentación geográfica sin perder clientes.", style_td)],
        [Paragraph("Fechas heterogéneas (DD/MM/AAAA)", style_td), Paragraph("Staging", style_td_center), Paragraph("STR_TO_DATE condicional con REGEXP", style_td), Paragraph("Permite tipado nativo DATE sin error 1411 en strict mode.", style_td)],
        [Paragraph("Montos <= 0 o negativos", style_td), Paragraph("Cuarentena", style_td_center), Paragraph("Aislamiento en pedidos_rechazados", style_td), Paragraph("Protege los ingresos y balances contables del Data Mart.", style_td)],
        [Paragraph("Transacciones duplicadas", style_td), Paragraph("Cuarentena / Mart", style_td_center), Paragraph("ROW_NUMBER() y UPSERT estable", style_td), Paragraph("Elimina sobreestimación de ventas y asegura idempotencia.", style_td)],
    ]
    t_matriz = Table(matriz_data, colWidths=[110, 60, 150, 184])
    t_matriz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_matriz)

    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 7: REFLEXIÓN CRÍTICA (PREGUNTA 3), REPRODUCIBILIDAD Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("10. Respuestas a Reflexión (Parte II), Entorno Docker y Conclusión", style_h1))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=10, spaceBefore=0))

    # Pregunta 3
    story.append(Paragraph("<b>Pregunta 3: ¿Cómo modificarías el proceso para admitir devoluciones?</b>", style_h2))
    story.append(Paragraph(
        "<b>Estrategia de Integración ETL y Modelado Dimensional:</b><br/>"
        "1. <b>Ingesta de Nueva Fuente:</b> Recibir un archivo complementario <code>devoluciones.csv</code> con campos <code>id_devolucion</code>, <code>id_pedido</code>, <code>fecha_devolucion</code>, <code>importe_devuelto</code> y <code>motivo_id</code>.<br/>"
        "2. <b>Validaciones en Staging:</b> Verificar integridad referencial (que el <code>id_pedido</code> exista en <code>fact_ordenes</code> y esté en estatus 'Entregado'), coherencia temporal (<code>fecha_devolucion >= fecha_pedido</code>) y consistencia económica (<code>importe_devuelto <= importe_pedido_original</code>).<br/>"
        "3. <b>Modelado Dimensional Recomendado:</b> Implementar una tabla de hechos dedicada <b><code>fact_devoluciones</code></b> vinculada a una dimensión <code>dim_motivo_devolucion</code>. Esto permite reflejar contablemente el impacto del reembolso en el periodo exacto en que ocurrió (sin alterar la foto histórica de la venta original) y recalcular las <b>Ventas Netas Reales</b> como:<br/>"
        "<font color='#1A365D'><b>Ventas Netas Reales = ∑ Ventas Entregadas - ∑ Importe Devoluciones</b></font>",
        style_body
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>11. Reproducibilidad Técnica y Entorno Docker</b>", style_h2))
    story.append(Paragraph(
        "Para garantizar reproducibilidad absoluta sin requerir instalación de dependencias en el sistema anfitrión "
        "(cumpliendo con la regla de gobernanza Docker del proyecto), el pipeline se ejecuta mediante el contenedor oficial "
        "<b>MySQL 8.0</b> configurado en <code>docker-compose.yml</code> y validado en el workflow de GitHub Actions [<code>.github/workflows/ci.yml</code>].<br/>"
        "Para ejecutar el pipeline automatizado de inicio a fin en una sola instrucción:<br/>"
        "<code><b>chmod +x unidad_4/ejecutar_laboratorio_docker.sh && ./unidad_4/ejecutar_laboratorio_docker.sh</b></code>",
        style_body
    ))
    story.append(Spacer(1, 10))

    # Conclusión ejecutiva
    story.append(Paragraph("<b>12. Conclusión Ejecutiva del Equipo 8</b>", style_h2))
    story.append(Paragraph(
        "El desarrollo del Laboratorio ETL para Casa&Estilo demostró que la construcción de un Data Mart no se limita a "
        "escribir sentencias SQL básicas, sino que exige una rigurosa arquitectura de ingeniería de datos: "
        "inmutabilidad en la capa de ingesta, normalización determinista en staging, aislamiento transparente de errores "
        "en mesas de rechazos, garantías de idempotencia para prevenir duplicidades contables y conciliaciones matemáticas "
        "de balance de masa. Estas prácticas aseguran que las decisiones estratégicas de la organización descansen sobre una base "
        "gobernada, precisa y reproducible.",
        style_body
    ))
    story.append(Spacer(1, 15))

    # Firmas
    firmas_data = [
        [Paragraph("<b>Sergio Jaziel Butzmann Martinez</b><br/>Matrícula: 2163239", style_td_center),
         Paragraph("<b>Arely Carrillo Sustaita</b><br/>Matrícula: 2226630", style_td_center),
         Paragraph("<b>Rafael Jesús Collazo Hernández</b><br/>Matrícula: 2169304", style_td_center)],
        [Paragraph("<i>Ingeniería en Tecnologías de Software</i>", style_td_center),
         Paragraph("<i>Ingeniería en Tecnologías de Software</i>", style_td_center),
         Paragraph("<i>Ingeniería en Tecnologías de Software</i>", style_td_center)],
    ]
    t_firmas = Table(firmas_data, colWidths=[168, 168, 168])
    t_firmas.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.75, c_secondary),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_firmas)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {output_pdf_path}")

if __name__ == '__main__':
    target_path = sys.argv[1] if len(sys.argv) > 1 else 'unidad_4/Equipo8_Laboratorio_ETL_Unidad_4.pdf'
    create_report(target_path)
