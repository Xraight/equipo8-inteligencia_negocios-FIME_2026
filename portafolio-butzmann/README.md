# 🌌 Presentación Ejecutiva HackWithInfy México · Sergio Butzmann

Entregable oficial para **HackWithInfy México**: Presentación ejecutiva de 3 diapositivas sobre perfil profesional, perspectiva estratégica sobre Inteligencia Artificial y caso de éxito/lecciones en retos de innovación Infosys.

Desarrollado con una arquitectura **100% aislada en Docker**, respetando la regla de cero contaminación del sistema anfitrión (*Zero Host Pollution*) y respaldado con un pipeline de validación automatizada CI/CD.

---

## 👥 Datos del Autor
- **Nombre:** Sergio Jaziel Butzmann Martínez
- **Institución:** Universidad Autónoma de Nuevo León (UANL) — Facultad de Ingeniería Mecánica y Eléctrica (FIME)
- **Especialidad:** Ingeniería en Inteligencia Artificial (IIA) / Tecnologías de Software (ITS)
- **Liderazgo:** CIAO & Tech Lead en USAIGE (Finalistas UANL Tiger Tank 2026) · Ganador Reto Infosys HackMTY con *Vygo*
- **Contacto:** sergio.butzmann.mtz@gmail.com · [GitHub @Xraight](https://github.com/Xraight) · [Portafolio butzmann.dev](https://butzmann.dev)

---

## 📑 Estructura de las 3 Diapositivas

| Slide | Título / Eje Temático | Contenido Principal |
| :---: | :--- | :--- |
| **01** | **Acerca de Mí** | Formación académica en FIME (UANL), especialidad en IA y software, liderazgo en USAIGE, especialización en RAG y edge computing, pasión estética Synthwave y filosofía *"Functionality with High Aesthetics"*. |
| **02** | **Perspectiva sobre IA** | Aspectos clave (RAG avanzado, memoria persistente, inferencia local en el Edge, Text-to-SQL y BI semántico), transición hacia agentes autónomos y análisis del impacto transformador en la ingeniería y la sociedad. |
| **03** | **Experiencia en HackWithInfy** | Caso de éxito: 1er Lugar en el Reto Infosys con *Vygo* (backend en tiempo real y cálculo de rutas con prioridad), aprendizajes de trabajo bajo presión y recomendaciones prácticas para futuros participantes y organizadores. |

---

## 📦 Archivos del Proyecto

```text
portafolio-butzmann/
├── generar_presentacion_pptx.py           # Script generador en Python usando python-pptx (ejecutable en Docker)
├── presentacion_hackwithinfy_butzmann.pptx # Presentación PowerPoint widescreen 16:9 generada
├── presentacion_interactiva.html          # Visor web interactivo con notas de orador y exportación PDF
├── SLIDES_DOCUMENTATION.md                # Documentación exhaustiva, guion de orador y justificación de diseño
├── validar_presentacion_docker.sh         # Script de validación automatizada CI/CD
└── README.md                              # Este archivo
```

---

## 🚀 Guía Rápida de Uso

### 1. Generar la Presentación PowerPoint (.pptx) con Docker
```bash
docker run --rm \
  -v "$(pwd)":/workspace \
  -w /workspace \
  localhost/equipo8-u5-generator \
  python3 generar_presentacion_pptx.py
```

### 2. Ejecutar la Validación Automatizada (CI/CD Local)
```bash
chmod +x validar_presentacion_docker.sh
./validar_presentacion_docker.sh
```

### 3. Abrir el Visor Interactivo Web
Abre directamente [presentacion_interactiva.html](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/portafolio-butzmann/presentacion_interactiva.html) en tu navegador.
- **Teclas de navegación:** Flechas `◀` y `▶` o `Espacio`.
- **Modo Presentador / Notas:** Presiona la tecla `N` para desplegar el guion de orador.
- **Pantalla Completa:** Presiona `F`.
- **Exportar a PDF:** Haz clic en *"Imprimir / PDF"* o presiona `Ctrl + P`.
