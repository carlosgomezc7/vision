import sys
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.tools.ux_design_tool import (
    hex_to_relative_luminance,
    validate_wcag_contrast,
    generate_w3c_design_tokens,
    audit_performance_budget,
)


class TestUXDesignTool:
    def test_hex_to_relative_luminance_black(self):
        lum = hex_to_relative_luminance("#000000")
        assert lum == 0.0

    def test_hex_to_relative_luminance_white(self):
        lum = hex_to_relative_luminance("#FFFFFF")
        assert lum == 1.0

    def test_hex_to_relative_luminance_shorthand(self):
        lum_short = hex_to_relative_luminance("#F00")
        lum_long = hex_to_relative_luminance("#FF0000")
        assert abs(lum_short - lum_long) < 1e-9

    def test_validate_wcag_pass_aa(self):
        result = validate_wcag_contrast("#000000", "#FFFFFF", is_large_text=False)
        data = json.loads(result)
        assert data["passes_wcag_aa"] is True
        assert data["status"] == "PASS"

    def test_validate_wcag_fail_aa(self):
        result = validate_wcag_contrast("#777777", "#888888", is_large_text=False)
        data = json.loads(result)
        assert data["passes_wcag_aa"] is False
        assert data["status"] == "FAIL"

    def test_validate_wcag_large_text_threshold(self):
        # Large text only needs 3.0:1
        result = validate_wcag_contrast("#666666", "#999999", is_large_text=True)
        data = json.loads(result)
        # This contrast is usually near the limit; we verify that the is_large_text logic works correctly
        assert "required_ratio_aa" in data
        assert data["required_ratio_aa"] == "3.0:1"

    def test_generate_w3c_design_tokens(self):
        palette = {"primary": "#0A2540", "accent": "#00D4AA"}
        typography = {"fontFamily": "Inter", "bodySize": "16px"}
        spacing = {"sm": "8px", "md": "16px"}
        result = generate_w3c_design_tokens(palette, typography, spacing)
        data = json.loads(result)
        assert data["color"]["primary"]["$type"] == "color"
        assert data["typography"]["fontFamily"]["$type"] == "fontFamily"
        assert data["spacing"]["md"]["$type"] == "dimension"

    def test_generate_w3c_tokens_empty(self):
        result = generate_w3c_design_tokens({})
        data = json.loads(result)
        assert data["color"] == {}
        assert data["typography"] == {}
        assert data["spacing"] == {}

    def test_audit_performance_budget_high_risk(self):
        result = audit_performance_budget("next.js", estimated_js_kb=600, animations_count=12)
        data = json.loads(result)
        assert data["evaluation"]["inp_risk"] == "HIGH"
        assert data["evaluation"]["lcp_risk"] == "HIGH"
        assert any("next/font" in r for r in data["recommendations"])

    def test_audit_performance_budget_low_risk(self):
        result = audit_performance_budget("react", estimated_js_kb=150, animations_count=2)
        data = json.loads(result)
        assert data["evaluation"]["inp_risk"] == "LOW"
        assert data["evaluation"]["lcp_risk"] == "OPTIMAL"
