# VISION — Servidor MCP de Memoria Sintética y Contexto Empresarial

![Docker Build](https://github.com/carlosgomezc7/vision/actions/workflows/docker-build.yml/badge.svg)
![Backup Sync](https://github.com/carlosgomezc7/vision/actions/workflows/backup_sync.yml/badge.svg)

**VISION** es el motor central de **CTI Soluciones**, diseñado como un servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) construido con [FastMCP](https://github.com/jlowin/fastmcp). Retiene el conocimiento estratégico sobre el desarrollo de **Intranets Empresariales B2B con Búsqueda Profunda (Deep Search)** y actúa como copiloto de diseño UI/UX, accesibilidad WCAG y gobernanza para el equipo de desarrollo.

---

## 📁 Estructura del Proyecto

```
vision/
├── .agents/                        # Configuración de Antigravity / agentes MCP
│   ├── AGENTS.md                   # Reglas globales del copiloto
│   ├── mcp.json                    # Registro del servidor MCP (stdio)
│   └── skills/                     # Skills especializados
│       ├── desarrollador_web/      # Arquitectura, backend, CI/CD, Zero Trust
│       ├── diseno_ux_consultor/    # Diseño UX/UI, WCAG 2.2, tokens W3C DTCG
│       ├── iniciar_proyecto/       # Protocolo de inicio de proyecto (Intranet vs Landing)
│       └── web_discovery/          # Entrevista estructurada de descubrimiento
├── .github/workflows/
│   ├── docker-build.yml            # CI/CD: build + push a GHCR
│   └── backup_sync.yml             # Backup automático de SQLite a JSON (artifact)
├── src/
│   ├── main.py                     # Punto de entrada del servidor FastMCP
│   ├── config.py                   # Rutas y constantes globales (dinámicas)
│   ├── auto_commit.py              # Auto-commit periódico a GitHub
│   ├── memory/
│   │   ├── vector_store.py         # Almacén de memoria SQLite (búsqueda por keywords)
│   │   └── seeder.py               # Sembrado automático de conocimiento base
│   ├── seed_data/                  # 13 documentos de conocimiento semilla (.md)
│   ├── tools/
│   │   ├── prd_intranet.py         # Generador de PRD corporativo
│   │   ├── architecture_tool.py    # Consulta de blueprints técnicos
│   │   ├── retrospect_tool.py      # Registro de lecciones aprendidas
│   │   ├── ux_design_tool.py       # WCAG 2.2, tokens W3C DTCG, Core Web Vitals
│   │   ├── issue_tracker.py        # Registro de incidencias (SQLite + ISSUES.md)
│   │   └── system_info.py          # Detección de entorno del sistema
│   └── future/                     # Roadmap de mejoras planificadas
│       └── README.md               # Documentación de búsqueda semántica con embeddings
├── templates/
│   └── client_discovery_template.json  # Template JSON para toma de requerimientos
├── Dockerfile                      # Multi-stage build (Python 3.12-slim)
├── requirements.txt                # fastmcp, python-dotenv
├── visionstart.sh                  # Script de inicio rápido (Linux)
├── vision_memory.db                # Base de datos SQLite (memoria + issues)
└── ISSUES.md                       # Registro bilingüe (ES/EN) de incidencias
```

---

## 🛠 Herramientas MCP Expuestas

El servidor registra las siguientes **9 herramientas**, **1 recurso** y **1 prompt** en el protocolo MCP:

### Herramientas (`@mcp.tool`)

| Herramienta | Descripción |
|---|---|
| `query_vision_memory` | Busca en la memoria sintética y base de conocimiento. |
| `create_intranet_prd` | Genera el PRD corporativo para una Intranet B2B. |
| `consult_architecture` | Consulta blueprints técnicos y de Deep Search. |
| `log_retrospective` | Registra aprendizajes o retrospectivas de proyecto. |
| `check_wcag_accessibility` | Valida contraste WCAG 2.2 AA (4.5:1 / 3.0:1). |
| `generate_design_tokens_w3c` | Genera tokens de diseño bajo especificación W3C DTCG. |
| `check_performance_budget` | Audita Core Web Vitals (INP, LCP, CLS). |
| `log_incident_issue` | Registra incidencias en SQLite + ISSUES.md. |
| `detect_system_environment` | Detecta OS, kernel y estado de Python. |

### Recurso y Prompt

| Tipo | Nombre | Descripción |
|---|---|---|
| `@mcp.resource` | `config://system_context` | Expone las directrices del sistema VISION. |
| `@mcp.prompt` | `vision_system_prompt` | Prompt oficial con contexto estratégico. |

---

## 🚀 Inicio Rápido

### 🐳 Docker (Recomendado)

Construir la imagen localmente:

```bash
docker build -t vision-mcp .
```

O jalar la última imagen desde GitHub Container Registry:

```bash
docker pull ghcr.io/carlosgomezc7/vision:latest
```

Ejecutar con volumen persistente para SQLite:

```bash
docker run -d --name vision -v vision-data:/app/data vision-mcp
```

Ver logs en tiempo real:

```bash
docker logs -f vision
```

Detener y eliminar:

```bash
docker stop vision && docker rm vision
```

### 🐍 Desarrollo Local (Linux / Arch / Omarch)

**Prerrequisitos:** Python 3.12+, `git`

El script `visionstart.sh` detecta el sistema, crea el `.venv` si no existe, instala dependencias y arranca el servidor:

```bash
./visionstart.sh
```

O manualmente:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

### 🔌 Configuración MCP (Antigravity / IDE)

El archivo `.agents/mcp.json` ya registra VISION como servidor MCP vía `stdio`. No requiere configuración adicional si usas Antigravity desde el workspace.

---

## ⚙️ CI/CD (GitHub Actions)

| Workflow | Trigger | Descripción |
|---|---|---|
| [`docker-build.yml`](.github/workflows/docker-build.yml) | Push a `main` | Compila la imagen Docker con Buildx (cache), publica en GHCR con tags `latest` + SHA. |
| [`backup_sync.yml`](.github/workflows/backup_sync.yml) | Push a `main` / Manual | Exporta `vision_memory.db` a JSON y lo sube como artifact (retención: 30 días). |

> Cada `git push` a `main` actualiza la imagen y genera un backup automáticamente.

---

## 🧩 Skills de Antigravity

VISION incluye 4 skills especializados que se activan automáticamente según el contexto de la conversación:

| Skill | Activación |
|---|---|
| **Desarrollador Web** | Arquitectura, backend/APIs, ADR, seguridad Zero Trust, CI/CD. |
| **Consultor de Diseño UX** | Diseño UI/UX, paleta de colores, WCAG 2.2, tokens W3C DTCG, Core Web Vitals. |
| **Iniciar Proyecto** | "nuevo proyecto", "crear proyecto" → bifurca entre *Intranet B2B* y *Landing Page*. |
| **Web Discovery** | Entrevista estructurada de descubrimiento, brief del cliente, genera JSON validado. |

---

## 📌 Registro de Incidencias

El proyecto mantiene un registro bilingüe (ES/EN) de incidencias en [`ISSUES.md`](ISSUES.md), sincronizado con SQLite (`vision_memory.db`).

Consultar desde la terminal:

```bash
python3 -c "from src.tools.issue_tracker import list_recorded_issues; print(list_recorded_issues())"
```

---

## 🔄 Auto-Commit (Opcional)

Sincroniza cambios a GitHub automáticamente cada 30 minutos:

```bash
python src/auto_commit.py
```

---

## 🔮 Roadmap

Consulta [`src/future/README.md`](src/future/README.md) para las mejoras planificadas, incluyendo:

- **Búsqueda semántica con embeddings** (ChromaDB + sentence-transformers) — se activará cuando la memoria supere 30+ documentos o se integren 2+ clientes reales.

---

## 📄 Licencia

Proyecto propietario de **CTI Soluciones** — Carlos Gómez.
