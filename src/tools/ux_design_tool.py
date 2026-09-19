import json
import math
import re
from src.logger import get_logger

logger = get_logger("vision.tools.ux_design")

HEX_COLOR_PATTERN = re.compile(r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


def hex_to_relative_luminance(hex_color: str) -> float:
    """Calculates relative luminance according to the WCAG 2.2 specification."""
    if not isinstance(hex_color, str) or not HEX_COLOR_PATTERN.match(hex_color.strip()):
        raise ValueError(f"Invalid hex color format: '{hex_color}'. Expected '#RGB' or '#RRGGBB'.")

    try:
        clean_hex = hex_color.strip().lstrip('#')
        if len(clean_hex) == 3:
            clean_hex = ''.join([c*2 for c in clean_hex])

        r = int(clean_hex[0:2], 16) / 255.0
        g = int(clean_hex[2:4], 16) / 255.0
        b = int(clean_hex[4:6], 16) / 255.0


        def adjust(c):
            return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)

        r_adj = adjust(r)
        g_adj = adjust(g)
        b_adj = adjust(b)

        return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj
    except Exception as e:
        logger.error("Error calculating luminance for %s: %s", hex_color, e, exc_info=True)
        raise


def validate_wcag_contrast(fg_hex: str, bg_hex: str, is_large_text: bool = False) -> str:
    """
    Strict WCAG 2.2 Level AA accessibility validator.
    Calculates the exact contrast without rounding up.
    Minimum: 4.5:1 for normal text, 3.0:1 for large text (>=18pt or >=14pt bold).
    """
    try:
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
                f"Passes WCAG 2.2 AA (Required {required_ratio}:1)."
                if passes_aa
                else f"Does NOT pass WCAG 2.2 AA. Requires at least {required_ratio}:1 but got {ratio:.4f}:1."
            )
        }

        logger.info("WCAG check: %s vs %s -> %s", fg_hex, bg_hex, result["status"])
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Error validating contrast %s vs %s: %s", fg_hex, bg_hex, e, exc_info=True)
        raise


def generate_w3c_design_tokens(color_palette: dict, typography: dict = None, spacing: dict = None) -> str:
    """
    Generates design tokens in the strict JSON format of the W3C Design Tokens Community Group (DTCG).
    Uses the $ prefix naming convention ($value, $type, $description).
    """
    try:
        tokens = {
            "color": {},
            "typography": {},
            "spacing": {}
        }

        for name, hex_val in color_palette.items():
            tokens["color"][name] = {
                "$value": hex_val,
                "$type": "color",
                "$description": f"Corporate color token {name} - CTI Soluciones"
            }

        if typography:
            for name, font_val in typography.items():
                tokens["typography"][name] = {
                    "$value": font_val,
                    "$type": "fontFamily" if "family" in name.lower() else "fontSize",
                    "$description": f"Typography token {name}"
                }

        if spacing:
            for name, space_val in spacing.items():
                tokens["spacing"][name] = {
                    "$value": space_val,
                    "$type": "dimension",
                    "$description": f"Spacing token {name}"
                }

        logger.info("W3C tokens generated: %d colors, %d typography, %d spacing",
                    len(tokens["color"]), len(tokens["typography"]), len(tokens["spacing"]))
        return json.dumps(tokens, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Error generating W3C tokens: %s", e, exc_info=True)
        raise


def audit_performance_budget(framework: str, estimated_js_kb: float, animations_count: int) -> str:
    """
    Evaluates the performance budget against Google Core Web Vitals:
    - INP (Interaction to Next Paint): < 200 ms
    - LCP (Largest Contentful Paint): < 2.5 s
    - CLS (Cumulative Layout Shift): <= 0.1
    """
    try:
        inp_risk = "HIGH" if estimated_js_kb > 300 or animations_count > 10 else "LOW"
        lcp_risk = "HIGH" if estimated_js_kb > 500 else "OPTIMAL"

        recommendations = []
        if estimated_js_kb > 250:
            recommendations.append("Implement code-splitting and dynamic imports to keep initial JS bundle < 250KB.")
        if animations_count > 5:
            recommendations.append("Use 'will-change' and CSS transform/opacity to prevent long main-thread tasks.")
        if framework.lower() == "next.js":
            recommendations.append("Use next/font and next/image for automatic LCP optimization and CLS prevention.")


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

        logger.info("Performance audit for %s: INP=%s, LCP=%s", framework, inp_risk, lcp_risk)
        return json.dumps(budget, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error("Error in performance audit: %s", e, exc_info=True)
        raise
