import json
from src.memory.vector_store import VisionMemoryStore

store = VisionMemoryStore()

def generate_intranet_prd(company_name: str, employee_count: int, modules: list, sso_provider: str) -> str:
    """Genera un PRD (Product Requirement Document) formal para una Intranet B2B basado en el intake del cliente."""
    prd = {
        "cliente": company_name,
        "colaboradores": employee_count,
        "proveedor_sso": sso_provider,
        "modulos_requeridos": modules,
        "stack_tecnologico": "Next.js (App Router) + Tailwind CSS + Supabase (PostgreSQL + pgvector)",
        "arquitectura_seguridad": "RBAC (Roles: Admin, Líder, Empleado) + SSO Integrado"
    }
    
    # Almacenar en la memoria de VISION
    doc_id = f"prd_{company_name.lower().replace(' ', '_')}"
    store.add_memory(doc_id=doc_id, text=json.dumps(prd, ensure_ascii=False), metadata={"type": "prd", "client": company_name})
    
    return json.dumps(prd, indent=2, ensure_ascii=False)
