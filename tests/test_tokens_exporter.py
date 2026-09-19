import sys
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.tools.tokens_exporter import export_tokens_to_css, audit_full_palette


class TestTokensExporter:
    def test_export_tokens_to_css_variables(self):
        tokens = {
            "color": {
                "primary": {"$value": "#0A2540", "$type": "color"},
                "accent": {"$value": "#00D4AA", "$type": "color"}
            },
            "spacing": {
                "md": {"$value": "16px", "$type": "dimension"}
            }
        }
        css = export_tokens_to_css(tokens, format_type="css_variables")
        assert ":root {" in css
        assert "--color-primary: #0A2540;" in css
        assert "--color-accent: #00D4AA;" in css
        assert "--spacing-md: 16px;" in css

    def test_export_tokens_to_tailwind(self):
        tokens = {
            "color": {
                "primary": {"$value": "#0A2540", "$type": "color"}
            }
        }
        tw = export_tokens_to_css(tokens, format_type="tailwind")
        assert "export const themeColors" in tw
        assert '"primary": "var(--color-primary)"' in tw

    def test_audit_full_palette_pass(self):
        # High contrast palette
        palette = {
            "background": "#FFFFFF",
            "foreground": "#000000",
            "primary": "#0A2540",
            "primary_foreground": "#FFFFFF"
        }
        audit_str = audit_full_palette(palette)
        audit = json.loads(audit_str)
        assert audit["overall_status"] == "COMPLIANT"
        assert audit["total_pairings_tested"] >= 2
        for p in audit["pairings"]:
            assert p["status"] == "PASS"

    def test_audit_full_palette_fail(self):
        # Low contrast palette
        palette = {
            "background": "#FFFFFF",
            "foreground": "#F0F0F0",
            "primary": "#EEEEEE",
            "primary_foreground": "#FFFFFF"
        }
        audit_str = audit_full_palette(palette)
        audit = json.loads(audit_str)
        assert audit["overall_status"] == "NON_COMPLIANT"
