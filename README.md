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
