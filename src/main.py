from fastmcp import FastMCP
from src.memory.vector_store import VisionMemoryStore
from src.tools.prd_intranet import generate_intranet_prd
from src.tools.architecture_tool import get_architecture_blueprint
from src.tools.retrospect_tool import record_lesson_learned

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

if __name__ == "__main__":
    mcp.run()
