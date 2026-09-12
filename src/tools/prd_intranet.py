import json
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.prd_intranet")
store = VisionMemoryStore()


def generate_intranet_prd(company_name: str, employee_count: int, modules: list, sso_provider: str) -> str:
    """Genera un PRD (Product Requirement Document) formal para una Intranet B2B basado en el intake del cliente."""
    try:
        prd = {
            "cliente": company_name,
            "colaboradores": employee_count,
            "proveedor_sso": sso_provider,
            "modulos_requeridos": modules,
            "stack_tecnologico": "Next.js (App Router) + Tailwind CSS + Supabase (PostgreSQL + pgvector)",
            "arquitectura_seguridad": "RBAC (Roles: Admin, Líder, Empleado) + SSO Integrado"
        }

        doc_id = f"prd_{company_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=json.dumps(prd, ensure_ascii=False),
            metadata={"type": "prd", "client": company_name}
        )
        logger.info("PRD generado y almacenado para cliente: %s", company_name)
        return json.dumps(prd, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Error al generar PRD para %s: %s", company_name, e, exc_info=True)
        raise
