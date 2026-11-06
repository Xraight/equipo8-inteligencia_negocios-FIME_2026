# 🛋️ Casa&Estilo - Data Mart de Ventas (Inteligencia de Negocios)

Repositorio oficial del **Equipo 8** para la unidad de aprendizaje de Inteligencia de Negocios (FIME, 2026). Este proyecto abarca el diseño dimensional, implementación física, consultas analíticas (OLAP), optimización y automatización de un Data Mart de Ventas para la empresa de retail **Casa&Estilo**.

---

## 👥 Miembros del Equipo
- **Arely Carrillo Sustaita** - 2226630
- **Rafael Jesús Collazo Hernández** - 2169304
- **Sergio Jaziel Butzmann Martinez** - 2163239

---

## 📂 Estructura General del Repositorio

El repositorio se encuentra organizado por unidades temáticas para facilitar la trazabilidad académica y técnica:

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml                      # Propuesta de CI/CD para validación de DDL y SQL
├── .docker/
│   └── servers.json                    # Preconfiguración del servidor para pgAdmin 4
├── docker-compose.yml                  # Entorno Docker para PostgreSQL 16 + pgAdmin 4 Web
├── GUIA_VISUALIZACION_EQUIPO.md        # Guía interactiva de visualización de datos y tablas
├── unidad_2/                           # Entregables y modelo base de Unidad 2
│   ├── Casa_Estilo_Diagrama_ER.drawio  # Diagrama entidad-relación / esquema estrella
│   ├── Equipo8_Practica_Unidad_2.pdf   # Reporte formal de la práctica
│   ├── Retail Equipo 8 Practica Unidad 2.pdf # Presentación del caso de estudio
│   ├── script dll.sql                  # Script DDL de PostgreSQL
│   ├── script_datos_simulados.sql      # Población de datos simulados para script dll.sql
│   ├── documentacion_datos_simulados.md # Documentación técnica de datos simulados
│   └── README.md                       # Documentación de Unidad 2
└── unidad_3/                           # Desarrollo técnico y analítico de Unidad 3
    ├── 01_modelo_unidad_2/             # Modelo dimensional base de Unidad 2
    │   ├── Casa_Estilo_Diagrama_ER.drawio # Esquema estrella dimensional
    │   ├── grano_y_diccionario_datos.md   # Grano de hechos y diccionario de dimensiones
    │   ├── ficha_decisiones_negocio.md    # 5 preguntas de negocio y rentabilidad con flete
    │   └── README.md
    ├── 02_ddl_y_datos/                 # Scripts DDL y datos de prueba / seeds
    │   ├── 01_ddl_schema.sql           # DDL idempotente del esquema estrella
    │   ├── 02_carga_datos.sql          # Carga determinista de 1,250 filas (Q1 y Q2 2026)
    │   ├── 03_verificacion_calidad_datos.sql # Auditoría de calidad, volumen y FKs
    │   └── README.md
    ├── 03_prompts_ia/                  # Registro de prompts e interacciones con IA
    │   ├── 01_prompt_inicial_reto1.md  # Prompt obligatorio de Reto 1 y revisión crítica
    │   ├── 02_prompt_error_agrupacion_1055.md # Reto 2: Diagnóstico de ONLY_FULL_GROUP_BY
    │   ├── 03_prompt_optimizacion_explain.md  # Reto 3: Asesoría de índices y EXPLAIN
    │   ├── 04_prompt_stored_procedure.md      # Reto 4: Parametrización en stored procedure
    │   ├── registro_decisiones_ia.md   # Matriz de decisiones y evidencia técnica
    │   └── README.md
    ├── 04_consultas_sql/               # Consultas analíticas y KPIs de negocio
    │   ├── 01_consulta_inicial_ia.sql  # Versión inicial sin validar de la IA
    │   ├── 02_consulta_final_validada.sql # Consulta final validada Top 5 regional Q2 vs Q1
    │   ├── 03_consultas_control_auditoria.sql # Pruebas de control de grano y muestra manual
    │   ├── 04_diferencias_sintaxis_motores.sql # Equivalencias PostgreSQL 16 vs MySQL 8
    │   └── README.md
    ├── 05_validacion_y_explain/        # Planes de ejecución (EXPLAIN) y optimización
    │   ├── 01_depuracion_error_1055.sql # Demostración y corrección de error 1055 / 42803
    │   ├── reporte_depuracion_1055.md   # Reporte formal de causa raíz y estándar SQL
    │   ├── 02_optimizacion_explain.sql  # Benchmarking con EXPLAIN ANALYZE antes y después
    │   ├── reporte_optimizacion_explain.md # Comparativa de costos e índices compuestos
    │   └── README.md
    ├── 06_stored_procedure/            # Procedimientos almacenados y funciones PL/pgSQL
    │   ├── 01_sp_reporte_rentabilidad_top5.sql # Rutina parametrizada por año y trimestre
    │   ├── 02_llamadas_de_prueba.sql   # Pruebas en escenario normal y caso límite
    │   ├── documentacion_stored_procedure.md # Especificación técnica y evidencias de salida
    │   └── README.md
    ├── 07_conclusion/                  # Conclusiones, hallazgos y reporte ejecutivo
    │   ├── conclusion_final.md         # Informe ejecutivo, juicio crítico y guión oral 5 min
    │   └── README.md
    └── README.md                       # Índice maestro de Unidad 3
└── unidad_4/                           # Laboratorio ETL: Del Archivo Crudo al Data Mart (MySQL 8.0)
    ├── 01_datos_crudos/                # DDL base, catálogo canónico y archivos crudos (pedidos/clientes)
    ├── 02_perfilado/                   # Detección de anomalías y tabla observaciones_perfilado
    ├── 03_staging_y_normalizacion/     # Normalización estatal canónica y tipado estricto DATE
    ├── 04_validacion_y_rechazos/       # Reglas de negocio, mesa de rechazos (cuarentena) y pedidos limpios
    ├── 05_carga_incremental/          # DDL del Data Mart y UPSERT con verificación de idempotencia
    ├── 06_conciliacion_auditoria/      # Balance de masa (raw = limpias + rechazadas) y etl_auditoria
    ├── 07_indicadores/                 # Ventas netas y entregas por estado y fecha
    ├── 08_reflexion/                   # Reflexión técnica sobre decisiones de limpieza
    ├── script_maestro_etl.sql          # Pipeline unificado reproducible de inicio a fin
    ├── ejecutar_laboratorio_docker.sh  # Script de ejecución automatizada en Docker
    └── README.md                       # Índice maestro de Unidad 4
└── unidad_5/                           # Del Data Mart al Dashboard Ejecutivo y al Comité Directivo
    ├── 01_datos_crudos/                # 4 CSVs originales e inmutables (1,200 transacciones)
    ├── 02_calidad_y_powerquery/        # Ingesta, tipado estricto, perfilado y código M
    ├── 03_modelo_estrella_powerpivot/  # Esquema estrella, cardinalidades 1:N y Time Intelligence
    ├── 04_medidas_dax/                 # 6 medidas fundamentales + comparativas YoY
    ├── 05_validacion_numerica/         # Conciliación cuantitativa (discrepancia $0.00)
    ├── 06_dashboard_ejecutivo/         # Maquetación, tarjetas KPI, gráficos y segmentadores
    ├── 07_analisis_cuatro_niveles/     # Descriptivo, diagnóstico, predictivo y prescriptivo
    ├── 08_comite_directivo/            # Deck de 7 slides, guion oral 15 min y bitácora IA
    ├── scripts_generacion/             # Automatización en Python (OpenPyXL, python-pptx, ReportLab)
    ├── Dockerfile                      # Entorno contenedorizado (Python 3.12-slim)
    ├── ejecutar_laboratorio_docker.sh  # Runner automatizado maestro 100% reproducible
    ├── U5_Dashboard_Equipo08.xlsx      # Entregable: Libro Excel con Modelo, DAX y Tablero
    ├── U5_Comite_Equipo08.pptx         # Entregable: Presentación ejecutiva (7 diapositivas 16:9)
    ├── U5_Evidencias_Equipo08.pdf      # Entregable: Reporte formal de evidencias académicas
    └── README.md                       # Índice maestro de Unidad 5
└── PIA/                                # Producto Integrador de Aprendizaje: Solución BI Casa&Estilo (30%)
    ├── 01_arquitectura_datos/          # Diagrama ER, Esquema Estrella, Diccionario y Justificación
    ├── 02_datamart_mysql/              # DDL Staging, DDL Data Mart, SPs ETL, Vistas y Balance de Masa
    ├── 03_dashboard_excel/             # Catálogo de 10 medidas DAX y especificación del tablero
    ├── 04_presentacion_ejecutiva/      # Guion de storytelling de 15 min y contenido de 10 diapositivas
    ├── scripts_docker/                 # Automatización en Python para generación de artefactos
    ├── ejecutar_pia_docker.sh          # Runner maestro 100% reproducible en Docker
    ├── PIA_Dashboard_CasaEstilo_Equipo08.xlsx # Entregable: Tablero Ejecutivo interactivo
    ├── PIA_Comite_CasaEstilo_Equipo08.pptx    # Entregable: Deck de 10 diapositivas para Comité Directivo
    ├── PIA_Evidencias_CasaEstilo_Equipo08.pdf # Entregable: Reporte formal de evidencias académicas
    ├── PIA_Equipo08_CasaEstilo.zip     # Entregable Oficial: Empaque unificado con todos los archivos
    └── README.md                       # Índice maestro del PIA
```

---

## 📑 Unidades del Proyecto

### 🔹 [Unidad 2: Modelado Dimensional y Arquitectura](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_2/README.md)
- **Función General:** Diseño del esquema estrella (Star Schema) enfocado en el grano de línea de orden de venta para retail.
- **Entregables:** Diagrama ER dimensional en draw.io, script DDL en PostgreSQL, datos simulados y reportes documentales.

### 🔹 [Unidad 3: Implementación, Consultas y Optimización](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/README.md)
Estructurada en 7 fases especializadas:
1. [`01_modelo_unidad_2`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/01_modelo_unidad_2/README.md): Arquitectura dimensional de referencia.
2. [`02_ddl_y_datos`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/02_ddl_y_datos/README.md): Creación de tablas y población de datos representativos.
3. [`03_prompts_ia`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/03_prompts_ia/README.md): Registro metodológico de asistencia con IA generativa.
4. [`04_consultas_sql`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/04_consultas_sql/README.md): Consultas analíticas para resolver interrogantes de negocio.
5. [`05_validacion_y_explain`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/05_validacion_y_explain/README.md): Auditoría de desempeño, métricas de ejecución y optimización con índices.
6. [`06_stored_procedure`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/06_stored_procedure/README.md): Funciones PL/pgSQL y procedimientos almacenados para lógica recurrente.
7. [`07_conclusion`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_3/07_conclusion/README.md): Resumen ejecutivo, respuestas a los objetivos comerciales y aprendizajes.

### 🔹 [Unidad 4: Laboratorio ETL - Del Archivo Crudo al Data Mart](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_4/README.md)
- **Función General:** Construcción de un pipeline ETL completo, reproducible e idempotente en MySQL 8.0 para migrar archivos crudos con anomalías intencionales (`clientes.csv`, `pedidos.sql`, `catalogo_estados.csv`) hacia un Data Mart gobernado.
- **Entregables:**
  - Diagnóstico sistemático de calidad de datos (`observaciones_perfilado`).
  - Staging inmutable y normalización estatal canónica (`stg_clientes`, `stg_pedidos`).
  - Mesa de rechazos en cuarentena con trazabilidad técnica (`pedidos_rechazados`).
  - Carga incremental mediante UPSERT con demostración matemática de idempotencia (`fact_ordenes`).
  - Bitácora de balance de masa y conciliación financiera (`etl_auditoria`).
  - Reportes de indicadores comerciales (Ventas netas y pedidos entregados).
  - Análisis crítico fundamentado sobre decisiones de limpieza y reglas de negocio.

### 🔹 [Unidad 5: Del Data Mart al Dashboard Ejecutivo y al Comité Directivo](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/README.md)
- **Función General:** Construcción y validación de un modelo analítico dimensional en esquema estrella a partir de 4 archivos CSV, desarrollo de medidas DAX en Power Pivot, maquetación de un dashboard gerencial interactivo en Excel 365 y análisis sustentado para la toma de decisiones del Comité Directivo.
- **Entregables:**
  - Ingesta y perfilado de calidad en Power Query (`02_calidad_y_powerquery/scripts_m_powerquery.m`).
  - Modelo de datos en esquema estrella y diagnóstico de relaciones (`03_modelo_estrella_powerpivot/`).
  - Catálogo formal de medidas DAX (`04_medidas_dax/catalogo_medidas_dax.md`).
  - Conciliación cuantitativa contra cifras de control con 100.00% de coincidencia y discrepancia $0.00 (`05_validacion_numerica/`).
  - Tablero de control ejecutivo interactivo (`U5_Dashboard_Equipo08.xlsx`).
  - Presentación ejecutiva para el Comité Directivo de 7 diapositivas panorámicas (`U5_Comite_Equipo08.pptx`).
  - Reporte integral de evidencias académicas en PDF (`U5_Evidencias_Equipo08.pdf`).
  - Runner automatizado en Docker (`unidad_5/ejecutar_laboratorio_docker.sh`).
  - **Verificación en Tiempo Real para el Aula:** Tablero web reactivo interactivo en Docker ([`unidad_5/iniciar_dashboard_en_vivo.sh`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/iniciar_dashboard_en_vivo.sh) en `http://localhost:8085`), runner proyectable en terminal ([`unidad_5/verificacion_en_vivo_terminal.sh`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/verificacion_en_vivo_terminal.sh)) y [Guía de Verificación en Vivo para el Aula](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/unidad_5/GUIA_VERIFICACION_EN_VIVO_AULA.md).

### 🏆 [Producto Integrador de Aprendizaje (PIA): Solución BI Empresarial Completa (30%)](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/README.md)
- **Función General:** Solución de Business Intelligence de principio a fin para la empresa asignada **Casa&Estilo** (Muebles y Decoración). Abarca desde la ingesta y perfilado de 11 fuentes RAW (+530,000 registros), diseño de arquitectura y Data Mart en MySQL 8.0 en esquema estrella (331,758 líneas de detalle con 100% de conciliación contable y discrepancia $0.00), hasta el desarrollo de 10 métricas DAX en Power Pivot, maquetación de un Dashboard Ejecutivo interactivo y un Deck de 10 diapositivas con guion de defensa de 15 minutos ante el Comité Directivo.
- **Entregables Oficiales:**
  - **1. Arquitectura de Datos (25%):** Diagrama ER operacional, esquema estrella, diccionario de datos y justificación técnica de modelado ([`PIA/01_arquitectura_datos/`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/01_arquitectura_datos/)).
  - **2. Data Mart en MySQL / SQL (25%):** DDL completo de Staging y Data Mart, Stored Procedures modulares, orquestador ETL con bitácora `etl_log`, índices de optimización, vistas analíticas y balance de masa oficial ([`PIA/02_datamart_mysql/`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/02_datamart_mysql/)).
  - **3. Dashboard en Excel (25%):** Libro corporativo con modelo de datos, 10 métricas DAX, scorecard de KPIs, tendencias y segmentadores ([`PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/PIA_Dashboard_CasaEstilo_Equipo08.xlsx)).
  - **4. Presentación Ejecutiva (25%):** Deck formal de 10 diapositivas panorámicas (16:9) ([`PIA/PIA_Comite_CasaEstilo_Equipo08.pptx`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/PIA_Comite_CasaEstilo_Equipo08.pptx)) y guion de storytelling de 15 minutos ([`PIA/04_presentacion_ejecutiva/01_guion_storytelling_15min.md`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/04_presentacion_ejecutiva/01_guion_storytelling_15min.md)).
  - **Reporte Formal de Evidencias:** Documento PDF académico de certificación ([`PIA/PIA_Evidencias_CasaEstilo_Equipo08.pdf`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/PIA_Evidencias_CasaEstilo_Equipo08.pdf)).
  - **Empaque Oficial Unificado:** Archivo ZIP que contiene el 100% de los componentes ([`PIA/PIA_Equipo08_CasaEstilo.zip`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/PIA_Equipo08_CasaEstilo.zip)).
  - **Runner Maestro Automatizado en Docker:** Script ejecutable de inicio a fin ([`PIA/ejecutar_pia_docker.sh`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/PIA/ejecutar_pia_docker.sh)).


---

## 🚀 Entorno de Ejecución y Visualización con Docker

Para garantizar reproducibilidad sin instalar dependencias globales en el sistema anfitrión, el proyecto incluye una configuración de **Docker Compose** con PostgreSQL 16 y **dos interfaces visuales**:

```bash
# 1. Levantar la base de datos y las aplicaciones visuales
docker compose up -d
```
- 🛋️ **Casa&Estilo BI Studio (Interfaz Amigable y Modo Exposición):** [**http://localhost:8080**](http://localhost:8080)
  - *Diseñada especialmente para la defensa oral de 5 minutos, visor de tablas estilo hoja de cálculo, reporte interactivo del Top 5 de rentabilidad por región (Q2 vs Q1 2026) y playground SQL con EXPLAIN.*
- 🛠️ **pgAdmin 4 (Administración de BD):** [http://localhost:5050](http://localhost:5050)
  - **Email:** `equipo8@fime.uanl.mx` | **Password:** `password`
- 🐘 **Base de datos directa (PostgreSQL 16):** `localhost:5432` (`casa_estilo_bi`, usuario: `postgres`, password: `password`)

> 📖 **Guía completa para el equipo:** Consulta la [**Guía de Visualización para el Equipo**](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/GUIA_VISUALIZACION_EQUIPO.md).

### Alternativa: Contenedor individual con CLI
```bash
# Iniciar contenedor temporal de PostgreSQL 16
docker run --name pg-casa-estilo -e POSTGRES_PASSWORD=password -e POSTGRES_DB=casa_estilo_bi -p 5432:5432 -d postgres:16-alpine

# Ejecutar el script DDL de Unidad 2 dentro del contenedor
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script dll.sql"

# Cargar los datos simulados en la base de datos
docker exec -i pg-casa-estilo psql -U postgres -d casa_estilo_bi < "unidad_2/script_datos_simulados.sql"
```

---

## 🔄 Propuesta de Pipeline CI/CD

Se integró un flujo de integración continua en [`.github/workflows/ci.yml`](file:///home/butzmann/.gemini/antigravity-ide/scratch/equipo8-inteligencia_negocios-FIME_2026/.github/workflows/ci.yml) utilizando GitHub Actions y un servicio contenedorizado de PostgreSQL (`postgres:16-alpine`):

1. **Trigger:** Eventos `push` y `pull_request` sobre la rama `main`.
2. **Validación de DDL:** Compilación y ejecución automática del esquema relacional en una base de datos limpia para detectar errores de sintaxis o claves foráneas huérfanas.
3. **Validación de Consultas y Procedimientos:** Ejecución secuencial de scripts en `unidad_3/` (`02_ddl_y_datos`, `06_stored_procedure`, `04_consultas_sql`) para garantizar que cualquier cambio mantenga la integridad y ejecute con éxito.
4. **Validación de Pipeline ETL (Unidad 4):** Ejecución automatizada en MySQL 8.0 del pipeline ETL completo (`script_maestro_etl.sql` y scripts modulares) con balance de masa.
5. **Validación de Data Mart, DAX y Entregables (Unidad 5):** Ejecución automatizada en contenedor Docker de la suite de validación numérica de cifras de control y regeneración de artefactos (`.xlsx`, `.pptx`, `.pdf`).
