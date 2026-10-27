# Implementation Plan: Motor de Escucha al Cliente y Creación de Landing Pages Personalizadas

## Overview

Transformar **VISION MCP** en un copiloto 100% especializado en **escuchar al cliente y diseñar/desarrollar Landing Pages personalizadas, estéticas y fieles a sus deseos**, eliminando todo rastro de Intranet B2B / Supabase / Auth, e implementando el **Motor de Diagnóstico de Preparación del Cliente (`audit_client_readiness` + `get_client_intake_guide`)** junto con la plantilla y guía de reunión en español.

## Dependency Graph

```text
1. Plantilla y Guía Cliente↔Repo (templates/client_discovery_template.json + guia_reunion_cliente.md)
       │
       ├── 2. Motor de Escucha y Auditoría de Preparación (src/tools/discovery_ingest.py + project_specs.py)
       │         │
       │         └── 3. Servidor FastMCP y Limpieza de Herramientas Legacy (src/main.py)
       │                   │
       │                   └── 4. Base de Conocimiento Semilla y SQLite FTS5 (src/seed_data/* + vision_memory.db)
       │                             │
       │                             └── 5. Reglas de Agente, Skills y Documentación (.agents/* + README.md)
```

## Architecture Decisions

- **Eliminación de herramientas de Intranet:** Se retiran `create_intranet_prd` (`src/tools/prd_intranet.py`) y `generate_supabase_rls_schema` (de `src/tools/project_specs.py` y `src/main.py`), dejando una arquitectura limpia dedicada a Landing Pages estáticas y modulares.
- **Nuevas herramientas MCP centradas en el cliente:**
  - `get_client_intake_guide(focus_area: str = "all")`: Devuelve la matriz estructurada en español de qué preguntarle al cliente durante la reunión y cómo cada respuesta alimenta a VISION.
  - `audit_client_readiness(payload: dict)`: Analiza el JSON de descubrimiento del cliente, calcula el `readiness_score` (0–100%), detecta campos faltantes (`missing_for_repo`), genera las preguntas exactas en español (`next_questions_for_client`) y prepara el pipeline de herramientas MCP listas para ejecutarse.
- **Purga y re-sembrado de `vision_memory.db`:** Se limpian los documentos antiguos de intranet en la tabla `memory` / `memory_fts` y se reemplazan los archivos de `src/seed_data/` por blueprints de Landing Pages personalizadas, psicología de color/tipografía, estructura de secciones de alta conversión y protocolo de escucha al cliente.

## Task List

Las tareas detalladas y sus criterios de aceptación están registrados en [`tasks/todo.md`](file:///home/carlosgomezc7/Projects/vision/tasks/todo.md):

### Fase 1: Plantilla del Cliente, Guía de Escucha y Motor de Preparación
- [ ] **Task 1:** Actualizar plantilla de descubrimiento en español y crear guía Cliente ↔ Repo (`templates/`).
- [ ] **Task 2:** Implementar `audit_client_readiness` y `get_client_intake_guide` en `src/tools/discovery_ingest.py` + tests.

### Checkpoint 1: Diagnóstico de Cliente Verificado
- [ ] `pytest tests/test_discovery_ingest.py -v` pasa al 100%.

### Fase 2: Limpieza de Herramientas MCP y Especificación de Landing Page
- [ ] **Task 3:** Purgar lógica de Intranet/Supabase en `src/tools/` y `src/main.py`, registrando las nuevas herramientas de cliente + actualizar tests.
- [ ] **Task 4:** Reemplazar `src/seed_data/` por conocimiento de Landing Pages personalizadas y re-indexar `vision_memory.db`.

### Checkpoint 2: Servidor MCP y Memoria Sintética Limpios
- [ ] `pytest tests/ -v` pasa al 100% y `vision_memory.db` contiene únicamente memoria de Landing Pages.

### Fase 3: Sincronización de Reglas, Skills y Documentación
- [ ] **Task 5:** Actualizar `.agents/AGENTS.md`, `.agents/skills/` (`iniciar_proyecto`, `web_discovery`, `desarrollador_web`, `diseno_ux_consultor`) y `README.md` eliminando todo rastro de intranet.

### Checkpoint Final: Entrega Completa
- [ ] Todos los tests en `pytest` pasan, `check_project_health` reporta `OPTIMAL` y `grep -i intranet` confirma cero rastros en los módulos activos.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
|Registros antiguos de Intranet persistidos dentro de `vision_memory.db` | Med | Limpiar los registros `seed_*` y `prd_*` antiguos de SQLite y re-ejecutar `seed_vision_mind()` en la Tarea 4. |
|Tests existentes que importaban `generate_intranet_prd` o `generate_supabase_rls_policies` | Med | Actualizar `tests/test_project_specs.py` y `tests/test_knowledge_and_devops.py` en la Tarea 3 para cubrir las nuevas funciones de Landing Page y Readiness. |

## Open Questions

- Ninguna. Listo para revisión y aprobación del plan.
