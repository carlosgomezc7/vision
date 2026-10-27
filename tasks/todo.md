# Task Breakdown: Motor de Escucha al Cliente y Landing Pages Personalizadas

## Task 1: Plantilla de Descubrimiento en Español y Guía "Qué Pedirle al Cliente vs. Qué Necesita el Repo"

**Description:** Actualizar `templates/client_discovery_template.json` con pistas (`_hint`) en español enfocadas 100% en Landing Pages personalizadas (eliminando opciones de intranet/auth/BD) y crear `templates/guia_reunion_cliente.md` con el mapa exacto entre lo que se escucha del cliente en la reunión y lo que consume el repositorio.

**Acceptance criteria:**
- [x] `templates/client_discovery_template.json` tiene todos los `_hint` y `_quick_guide` en español claro, incluye secciones de estética/referencias visuales/secciones/CTA y no menciona intranet ni autenticación.
- [x] `templates/guia_reunion_cliente.md` documenta los 5 bloques de conversación con el cliente (Esencia y Objetivo, Identidad Visual, Estructura de Secciones y Copy, Contacto/Conversión, Dominio/Entrega) indicando qué herramienta del repo consume cada dato.

**Verification:**
- [x] JSON válido: `/home/carlosgomezc7/Projects/vision/.venv/bin/python -c "import json; json.load(open('templates/client_discovery_template.json'))"`
- [x] Sin menciones a intranet: `! grep -i "intranet" templates/client_discovery_template.json templates/guia_reunion_cliente.md`

**Dependencies:** None

**Files touched:**
- `templates/client_discovery_template.json`
- `templates/guia_reunion_cliente.md`

---

## Task 2: Motor de Escucha y Diagnóstico de Preparación (`audit_client_readiness` y `get_client_intake_guide`)

**Description:** Mejorar `src/tools/discovery_ingest.py` para procesar todos los bloques de una Landing Page (negocio, identidad visual, contenido/secciones, conversiones/integraciones y dominio/hosting), agregar `audit_client_readiness(payload)` que calcula el `readiness_score` (0–100%), detecta campos faltantes (`missing_for_repo`) y genera preguntas en español (`next_questions_for_client`), y agregar `get_client_intake_guide(focus_area)`.

**Acceptance criteria:**
- [x] `audit_client_readiness` evalúa los campos esenciales de una Landing Page personalizada y devuelve `readiness_score`, `status` (`READY_TO_BUILD` o `NEEDS_CLIENT_INPUT`), `confirmed_fields`, `missing_for_repo`, `next_questions_for_client` y `recommended_mcp_pipeline`.
- [x] `get_client_intake_guide` devuelve en español qué preguntarle al cliente y para qué lo usa el repositorio.
- [x] `tests/test_discovery_ingest.py` valida payloads completos (100%), incompletos (<100%) y la guía de preguntas.

**Verification:**
- [x] Tests pasan: `/home/carlosgomezc7/Projects/vision/.venv/bin/pytest tests/test_discovery_ingest.py -v`

**Dependencies:** Task 1

**Files touched:**
- `src/tools/discovery_ingest.py`
- `tests/test_discovery_ingest.py`

---

## Checkpoint 1: Diagnóstico de Cliente Verificado
- [x] `templates/client_discovery_template.json` es JSON válido y 100% en español.
- [x] `pytest tests/test_discovery_ingest.py -v` pasa sin errores (4/4 passed).

---

## Task 3: Purgar Herramientas de Intranet/Supabase y Enriquecer Especificación de Landing Page

**Description:** Eliminar `src/tools/prd_intranet.py` y `generate_supabase_rls_policies` de `src/tools/project_specs.py`. Enriquecer `create_landing_page_spec` en `src/tools/project_specs.py` para que reciba también paleta de colores, tipografías, referencias visuales y estructura de contenido del cliente. Actualizar `src/main.py` exponiendo `audit_client_readiness` y `get_client_intake_guide`, y actualizar los tests en `tests/test_project_specs.py` y `tests/test_knowledge_and_devops.py`.

**Acceptance criteria:**
- [x] `src/tools/prd_intranet.py` es eliminado y `generate_supabase_rls_policies` ya no existe en `src/tools/project_specs.py`.
- [x] `src/main.py` registra `audit_client_readiness` y `get_client_intake_guide` y su `SYSTEM_INSTRUCTIONS` está 100% enfocado en Landing Pages personalizadas.
- [x] `create_landing_page_spec` genera especificaciones ricas y personalizadas (secciones, estilo, paleta, tipografía, CTA, componentes modulares en `src/components/landing/`).

**Verification:**
- [x] Tests pasan: `/home/carlosgomezc7/Projects/vision/.venv/bin/pytest tests/test_project_specs.py tests/test_knowledge_and_devops.py -v`
- [x] Servidor importa sin errores: `/home/carlosgomezc7/Projects/vision/.venv/bin/python -c "import src.main"`

**Dependencies:** Task 2

**Files touched:**
- `src/main.py`
- `src/tools/project_specs.py`
- `src/tools/prd_intranet.py` (eliminado)
- `tests/test_project_specs.py`
- `tests/test_knowledge_and_devops.py`

---

## Task 4: Actualizar Base de Conocimiento Semilla (`src/seed_data/`) y Limpiar `vision_memory.db`

**Description:** Reemplazar los archivos de `src/seed_data/` que hablaban de Intranet/SSO/Supabase/Multitenant por guías semilla enfocadas en creación de Landing Pages personalizadas, escucha activa al cliente, arquitectura modular en Next.js + Tailwind + shadcn/ui, tokens W3C DTCG, accesibilidad WCAG 2.2 AA y despliegue web. Purgar registros antiguos de intranet en `vision_memory.db` y re-sembrar la memoria FTS5.

**Acceptance criteria:**
- [x] Ningún archivo en `src/seed_data/` ni `tests/test_vector_store.py` menciona Intranet, Supabase RLS o SSO.
- [x] `vision_memory.db` es re-indexada con los documentos semilla de Landing Pages y `query_vision_memory("landing page")` devuelve los nuevos blueprints.

**Verification:**
- [x] Tests pasan: `/home/carlosgomezc7/Projects/vision/.venv/bin/pytest tests/ -v`
- [x] Verificación de BD sin intranet: 0 registros encontrados.

**Dependencies:** Task 3

**Files touched:**
- `src/seed_data/` (12 archivos `.md`)
- `tests/test_vector_store.py`
- `vision_memory.db`

---

## Checkpoint 2: Servidor MCP y Memoria Sintética 100% Landing Pages
- [x] `pytest tests/ -v` pasa al 100% (40/40 passed).
- [x] `vision_memory.db` tiene 0 registros con la palabra "intranet".

---

## Task 5: Sincronizar Reglas (`.agents/AGENTS.md`), Skills Principales y `README.md`

**Description:** Actualizar `.agents/AGENTS.md`, `.agents/skills/iniciar_proyecto/SKILL.md`, `.agents/skills/web_discovery/SKILL.md`, `.agents/skills/desarrollador_web/SKILL.md`, `.agents/skills/diseno_ux_consultor/SKILL.md` y `README.md` para eliminar cualquier rastro de Intranet B2B y dejar el flujo de trabajo centrado en escuchar al cliente, validar preparación (`audit_client_readiness`) y construir Landing Pages personalizadas.

**Acceptance criteria:**
- [x] `.agents/AGENTS.md` y los 4 skills del proyecto definen a VISION como especialista en Landing Pages personalizadas y escucha activa al cliente.
- [x] `README.md` documenta el flujo centrado en el cliente, las nuevas herramientas MCP (`get_client_listening_guide`, `audit_client_readiness_score`, `create_landing_page_specification`) y la integración con Context7.

**Verification:**
- [x] Cero menciones a intranet en archivos clave verificado.
- [x] Diagnóstico de salud reporta `OPTIMAL`.

**Dependencies:** Task 4

**Files touched:**
- `.agents/AGENTS.md`
- `.agents/skills/iniciar_proyecto/SKILL.md`
- `.agents/skills/web_discovery/SKILL.md`
- `.agents/skills/desarrollador_web/SKILL.md`
- `.agents/skills/diseno_ux_consultor/SKILL.md`
- `README.md`
- `src/future/README.md`

---

## Checkpoint Final: Entrega Completa
- [x] Todos los criterios de aceptación de `SPEC.md` se cumplen.
- [x] `pytest tests/ -v` pasa al 100% (40 de 40 tests en verde).
- [x] Cero rastros de intranet en código, base de datos SQLite, plantillas, reglas y skills.
