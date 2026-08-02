from fastmcp import FastMCP
from src.memory.vector_store import VisionMemoryStore
from src.tools.prd_intranet import generate_intranet_prd
from src.tools.architecture_tool import get_architecture_blueprint
from src.tools.retrospect_tool import record_lesson_learned
from src.tools.ux_design_tool import (
    validate_wcag_contrast,
    generate_w3c_design_tokens,
    audit_performance_budget,
)

mcp = FastMCP("VISION - CTI Soluciones")
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

if __name__ == "__main__":
    mcp.run()
