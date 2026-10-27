# Spec: VISION — Motor de Escucha al Cliente y Creación de Landing Pages Personalizadas

## Objective

Enfocar **VISION MCP** al **100% en la creación de Landing Pages y Páginas Web bonitas, personalizadas y fieles a lo que desea el cliente**, eliminando cualquier rastro de "Intranet B2B / Supabase / Auth / RBAC" del repositorio y priorizando la **fase de escucha activa al cliente**:

1. **Prioridad al Cliente (Saber qué escuchar y qué pedirle):**
   - Proveer una guía conversacional clara en español ([`templates/guia_reunion_cliente.md`](file:///home/carlosgomezc7/Projects/vision/templates/guia_reunion_cliente.md) y herramienta MCP `get_client_intake_guide`) que permita a Carlos enfocarse en escuchar la historia, estética, secciones, objetivos de conversión (CTA) y referencias visuales del cliente.
   - Traducir la plantilla [`templates/client_discovery_template.json`](file:///home/carlosgomezc7/Projects/vision/templates/client_discovery_template.json) con pistas (`_hint`) en español y campos orientados al diseño y contenido de Landing Pages personalizadas.
2. **Saber qué necesita el Repositorio (`audit_client_readiness`):**
   - Evaluar el JSON o las notas del cliente y calcular un **Índice de Preparación (`readiness_score`: 0–100%)** para construir la Landing Page sin inventar ni adivinar lo que el cliente quiere.
   - Identificar exactamente qué datos faltan (`missing_for_repo`) para alimentar las herramientas de diseño y especificación (`create_landing_page_specification`, `generate_design_tokens_w3c`, `audit_theme_palette`, `export_tokens_to_stylesheet`, `check_performance_budget`).
   - Entregar las **preguntas exactas de seguimiento en español (`next_questions_for_client`)** listas para enviar al cliente si algún punto clave quedó pendiente.
3. **Limpieza Total de Rastros de Intranet:**
   - Eliminar herramientas, seeds, reglas y textos de Intranet B2B (`create_intranet_prd`, `generate_supabase_rls_schema`, seeds de login/SSO/Supabase/multitenant) y reemplazar la base de conocimiento semilla (`src/seed_data/`) y skills (`.agents/skills/` y `.agents/AGENTS.md`) por conocimiento especializado en **Landing Pages de alto impacto visual, arquitectura modular por secciones, diseño personalizado, conversión (CTA) y accesibilidad WCAG 2.2 AA**.

## Tech Stack

- **Lenguaje Servidor MCP:** Python 3.12+ (`fastmcp==3.4.5`, SQLite WAL + FTS5 BM25, `pytest==8.3.3`)
- **Stack Objetivo para las Landing Pages Generadas:** Next.js (App Router, 100% estático/modular sin bases de datos ni auth), Tailwind CSS, `shadcn/ui`, Lucide Icons, tipografías personalizadas y tokens W3C DTCG.
- **Documentación Oficial en Vivo:** Context7 MCP (`https://mcp.context7.com/mcp`)

## Commands

```bash
# Ejecutar toda la suite de pruebas unitarias
/home/carlosgomezc7/Projects/vision/.venv/bin/pytest tests/ -v

# Verificar que no queden rastros de intranet en código, seeds ni reglas principales
grep -rn -i "intranet" src/ templates/ tests/ .agents/AGENTS.md .agents/skills/iniciar_proyecto/ .agents/skills/desarrollador_web/ .agents/skills/diseno_ux_consultor/ .agents/skills/web_discovery/ README.md

# Verificar salud del servidor MCP y base de datos SQLite/FTS5
/home/carlosgomezc7/Projects/vision/.venv/bin/python -c "from src.tools.devops_tool import get_project_health_status; print(get_project_health_status())"
```

## Project Structure

```text
vision/
├── SPEC.md                                     → Especificación viva del sistema
├── tasks/
│   ├── plan.md                                 → Plan de implementación técnico
│   └── todo.md                                 → Lista de tareas verificables con checkpoints
├── templates/
│   ├── client_discovery_template.json          → Plantilla JSON en español para toma de requerimientos de Landing Page
│   └── guia_reunion_cliente.md                 → Guía práctica: qué escuchar del cliente vs. qué necesita el repo
├── src/
│   ├── main.py                                 → Servidor FastMCP 100% enfocado en Landing Pages personalizadas
│   ├── memory/
│   │   ├── vector_store.py                     → Almacén SQLite FTS5 BM25
│   │   └── seeder.py                           → Indexador de conocimiento semilla
│   ├── seed_data/                              → Conocimiento semilla 100% enfocado en Landing Pages, estética y escucha al cliente
│   └── tools/
│       ├── discovery_ingest.py                 → Ingesta, auditoría de preparación (readiness_score) y guía del cliente
│       ├── project_specs.py                    → Generador de especificación modular de Landing Page
│       ├── ux_design_tool.py                   → Contraste WCAG 2.2 AA, tokens W3C DTCG y Core Web Vitals
│       ├── tokens_exporter.py                  → Exportador de tokens a CSS Variables / Tailwind y auditor de paleta
│       ├── architecture_tool.py                → Consulta de blueprints de Landing Pages y diseño
│       ├── knowledge_tool.py                   → Ingesta de referencias y manuales de marca del cliente
│       ├── retrospect_tool.py                  → Lecciones aprendidas de proyectos
│       ├── issue_tracker.py                    → Seguimiento de incidencias
│       ├── devops_tool.py                      → Diagnóstico de salud y checkpoints Git
│       └── system_info.py                      → Información del entorno
└── tests/                                      → Suite de pruebas unitarias con pytest
```

## Code Style

```python
def audit_client_readiness(payload: dict) -> str:
    """
    Evalúa qué tan completa está la información del cliente para construir
    su Landing Page personalizada sin suposiciones.
    Devuelve JSON con readiness_score (0-100), missing_for_repo,
    next_questions_for_client (en español) y ready_tools.
    """
```

## Testing Strategy

- **Framework:** `pytest` en `tests/`.
- **Pruebas clave:**
  - `test_discovery_ingest.py`: Prueba `ingest_discovery_data`, `audit_client_readiness` (con payload incompleto vs. payload completo al 100%) y `get_client_intake_guide`.
  - `test_project_specs.py`: Prueba `create_landing_page_spec` verificando estructura modular de secciones, estilo visual, CTA y cero dependencias de autenticación/BD.
  - `test_knowledge_and_devops.py`: Verifica el sembrado de los nuevos documentos semilla de Landing Pages y limpieza de la base de datos SQLite.

## Boundaries

- **Always do:**
  - Priorizar los gustos, colores, referencias, secciones y objetivos del cliente.
  - Detectar y reportar explícitamente cualquier campo marcado como `"not_determined"` o vacío antes de generar código, entregando las preguntas en español para el cliente.
  - Mantener arquitectura modular en las Landing Pages (`src/components/landing/Header.tsx`, `Hero.tsx`, `Services.tsx`, etc.).
  - Ejecutar `pytest` tras cada tarea.
- **Ask first:**
  - Añadir paquetes nuevos en `requirements.txt`.
  - Modificar workflows de `.github/workflows/`.
- **Never do:**
  - Incluir referencias, herramientas o código de Intranet, Login, Supabase, RBAC o bases de datos.
  - Inventar colores, textos o secciones que el cliente no haya definido sin antes señalarlo en el diagnóstico de preparación.

## Success Criteria

1. **Cero rastros de Intranet:** `src/`, `templates/`, `tests/`, `README.md`, `.agents/AGENTS.md` y los 4 skills principales de `.agents/skills/` están 100% libres de lógica o menciones a Intranets B2B / Supabase / RBAC, y la tabla `memory` de `vision_memory.db` se re-indexa únicamente con conocimiento de Landing Pages personalizadas.
2. **Matriz Cliente ↔ Repo Activa:** `get_client_intake_guide` y `templates/guia_reunion_cliente.md` detallan qué preguntarle al cliente en español y qué herramienta del repo consume cada dato.
3. **Diagnóstico de Preparación (`audit_client_readiness`):** Evalúa cualquier `client_discovery_template.json` devolviendo `readiness_score` (0–100%), `missing_for_repo`, `next_questions_for_client` y los parámetros listos para crear la Landing Page.
4. **Tests en Verde:** `pytest tests/ -v` pasa al 100% sin errores.

## Open Questions

- Ninguna. El alcance quedó 100% definido por el usuario.
