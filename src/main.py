import sys
from pathlib import Path

# Allow direct execution (python src/main.py) by adding the project root to sys.path
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
from src.tools.issue_tracker import record_issue, list_recorded_issues, update_issue_status
from src.tools.system_info import format_system_info_report
from src.tools.project_specs import create_landing_page_spec, generate_supabase_rls_policies
from src.tools.discovery_ingest import ingest_discovery_data
from src.tools.tokens_exporter import export_tokens_to_css, audit_full_palette
from src.tools.knowledge_tool import ingest_knowledge_document
from src.tools.devops_tool import get_project_health_status, trigger_git_checkpoint
from src.logger import setup_logging, get_logger
from src.config import LOG_FILE

# Configure logging before any other operation
setup_logging(log_file=LOG_FILE)
logger = get_logger("vision.main")

SYSTEM_INSTRUCTIONS = """
VISION - CTI Soluciones (MCP Context)
=====================================
Intelligence and Architecture Server for designing and developing B2B Enterprise Intranets and Custom Corporate Portals.

Core Principles and Business Context:
1. Business Model: Development of corporate intranets with Deep Search engines (Deep Search/RAG), reduction of operational time, and Zero Trust security.
2. Architecture & Security: Integration of RBAC, SSO (Azure AD / Google Workspace), hybrid/cloud architecture (AWS / On-Premise), and SQL Server / Supabase PostgreSQL.
3. Design & UX / Accessibility: Strict WCAG 2.2 AA compliance (minimum contrast 4.5:1 normal text, 3.0:1 large text), 200% scaling without horizontal scroll, 100% keyboard navigation, and W3C DTCG design tokens.
4. Project Start Protocol: Automatic detection of new project intents, strict bifurcation (B2B Intranet vs Landing Page), elicitation flow, and reuse of standard components.
5. Synthetic Memory: Continuous querying and recording of lessons learned and blueprints in SQLite with FTS5 BM25 search.
"""

# Initialize FastMCP with global system instructions
mcp = FastMCP("VISION - CTI Soluciones", instructions=SYSTEM_INSTRUCTIONS)

store = VisionMemoryStore()

# Ensure automatic memory seeding on startup
try:
    seed_count = seed_vision_mind(store=store)
    logger.info("Memory initialized with %d seed knowledge documents.", seed_count)
except Exception as e:
    logger.error("Error seeding memory: %s", e, exc_info=True)


def _safe_tool_call(func, *args, **kwargs) -> str:
    """Centralized wrapper to capture exceptions in MCP tools."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error("Error in MCP tool %s: %s", func.__name__, e, exc_info=True)
        return f"⚠️ Internal error in tool '{func.__name__}': {e}"


# ─── Knowledge & Deep Search Tools ──────────────────────────────────────────

@mcp.tool()
def query_vision_memory(query: str) -> str:
    """Searches the synthetic memory and knowledge base of VISION using SQLite FTS5 BM25 ranking."""
    return _safe_tool_call(_query_vision_memory_impl, query)


def _query_vision_memory_impl(query: str) -> str:
    results = store.query_memory(query, n_results=3)
    docs = results.get("documents", [[]])[0]
    if not docs:
        return "No relevant memories found."
    return "\n\n".join(docs)


@mcp.tool()
def ingest_custom_document(title: str, category: str, content: str, tags: list = None) -> str:
    """Dynamically ingests and indexes external documents, client policies, or manuals into VISION memory."""
    return _safe_tool_call(ingest_knowledge_document, title, category, content, tags, store=store)


@mcp.tool()
def consult_architecture(topic: str) -> str:
    """Queries technical blueprints and Deep Search guides in memory."""
    return _safe_tool_call(get_architecture_blueprint, topic, store=store)


@mcp.tool()
def log_retrospective(project_name: str, lesson: str) -> str:
    """Records a lesson learned or key decision for a project in long-term memory."""
    return _safe_tool_call(record_lesson_learned, project_name, lesson, store=store)


# ─── Project Specification & Discovery Tools ────────────────────────────────

@mcp.tool()
def ingest_client_discovery(payload: dict) -> str:
    """Ingests and validates the client discovery payload from web_discovery into VISION memory."""
    return _safe_tool_call(ingest_discovery_data, payload, store=store)


@mcp.tool()
def create_intranet_prd(company_name: str, employee_count: int, modules: list, sso_provider: str) -> str:
    """Generates the corporate PRD for a B2B Intranet (Bifurcation B)."""
    return _safe_tool_call(generate_intranet_prd, company_name, employee_count, modules, sso_provider, store=store)


@mcp.tool()
def create_landing_page_specification(company_name: str, sections: list, cta_goal: str, style_adjectives: list = None) -> str:
    """Generates a formal specification for a public Landing Page (Bifurcation A - no database/auth)."""
    return _safe_tool_call(create_landing_page_spec, company_name, sections, cta_goal, style_adjectives, store=store)


@mcp.tool()
def generate_supabase_rls_schema(company_name: str, modules: list, roles: list = None) -> str:
    """Generates PostgreSQL SQL schema with Zero Trust Row Level Security (RLS) policies for Supabase."""
    return _safe_tool_call(generate_supabase_rls_policies, company_name, modules, roles)


# ─── UX, UI & Design Token Tools ────────────────────────────────────────────

@mcp.tool()
def check_wcag_accessibility(fg_hex: str, bg_hex: str, is_large_text: bool = False) -> str:
    """Validates strict WCAG 2.2 Level AA contrast (4.5:1 normal text, 3.0:1 large text) without rounding."""
    return _safe_tool_call(validate_wcag_contrast, fg_hex, bg_hex, is_large_text)


@mcp.tool()
def generate_design_tokens_w3c(color_palette: dict, typography: dict = None, spacing: dict = None) -> str:
    """Generates design tokens under the strict W3C DTCG specification ($value, $type, $description)."""
    return _safe_tool_call(generate_w3c_design_tokens, color_palette, typography, spacing)


@mcp.tool()
def export_tokens_to_stylesheet(tokens_input: dict, format_type: str = "css_variables") -> str:
    """Converts W3C DTCG design tokens to CSS Custom Properties (:root) or Tailwind CSS config."""
    return _safe_tool_call(export_tokens_to_css, tokens_input, format_type)


@mcp.tool()
def audit_theme_palette(palette: dict) -> str:
    """Audits a complete corporate theme palette against WCAG 2.2 AA cross-pairings."""
    return _safe_tool_call(audit_full_palette, palette)


@mcp.tool()
def check_performance_budget(framework: str, estimated_js_kb: float, animations_count: int) -> str:
    """Audits the performance budget to ensure Core Web Vitals (INP < 200ms, LCP < 2.5s, CLS <= 0.1)."""
    return _safe_tool_call(audit_performance_budget, framework, estimated_js_kb, animations_count)


# ─── Issue Tracking & DevOps Tools ──────────────────────────────────────────

@mcp.tool()
def log_incident_issue(title: str, category: str, description_es: str, description_en: str, solution: str = "", status: str = "Resolved") -> str:
    """Records an incident or issue in the VISION tracking system (SQLite + ISSUES.md)."""
    return _safe_tool_call(record_issue, title, category, description_es, description_en, solution, status)


@mcp.tool()
def update_recorded_issue(issue_number: int, new_status: str, solution: str = "") -> str:
    """Updates status and solution for an existing issue in SQLite."""
    return _safe_tool_call(update_issue_status, issue_number, new_status, solution)


@mcp.tool()
def get_issues_log(category: str = None, status: str = None, limit: int = 50, offset: int = 0) -> str:
    """Retrieves recorded incidents from the VISION database with optional filtering and pagination."""
    return _safe_tool_call(list_recorded_issues, category, status, limit, offset)


@mcp.tool()
def detect_system_environment() -> str:
    """Automatically detects the operating system environment (Omarch / Arch Linux), kernel, and Python status."""
    return _safe_tool_call(format_system_info_report)


@mcp.tool()
def check_project_health() -> str:
    """Performs a comprehensive diagnostic report of VISION database, knowledge base, issues, and Git."""
    return _safe_tool_call(get_project_health_status, store=store)


@mcp.tool()
def make_git_checkpoint(message: str) -> str:
    """Creates an on-demand conventional Git checkpoint commit for the current project state."""
    return _safe_tool_call(trigger_git_checkpoint, message)


# ─── Resources & Prompts ───────────────────────────────────────────────────

@mcp.resource("config://system_context")
def get_system_context_resource() -> str:
    """MCP resource that exposes the VISION - CTI Soluciones system context and guidelines."""
    return SYSTEM_INSTRUCTIONS


@mcp.prompt()
def vision_system_prompt() -> str:
    """Official prompt with VISION's strategic context to guide interactions."""
    return f"You are VISION, the CTI Soluciones copilot. System guidelines:\n\n{SYSTEM_INSTRUCTIONS}"


if __name__ == "__main__":
    logger.info("🚀 VISION MCP Server started and ready.")
    mcp.run()
