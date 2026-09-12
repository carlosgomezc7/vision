import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.tools.system_info import get_system_info, format_system_info_report


class TestSystemInfo:
    def test_get_system_info_structure(self):
        info = get_system_info()
        required_keys = ["os_name", "pretty_name", "kernel", "arch", "python_version", "is_arch_based", "is_omarch"]
        for key in required_keys:
            assert key in info

    def test_get_system_info_types(self):
        info = get_system_info()
        assert isinstance(info["kernel"], str)
        assert isinstance(info["arch"], str)
        assert isinstance(info["python_version"], str)
        assert isinstance(info["is_arch_based"], bool)
        assert isinstance(info["is_omarch"], bool)

    def test_format_system_info_report(self):
        report = format_system_info_report()
        assert "Sistema Detectado" in report
        assert "Kernel" in report
        assert "Python" in report
