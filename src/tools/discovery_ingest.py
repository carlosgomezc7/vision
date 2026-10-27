import json
from src.memory.vector_store import VisionMemoryStore
from src.logger import get_logger

logger = get_logger("vision.tools.discovery_ingest")


def _extract_val(field):
    """Helper to unwrap values whether they are flat primitives or {value, certainty} / {valor, certeza} objects."""
    if isinstance(field, dict):
        if "valor" in field:
            return field["valor"]
        if "value" in field:
            return field["value"]
    return field


def _extract_certainty(field) -> str:
    """Helper to get certainty tag."""
    if isinstance(field, dict):
        return field.get("certeza") or field.get("certainty") or "reported"
    return "reported" if field else "not_determined"


def _is_populated(val) -> bool:
    """Checks if a field has actual content and is not empty or marked unready."""
    if val is None:
        return False
    if isinstance(val, str) and not val.strip():
        return False
    if isinstance(val, (list, dict)) and len(val) == 0:
        return False
    return True


def get_client_intake_guide(focus_area: str = "all") -> str:
    """
    Returns the conversational listening guide in Spanish for meetings with clients,
    mapping what to ask to what the VISION repository requires.
    """
    guide = {
        "titulo": "Guía de Escucha al Cliente para Landing Pages Personalizadas",
        "descripcion": "Preguntas estratégicas en lenguaje de negocio y su mapeo a herramientas de VISION MCP.",
        "bloques_de_escucha": [
            {
                "bloque": "1. Esencia y Propuesta de Valor",
                "pregunta_conversacional": "¿Cómo se llama tu marca y qué problema resuelves mejor que nadie?",
                "campo_destino": "perfil_negocio.nombre_empresa y propuesta_de_valor",
                "herramienta_repo": "create_landing_page_specification",
                "para_que_lo_usa_el_repo": "Genera el título SEO, OpenGraph, copy del Hero y propósito del portal."
            },
            {
                "bloque": "2. Acción Deseada del Visitante (CTA)",
                "pregunta_conversacional": "¿Qué es lo más importante que deseas que haga el visitante al entrar a tu página?",
                "campo_destino": "perfil_negocio.objetivo_principal_landing y llamado_a_la_accion_cta",
                "herramienta_repo": "create_landing_page_specification",
                "para_que_lo_usa_el_repo": "Define el botón principal de conversión (WhatsApp, formulario, llamada o agenda)."
            },
            {
                "bloque": "3. Gusto Visual y Referencias",
                "pregunta_conversacional": "¿Qué páginas web admiras visualmente y con qué adjetivos describirías tu estilo ideal?",
                "campo_destino": "identidad_visual_y_marca.adjetivos_estilo_visual y sitios_de_referencia_que_le_gustan",
                "herramienta_repo": "generate_design_tokens_w3c y create_landing_page_specification",
                "para_que_lo_usa_el_repo": "Guía la selección de tipografía, espaciados y componentes shadcn/ui."
            },
            {
                "bloque": "4. Colores y Restricciones de Marca",
                "pregunta_conversacional": "¿Cuentas con colores corporativos definidos o hay algún color que NO quieras ver jamás?",
                "campo_destino": "identidad_visual_y_marca.paleta_de_colores",
                "herramienta_repo": "audit_theme_palette, check_wcag_accessibility, export_tokens_to_stylesheet",
                "para_que_lo_usa_el_repo": "Verifica contraste WCAG 2.2 AA (4.5:1) y exporta variables CSS/Tailwind."
            },
            {
                "bloque": "5. Estructura de Secciones y Contacto",
                "pregunta_conversacional": "¿Qué secciones consideras indispensables y por qué medios prefieres que te contacten?",
                "campo_destino": "estructura_y_contenido.secciones_requeridas y conversion_y_contacto",
                "herramienta_repo": "create_landing_page_specification",
                "para_que_lo_usa_el_repo": "Modula componentes independientes en src/components/landing/*.tsx."
            }
        ]
    }

    if focus_area and focus_area.lower() != "all":
        filtered = [b for b in guide["bloques_de_escucha"] if focus_area.lower() in b["bloque"].lower()]
        if filtered:
            guide["bloques_de_escucha"] = filtered

    return json.dumps(guide, indent=2, ensure_ascii=False)


def audit_client_readiness(payload: dict, store: VisionMemoryStore = None) -> str:
    """
    Audits a client discovery payload against VISION's required inputs for custom Landing Pages.
    Calculates a readiness_score (0-100%), detects missing parameters for the repo,
    generates ready-to-ask follow-up questions in Spanish, and lists the ready MCP pipeline.
    """
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a valid dictionary or JSON object.")

    # Support both Spanish and English keys
    biz = payload.get("perfil_negocio") or payload.get("business_profile") or {}
    visual = payload.get("identidad_visual_y_marca") or payload.get("branding_assets") or {}
    content = payload.get("estructura_y_contenido") or payload.get("content") or payload.get("technical_scope") or {}
    contact = payload.get("conversion_y_contacto") or payload.get("infrastructure") or {}

    company_name = _extract_val(biz.get("nombre_empresa") or biz.get("company_name"))
    value_prop = _extract_val(biz.get("propuesta_de_valor") or biz.get("value_proposition"))
    sector = _extract_val(biz.get("sector_industria") or biz.get("business_sector"))

    cta_goal = _extract_val(
        content.get("llamado_a_la_accion_cta")
        or biz.get("objetivo_principal_landing")
        or biz.get("primary_goal")
    )

    colors = _extract_val(
        visual.get("paleta_de_colores", {}).get("colores_deseados_hex")
        if isinstance(visual.get("paleta_de_colores"), dict)
        else visual.get("color_palette", {}).get("hex_codes")
    )
    style_adjectives = _extract_val(visual.get("adjetivos_estilo_visual") or visual.get("style_adjectives"))

    sections = _extract_val(
        content.get("secciones_requeridas")
        or content.get("pages_sections")
        or content.get("required_sections")
    )

    contact_channels = _extract_val(
        contact.get("canales_de_contacto")
        or contact.get("required_integrations")
    )
    domain = _extract_val(contact.get("dominio") or contact.get("domain_name"))

    confirmed_fields = {}
    missing_for_repo = []
    next_questions = []

    score = 0

    # 1. Negocio y Propuesta de Valor (25 pts)
    if _is_populated(company_name):
        score += 15
        confirmed_fields["company_name"] = company_name
    else:
        missing_for_repo.append({
            "parametro": "nombre_empresa",
            "herramienta_afectada": "create_landing_page_specification",
            "razon": "Requerido para el título SEO, OpenGraph y branding de la Landing Page."
        })
        next_questions.append("¿Cuál es el nombre comercial exacto con el que deseas que aparezca tu empresa en la web?")

    if _is_populated(value_prop):
        score += 10
        confirmed_fields["value_proposition"] = value_prop
    else:
        missing_for_repo.append({
            "parametro": "propuesta_de_valor",
            "herramienta_afectada": "create_landing_page_specification",
            "razon": "Requerido para redactar el titular persuasivo del Hero."
        })
        next_questions.append("En una frase, ¿cuál es el beneficio o solución principal que ofreces a tus clientes?")

    # 2. Objetivo de Conversión / CTA (25 pts)
    if _is_populated(cta_goal):
        score += 25
        confirmed_fields["cta_goal"] = cta_goal
    else:
        missing_for_repo.append({
            "parametro": "llamado_a_la_accion_cta",
            "herramienta_afectada": "create_landing_page_specification",
            "razon": "Necesario para diseñar el botón de conversión principal (ej: WhatsApp, Cotización, Agendar)."
        })
        next_questions.append("¿Qué acción específica quieres que realice el visitante? (ej: enviar WhatsApp, llenar formulario, llamar por teléfono)")

    # 3. Identidad Visual y Colores (25 pts)
    visual_score = 0
    if _is_populated(colors):
        visual_score += 15
        confirmed_fields["colors"] = colors
    else:
        missing_for_repo.append({
            "parametro": "colores_deseados_hex",
            "herramienta_afectada": "audit_theme_palette y export_tokens_to_stylesheet",
            "razon": "Requerido para generar la paleta de colores CSS con contraste WCAG 2.2 AA (o confirmar si VISION debe proponerla)."
        })
        next_questions.append("¿Cuentas con colores corporativos en código hexadecimal o prefieres que te propongamos una paleta basada en tu estilo?")

    if _is_populated(style_adjectives):
        visual_score += 10
        confirmed_fields["style_adjectives"] = style_adjectives
    else:
        missing_for_repo.append({
            "parametro": "adjetivos_estilo_visual",
            "herramienta_afectada": "generate_design_tokens_w3c",
            "razon": "Define la dirección visual y personalidad (ej: moderno, minimalista, sobrio, elegante)."
        })
        next_questions.append("¿Con qué 2 o 3 adjetivos describirías la personalidad visual que buscas? (ej: moderno, elegante, limpio, tecnológico)")
    score += visual_score

    # 4. Estructura de Secciones (15 pts)
    if _is_populated(sections):
        score += 15
        confirmed_fields["sections"] = sections
    else:
        missing_for_repo.append({
            "parametro": "secciones_requeridas",
            "herramienta_afectada": "create_landing_page_specification",
            "razon": "Determina qué componentes modulares en src/components/landing/*.tsx deben crearse."
        })
        next_questions.append("¿Qué secciones clave deseas incluir? (ej: Hero, Servicios, Nosotros, Testimonios, Contacto)")

    # 5. Canales de Contacto / Dominio (10 pts)
    contact_score = 0
    if _is_populated(contact_channels):
        contact_score += 5
        confirmed_fields["contact_channels"] = contact_channels
    if _is_populated(domain):
        contact_score += 5
        confirmed_fields["domain"] = domain
    score += contact_score

    ready_pipeline = []
    if _is_populated(colors):
        ready_pipeline.append("audit_theme_palette")
        ready_pipeline.append("export_tokens_to_stylesheet")
    if _is_populated(style_adjectives):
        ready_pipeline.append("generate_design_tokens_w3c")
    if _is_populated(company_name) and _is_populated(cta_goal):
        ready_pipeline.append("create_landing_page_specification")

    status = "READY_TO_BUILD" if score >= 80 and _is_populated(company_name) and _is_populated(cta_goal) else "NEEDS_CLIENT_INPUT"

    report = {
        "status": status,
        "readiness_score": score,
        "client": company_name or "Cliente por definir",
        "confirmed_fields": confirmed_fields,
        "missing_for_repo": missing_for_repo,
        "next_questions_for_client": next_questions,
        "ready_to_execute_tools": ready_pipeline,
        "veredicto": (
            "✅ Información completa para construir la Landing Page personalizada."
            if status == "READY_TO_BUILD"
            else f"⚠️ Preparación al {score}%. Realiza las preguntas de seguimiento al cliente para completar los insumos del repo."
        )
    }

    # Index in memory if client name is known
    if store is not None and company_name:
        doc_id = f"readiness_{company_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=f"Landing Page Readiness Audit for {company_name}: Score {score}%. Status: {status}. Confirmed: {list(confirmed_fields.keys())}.",
            metadata={"type": "readiness_audit", "client": company_name, "score": score}
        )

    logger.info("Readiness audit completed for %s: score=%d%% (%s)", company_name, score, status)
    return json.dumps(report, indent=2, ensure_ascii=False)


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
        biz = payload.get("perfil_negocio") or payload.get("business_profile") or {}
        visual = payload.get("identidad_visual_y_marca") or payload.get("branding_assets") or {}
        content = payload.get("estructura_y_contenido") or payload.get("content") or payload.get("technical_scope") or {}
        infra = payload.get("infraestructura_y_entrega") or payload.get("infrastructure") or {}

        company_name = _extract_val(biz.get("nombre_empresa") or biz.get("company_name")) or "Cliente Sin Nombre"
        sector = _extract_val(biz.get("sector_industria") or biz.get("business_sector")) or "General"
        primary_goal = _extract_val(biz.get("objetivo_principal_landing") or biz.get("primary_goal")) or "Presencia Digital"
        value_prop = _extract_val(biz.get("propuesta_de_valor") or biz.get("value_proposition")) or "Servicios Profesionales"

        colors = _extract_val(
            visual.get("paleta_de_colores", {}).get("colores_deseados_hex")
            if isinstance(visual.get("paleta_de_colores"), dict)
            else visual.get("color_palette", {}).get("hex_codes", [])
        ) or []
        typography = _extract_val(
            visual.get("tipografia", {}).get("familias_preferidas")
            if isinstance(visual.get("tipografia"), dict)
            else visual.get("typography", {}).get("font_families", [])
        ) or []
        style_adjectives = _extract_val(visual.get("adjetivos_estilo_visual") or visual.get("style_adjectives", [])) or []

        sections = _extract_val(
            content.get("secciones_requeridas")
            or content.get("pages_sections")
            or content.get("required_sections", [])
        ) or ["Hero", "Servicios", "Nosotros", "Contacto"]

        domain = _extract_val(infra.get("dominio") or infra.get("domain_name")) or "Por definir"
        hosting = _extract_val(infra.get("preferencia_hosting") or infra.get("hosting_preference")) or "Vercel / AWS"

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
            "landing_structure": {
                "sections": sections,
                "domain": domain,
                "hosting": hosting
            }
        }

        doc_id = f"discovery_{company_name.lower().replace(' ', '_')}"
        store.add_memory(
            doc_id=doc_id,
            text=f"Landing Page Brief: {company_name} ({sector}). Propuesta: {value_prop}. Meta: {primary_goal}. Secciones: {', '.join(sections) if isinstance(sections, list) else sections}. Colores: {', '.join(colors) if isinstance(colors, list) else colors}. Estilo: {', '.join(style_adjectives) if isinstance(style_adjectives, list) else style_adjectives}.",
            metadata={"type": "landing_discovery", "client": company_name, "sector": sector}
        )

        logger.info("Landing page discovery brief successfully ingested for %s", company_name)
        return json.dumps(digest, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Error ingesting discovery payload: %s", e, exc_info=True)
        raise
