import json
from src.tools.ux_design_tool import hex_to_relative_luminance, HEX_COLOR_PATTERN
from src.logger import get_logger

logger = get_logger("vision.tools.tokens_exporter")


def export_tokens_to_css(tokens_input, format_type: str = "css_variables") -> str:
    """
    Translates W3C DTCG design tokens ($value, $type) into production CSS Custom Properties
    or Tailwind CSS theme variables.
    """
    try:
        if isinstance(tokens_input, str):
            tokens = json.loads(tokens_input)
        elif isinstance(tokens_input, dict):
            tokens = tokens_input
        else:
            raise ValueError("tokens_input must be a JSON string or dictionary.")

        css_vars = []
        tailwind_colors = {}

        # Parse color tokens
        color_group = tokens.get("color", {})
        for name, data in color_group.items():
            val = data.get("$value") if isinstance(data, dict) else data
            if val:
                css_var_name = f"--color-{name.replace('_', '-')}"
                css_vars.append(f"  {css_var_name}: {val};")
                tailwind_colors[name] = f"var({css_var_name})"

        # Parse typography tokens
        typo_group = tokens.get("typography", {})
        for name, data in typo_group.items():
            val = data.get("$value") if isinstance(data, dict) else data
            if val:
                css_var_name = f"--font-{name.replace('_', '-')}"
                css_vars.append(f"  {css_var_name}: {val};")

        # Parse spacing tokens
        spacing_group = tokens.get("spacing", {})
        for name, data in spacing_group.items():
            val = data.get("$value") if isinstance(data, dict) else data
            if val:
                css_var_name = f"--spacing-{name.replace('_', '-')}"
                css_vars.append(f"  {css_var_name}: {val};")

        if format_type.lower() == "tailwind":
            tailwind_block = [
                "// Tailwind CSS Theme Extension (paste in tailwind.config.ts or globals.css @theme)",
                "export const themeColors = {",
            ]
            for k, v in tailwind_colors.items():
                tailwind_block.append(f'  "{k}": "{v}",')
            tailwind_block.append("};")
            return "\n".join(tailwind_block)

        # Default: CSS Custom Properties
        output = [
            "/* W3C DTCG Generated CSS Variables — CTI Soluciones */",
            ":root {",
            *css_vars,
            "}",
            "",
            "/* Utility class mapping */",
            ".bg-primary { background-color: var(--color-primary); }",
            ".text-primary { color: var(--color-primary); }"
        ]
        return "\n".join(output)

    except Exception as e:
        logger.error("Error exporting tokens to CSS: %s", e, exc_info=True)
        raise


def audit_full_palette(palette: dict) -> str:
    """
    Audits a complete corporate theme palette against WCAG 2.2 AA (4.5:1 normal, 3.0:1 large).
    Evaluates key pairings:
    - background vs text / foreground
    - primary vs primary_foreground (or white)
    - surface / card vs card_foreground
    - secondary vs secondary_foreground
    """
    try:
        # Standardize keys to lowercase
        norm = {k.lower().replace("-", "_"): v for k, v in palette.items() if isinstance(v, str)}

        # Define evaluation pairs
        pairs = []
        bg = norm.get("background") or norm.get("bg") or "#FFFFFF"
        fg = norm.get("text") or norm.get("foreground") or norm.get("fg") or "#111827"
        pairs.append(("background_vs_text", bg, fg, False))

        if "primary" in norm:
            pri = norm["primary"]
            pri_fg = norm.get("primary_foreground") or norm.get("primary_text") or "#FFFFFF"
            pairs.append(("primary_button_vs_text", pri, pri_fg, False))
            pairs.append(("primary_vs_background", pri, bg, True))

        if "card" in norm:
            card_bg = norm["card"]
            card_fg = norm.get("card_foreground") or fg
            pairs.append(("card_bg_vs_card_text", card_bg, card_fg, False))

        if "secondary" in norm:
            sec = norm["secondary"]
            sec_fg = norm.get("secondary_foreground") or fg
            pairs.append(("secondary_vs_text", sec, sec_fg, False))

        results = []
        all_passed = True

        for label, color_a, color_b, is_large in pairs:
            try:
                l1 = hex_to_relative_luminance(color_a)
                l2 = hex_to_relative_luminance(color_b)
                ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
                req = 3.0 if is_large else 4.5
                passed = ratio >= req
                if not passed:
                    all_passed = False

                results.append({
                    "pairing": label,
                    "color_a": color_a,
                    "color_b": color_b,
                    "ratio": f"{ratio:.2f}:1",
                    "required": f"{req}:1",
                    "status": "PASS" if passed else "FAIL"
                })
            except Exception as pe:
                results.append({
                    "pairing": label,
                    "color_a": color_a,
                    "color_b": color_b,
                    "error": str(pe),
                    "status": "ERROR"
                })
                all_passed = False

        summary = {
            "overall_status": "COMPLIANT" if all_passed else "NON_COMPLIANT",
            "total_pairings_tested": len(results),
            "pairings": results,
            "recommendation": (
                "Palette strictly passes WCAG 2.2 Level AA."
                if all_passed
                else "Adjust luminances of failing pairings to achieve at least 4.5:1 for body text."
            )
        }

        return json.dumps(summary, indent=2, ensure_ascii=False)

    except Exception as e:
        logger.error("Error auditing full palette: %s", e, exc_info=True)
        raise
