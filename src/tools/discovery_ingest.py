import json
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.discovery_ingest")


def _extract_val(field):
    """Helper to unwrap values whether they are flat primitives or {value, certainty} objects."""
    if isinstance(field, dict) and "value" in field:
        return field["value"]
    return field


def ingest_discovery_data(payload: dict, store: VisionMemoryStore = None) -> str:
    """
    Ingests and validates the client discovery payload (from web_discovery / client_discovery_template.json).
    Stores the full structured brief into VISION's synthetic memory and returns an executive digest.
    """
    if store is None:
        store = VisionMemoryStore()

    if not isinstance(payload, dict):
        raise ValueError("Payload must be a valid dictionary or JSON object.")

    try:
        biz = payload.get("business_profile", {})
        branding = payload.get("branding_assets", {})
        tech = payload.get("technical_scope", {})
        infra = payload.get("infrastructure", {})

        company_name = _extract_val(biz.get("company_name")) or "Unnamed Client"
        sector = _extract_val(biz.get("business_sector")) or "General"
        primary_goal = _extract_val(biz.get("primary_goal")) or "Digital Presence"
        value_prop = _extract_val(biz.get("value_proposition")) or "Enterprise Solutions"

        colors = _extract_val(branding.get("color_palette", {}).get("hex_codes", []))
        typography = _extract_val(branding.get("typography", {}).get("font_families", []))
        style_adjectives = _extract_val(branding.get("style_adjectives", []))

        pages_est = _extract_val(tech.get("estimated_pages")) or 1
        integrations = _extract_val(tech.get("required_integrations")) or []
        preferred_cms = _extract_val(tech.get("preferred_cms")) or "Next.js"

        domain = _extract_val(infra.get("domain_name")) or "TBD"
        hosting = _extract_val(infra.get("hosting_preference")) or "Cloud / AWS"

        digest = {
            "status": "INGESTED_SUCCESSFULLY",
            "client": company_name,
            "business_sector": sector,
            "primary_goal": primary_goal,
            "value_proposition": value_prop,
            "branding": {
                "palette_hex": colors,
                "font_families": typography,
                "style_adjectives": style_adjectives
            },
            "technical_scope": {
                "estimated_pages": pages_est,
                "integrations": integrations,
                "preferred_stack": preferred_cms
            },
            "infrastructure": {
                "domain": domain,
                "hosting": hosting
            }
        }

        # Store in memory store
        doc_id = f"discovery_{company_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=f"Client Discovery Brief: {company_name} ({sector}). Goal: {primary_goal}. Value: {value_prop}. Tech: {preferred_cms}. Hosting: {hosting}. Colors: {', '.join(colors) if isinstance(colors, list) else colors}.",
            metadata={"type": "client_discovery", "client": company_name, "sector": sector}
        )

        logger.info("Discovery brief successfully ingested for %s", company_name)
        return json.dumps(digest, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Error ingesting discovery payload: %s", e, exc_info=True)
        raise
