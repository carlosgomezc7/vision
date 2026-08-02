import json
import math

def hex_to_relative_luminance(hex_color: str) -> float:
    """Calcula la luminancia relativa según especificación WCAG 2.2."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0

    def adjust(c):
        return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)

    r_adj = adjust(r)
    g_adj = adjust(g)
    b_adj = adjust(b)

    return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj

def validate_wcag_contrast(fg_hex: str, bg_hex: str, is_large_text: bool = False) -> str:
    """
    Validador estricto de accesibilidad WCAG 2.2 Nivel AA.
    Calcula el contraste exacto sin redondear hacia arriba.
    Mínimo: 4.5:1 para texto normal, 3.0:1 para texto grande (>=18pt o >=14pt bold).
    """
    l1 = hex_to_relative_luminance(fg_hex)
    l2 = hex_to_relative_luminance(bg_hex)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    ratio = (lighter + 0.05) / (darker + 0.05)
    
    required_ratio = 3.0 if is_large_text else 4.5
    passes_aa = ratio >= required_ratio
    passes_aaa = ratio >= (4.5 if is_large_text else 7.0)

    result = {
        "fg_hex": fg_hex,
        "bg_hex": bg_hex,
        "is_large_text": is_large_text,
        "exact_ratio": f"{ratio:.4f}:1",
        "raw_ratio": ratio,
        "required_ratio_aa": f"{required_ratio}:1",
        "passes_wcag_aa": passes_aa,
        "passes_wcag_aaa": passes_aaa,
        "status": "PASS" if passes_aa else "FAIL",
        "notes": (
            f"Cumple con WCAG 2.2 AA (Requerido {required_ratio}:1)."
            if passes_aa
            else f"NO cumple con WCAG 2.2 AA. Requiere al menos {required_ratio}:1 pero obtuvo {ratio:.4f}:1."
        )
    }

    return json.dumps(result, indent=2, ensure_ascii=False)

def generate_w3c_design_tokens(color_palette: dict, typography: dict = None, spacing: dict = None) -> str:
    """
    Genera tokens de diseño bajo el formato estricto JSON de W3C Design Tokens Community Group (DTCG).
    Usa la nomenclatura con prefijos $ ($value, $type, $description).
    """
    tokens = {
        "color": {},
        "typography": {},
        "spacing": {}
    }

    for name, hex_val in color_palette.items():
        tokens["color"][name] = {
            "$value": hex_val,
            "$type": "color",
            "$description": f"Token de color {name} corporativo CTI Soluciones"
        }

    if typography:
        for name, font_val in typography.items():
            tokens["typography"][name] = {
                "$value": font_val,
                "$type": "fontFamily" if "family" in name.lower() else "fontSize",
                "$description": f"Token tipográfico {name}"
            }

    if spacing:
        for name, space_val in spacing.items():
            tokens["spacing"][name] = {
                "$value": space_val,
                "$type": "dimension",
                "$description": f"Token de espaciado {name}"
            }

    return json.dumps(tokens, indent=2, ensure_ascii=False)

def audit_performance_budget(framework: str, estimated_js_kb: float, animations_count: int) -> str:
    """
    Evalúa el presupuesto de rendimiento contra los Core Web Vitals de Google:
    - INP (Interaction to Next Paint): < 200 ms
    - LCP (Largest Contentful Paint): < 2.5 s
    - CLS (Cumulative Layout Shift): <= 0.1
    """
    inp_risk = "ALTO" if estimated_js_kb > 300 or animations_count > 10 else "BAJO"
    lcp_risk = "ALTO" if estimated_js_kb > 500 else "OPTIMO"
    
    recommendations = []
    if estimated_js_kb > 250:
        recommendations.append("Implementar Code-splitting y Dynamic Imports para mantener JS inicial < 250KB.")
    if animations_count > 5:
        recommendations.append("Usar 'will-change' y CSS transform/opacity para evitar tareas largas en el hilo principal.")
    if framework.lower() == "next.js":
        recommendations.append("Utilizar next/font y next/image para optimización automática de LCP y prevención de CLS.")

    budget = {
        "framework": framework,
        "targets": {
            "INP": "< 200 ms",
            "LCP": "< 2.5 s",
            "CLS": "<= 0.1"
        },
        "evaluation": {
            "estimated_js_bundle_kb": estimated_js_kb,
            "animations_count": animations_count,
            "inp_risk": inp_risk,
            "lcp_risk": lcp_risk
        },
        "recommendations": recommendations
    }

    return json.dumps(budget, indent=2, ensure_ascii=False)
