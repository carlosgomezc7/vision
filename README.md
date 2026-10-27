# VISION — Servidor MCP para Creación de Landing Pages Personalizadas
*CTI Soluciones — Carlos Gómez*

![Docker Build](https://github.com/carlosgomezc7/vision/actions/workflows/docker-build.yml/badge.svg)
![Backup Sync](https://github.com/carlosgomezc7/vision/actions/workflows/backup_sync.yml/badge.svg)

**VISION** es el motor central de **CTI Soluciones**, diseñado como un servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) construido con [FastMCP](https://github.com/jlowin/fastmcp). Su propósito exclusivo es **darle prioridad al cliente: escucharlo, auditar qué insumos necesita el repositorio y generar Landing Pages bonitas, personalizadas, accesibles (WCAG 2.2 AA) y de alta conversión**, eliminando cualquier complejidad o sobrecarga técnica innecesaria.

---

## 📁 Estructura del Proyecto

```
vision/
├── SPEC.md                                 # Especificación viva del sistema
├── tasks/
│   ├── plan.md                             # Plan técnico de implementación
│   └── todo.md                             # Desglose de tareas con checkpoints
├── .agents/                                # Configuración de Antigravity / agentes MCP
│   ├── AGENTS.md                           # Reglas globales del copiloto
│   ├── mcp.json                            # Registro multi-servidor (VISION + Context7)
│   ├── mcp_config.json                     # Configuración de descubrimiento MCP
│   └── skills/                             # Skills especializados
│       ├── desarrollador_web/              # Arquitectura frontend modular (Next.js estático)
│       ├── diseno_ux_consultor/            # Diseño UI/UX, WCAG 2.2 AA, tokens W3C DTCG
│       ├── iniciar_proyecto/               # Flujo guiado para iniciar Landing Pages
│       └── web_discovery/                  # Entrevista de descubrimiento y escucha al cliente
├── templates/
│   ├── client_discovery_template.json      # Plantilla estructurada en español para toma de requerimientos
│   └── guia_reunion_cliente.md             # Matriz: qué escuchar del cliente vs. qué consume el repo
├── src/
│   ├── main.py                             # Punto de entrada del servidor FastMCP
│   ├── config.py                           # Rutas y constantes globales
│   ├── auto_commit.py                      # Auto-commit periódico a GitHub
│   ├── memory/
│   │   ├── vector_store.py                 # Almacén SQLite FTS5 BM25 en modo WAL
│   │   └── seeder.py                       # Sembrado automático de conocimiento base
│   ├── seed_data/                          # 12 documentos semilla de Landing Pages (.md)
│   ├── tools/
│   │   ├── discovery_ingest.py             # Ingesta, readiness score y guía de escucha al cliente
│   │   ├── project_specs.py                # Especificación modular de Landing Pages
│   │   ├── ux_design_tool.py               # Contraste WCAG 2.2 AA y tokens W3C DTCG
│   │   ├── tokens_exporter.py              # Exportador a CSS Variables / Tailwind y auditoría
│   │   ├── architecture_tool.py            # Blueprints de arquitectura frontend
│   │   ├── retrospect_tool.py              # Registro de aprendizajes
│   │   ├── knowledge_tool.py               # Ingesta de manuales de marca de clientes
│   │   ├── issue_tracker.py                # Registro de incidencias (SQLite + ISSUES.md)
│   │   ├── devops_tool.py                  # Diagnóstico de salud y checkpoints Git
│   │   └── system_info.py                  # Detección de entorno del sistema
│   └── future/                             # Roadmap de mejoras planificadas (Embeddings)
├── Dockerfile                              # Multi-stage build (Python 3.12-slim)
├── requirements.txt                        # fastmcp, python-dotenv, pytest
├── visionstart.sh                          # Script de inicio rápido (Linux / Arch)
├── vision_memory.db                        # Base de datos SQLite (memoria FTS5 + issues)
└── ISSUES.md                               # Registro bilingüe (ES/EN) de incidencias
```

---

## 🛠 Herramientas MCP Expuestas

El servidor registra **17 herramientas**, **1 recurso** y **1 prompt** en FastMCP, integrando además **Context7 MCP** para documentación oficial en tiempo real:

### Herramientas (`@mcp.tool`)

| Herramienta | Categoría | Descripción |
|---|---|---|
| `get_client_listening_guide` | Escucha al Cliente | Devuelve la guía en español de qué preguntarle al cliente y para qué lo usa el repo. |
| `audit_client_readiness_score` | Diagnóstico | Evalúa el brief del cliente (0–100%), detecta datos faltantes y genera preguntas de seguimiento. |
| `ingest_client_discovery` | Descubrimiento | Ingesta y valida el brief de la Landing Page en la memoria SQLite FTS5. |
| `create_landing_page_specification` | Especificación | Genera la arquitectura modular en Next.js (`src/components/landing/*`) sin BD ni auth. |
| `check_wcag_accessibility` | Accesibilidad | Valida contraste estricto WCAG 2.2 AA (4.5:1 normal / 3.0:1 grande) sin redondeo. |
| `generate_design_tokens_w3c` | Diseño UX/UI | Genera tokens de diseño bajo especificación W3C DTCG (`$value`, `$type`, `$description`). |
| `export_tokens_to_stylesheet` | Diseño UX/UI | Exporta tokens W3C DTCG a CSS Custom Properties (`:root`) o variables Tailwind CSS. |
| `audit_theme_palette` | Diseño UX/UI | Audita una paleta corporativa completa en cruces de pares contra WCAG 2.2 AA. |
| `check_performance_budget` | Rendimiento | Audita presupuesto de rendimiento para Core Web Vitals (INP < 200ms, LCP < 2.5s, CLS <= 0.1). |
| `query_vision_memory` | Memoria & RAG | Busca en la memoria sintética usando SQLite FTS5 con ranking BM25. |
| `ingest_custom_document` | Memoria & RAG | Ingesta dinámicamente manuales de marca o referencias del cliente en FTS5. |
| `consult_architecture` | Arquitectura | Consulta blueprints técnicos de componentes modulares y diseño web en memoria. |
| `log_retrospective` | Memoria & RAG | Registra aprendizajes y decisiones de diseño en memoria a largo plazo. |
| `log_incident_issue` | DevOps & Issues | Registra incidencias bilingües (ES/EN) en SQLite + `ISSUES.md`. |
| `update_recorded_issue` | DevOps & Issues | Actualiza el estado y solución de una incidencia registrada en SQLite. |
| `get_issues_log` | DevOps & Issues | Consulta incidencias registradas con filtros por categoría/estado y paginación. |
| `detect_system_environment` | DevOps & Issues | Detecta entorno OS (Omarch / Arch Linux), kernel y estado de Python. |
| `check_project_health` | DevOps & Issues | Diagnóstico integral de SQLite, FTS5, base de conocimiento, issues y Git. |
| `make_git_checkpoint` | DevOps & Issues | Crea un commit checkpoint convencional bajo demanda del estado del proyecto. |

### Servidores MCP Configurados (`.agents/mcp.json` y `.agents/mcp_config.json`)

| Servidor | Transporte | Propósito |
|---|---|---|
| `vision` | `stdio` (`python -m src.main`) | Motor local de memoria, escucha al cliente, UX/WCAG y especificaciones de Landing Pages. |
| `context7` | `http` (`https://mcp.context7.com/mcp`) | Documentación oficial en tiempo real (`resolve-library-id`, `query-docs`) para Next.js, Tailwind y shadcn/ui. |

---

## 🚀 Inicio Rápido

### 🐍 Desarrollo Local (Linux / Arch / Omarch)

El script `visionstart.sh` detecta el sistema, activa el `.venv`, comprueba dependencias y arranca el servidor:

```bash
./visionstart.sh
```

O manualmente:

```bash
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
python -m src.main
```

### 🐳 Docker

```bash
docker build -t vision-mcp .
docker run -d --name vision -v vision-data:/app/data vision-mcp
```

---

## 🧩 Skills de Antigravity

VISION incluye 4 skills especializados que se activan automáticamente según el contexto:

| Skill | Activación |
|---|---|
| **Iniciar Proyecto** | "nuevo proyecto", "crear landing page" → Escucha al cliente, audita preparación y genera Next.js modular. |
| **Consultor de Diseño UX** | Diseño UI/UX, paleta de colores, WCAG 2.2 AA, tokens W3C DTCG, Core Web Vitals. |
| **Web Discovery** | Entrevista de descubrimiento con el cliente, genera JSON validado y ejecuta `audit_client_readiness_score`. |
| **Desarrollador Web** | Arquitectura modular frontend, componentes `shadcn/ui`, HTML5 semántico y exportación estática. |

---

## 📄 Licencia

Proyecto propietario de **CTI Soluciones** — Carlos Gómez.
