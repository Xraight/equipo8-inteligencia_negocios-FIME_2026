# 📖 Documentación Oficial: Presentación Ejecutiva HackWithInfy México (Estilo Portafolio Butzmann)

> **Autor:** Sergio Jaziel Butzmann Martínez (`@Xraight`)  
> **Institución:** Universidad Autónoma de Nuevo León (UANL) — Facultad de Ingeniería Mecánica y Eléctrica (FIME)  
> **Estilo Visual:** Synthwave Retro-Futuristic Lab (`portafolio-butzmann`)  
> **Formato:** Presentación Ejecutiva 16:9 Widescreen (.pptx) & Visor Web Interactivo (.html)  
> **Entorno de Ejecución:** 100% Contenedorizado en Docker (Cero dependencias en el host)  

---

## 🎨 1. Sistema de Diseño Idéntico al Portafolio (`synthwave.css`)

Tanto el visor web interactivo como la presentación PowerPoint generada adoptan con fidelidad absoluta los tokens de diseño, tipografías y efectos visuales de tu portafolio personal:

| Token / Elemento | Valor / Implementación | Aplicación en la Presentación |
| :--- | :--- | :--- |
| **Fondo Base** | `--bg-deep: #070312` | Fondo inmersivo espacial oscuro. |
| **Superficie de Tarjetas** | `--bg-surface: #0e0724` / `--bg-card: rgba(20, 10, 46, 0.78)` | Tarjetas modulares de cristal con resplandor suave. |
| **Terminal Cyberpunk** | `--bg-terminal: #0a0519` + bordes neón rosa | Componente `sysinfo` con los dots estilo Unix (`#ff5f56`, `#ffbd2e`, `#27c93f`). |
| **Acento Neón Rosa** | `--neon-pink: #ff007f` | Barra decorativa synthwave, bordes y botones de acción principal. |
| **Acento Neón Cian** | `--neon-cyan: #00f0ff` | Titulares técnicos, tags `// 0X ·`, tarjetas de RAG y badges de stack. |
| **Acento Neón Púrpura** | `--neon-purple: #9d00ff` | Tarjetas de agentes autónomos, evolución de IA y DevOps. |
| **Acento Neón Ámbar** | `--neon-amber: #ff9900` | Tarjetas de impacto multidimensional y recomendaciones estratégicas. |
| **Acento Verde Éxito** | `--neon-green: #27c93f` | Indicador de 1er Lugar Reto Infosys y status `🟢 Open to collaborate`. |
| **Tipografía Display** | Google Font `Orbitron` | Encabezados, títulos de sección y botones en mayúsculas con espaciado amplio. |
| **Tipografía Lectura** | Google Font `Outfit` | Párrafos y descripciones de tarjetas con alta legibilidad. |
| **Tipografía Código** | Google Font `JetBrains Mono` | Tags, indicadores de terminal y badges de tecnologías. |
| **Ambiente Retro** | Sol ochentero con scanlines + Rejilla 3D | Sol con franjas animado y suelo de rejilla en perspectiva (`rotateX(65deg)`). |
| **Efecto CRT** | Scanlines CRT intercambiables | Capa de líneas CRT activable con el botón o presionando la tecla `C`. |
| **Audio Sintetizado** | Web Audio API (`SoundFX`) | Generación en tiempo real de tonos láser y switch (cero archivos MP3 externos). |

---

## 📑 2. Estructura y Contenido de las 3 Diapositivas

### 🪪 Slide 1: Acerca de Mí (Identidad, Formación & Pasión)
- **Titular:** Sergio Jaziel Butzmann Martínez (`@Xraight`)
- **Subtítulo:** Ingeniería en Inteligencia Artificial / Tecnologías de Software · UANL (FIME)
- **Columna 1 (Cian):** Alma máter en FIME (UANL), especialidad en IA y software, CIAO & Tech Lead en USAIGE (finalistas Tiger Tank 2026), modelado dimensional en bases de datos.
- **Columna 2 (Púrpura):** Stack técnico (RAG avanzado, embeddings, bases vectoriales, Cloudflare D1/Workers, Docker, CI/CD con GitHub Actions).
- **Columna 3 (Terminal Cyberpunk):** Bloque `sysinfo` con metadatos del operador, estética Synthwave, filosofía *"Functionality with High Aesthetics"* y tasa de contaminación del host (`0.0%`).

### 🧠 Slide 2: Perspectiva sobre la Inteligencia Artificial
- **Titular:** Mi Perspectiva sobre la Inteligencia Artificial
- **Subtítulo:** De la inferencia pasiva a sistemas agénticos autónomos y decisiones en tiempo real
- **Columna 1 (Cian - Lo Más Interesante):** RAG dinámico contra alucinaciones, agentes autónomos con bucles ReAct y llamadas a herramientas (MCP), inferencia local ultrarrápida con SLMs en el Edge, Text-to-SQL guiado por modelos semánticos.
- **Columna 2 (Púrpura - Evolución):** De interfaces de chat a "colegas de software" dentro del IDE y CI/CD; arquitecturas híbridas deterministas + probabilísticas; elevación del rol del programador hacia la arquitectura y validación formal.
- **Columna 3 (Ámbar - Impacto Sistémico):** Reducción de tiempos de desarrollo (10x), amplificación de habilidades humanas, aplicaciones transformadoras en medicina y logística, gobernanza ética con trazabilidad en contenedores.

### 🏆 Slide 3: Experiencia en HackWithInfy México & Reto Infosys
- **Titular:** Experiencia en HackWithInfy México & Reto Infosys
- **Subtítulo:** 1er Lugar Reto Infosys con Vygo · Aprendizajes bajo presión y recomendaciones para futuras ediciones
- **Cuadrante 1 (Verde - El Hito):** Creación de *Vygo*: backend de alta concurrencia en tiempo real, integración de modelos de prioridad y cálculo de rutas inteligentes optimizadas ante incidentes viales.
- **Cuadrante 2 (Cian - Aprendizajes):** La contenedorización con Docker como blindaje frente a fallos de demo; priorización del impacto medible de negocio antes que código inflado.
- **Cuadrante 3 (Púrpura - Consejos Participantes):** Pre-construir plantillas en Docker para no perder horas de configuración; realizar demos en vivo con datos y métricas de latencia reales.
- **Cuadrante 4 (Ámbar - Propuestas Infosys):** Continuar planteando desafíos basados en streams de datos y APIs en tiempo real; fomentar sesiones de mentoría técnica 1-a-1 de 10 minutos con ingenieros senior de Infosys.

---

## 🎙️ 3. Guion de Exposición por Diapositiva (*Speaker Notes*)

Duración total recomendada: **4 minutos** (aprox. 80-90 segundos por diapositiva).

### Diapositiva 1 (90s):
> *"¡Hola! Mi nombre es Sergio Jaziel Butzmann Martínez. Estudio Ingeniería en Inteligencia Artificial en la FIME de la Universidad Autónoma de Nuevo León. Actualmente me desempeño como CIAO y líder técnico en USAIGE, donde construimos arquitecturas RAG y flujos continuos de datos para alta disponibilidad, proyecto con el que llegamos a la final de UANL Tiger Tank.*  
> *Mi especialidad técnica se basa en el edge computing con Cloudflare, sistemas distribuidos, DevOps y la inteligencia artificial aplicada, con una filosofía inquebrantable: cero dependencias en el sistema anfitrión, 100% desarrollo en Docker y CI/CD automatizado.*  
> *En lo personal, soy un apasionado de la estética Synthwave y la síntesis de audio retro, porque creo firmemente que el software de alto rendimiento merece interfaces memorables que inspiren."*

### Diapositiva 2 (90s):
> *"Mi perspectiva sobre la IA se aleja de la simple generación de texto para enfocarse en sistemas agénticos autónomos con memoria persistente y razonamiento sobre herramientas operacionales. Veo una clara convergencia entre el rigor determinista de las bases de datos relacionales y la flexibilidad de los modelos probabilísticos.*  
> *Respecto a su evolución, transitamos de ventanas de chat a 'colegas de software' integrados en el IDE y en el pipeline de CI/CD. El valor del ingeniero ya no está en memorizar sintaxis, sino en la arquitectura y validación formal de sistemas.*  
> *En el plano social, esto desbloquea soluciones críticas en medicina y logística urbana, exigiéndonos un compromiso ético absoluto en trazabilidad y privacidad."*

### Diapositiva 3 (90s):
> *"Nuestra experiencia en los retos de Infosys culminó con el 1er lugar gracias a Vygo, una plataforma de rutas inteligentes y prioridad ante incidentes en tiempo real. La clave del éxito fue llegar con un stack dockerizado que garantizó estabilidad total durante la demo en vivo ante los jueces.*  
> *Mi recomendación para futuros participantes es priorizar el impacto del negocio y la demo en tiempo real sobre código inflado; y para el comité de Infosys, continuar potenciando estos retos con flujos de datos reales y mentorías técnicas 1-a-1 durante la madrugada del evento."*

---

## 🐳 4. Instrucciones de Ejecución con Docker

### Generar la Presentación PowerPoint (.pptx):
```bash
docker run --rm \
  -v "$(pwd)":/workspace \
  -w /workspace \
  localhost/equipo8-u5-generator \
  python3 generar_presentacion_pptx.py
```

### Ejecutar el Visor Web Interactivo:
Abre [presentacion_interactiva.html](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/portafolio-butzmann/presentacion_interactiva.html) en tu navegador.
- **`◀` / `▶` o `Espacio`:** Avanzar / retroceder diapositiva.
- **`N`:** Mostrar / ocultar panel flotante de notas de orador.
- **`F`:** Modo pantalla completa.
- **`C`:** Activar / desactivar filtro de Scanlines CRT.
- **`M`:** Activar / desactivar efectos de sonido retro Web Audio API.
- **`Ctrl + P`:** Imprimir o guardar en PDF en alta resolución.
