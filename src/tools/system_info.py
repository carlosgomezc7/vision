import platform
import os
import sys
from src.logger import get_logger

logger = get_logger("vision.tools.system_info")


def get_system_info() -> dict:
    """Automatically detects the operating system environment (Omarch / Arch Linux)."""
    try:
        os_info = {
            "os_name": "Linux",
            "pretty_name": "Arch Linux",
            "kernel": platform.release(),
            "arch": platform.machine(),
            "python_version": sys.version.split()[0],
            "is_arch_based": False,
            "is_omarch": False
        }

        os_release_path = "/etc/os-release"
        if os.path.exists(os_release_path):
            with open(os_release_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, val = line.strip().split("=", 1)
                        val = val.strip('"')
                        if key == "PRETTY_NAME":
                            os_info["pretty_name"] = val
                        elif key == "ID":
                            os_info["id"] = val

        if os.path.exists("/etc/arch-release") or os_info.get("id") == "arch":
            os_info["is_arch_based"] = True

        hostname = platform.node()
        if "omarch" in hostname.lower() or "omarch" in os_info["pretty_name"].lower():
            os_info["is_omarch"] = True

        logger.debug("System info detected: %s", os_info)
        return os_info
    except Exception as e:
        logger.error("Error detecting system: %s", e, exc_info=True)
        raise


def format_system_info_report() -> str:
    """Returns a structured report of the detected operating system."""
    try:
        info = get_system_info()
        omarch_tag = " (Omarch / Arch Linux)" if info["is_arch_based"] else ""
        report = (
            f"🐧 Detected System: {info['pretty_name']}{omarch_tag}\n"
            f"🖥️ Kernel: {info['kernel']} ({info['arch']})\n"
            f"🐍 Python: {info['python_version']} (Virtual environment `.venv`)\n"
            f"📦 Base package manager: pacman / yay\n"
            f"⚙️ Status: Auto-detection active"
        )
        logger.info("System report generated.")
        return report
    except Exception as e:
        logger.error("Error formatting system report: %s", e, exc_info=True)
        return f"⚠️ Error detecting system: {e}"
