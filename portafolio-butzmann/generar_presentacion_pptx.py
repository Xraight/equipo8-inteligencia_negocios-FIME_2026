#!/usr/bin/env python3
"""
=============================================================================
GENERADOR DE PRESENTACIÓN EJECUTIVA HACKWITHINFY - SERGIO BUTZMANN
ESTILO OFICIAL: SYNTHWAVE RETRO-FUTURISTIC LAB (PORTAFOLIO BUTZMANN)
=============================================================================
Genera una presentación PowerPoint (.pptx) en formato widescreen 16:9 con
el diseño idéntico al Portafolio Butzmann:
- Paleta oficial: #070312 (Fondo), #0E0724 (Superficie), #140A2E (Tarjetas)
- Acentos neón: Pink #FF007F, Cyan #00F0FF, Purple #9D00FF, Amber #FF9900
- Tarjeta Cyberpunk Terminal sysinfo para "Acerca de Mí"
- Ejecutable 100% dentro de Docker (sin dependencias en el host)
=============================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Paleta Oficial Portafolio Butzmann (synthwave.css)
    BG_DEEP = RGBColor(7, 3, 18)           # #070312
    BG_SURFACE = RGBColor(14, 7, 36)       # #0e0724
    BG_CARD = RGBColor(20, 10, 46)         # #140a2e
    BG_TERMINAL = RGBColor(10, 5, 25)      # #0a0519
    BORDER_SUBTLE = RGBColor(65, 30, 105)  # rgba(168, 85, 247, 0.25)
    
    # Acentos Neón
    NEON_PINK = RGBColor(255, 0, 127)      # #ff007f
    NEON_CYAN = RGBColor(0, 240, 255)      # #00f0ff
    NEON_PURPLE = RGBColor(157, 0, 255)    # #9d00ff
    NEON_AMBER = RGBColor(255, 153, 0)     # #ff9900
    NEON_GREEN = RGBColor(39, 201, 63)     # #27c93f
    DOT_RED = RGBColor(255, 95, 86)        # #ff5f56
    DOT_YELLOW = RGBColor(255, 189, 46)    # #ffbd2e

    # Texto
    TEXT_PRIMARY = RGBColor(248, 246, 255) # #f8f6ff
    TEXT_SECONDARY = RGBColor(181, 169, 214)# #b5a9d6
    TEXT_MUTED = RGBColor(121, 108, 158)   # #796c9e
    TEXT_CODE_YELLOW = RGBColor(255, 230, 0)# #ffe600

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DEEP
        bg.line.fill.background()

        # Barra decorativa de perspectiva Synthwave en la parte inferior
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.42), Inches(13.333), Inches(0.08)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = NEON_PINK
        bar.line.fill.background()
        return bg

    def add_header(slide, tag_num, tag_text, title, subtitle):
        # Tag Synthwave // 0X · TAG
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.733), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"// {tag_num} · {tag_text.upper()}"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = NEON_CYAN
        p_tag.font.name = "Calibri"

        # Título principal con peso display
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_PRIMARY
        p_t.font.name = "Calibri"

        # Subtítulo descriptivo
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.36), Inches(11.733), Inches(0.38))
        tf_s = sub_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.size = Pt(11)
        p_s.font.color.rgb = TEXT_SECONDARY
        p_s.font.name = "Calibri"

    def add_card(slide, left, top, width, height, border_color=BORDER_SUBTLE, bg_color=BG_SURFACE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.4)
        return card

    # =========================================================================
    # SLIDE 1: ACERCA DE MÍ (CON TERMINAL CYBERPUNK SYSINFO)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    add_header(
        slide1,
        "01",
        "Perfil Profesional & Identidad Técnica",
        "Sergio Jaziel Butzmann Martínez",
        "Ingeniería en Inteligencia Artificial / Tecnologías de Software · UANL (FIME) · @Xraight"
    )

    col_w = Inches(3.68)
    gap = Inches(0.34)
    y_cards = Inches(1.85)
    h_cards = Inches(5.15)

    # Col 1: Formación & Liderazgo (Cyan)
    x1 = Inches(0.8)
    add_card(slide1, x1, y_cards, col_w, h_cards, border_color=NEON_CYAN)
    tb1 = slide1.shapes.add_textbox(x1 + Inches(0.25), y_cards + Inches(0.22), col_w - Inches(0.5), h_cards - Inches(0.44))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "🏛️ FORMACIÓN & LIDERAZGO"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NEON_CYAN

    items_col1 = [
        ("Alma Máter:", "Universidad Autónoma de Nuevo León (UANL) — Facultad de Ingeniería Mecánica y Eléctrica (FIME)."),
        ("Especialidad:", "Ingeniería en Inteligencia Artificial (IIA) y Tecnologías de Software (ITS)."),
        ("CIAO & Tech Lead:", "USAIGE — Liderazgo en arquitectura fullstack, servidores VPS, modelos RAG y pipelines de datos. Finalistas en Tiger Tank UANL 2026."),
        ("Analítica & Bases de Datos:", "Diseño dimensional de Data Marts, optimización de índices B-Tree y consultas analíticas de alto rendimiento en FIME."),
        ("Ubicación:", "Monterrey, Nuevo León, México.")
    ]
    for lbl, desc in items_col1:
        p_lbl = tf1.add_paragraph()
        p_lbl.text = f"\n• {lbl}"
        p_lbl.font.size = Pt(10)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_PRIMARY
        p_desc = tf1.add_paragraph()
        p_desc.text = f"  {desc}"
        p_desc.font.size = Pt(9.2)
        p_desc.font.color.rgb = TEXT_SECONDARY

    # Col 2: Stack & Especialización (Purple)
    x2 = x1 + col_w + gap
    add_card(slide1, x2, y_cards, col_w, h_cards, border_color=NEON_PURPLE)
    tb2 = slide1.shapes.add_textbox(x2 + Inches(0.25), y_cards + Inches(0.22), col_w - Inches(0.5), h_cards - Inches(0.44))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "⚡ STACK & ESPECIALIZACIÓN"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NEON_PURPLE

    items_col2 = [
        ("IA Aplicada & Agentes:", "Arquitecturas RAG avanzadas, embeddings semánticos, bases vectoriales y agentes autónomos (bucles ReAct)."),
        ("Edge Computing & Cloud:", "Cloudflare Workers, D1 (SQLite distribuido a nivel global) y arquitecturas serverless de latencia ultra-baja."),
        ("DevOps & Regla de Oro:", "Cero contaminación del host: 100% desarrollo en contenedores Docker y flujos automatizados de CI/CD con GitHub Actions."),
        ("Lenguajes & Herramientas:", "Python (FastAPI, Scikit-Learn, PyData), TypeScript, React, PostgreSQL/MySQL y arquitecturas limpias."),
    ]
    for lbl, desc in items_col2:
        p_lbl = tf2.add_paragraph()
        p_lbl.text = f"\n• {lbl}"
        p_lbl.font.size = Pt(10)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_PRIMARY
        p_desc = tf2.add_paragraph()
        p_desc.text = f"  {desc}"
        p_desc.font.size = Pt(9.2)
        p_desc.font.color.rgb = TEXT_SECONDARY

    # Col 3: Terminal Cyberpunk (Idéntico a AboutSection.tsx del Portafolio)
    x3 = x2 + col_w + gap
    add_card(slide1, x3, y_cards, col_w, h_cards, border_color=NEON_PINK, bg_color=BG_TERMINAL)
    
    # Barra de ventana terminal con los 3 dots
    tb_term_head = slide1.shapes.add_textbox(x3 + Inches(0.2), y_cards + Inches(0.15), col_w - Inches(0.4), Inches(0.4))
    tf_th = tb_term_head.text_frame
    p_th = tf_th.paragraphs[0]
    p_th.text = "● ● ●  butzmann@edge-node:~$ sysinfo"
    p_th.font.size = Pt(9.5)
    p_th.font.bold = True
    p_th.font.color.rgb = NEON_PINK
    p_th.font.name = "Courier New"

    tb3 = slide1.shapes.add_textbox(x3 + Inches(0.2), y_cards + Inches(0.6), col_w - Inches(0.4), h_cards - Inches(0.75))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    lines_terminal = [
        ('operator', '"Sergio Jaziel Butzmann"', TEXT_CODE_YELLOW),
        ('handle', '"@Xraight"', TEXT_CODE_YELLOW),
        ('aesthetic', '"Synthwave / Cyberpunk 80s"', TEXT_CODE_YELLOW),
        ('audio_synth', '"Web Audio API (No MP3)"', TEXT_CODE_YELLOW),
        ('status', '"🟢 Open to collaborate"', NEON_GREEN),
        ('philosophy', '"Functionality with High Aesthetics"', TEXT_CODE_YELLOW),
        ('host_pollution', '0.0% (100% Docker)', NEON_PINK),
        ('contact', '"sergio.butzmann.mtz@gmail.com"', TEXT_CODE_YELLOW),
        ('portfolio', '"butzmann.dev"', NEON_CYAN),
    ]
    for key, val, val_color in lines_terminal:
        p_line = tf3.add_paragraph() if tf3.paragraphs[0].text else tf3.paragraphs[0]
        p_line.text = f'{key}: {val},'
        p_line.font.size = Pt(9.2)
        p_line.font.name = "Courier New"
        p_line.font.color.rgb = val_color

    # =========================================================================
    # SLIDE 2: PERSPECTIVA SOBRE INTELIGENCIA ARTIFICIAL
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(
        slide2,
        "02",
        "Paradigmas, Evolución & Impacto Sistémico",
        "Mi Perspectiva sobre la Inteligencia Artificial",
        "De la inferencia pasiva a sistemas agénticos autónomos y decisiones en tiempo real"
    )

    # 3 Columnas
    # Card 1: Lo Más Interesante (Cyan)
    x1 = Inches(0.8)
    add_card(slide2, x1, y_cards, col_w, h_cards, border_color=NEON_CYAN)
    tb2_1 = slide2.shapes.add_textbox(x1 + Inches(0.25), y_cards + Inches(0.22), col_w - Inches(0.5), h_cards - Inches(0.44))
    tf2_1 = tb2_1.text_frame
    tf2_1.word_wrap = True

    p = tf2_1.paragraphs[0]
    p.text = "🔍 LO MÁS INTERESANTE"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NEON_CYAN

    points2_1 = [
        ("Sistemas RAG & Memoria:", "Superar el prompt estático: alimentar modelos con bases vectoriales y datos en vivo para erradicar alucinaciones."),
        ("Agentes Autónomos (ReAct):", "Modelos que planifican, razonan, invocan terminales y herramientas (MCP) y auto-corrigen errores iterativamente."),
        ("Inferencia Eficiente en el Edge:", "Modelos compactos (SLMs) ejecutándose localmente con privacidad de datos y latencia cero."),
        ("Convergencia BI + Text-to-SQL:", "Modelado semántico que traduce preguntas de negocio complejas en SQL optimizado con gobernanza de datos.")
    ]
    for title, desc in points2_1:
        p_t = tf2_1.add_paragraph()
        p_t.text = f"\n▸ {title}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_PRIMARY
        p_d = tf2_1.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(9.2)
        p_d.font.color.rgb = TEXT_SECONDARY

    # Card 2: Evolución de la IA (Purple)
    x2 = x1 + col_w + gap
    add_card(slide2, x2, y_cards, col_w, h_cards, border_color=NEON_PURPLE)
    tb2_2 = slide2.shapes.add_textbox(x2 + Inches(0.25), y_cards + Inches(0.22), col_w - Inches(0.5), h_cards - Inches(0.44))
    tf2_2 = tb2_2.text_frame
    tf2_2.word_wrap = True

    p = tf2_2.paragraphs[0]
    p.text = "🚀 VISIÓN DE EVOLUCIÓN"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NEON_PURPLE

    points2_2 = [
        ("De Chatbots a Colegas de Software:", "Transición desde una ventana de chat aislada hacia agentes embebidos en el ciclo continuo del IDE y CI/CD."),
        ("Arquitecturas Híbridas:", "Convergencia del rigor determinista (bases de datos SQL, algoritmos de grafos) con la flexibilidad probabilística de los LLMs."),
        ("El Rol del Ingeniero se Eleva:", "El valor profesional pasa de recordar sintaxis repetitiva al diseño de arquitectura, pruebas y validación formal."),
        ("Enjambres Multi-Agente:", "Modelos especializados que colaboran, depuran y auditan mutuamente la seguridad antes del despliegue.")
    ]
    for title, desc in points2_2:
        p_t = tf2_2.add_paragraph()
        p_t.text = f"\n▸ {title}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_PRIMARY
        p_d = tf2_2.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(9.2)
        p_d.font.color.rgb = TEXT_SECONDARY

    # Card 3: Impacto Multidimensional (Amber)
    x3 = x2 + col_w + gap
    add_card(slide2, x3, y_cards, col_w, h_cards, border_color=NEON_AMBER)
    tb2_3 = slide2.shapes.add_textbox(x3 + Inches(0.25), y_cards + Inches(0.22), col_w - Inches(0.5), h_cards - Inches(0.44))
    tf2_3 = tb2_3.text_frame
    tf2_3.word_wrap = True

    p = tf2_3.paragraphs[0]
    p.text = "🌐 IMPACTO MULTIDIMENSIONAL"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = NEON_AMBER

    points2_3 = [
        ("En la Tecnología:", "Aceleración 10x del time-to-market. Equipos pequeños pueden orquestar arquitecturas de nivel corporativo global."),
        ("En las Profesiones:", "No desplaza al ingeniero capacitado; amplifica exponencialmente a quien domina fundamentos y pensamiento crítico."),
        ("En la Sociedad & Ética:", "Capacidad inédita para resolver desafíos complejos en medicina personalizada, movilidad y educación."),
        ("Gobernanza Necesaria:", "Exigencia de auditoría algorítmica, trazabilidad de datos y reproducibilidad en contenedores aislados.")
    ]
    for title, desc in points2_3:
        p_t = tf2_3.add_paragraph()
        p_t.text = f"\n▸ {title}"
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_PRIMARY
        p_d = tf2_3.add_paragraph()
        p_d.text = f"  {desc}"
        p_d.font.size = Pt(9.2)
        p_d.font.color.rgb = TEXT_SECONDARY

    # =========================================================================
    # SLIDE 3: EXPERIENCIA EN HACKWITHINFY MÉXICO
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(
        slide3,
        "03",
        "Caso de Éxito & Lecciones de Innovación Competitiva",
        "Experiencia en HackWithInfy México & Reto Infosys",
        "1er Lugar Reto Infosys con Vygo · Aprendizajes bajo presión y recomendaciones para futuras ediciones"
    )

    quad_w = Inches(5.7)
    quad_h = Inches(2.45)
    gap_x = Inches(0.33)
    gap_y = Inches(0.25)
    top_row_y = Inches(1.85)
    bottom_row_y = top_row_y + quad_h + gap_y

    # Cuadrante 1: Hito (Green)
    add_card(slide3, Inches(0.8), top_row_y, quad_w, quad_h, border_color=NEON_GREEN)
    tb3_1 = slide3.shapes.add_textbox(Inches(1.05), top_row_y + Inches(0.18), quad_w - Inches(0.5), quad_h - Inches(0.36))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True

    p = tf3_1.paragraphs[0]
    p.text = "🏆 EL MOMENTO CUMBRE: 1ER LUGAR CON VYGO"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NEON_GREEN

    p = tf3_1.add_paragraph()
    p.text = "• Proyecto Ganador 'Vygo':"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_1.add_paragraph()
    p.text = "  Backend de alta concurrencia en tiempo real, integración de modelos de prioridad y cálculo de rutas inteligentes optimizadas ante incidentes viales."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf3_1.add_paragraph()
    p.text = "• Experiencia Contra Reloj:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_1.add_paragraph()
    p.text = "  Diseño, programación ininterrumpida y despliegue con configuración DNS y CI/CD automatizado, culminando con la victoria en el Reto Infosys."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    # Cuadrante 2: Aprendizajes (Cyan)
    add_card(slide3, Inches(0.8) + quad_w + gap_x, top_row_y, quad_w, quad_h, border_color=NEON_CYAN)
    tb3_2 = slide3.shapes.add_textbox(Inches(1.05) + quad_w + gap_x, top_row_y + Inches(0.18), quad_w - Inches(0.5), quad_h - Inches(0.36))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True

    p = tf3_2.paragraphs[0]
    p.text = "🧠 PRINCIPALES APRENDIZAJES"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NEON_CYAN

    p = tf3_2.add_paragraph()
    p.text = "• Docker como Blindaje Técnico:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_2.add_paragraph()
    p.text = "  Tener el stack dockerizado eliminó el clásico 'en mi máquina sí funciona', permitiendo iterar a alta velocidad sin fricciones entre compañeros."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf3_2.add_paragraph()
    p.text = "• Impacto Demostrable > Complejidad Inflada:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_2.add_paragraph()
    p.text = "  Los jueces evalúan la solución de valor demostrable y la baja latencia de respuesta antes que código inflado o funcionalidades a medias."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    # Cuadrante 3: Recomendaciones Participantes (Purple)
    add_card(slide3, Inches(0.8), bottom_row_y, quad_w, quad_h, border_color=NEON_PURPLE)
    tb3_3 = slide3.shapes.add_textbox(Inches(1.05), bottom_row_y + Inches(0.18), quad_w - Inches(0.5), quad_h - Inches(0.36))
    tf3_3 = tb3_3.text_frame
    tf3_3.word_wrap = True

    p = tf3_3.paragraphs[0]
    p.text = "💡 RECOMENDACIONES PARA PARTICIPANTES"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NEON_PURPLE

    p = tf3_3.add_paragraph()
    p.text = "1. Pre-construir Plantillas en Docker:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_3.add_paragraph()
    p.text = "   No gastar las primeras horas configurando Node, Python o Postgres en local. Llegar con plantillas listas y reproducibles en contenedores."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf3_3.add_paragraph()
    p.text = "2. Pitch con Datos en Tiempo Real:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_3.add_paragraph()
    p.text = "   Una demo en vivo con métricas de rendimiento y latencia medible convence mucho más que 20 diapositivas teóricas."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    # Cuadrante 4: Recomendaciones Infosys (Amber)
    add_card(slide3, Inches(0.8) + quad_w + gap_x, bottom_row_y, quad_w, quad_h, border_color=NEON_AMBER)
    tb3_4 = slide3.shapes.add_textbox(Inches(1.05) + quad_w + gap_x, bottom_row_y + Inches(0.18), quad_w - Inches(0.5), quad_h - Inches(0.36))
    tf3_4 = tb3_4.text_frame
    tf3_4.word_wrap = True

    p = tf3_4.paragraphs[0]
    p.text = "🚀 RECOMENDACIONES PARA EL COMITÉ INFOSYS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NEON_AMBER

    p = tf3_4.add_paragraph()
    p.text = "1. Retos con Streams de Datos en Vivo:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_4.add_paragraph()
    p.text = "   Incentivar desafíos basados en flujos de telemetría y APIs activas que desafíen la escalabilidad y resiliencia arquitectónica del equipo."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    p = tf3_4.add_paragraph()
    p.text = "2. Mentorías de Arquitectura 1-a-1:"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p = tf3_4.add_paragraph()
    p.text = "   Espacios de retroalimentación de 10 minutos con ingenieros senior de Infosys durante la madrugada del evento elevan exponencialmente el nivel técnico."
    p.font.size = Pt(8.8)
    p.font.color.rgb = TEXT_SECONDARY

    # Guardar presentación
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(out_dir, "presentacion_hackwithinfy_butzmann.pptx")
    prs.save(out_path)
    print(f"✅ Presentación PPTX 16:9 generada exitosamente en:\n   {out_path}")

if __name__ == "__main__":
    create_deck()
