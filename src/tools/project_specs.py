import json
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.project_specs")


def create_landing_page_spec(
    company_name: str,
    sections: list = None,
    cta_goal: str = "Contactar por WhatsApp o Formulario",
    style_adjectives: list = None,
    palette_hex: list = None,
    typography: list = None,
    contact_channels: list = None,
    store: VisionMemoryStore = None,
) -> str:
    """
    Generates a formal specification for a custom, beautiful, and accessible Landing Page.
    Ensures modular architecture under src/components/landing/* with zero database or authentication dependencies.
    """
    if store is None:
        store = VisionMemoryStore()

    try:
        clean_name = company_name.strip() if company_name else "Cliente"
        sections_list = [s.strip().capitalize() for s in sections] if sections else ["Hero", "Servicios", "Nosotros", "Contacto"]
        adjectives = style_adjectives or ["moderno", "limpio", "elegante", "accesible"]
        colors = palette_hex or ["#0F172A", "#2563EB", "#F8FAFC"]
        typo = typography or ["Inter", "sans-serif"]
        channels = contact_channels or ["WhatsApp", "Formulario"]

        component_hierarchy = {
            "Header": {
                "file": "src/components/landing/Header.tsx",
                "description": f"Cabecera con logotipo de {clean_name}, navegación interna suave a secciones y botón CTA destacado."
            }
        }

        for sec in sections_list:
            comp_name = f"{sec}.tsx"
            component_hierarchy[sec] = {
                "file": f"src/components/landing/{comp_name}",
                "description": f"Componente dedicado y modular para la sección {sec} de {clean_name}."
            }

        component_hierarchy["Footer"] = {
            "file": "src/components/landing/Footer.tsx",
            "description": f"Pie de página accesible con derechos reservados, enlaces rápidos y datos de contacto de {clean_name}."
        }

        spec = {
            "project_type": "Landing Page Personalizada / Sitio Web Corporativo",
            "client": clean_name,
            "architecture": "Next.js App Router (100% Estático y Modular — Cero Auth / Cero BD)",
            "primary_cta_goal": cta_goal,
            "style_adjectives": adjectives,
            "color_palette_hex": colors,
            "typography": typo,
            "contact_channels": channels,
            "tech_stack": {
                "framework": "Next.js (App Router, static export)",
                "styling": "Tailwind CSS + Lucide React + shadcn/ui",
                "design_tokens": "W3C DTCG ($value, $type) exportado a CSS Variables",
                "hosting_target": "Vercel, AWS S3/CloudFront o Hostinger"
            },
            "required_sections": sections_list,
            "component_structure": component_hierarchy,
            "seo_metadata": {
                "title": f"{clean_name} — Sitio Oficial",
                "description": f"Descubre {clean_name}. {cta_goal}.",
                "open_graph": {
                    "type": "website",
                    "locale": "es_MX",
                    "site_name": clean_name
                }
            },
            "rules": [
                "Arquitectura modular estricta: page.tsx solo orquesta e importa desde src/components/landing/*",
                "Contraste estricto WCAG 2.2 AA (4.5:1 texto normal, 3.0:1 texto grande) en todos los elementos interactivos",
                "100% navegable por teclado con indicador visual de foco explícito",
                "Escalado al 200% sin desbordamiento horizontal (responsive mobile-first)",
                "Cero dependencias de autenticación, sesiones de servidor o bases de datos relacionales"
            ]
        }

        doc_id = f"spec_landing_{clean_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=json.dumps(spec, ensure_ascii=False),
            metadata={"type": "landing_page_spec", "client": clean_name}
        )

        logger.info("Landing page spec generated and indexed for client: %s", clean_name)
        return json.dumps(spec, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Error generating landing page spec for %s: %s", company_name, e, exc_info=True)
        raise
