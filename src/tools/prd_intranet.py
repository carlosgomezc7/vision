import json
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.prd_intranet")


def generate_intranet_prd(
    company_name: str,
    employee_count: int,
    modules: list,
    sso_provider: str,
    store: VisionMemoryStore = None,
) -> str:
    """Generates a formal PRD (Product Requirement Document) for a B2B Intranet based on client intake."""
    if store is None:
        store = VisionMemoryStore()

    try:
        prd = {
            "client": company_name,
            "employees": employee_count,
            "sso_provider": sso_provider,
            "required_modules": modules,
            "tech_stack": "Next.js (App Router) + Tailwind CSS + Supabase (PostgreSQL + pgvector)",
            "security_architecture": "RBAC (Roles: Admin, Lead, Employee) + Integrated SSO"
        }

        doc_id = f"prd_{company_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=json.dumps(prd, ensure_ascii=False),
            metadata={"type": "prd", "client": company_name}
        )
        logger.info("PRD generated and stored for client: %s", company_name)
        return json.dumps(prd, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Error generating PRD for %s: %s", company_name, e, exc_info=True)
        raise
