import sys
from pathlib import Path

# Permitir la ejecución directa (python src/main.py) añadiendo la raíz del proyecto a sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastmcp import FastMCP
from src.memory.vector_store import VisionMemoryStore
from src.memory.seeder import seed_vision_mind
from src.tools.prd_intranet import generate_intranet_prd
from src.tools.architecture_tool import get_architecture_blueprint
from src.tools.retrospect_tool import record_lesson_learned
from src.tools.ux_design_tool import (
    validate_wcag_contrast,
    generate_w3c_design_tokens,
    audit_performance_budget,
)

SYSTEM_INSTRUCTIONS = """
VISION - CTI Soluciones (MCP Context)
=====================================
Servidor de Inteligencia y Arquitectura para el diseño y desarrollo de Intranets Empresariales B2B y Portales Corporativos a la Medida.

Principios Fundamentales y Contexto de Negocio:
1. Modelo de Negocio: Desarrollo de intranets corporativas con motores de Búsqueda Profunda (Deep Search/RAG), reducción de tiempos operativos y seguridad Zero Trust.
2. Arquitectura & Seguridad: Integración de RBAC, SSO (Azure AD / Google Workspace), arquitectura híbrida/cloud (AWS / On-Premise) y SQL Server.
3. Diseño & UX / Accesibilidad: Cumplimiento estricto de WCAG 2.2 AA (contraste mínimo 4.5:1 texto normal, 3.0:1 texto grande), escalado a 200% sin scroll horizontal, navegación por teclado 100% y tokens de diseño W3C DTCG.
4. Protocolo de Inicio de Proyecto: Detección automática de intenciones de nuevo proyecto, flujo de elicitación (Cliente, Ruta, Git, Supabase, Branding) y reutilización de componentes estándar.
5. Memoria Sintética: Consulta y registro continuo de lecciones aprendidas y blueprints en la base de conocimiento SQLite/Vectorial.
"""

# Inicializar FastMCP con instrucciones globales del sistema
mcp = FastMCP("VISION - CTI Soluciones", instructions=SYSTEM_INSTRUCTIONS)

# Garantizar el sembrado automático de memoria al iniciar
try:
    seed_vision_mind()
except Exception as e:
    print(f"Aviso al sembrar memoria: {e}", file=sys.stderr)

store = VisionMemoryStore()

@mcp.tool()
def query_vision_memory(query: str) -> str:
    """Busca en la memoria sintética y base de conocimiento de VISION."""
    results = store.query_memory(query, n_results=3)
    docs = results.get("documents", [[]])[0]
    if not docs:
        return "No se encontraron memorias relevantes."
    return "\n\n".join(docs)

@mcp.tool()
def create_intranet_prd(company_name: str, employee_count: int, modules: list, sso_provider: str) -> str:
    """Genera el PRD corporativo para una Intranet B2B."""
    return generate_intranet_prd(company_name, employee_count, modules, sso_provider)

@mcp.tool()
def consult_architecture(topic: str) -> str:
    """Consulta los blueprints técnicos y de Deep Search en la memoria."""
    return get_architecture_blueprint(topic)

@mcp.tool()
def log_retrospective(project_name: str, lesson: str) -> str:
    """Registra un aprendizaje o retrospectiva del proyecto."""
    return record_lesson_learned(project_name, lesson)

@mcp.tool()
def check_wcag_accessibility(fg_hex: str, bg_hex: str, is_large_text: bool = False) -> str:
    """Valida el contraste WCAG 2.2 Nivel AA estricto (4.5:1 texto normal, 3.0:1 texto grande) sin redondear."""
    return validate_wcag_contrast(fg_hex, bg_hex, is_large_text)

@mcp.tool()
def generate_design_tokens_w3c(color_palette: dict, typography: dict = None, spacing: dict = None) -> str:
    """Genera tokens de diseño bajo especificación estricta W3C DTCG ($value, $type, $description)."""
    return generate_w3c_design_tokens(color_palette, typography, spacing)

@mcp.tool()
def check_performance_budget(framework: str, estimated_js_kb: float, animations_count: int) -> str:
    """Audita el presupuesto de rendimiento para garantizar Core Web Vitals (INP < 200ms, LCP < 2.5s, CLS <= 0.1)."""
    return audit_performance_budget(framework, estimated_js_kb, animations_count)

@mcp.resource("config://system_context")
def get_system_context_resource() -> str:
    """Recurso MCP que expone el contexto y directrices del sistema VISION - CTI Soluciones."""
    return SYSTEM_INSTRUCTIONS

@mcp.prompt()
def vision_system_prompt() -> str:
    """Prompt oficial con el contexto estratégico de VISION para guiar la interacción."""
    return f"Eres VISION, el copilot de CTI Soluciones. Directrices del sistema:\n\n{SYSTEM_INSTRUCTIONS}"

if __name__ == "__main__":
    mcp.run()
